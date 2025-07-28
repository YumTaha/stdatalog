import asyncio
import struct
import socket
import os
import shutil
import sys
import logging
import colorlog
import argparse
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
DOWN_THRESHOLD_IN_MIN = -10  # in/min
# Speed sensor logic
START_THRESHOLD_SP = 0.5  # rad/s

def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

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


async def ble_speed_task(controller):
    client = BleakClient(DEVICE_MAC_ADDRESS_SP)
    controller.speed_client = client
    reconnect_timeout = 15

    while True:
        try:
            logger.info(f"Connecting to Speed BLE device at {DEVICE_MAC_ADDRESS_SP} ...")

            # Scan to rediscover
            found = False
            devices = await BleakScanner.discover(timeout=5.0)
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
                asyncio.create_task(controller.update_data_collection_state())

            await client.start_notify(VELOCITY_CHAR_UUID_SP, notification_handler)
            logger.info("Listening for speed updates.")
            while client.is_connected:
                await asyncio.sleep(1)

            logger.warning("Speed BLE disconnected.")
            if controller.sent_state != "stopped":
                logger.info("Sending 'stop' due to Speed disconnect.")
                try:
                    controller.sock.sendall(b'stop\n')
                    controller.sent_state = 'stopped'
                except Exception as e:
                    logger.warning(f"Failed to send 'stop': {e}")

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
            await asyncio.sleep(5)  # backoff

async def ble_feedrate_task(controller, ready_event):
    client = BleakClient(DEVICE_MAC_ADDRESS_FR)
    controller.feedrate_client = client
    reconnect_timeout = 15

    while True:
        try:
            logger.info(f"Connecting to Feedrate BLE device at {DEVICE_MAC_ADDRESS_FR} ...")

            # Scan to rediscover
            found = False
            devices = await BleakScanner.discover(timeout=5.0)
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
            await asyncio.sleep(5)  # backoff

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
            # Uncomment and implement if you want folder cleanup:
            # asyncio.create_task(cut_folder_manager()),
        ]
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Ctrl+C received, shutting down.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
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
