import asyncio
import logging
import struct
import socket
import os
import time
import signal
from datetime import datetime
from bleak import BleakClient, BleakScanner
import colorlog

# === Configuration ===
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 8888
BLE_MACS = {
    "Feedrate": "DE:6D:5D:2A:BD:58",
    "Speed": "F9:51:AC:0F:75:9E"
}
UUIDS = {
    "Feedrate": "2772836b-8bb0-4d0f-a52c-254b5d1fa438",
    "Speed": "04403980-1579-4b57-81eb-bfcdce019b9f"
}
FEEDRATE_START_THRESHOLD = -20.0
SPEED_REQUIRED_THRESHOLD = 0.3
BETWEEN_COMMANDS = 0.2  # seconds
ACQ_FOLDER = "../acquisition_data"
LOG_FILE = f"{ACQ_FOLDER}/ble_disconnects.txt"

# === Globals ===
ble_connected = {name: False for name in BLE_MACS}
latest_values = {name: None for name in BLE_MACS}
socket_writer = None
socket_connected = False
last_command_sent = None
_last_command_time = 0
disconnect_timers = {}

# Global shutdown flag
shutdown_event = asyncio.Event()

async def interruptible_sleep(duration):
    """Sleep that can be interrupted by shutdown event."""
    try:
        await asyncio.wait_for(
            asyncio.wait([
                asyncio.create_task(asyncio.sleep(duration)),
                asyncio.create_task(shutdown_event.wait())
            ], return_when=asyncio.FIRST_COMPLETED),
            timeout=duration + 1
        )
    except asyncio.TimeoutError:
        pass

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

# === Logging Setup ===
logger = logging.getLogger("BLEMonitor")
handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# === BLE Float Parser ===
def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

