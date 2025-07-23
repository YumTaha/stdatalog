import asyncio
import struct
import socket
import os
import shutil
import time
import sys
import logging
from bleak import BleakScanner, BleakClient

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
DEVICE_NAME = "Speed"
SERVICE_UUID = "04403980-1579-4b57-81eb-bfcdce019b9e"
CHAR_UUID = "04403980-1579-4b57-81eb-bfcdce019b9f"

# IPC config
SOCKET_PORT = 8888

# Acquisition folder management
ACQ_FOLDER = "../acquisition_data"  # must match your CLI logger's OUTPUT_FOLDER
MAX_SUBFOLDERS = 10                 # for general cleanup
MAX_CUT_FOLDERS = 20                 # set to -1 to disable cut folder cleanup
FOLDER_CHECK_INTERVAL = 10          # seconds between folder checks

# Thresholds for BLE logic
START_THRESHOLD = 0.5  # rad/s
STOP_THRESHOLD = 0.2   # rad/s

def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

async def acquisition_folder_manager():
    """Keeps only the newest MAX_SUBFOLDERS subfolders in ACQ_FOLDER."""
    logger.info("Starting acquisition folder manager")
    while True:
        try:
            if not os.path.isdir(ACQ_FOLDER):
                await asyncio.sleep(FOLDER_CHECK_INTERVAL)
                continue
            # List all subfolders
            entries = [
                os.path.join(ACQ_FOLDER, d) for d in os.listdir(ACQ_FOLDER)
                if os.path.isdir(os.path.join(ACQ_FOLDER, d))
            ]
            if len(entries) > MAX_SUBFOLDERS:
                entries.sort(key=lambda x: os.path.getmtime(x))
                to_delete = entries[:-MAX_SUBFOLDERS]
                for folder in to_delete:
                    try:
                        logger.info(f"[FolderMonitor] Deleting old acquisition folder: {folder}")
                        shutil.rmtree(folder)
                    except Exception as e:
                        logger.error(f"[FolderMonitor] Failed to delete {folder}: {e}")
        except Exception as e:
            logger.error(f"[FolderMonitor] Error: {e}")
        await asyncio.sleep(FOLDER_CHECK_INTERVAL)

async def cut_folder_manager():
    """Keeps only the newest MAX_CUT_FOLDERS cut_x subfolders in ACQ_FOLDER. Disabled if MAX_CUT_FOLDERS < 0."""
    if MAX_CUT_FOLDERS < 0:
        logger.info("[CutFolderMonitor] MAX_CUT_FOLDERS < 0: Cut folder cleanup is disabled.")
        return
    logger.info("Starting cut folder manager")
    while True:
        try:
            if not os.path.isdir(ACQ_FOLDER):
                await asyncio.sleep(FOLDER_CHECK_INTERVAL)
                continue
            # Only cut_x folders
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
    max_retries = 30  # Try for 1 minute
    
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

    logger.info("Scanning for BLE devices (5 seconds)...")
    device = None
    try:
        devices = await BleakScanner.discover(timeout=5.0)
        logger.info(f"Found {len(devices)} BLE devices")
        
        for d in devices:
            logger.debug(f"Device: {d.name} ({d.address})")
            if (d.name and d.name == DEVICE_NAME) or (getattr(d, "local_name", None) == DEVICE_NAME):
                device = d
                break
    except Exception as e:
        logger.error(f"Error during BLE scanning: {e}")
        sock.close()
        return

    if not device:
        logger.error(f"Device named '{DEVICE_NAME}' not found.")
        sock.close()
        return

    logger.info(f"Found device: {device.name} ({device.address}), connecting to BLE...")
    sent_state = None  # None, "started", "stopped"

    try:
        async with BleakClient(device.address) as client:
            if not client.is_connected:
                logger.error("Could not connect to BLE device.")
                sock.close()
                return

            logger.info("Connected to BLE device. Subscribing to notifications...")

            def notification_handler(sender, data):
                nonlocal sent_state
                try:
                    value = parse_float32_le(data)
                    logger.info(f"Rotational Velocity: {value:.2f} rad/s")
                    if sent_state != "started" and value >= START_THRESHOLD:
                        logger.info("Threshold exceeded: sending 'start'")
                        sock.sendall(b'start\n')
                        sent_state = "started"
                    elif sent_state != "stopped" and value <= STOP_THRESHOLD:
                        logger.info("Below stop threshold: sending 'stop'")
                        sock.sendall(b'stop\n')
                        sent_state = "stopped"
                except Exception as e:
                    logger.error(f"Malformed data: {data} ({e})")

            try:
                await client.start_notify(CHAR_UUID, notification_handler)
                logger.info("Listening for updates. Service will run continuously.")
                while True:
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error during notification handling: {e}")
            finally:
                await client.stop_notify(CHAR_UUID)
                logger.info("Stopped BLE notifications.")
                
    except Exception as e:
        logger.error(f"BLE connection error: {e}")
    finally:
        sock.close()
        logger.info("Socket closed.")

async def main():
    """Main service function"""
    logger.info("BLE Service starting...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Create tasks to avoid duplicate execution
        tasks = [
            asyncio.create_task(ble_and_ipc_task(sock)),
            asyncio.create_task(acquisition_folder_manager()),
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
