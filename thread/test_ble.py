import socket
import asyncio
import logging
import colorlog
from bleak import BleakClient, BleakScanner

# === Logging Setup ===
logger = logging.getLogger("BLETest")
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

# === Config ===
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 8888
BLE_MACS = {
    "Feedrate": "DE:6D:5D:2A:BD:58",
    "Speed": "F9:51:AC:0F:75:9E"
}

ble_status = {name: False for name in BLE_MACS}
clients = {name: None for name in BLE_MACS}
socket_connected = False
socket_writer = None

# === Persistent Socket Connection ===
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
                try:
                    writer.write(b'\n')  # Heartbeat (can be any byte)
                    await writer.drain()
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.warning(f"❌ Socket lost during heartbeat: {e}")
                    break

        except Exception as e:
            logger.warning(f"❌ Failed to connect to socket: {e}")

        socket_connected = False
        if socket_writer:
            socket_writer.close()
            try:
                await socket_writer.wait_closed()
            except:
                pass
        socket_writer = None
        await asyncio.sleep(2)


async def connect_ble(name, mac, ready_event: asyncio.Event = None):
    global ble_status, clients
    first_connection_done = False

    while True:
        try:
            logger.info(f"🔍 Scanning for {name}...")
            devices = await BleakScanner.discover(timeout=5.0)
            if any(d.address.upper() == mac for d in devices):
                logger.info(f"📡 {name} found. Connecting...")
                client = BleakClient(mac)
                await client.connect(timeout=10.0)
                if client.is_connected:
                    logger.info(f"✅ {name} BLE connected")
                    clients[name] = client
                    ble_status[name] = True

                    if ready_event and not first_connection_done:
                        ready_event.set()
                        first_connection_done = True

                    while client.is_connected:
                        await asyncio.sleep(1)

                    logger.warning(f"⚠️ {name} BLE disconnected")
                    ble_status[name] = False
                    await client.disconnect()
            else:
                logger.warning(f"❌ {name} not found during scan")
                ble_status[name] = False
        except Exception as e:
            logger.error(f"⚠️ {name} BLE error: {e}")
            ble_status[name] = False
        await asyncio.sleep(2)


# === Startup Coordinated BLE Tasks ===
async def feedrate_ble_task(ready_event: asyncio.Event):
    await connect_ble("Feedrate", BLE_MACS["Feedrate"], ready_event)


async def speed_ble_task(ready_event: asyncio.Event):
    await ready_event.wait()
    logger.info("📬 Feedrate ready. Starting Speed BLE task...")
    await connect_ble("Speed", BLE_MACS["Speed"])

# === Main logic ===
async def main_loop():
    while True:
        if socket_connected and all(ble_status.values()):
            logger.info("✅ All systems go. Running main task...")
            for _ in range(5):
                logger.info("🏃 Doing work...")
                await asyncio.sleep(1)
                if not socket_connected or not all(ble_status.values()):
                    logger.warning("🛑 Connection lost. Pausing work.")
                    break
        else:
            logger.info("⏸ Waiting for all connections...")
            await asyncio.sleep(2)

# === Entrypoint ===
async def main():
    feedrate_ready = asyncio.Event()

    await asyncio.gather(
        maintain_socket(),
        feedrate_ble_task(feedrate_ready),
        speed_ble_task(feedrate_ready),
        main_loop()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🧼 Shutdown requested by user.")