# === Logging Function ===
def log_disconnection(sensor_name: str, reason: str):
    try:
        os.makedirs(ACQ_FOLDER, exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{now} - {sensor_name} {reason}\n")
    except Exception as e:
        logger.error(f"Failed to log disconnection: {e}")

# === Timer for BLE reconnect ===
async def handle_disconnect_timeout(sensor_name):
    try:
        await interruptible_sleep(60)
        if not ble_connected[sensor_name] and not shutdown_event.is_set():
            _send_command("stop")
            log_disconnection(sensor_name, "1min timeout - stop sent")
    except asyncio.CancelledError:
        logger.debug(f"Disconnect timer for {sensor_name} cancelled")
    except Exception as e:
        logger.error(f"Error in disconnect timeout for {sensor_name}: {e}")

def on_ble_disconnect(sensor_name):
    if ble_connected[sensor_name]:
        ble_connected[sensor_name] = False
        latest_values[sensor_name] = None
        log_disconnection(sensor_name, "disconnected")
        if sensor_name in disconnect_timers:
            disconnect_timers[sensor_name].cancel()
        disconnect_timers[sensor_name] = asyncio.create_task(handle_disconnect_timeout(sensor_name))

def on_ble_reconnect(sensor_name):
    ble_connected[sensor_name] = True
    if sensor_name in disconnect_timers:
        disconnect_timers[sensor_name].cancel()
        del disconnect_timers[sensor_name]

# === Socket Connection ===
async def maintain_socket():
    global socket_connected, socket_writer
    while not shutdown_event.is_set():
        try:
            logger.debug("Attempting socket connection...")
            reader, writer = await asyncio.open_connection(SOCKET_HOST, SOCKET_PORT)
            socket_writer = writer
            socket_connected = True
            logger.info("Socket connected")
            while not shutdown_event.is_set():
                writer.write(b'\n')
                await writer.drain()
                await interruptible_sleep(2)
        except Exception as e:
            logger.warning(f"Socket lost: {e}")
            socket_connected = False
            if socket_writer:
                socket_writer.close()
                try:
                    await socket_writer.wait_closed()
                except:
                    pass
            socket_writer = None
            await interruptible_sleep(2)

# === BLE Connection Logic ===
async def connect_ble(name, mac, uuid, handler, ready_event=None):
    first_time = True
    while not shutdown_event.is_set():
        try:
            logger.info(f"Scanning for {name}...")
            devices = await BleakScanner.discover(timeout=5.0)
            if not any(d.address.upper() == mac for d in devices):
                await interruptible_sleep(2)
                continue

            logger.info(f"{name} found. Connecting...")
            client = BleakClient(mac)
            await client.connect(timeout=10.0)
            if not client.is_connected:
                raise RuntimeError(f"{name} connection failed")

            logger.info(f"{name} BLE connected")
            on_ble_reconnect(name)
            if ready_event and first_time:
                ready_event.set()
                first_time = False

            await client.start_notify(uuid, handler)

            while client.is_connected and not shutdown_event.is_set():
                await asyncio.sleep(1)

            if shutdown_event.is_set():
                logger.info(f"{name} BLE task received shutdown signal.")
                try:
                    if client.is_connected:
                        await client.stop_notify(uuid)
                        await client.disconnect()
                        logger.info(f"Disconnected {name} BLE device.")
                except Exception as e:
                    logger.warning(f"{name} BLE cleanup error: {e}")
                break

            logger.warning(f"{name} BLE disconnected")
            on_ble_disconnect(name)

        except Exception as e:
            logger.error(f"{name} BLE error: {e}")
        await interruptible_sleep(2)

# === Notification Handlers ===
def feedrate_notify_handler(sender, data):
    raw = parse_float32_le(data)
    v_in_min = round(raw * 39.3701 * 60, 3)
    latest_values["Feedrate"] = v_in_min
    _print_debug()
    _check_and_send_command()

def speed_notify_handler(sender, data):
    raw = parse_float32_le(data)
    latest_values["Speed"] = round(raw, 3)
    _print_debug()
    _check_and_send_command()

# === Debug Print & Command Logic ===
def _print_debug():
    if logger.isEnabledFor(logging.DEBUG):
        s = latest_values["Speed"]
        f = latest_values["Feedrate"]
        speed_str = f"{s:.2f}" if s is not None else "###"
        feed_str = f"{f:.2f}" if f is not None else "###"
        logger.debug(f"({speed_str}, {feed_str})")

def _check_and_send_command():
    global last_command_sent
    speed = latest_values["Speed"]
    feed = latest_values["Feedrate"]
    if speed is None or feed is None:
        return

    if speed > SPEED_REQUIRED_THRESHOLD and feed < FEEDRATE_START_THRESHOLD:
        if last_command_sent != "start":
            _send_command("start")
            last_command_sent = "start"
    else:
        if last_command_sent != "stop":
            _send_command("stop")
            last_command_sent = "stop"

def _send_command(cmd: str):
    global _last_command_time
    now = time.monotonic()
    if now - _last_command_time < BETWEEN_COMMANDS:
        return
    _last_command_time = now

    if socket_connected and socket_writer:
        try:
            socket_writer.write((cmd + "\n").encode())
            logger.info(f"Sent command: {cmd}")
        except Exception as e:
            logger.warning(f"Failed to send command: {e}")

# === BLE Sequence Orchestration ===
async def ble_startup_sequence():
    ready_event = asyncio.Event()
    task_feed = asyncio.create_task(connect_ble("Feedrate", BLE_MACS["Feedrate"], UUIDS["Feedrate"], feedrate_notify_handler, ready_event))
    await ready_event.wait()
    logger.info("Feedrate ready. Starting Speed BLE task...")
    task_speed = asyncio.create_task(connect_ble("Speed", BLE_MACS["Speed"], UUIDS["Speed"], speed_notify_handler))
    await asyncio.gather(task_feed, task_speed)

# === Monitoring Logic ===
async def monitor_main():
    while not shutdown_event.is_set():
        if not (socket_connected and all(ble_connected.values())):
            logger.info("Waiting for all connections...")
        await interruptible_sleep(2)

# === Entrypoint ===
async def main():
    logger.info("BLE + Socket Monitor starting...")
    try:
        tasks = [
            asyncio.create_task(maintain_socket()),
            asyncio.create_task(ble_startup_sequence()),
            asyncio.create_task(monitor_main())
        ]
        
        # Wait for either tasks to complete or shutdown signal
        done, pending = await asyncio.wait(
            tasks + [asyncio.create_task(shutdown_event.wait())],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel any pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
                
    except KeyboardInterrupt:
        logger.info("Ctrl+C received, shutting down.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            # Cancel any pending disconnect timers
            for timer_task in disconnect_timers.values():
                if timer_task and not timer_task.done():
                    timer_task.cancel()
                    try:
                        await timer_task
                    except asyncio.CancelledError:
                        pass
            
            # Close socket connection
            if socket_writer:
                socket_writer.close()
                try:
                    await socket_writer.wait_closed()
                except:
                    pass
                logger.info("Disconnected socket connection.")
            
            logger.info("Service shutdown complete.")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting by user request.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
