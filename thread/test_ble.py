import asyncio
import logging
import struct
import socket
import colorlog
from bleak import BleakClient, BleakScanner

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

# === Globals ===
ble_connected = {name: False for name in BLE_MACS}
latest_values = {name: None for name in BLE_MACS}
socket_writer = None
socket_connected = False

# === Logging Setup ===
logger = logging.getLogger("BLEMonitor")
handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# === BLE Float Parser ===
def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

# === Socket Connection ===
async def maintain_socket():
    global socket_connected, socket_writer
    while True:
        try:
            logger.debug("🔍 Attempting socket connection...")
            reader, writer = await asyncio.open_connection(SOCKET_HOST, SOCKET_PORT)
            socket_writer = writer
            socket_connected = True
            logger.info("🔌 Socket connected")

            while True:
                writer.write(b'\n')
                await writer.drain()
                await asyncio.sleep(2)
        except Exception as e:
            logger.warning(f"❌ Socket lost: {e}")
            socket_connected = False
            if socket_writer:
                socket_writer.close()
                try:
                    await socket_writer.wait_closed()
                except:
                    pass
            socket_writer = None
            await asyncio.sleep(2)

# === BLE Connect Logic ===
async def connect_ble(name, mac, uuid, handler, ready_event=None):
    global ble_connected, latest_values
    first_time = True

    while True:
        try:
            logger.info(f"🔍 Scanning for {name}...")
            devices = await BleakScanner.discover(timeout=5.0)
            if not any(d.address.upper() == mac for d in devices):
                logger.warning(f"❌ {name} not found.")
                await asyncio.sleep(2)
                continue

            logger.info(f"📡 {name} found. Connecting...")
            client = BleakClient(mac)
            await client.connect(timeout=10.0)

            if not client.is_connected:
                raise RuntimeError(f"{name} connection failed")

            logger.info(f"✅ {name} BLE connected")
            ble_connected[name] = True
            if ready_event and first_time:
                ready_event.set()
                first_time = False

            await client.start_notify(uuid, handler)

            while client.is_connected:
                await asyncio.sleep(1)

            logger.warning(f"⚠️ {name} BLE disconnected")
        except Exception as e:
            logger.error(f"⚠️ {name} BLE error: {e}")
        finally:
            ble_connected[name] = False
            latest_values[name] = None  # Clear value on disconnect
            _print_debug()
            await asyncio.sleep(2)

# === Notification Handlers ===
def feedrate_notify_handler(sender, data):
    raw = parse_float32_le(data)
    v_in_min = round(raw * 39.3701 * 60, 3)
    latest_values["Feedrate"] = v_in_min
    _print_debug()

def speed_notify_handler(sender, data):
    raw = parse_float32_le(data)
    latest_values["Speed"] = round(raw, 3)
    _print_debug()

def _print_debug():
    if logger.isEnabledFor(logging.DEBUG):
        s = latest_values["Speed"]
        f = latest_values["Feedrate"]
        speed_str = f"{s:.2f}" if s is not None else "###"
        feed_str = f"{f:.2f}" if f is not None else "###"
        logger.debug(f"({speed_str}, {feed_str})")

# === Orchestrator ===
async def ble_startup_sequence():
    ready_event = asyncio.Event()
    task_feed = asyncio.create_task(connect_ble("Feedrate", BLE_MACS["Feedrate"], UUIDS["Feedrate"], feedrate_notify_handler, ready_event))
    await ready_event.wait()
    logger.info("📬 Feedrate ready. Starting Speed BLE task...")
    task_speed = asyncio.create_task(connect_ble("Speed", BLE_MACS["Speed"], UUIDS["Speed"], speed_notify_handler))
    await asyncio.gather(task_feed, task_speed)

# === Logic Monitor ===
async def monitor_main():
    while True:
        if not (socket_connected and all(ble_connected.values())):
            logger.info("⏸ Waiting for all connections...")
        await asyncio.sleep(2)

# === Entrypoint ===
async def main():
    logger.info("🚀 BLE + Socket Monitor starting...")
    await asyncio.gather(
        maintain_socket(),
        ble_startup_sequence(),
        monitor_main()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🧼 Shutdown requested by user.")
