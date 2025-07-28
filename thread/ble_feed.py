import asyncio
import struct
import socket
import os
import shutil
import time
import sys
import logging
from bleak import BleakClient

# Configure logging for service operation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# BLE config
DEVICE_NAME = "FRM"
DEVICE_MAC_ADDRESS = "DE:6D:5D:2A:BD:58" 
VELOCITY_CHAR_UUID = "2772836b-8bb0-4d0f-a52c-254b5d1fa438"

# IPC config
SOCKET_PORT = 8888

# Acquisition folder management
ACQ_FOLDER = "../acquisition_data"
MAX_CUT_FOLDERS = -1

# Threshold for feedrate (in/min)
DOWN_THRESHOLD = -0.5  # in/min

def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

async def cut_folder_manager():
    if MAX_CUT_FOLDERS < 0:
        logger.info("[CutFolderMonitor] MAX_CUT_FOLDERS < 0: Cut folder cleanup is disabled.")
        return
    logger.info("Starting cut folder manager")
    while True:
        try:
            if not os.path.isdir(ACQ_FOLDER):
                await asyncio.sleep(FOLDER_CHECK_INTERVAL)
                continue
            entries = [
                os.path.join(ACQ_FOLDER, d) for d in os.listdir(ACQ_FOLDER)
                if os.path.isdir(os.path.join(ACQ_FOLDER, d)) and d.startswith('cut_')
            ]
            if len(entries) > MAX_CUT_FOLDERS:
                entries.sort(key=lambda x: os.path.getmtime(x))
                to_delete = entries[:-MAX_CUT_FOLDERS]
                for folder in to_delete:
                    try:
                        logger.info(f"[CutFolderMonitor] Deleting old cut folder: {folder}")
                        shutil.rmtree(folder)
                    except Exception as e:
                        logger.error(f"[CutFolderMonitor] Failed to delete {folder}: {e}")
        except Exception as e:
            logger.error(f"[CutFolderMonitor] Error: {e}")
        await asyncio.sleep(FOLDER_CHECK_INTERVAL)

async def ble_and_ipc_task(sock):
    logger.info(f"Connecting to CLI logger at localhost:{SOCKET_PORT}...")
    retry_count = 0
    max_retries = 30
    
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

    logger.info(f"Connecting to BLE device with MAC: {DEVICE_MAC_ADDRESS} ...")
    sent_state = None  # None, "started", "stopped"

    try:
        async with BleakClient(DEVICE_MAC_ADDRESS) as client:
            if not client.is_connected:
                logger.error("Could not connect to BLE device.")
                sock.close()
                return

            logger.info("Connected to BLE device. Subscribing to notifications...")

            def notification_handler(sender, data):
                nonlocal sent_state
                try:
                    raw_v = parse_float32_le(data)  # m/s
                    v_in_min = raw_v * 39.3701 * 60
                    v_in_min = round(v_in_min, 3)
                    logger.info(f"Feedrate Velocity: {v_in_min} in/min")

                    if sent_state != "started" and v_in_min < DOWN_THRESHOLD:
                        logger.info("Feedrate DOWN: sending 'start'")
                        sock.sendall(b'start\n')
                        sent_state = "started"
                    elif sent_state != "stopped" and v_in_min >= DOWN_THRESHOLD:
                        logger.info("Feedrate STOP: sending 'stop'")
                        sock.sendall(b'stop\n')
                        sent_state = "stopped"
                except Exception as e:
                    logger.error(f"Malformed data: {data} ({e})")

            try:
                await client.start_notify(VELOCITY_CHAR_UUID, notification_handler)
                logger.info("Listening for feedrate updates. Service will run continuously.")
                while True:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error during notification handling: {e}")
            finally:
                await client.stop_notify(VELOCITY_CHAR_UUID)
                logger.info("Stopped BLE notifications.")
                
    except Exception as e:
        logger.error(f"BLE connection error: {e}")
    finally:
        sock.close()
        logger.info("Socket closed.")

async def main():
    logger.info("Feedrate BLE Service starting...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tasks = [
            asyncio.create_task(ble_and_ipc_task(sock)),
            asyncio.create_task(cut_folder_manager()),
        ]
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Ctrl+C received, shutting down.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            sock.close()
            logger.info("Service shutdown complete.")
        except Exception:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting by user request.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
