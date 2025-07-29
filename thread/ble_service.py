import asyncio
import struct
import socket
import os
import shutil
import sys
import logging
import colorlog
import subprocess
import argparse
from datetime import datetime
from bleak import BleakClient, BleakScanner

logger = logging.getLogger(__name__)

# BLE config
DEVICE_MAC_ADDRESS_FR = "DE:6D:5D:2A:BD:58"  # Feedrate sensor
DEVICE_MAC_ADDRESS_SP = "F9:51:AC:0F:75:9E"  # Speed sensor
VELOCITY_CHAR_UUID_FR = "2772836b-8bb0-4d0f-a52c-254b5d1fa438"   # Feedrate velocity (m/s)
VELOCITY_CHAR_UUID_SP = "04403980-1579-4b57-81eb-bfcdce019b9f"   # Speed (rad/s)

# IPC config
SOCKET_PORT = 8888

# Acquisition folder management
ACQ_FOLDER = "../acquisition_data"

# Feedrate logic
DOWN_THRESHOLD_IN_MIN = -15  # in/min
# Speed sensor logic
START_THRESHOLD_SP = 0.5  # rad/s

def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

def check_bluetooth_adapter():
    """Check if hci1 Bluetooth adapter is ready and functional"""
    try:
        # Check if adapter is UP and RUNNING
        result = subprocess.run(["hciconfig", "hci1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "UP RUNNING" not in result.stdout.decode():
            return False
            
        # Additional check: try to do a quick scan to verify adapter is functional
        try:
            scan_result = subprocess.run(["timeout", "2", "hcitool", "-i", "hci1", "scan"], 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
            # If scan command runs without error, adapter is likely functional
            return True
        except subprocess.TimeoutError:
            # Timeout is acceptable, means scan was working but just took time
            return True
        except Exception:
            # If hcitool fails, adapter might not be fully ready
            logger.debug("hcitool scan failed, adapter may not be fully ready")
            return False
            
    except Exception as e:
        logger.warning(f"Error checking Bluetooth adapter: {e}")
        return False

async def wait_for_adapter_ready():
    """Wait for Bluetooth adapter to be fully ready with progressive backoff"""
    max_attempts = 6
    base_delay = 2
    
    for attempt in range(max_attempts):
        if check_bluetooth_adapter():
            if attempt > 0:
                logger.info(f"Bluetooth adapter hci1 is ready after {attempt + 1} attempts")
            return True
        
        delay = base_delay * (2 ** attempt)  # Progressive backoff: 2, 4, 8, 16, 32, 64 seconds
        logger.warning(f"Bluetooth adapter hci1 not ready. Waiting {delay} seconds... (attempt {attempt + 1}/{max_attempts})")
        await asyncio.sleep(delay)
    
    logger.error("Bluetooth adapter hci1 failed to become ready after maximum attempts")
    return False

class DataCollectionController:
    def __init__(self, sock):
        self.sock = sock
        self.feedrate_active = False
        self.speed_active = False
        self.sent_state = None  # 'started' or 'stopped'
        self.current_machine_state = None  # For state logs
        self.lock = asyncio.Lock()
        # Store client references
        self.feedrate_client = None
        self.speed_client = None
        # Speed sensor disconnect tracking
        self.speed_disconnect_time = None
        self.speed_stop_timer_task = None

    async def update_data_collection_state(self):
        async with self.lock:
            new_machine_state = None

            if self.speed_active and self.feedrate_active:
                new_machine_state = "CUTTING (blade running, moving down)"
                if self.sent_state != 'started':
                    logger.info("Criteria met: Sending 'start'")
                    self.sock.sendall(b'start\n')
                    self.sent_state = 'started'
            elif self.speed_active and not self.feedrate_active:
                new_machine_state = "BLADE RESETTING (blade running, moving up)"
                if self.sent_state != 'stopped':
                    logger.info("Criteria NOT met: Sending 'stop'")
                    self.sock.sendall(b'stop\n')
                    self.sent_state = 'stopped'
            else:
                new_machine_state = "BLADE STOPPED (no spinning)"
                if self.sent_state != 'stopped':
                    logger.info("Criteria NOT met: Sending 'stop'")
                    self.sock.sendall(b'stop\n')
                    self.sent_state = 'stopped'

            # Only log if the state changed, to avoid log spam
            if new_machine_state != self.current_machine_state:
                logger.info(f"Machine State: {new_machine_state}")
                self.current_machine_state = new_machine_state

    def log_speed_disconnect(self):
        """Log speed sensor disconnection time to a file in acquisition_data folder."""
        try:
            # Ensure acquisition_data folder exists
            acq_folder = os.path.abspath(ACQ_FOLDER)
            os.makedirs(acq_folder, exist_ok=True)
            
            # Create log file path
            log_file = os.path.join(acq_folder, "speed_sensor_disconnections.txt")
            
            # Log the disconnection time
            disconnect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a") as f:
                f.write(f"{disconnect_time} - Speed sensor disconnected\n")
            
            logger.info(f"Logged speed sensor disconnection at {disconnect_time}")
        except Exception as e:
            logger.error(f"Failed to log speed sensor disconnection: {e}")

    async def handle_speed_disconnect_delayed_stop(self):
        """Handle delayed stop command after speed sensor disconnect (1 minute delay)."""
        try:
            logger.info("Starting 1-minute timer before sending stop command due to speed disconnect...")
            await asyncio.sleep(60)  # Wait 1 minute
            
            # Check if speed sensor is still disconnected
            if self.speed_disconnect_time is not None:
                logger.info("1 minute passed since speed disconnect - sending 'stop' command")
                if self.sent_state != "stopped":
                    try:
                        self.sock.sendall(b'stop\n')
                        self.sent_state = 'stopped'
                    except Exception as e:
                        logger.warning(f"Failed to send delayed 'stop': {e}")
            else:
                logger.info("Speed sensor reconnected during delay - not sending stop command")
        except asyncio.CancelledError:
            logger.info("Speed disconnect timer cancelled - sensor reconnected")
        except Exception as e:
            logger.error(f"Error in delayed stop handler: {e}")
        finally:
            self.speed_stop_timer_task = None

async def ble_speed_task(controller):
    client = BleakClient(DEVICE_MAC_ADDRESS_SP)
    controller.speed_client = client
    reconnect_timeout = 15

    # Wait for adapter to be ready at startup
    if not await wait_for_adapter_ready():
        logger.error("Speed BLE task aborting - adapter never became ready")
        return

    while True:
        try:
            logger.info(f"Connecting to Speed BLE device at {DEVICE_MAC_ADDRESS_SP} ...")

            # Scan to rediscover
            found = False
            devices = await BleakScanner.discover(timeout=5.0, adapter="hci1")
            for d in devices:
                if d.address.upper() == DEVICE_MAC_ADDRESS_SP.upper():
                    found = True
                    break

            if not found:
                logger.warning("Speed sensor not found. Retrying...")
                await asyncio.sleep(5)
                continue

            await asyncio.wait_for(client.connect(), timeout=reconnect_timeout)
            if not client.is_connected:
                raise RuntimeError("Speed sensor connection failed.")

            logger.info("Connected to Speed BLE. Subscribing...")

            def notification_handler(sender, data):
                value = parse_float32_le(data)
                logger.debug(f"Speed: {value:.3f} rad/s")
                controller.speed_active = value >= START_THRESHOLD_SP
                
                # Cancel any pending disconnect timer if speed sensor is working
                if controller.speed_stop_timer_task is not None:
                    controller.speed_stop_timer_task.cancel()
                    controller.speed_stop_timer_task = None
                    logger.info("Speed sensor reconnected - cancelled disconnect timer")
                
                # Clear disconnect time since sensor is working
                controller.speed_disconnect_time = None
                
                asyncio.create_task(controller.update_data_collection_state())

            await client.start_notify(VELOCITY_CHAR_UUID_SP, notification_handler)
            logger.info("Listening for speed updates.")
            
            # Clear disconnect tracking since we're connected
            controller.speed_disconnect_time = None
            if controller.speed_stop_timer_task is not None:
                controller.speed_stop_timer_task.cancel()
                controller.speed_stop_timer_task = None
            
            while client.is_connected:
                await asyncio.sleep(1)

            logger.warning("Speed BLE disconnected.")
            
            # Log the disconnection and start delayed stop timer
            controller.speed_disconnect_time = datetime.now()
            controller.log_speed_disconnect()
            
            # Start the delayed stop timer (only if not already running)
            if controller.speed_stop_timer_task is None:
                controller.speed_stop_timer_task = asyncio.create_task(
                    controller.handle_speed_disconnect_delayed_stop()
                )

        except asyncio.TimeoutError:
            logger.error("Speed connection timed out.")
        except Exception as e:
            logger.error(f"BLE error (speed): {e}")
        finally:
            try:
                if client.is_connected:
                    await client.stop_notify(VELOCITY_CHAR_UUID_SP)
                    await client.disconnect()
            except Exception as e:
                logger.warning(f"Speed BLE cleanup error: {e}")
            
            # Set speed as inactive since we're disconnected
            controller.speed_active = False
            
            # Quick adapter check before retry
            if not check_bluetooth_adapter():
                logger.warning("Bluetooth adapter issue detected. Waiting longer before retry...")
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(5)  # Normal backoff

async def ble_feedrate_task(controller, ready_event):
    client = BleakClient(DEVICE_MAC_ADDRESS_FR)
    controller.feedrate_client = client
    reconnect_timeout = 15

    # Wait for adapter to be ready at startup
    if not await wait_for_adapter_ready():
        logger.error("Feedrate BLE task aborting - adapter never became ready")
        return

    while True:
        try:
            logger.info(f"Connecting to Feedrate BLE device at {DEVICE_MAC_ADDRESS_FR} ...")

            # Scan to rediscover
            found = False
            devices = await BleakScanner.discover(timeout=5.0, adapter="hci1")
            for d in devices:
                if d.address.upper() == DEVICE_MAC_ADDRESS_FR.upper():
                    found = True
                    break

            if not found:
                logger.warning("Feedrate sensor not found. Retrying...")
                await asyncio.sleep(5)
                continue

            await asyncio.wait_for(client.connect(), timeout=reconnect_timeout)
            if not client.is_connected:
                raise RuntimeError("Feedrate sensor connection failed.")

            logger.info("Connected to Feedrate BLE. Subscribing...")

            def notification_handler(sender, data):
                raw_v = parse_float32_le(data)
                v_in_min = round(raw_v * 39.3701 * 60, 3)
                logger.debug(f"Feedrate: {v_in_min} in/min")
                controller.feedrate_active = v_in_min < DOWN_THRESHOLD_IN_MIN
                asyncio.create_task(controller.update_data_collection_state())

            await client.start_notify(VELOCITY_CHAR_UUID_FR, notification_handler)
            logger.info("Listening for feedrate updates.")
            ready_event.set()
            while client.is_connected:
                await asyncio.sleep(1)

            logger.warning("Feedrate BLE disconnected.")

        except asyncio.TimeoutError:
            logger.error("Feedrate connection timed out.")
        except Exception as e:
            logger.error(f"BLE error (feedrate): {e}")
        finally:
            try:
                if client.is_connected:
                    await client.stop_notify(VELOCITY_CHAR_UUID_FR)
                    await client.disconnect()
            except Exception as e:
                logger.warning(f"Feedrate BLE cleanup error: {e}")
            
            # Quick adapter check before retry
            if not check_bluetooth_adapter():
                logger.warning("Bluetooth adapter issue detected. Waiting longer before retry...")
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(5)  # Normal backoff

async def ble_and_ipc_task(controller):
    logger.info(f"Connecting to CLI logger at localhost:{SOCKET_PORT}...")
    retry_count = 0
    max_retries = 30
    sock = controller.sock
    while retry_count < max_retries:
        try:
            sock.connect(('127.0.0.1', SOCKET_PORT))
            logger.info("Connected to CLI logger.")
            break
        except ConnectionRefusedError:
            retry_count += 1
            logger.info(f"CLI logger not available yet. Retrying in 2 seconds... (attempt {retry_count}/{max_retries})")
            await asyncio.sleep(2)
    if retry_count >= max_retries:
        logger.error("Failed to connect to CLI logger after maximum retries. Exiting.")
        return

    # Orchestrate BLE connections in sequence
    ready_event = asyncio.Event()
    feedrate_task = asyncio.create_task(ble_feedrate_task(controller, ready_event))

    await ready_event.wait()  # Wait until feedrate BLE is connected and subscribed
    logger.info("Feedrate BLE ready. Proceeding to connect Speed BLE...")

    speed_task = asyncio.create_task(ble_speed_task(controller))

    # Wait for both tasks. If either fails, abort.
    results = await asyncio.gather(feedrate_task, speed_task, return_exceptions=True)
    for res in results:
        if res is False:
            logger.error("A BLE connection failed—aborting main service.")
            return

async def main():
    logger.info("Dual BLE Service starting (feedrate + speed)...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controller = DataCollectionController(sock)
    try:
        tasks = [
            asyncio.create_task(ble_and_ipc_task(controller)),
        ]
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Ctrl+C received, shutting down.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            # Cancel any pending speed disconnect timer
            if controller.speed_stop_timer_task is not None:
                controller.speed_stop_timer_task.cancel()
                controller.speed_stop_timer_task = None
                logger.info("Cancelled speed disconnect timer during shutdown")
            
            if controller.feedrate_client and controller.feedrate_client.is_connected:
                await controller.feedrate_client.disconnect()
                logger.info("Disconnected Feedrate BLE device.")
            if controller.speed_client and controller.speed_client.is_connected:
                await controller.speed_client.disconnect()
                logger.info("Disconnected Speed BLE device.")
            sock.close()
            logger.info("Service shutdown complete.")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dual BLE Logger")
    parser.add_argument('--log', default="INFO", help="Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    args = parser.parse_args()

    root_level = logging.INFO if args.log.upper() == "DEBUG" else getattr(logging, args.log.upper(), logging.INFO)

    # Use colorlog for colored console logs
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler = colorlog.StreamHandler()
    handler.setFormatter(color_formatter)

    # Replace handlers for the root logger
    logging.root.handlers = []
    logging.root.addHandler(handler)
    logging.root.setLevel(root_level)

    logger.setLevel(getattr(logging, args.log.upper(), logging.INFO))

    # Suppress Bleak/dbus logs at DEBUG level
    if args.log.upper() == "DEBUG":
        logging.getLogger("bleak").setLevel(logging.WARNING)
        logging.getLogger("dbus_fast").setLevel(logging.WARNING)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting by user request.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
