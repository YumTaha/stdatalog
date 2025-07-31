#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import re
import asyncio
import time
import shutil
import glob
import signal
from datetime import datetime

# --- LOGGING SETUP ---
import logging
import colorlog

LOG_FILE = os.path.expanduser("/home/kirwinr/logs/stdatalog-cli.log")

logger = logging.getLogger("HSDatalogApp")
logger.setLevel(logging.INFO)

# File handler (no ANSI)
file_handler = logging.FileHandler(LOG_FILE, mode='a')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'))

# Console handler (with color if TTY)
console_handler = logging.StreamHandler()
if sys.stderr.isatty():
    console_handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))
else:
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ROOT:
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Go up as needed to reach your real project root, e.g.
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "../../../.."))

# ---- SETTINGS ----
ACQ_TIME = 1    # seconds to log data
DELAY = 14      # seconds to wait
DEVICE_CONFIG_PATH = os.path.join(PROJECT_ROOT, "device_config.json")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "acquisition_data")
SOCKET_PORT = 8888

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
    logger.info(f"[SIGNAL] Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

# Ensure the TUI and SDK are in the path
logger.debug("[STARTUP] Adding TUI path to sys.path...")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'TUI')))
logger.debug("[STARTUP] Importing stdatalog_TUI...")
from stdatalog_TUI import HSDInfo
logger.debug("[STARTUP] Importing HSDLink...")
from stdatalog_core.HSD_link.HSDLink import HSDLink
logger.debug("[STARTUP] All imports completed!")

async def async_socket_listener(state):
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, state),
        '127.0.0.1', SOCKET_PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f'[IPC] Async IPC server running on {addrs}')
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer, state):
    addr = writer.get_extra_info('peername')
    logger.info(f'[IPC] Connected by {addr}')
    try:
        while not shutdown_event.is_set():
            try:
                data = await asyncio.wait_for(reader.read(32), timeout=1.0)
            except asyncio.TimeoutError:
                continue  # Check shutdown event again
            
            if not data:
                logger.warning(f'[IPC] Disconnected by {addr}')
                break
            cmd = data.decode('utf-8').strip().lower()
            if cmd == "start" and not state["running"]:
                state["command"] = "start"
            elif cmd == "stop" and state["running"]:
                state["command"] = "stop"
            elif cmd == "exit":
                state["command"] = "exit"
                break
    except ConnectionResetError:
        logger.warning(f"[IPC] Disconnected by {addr}")
    finally:
        writer.close()
        await writer.wait_closed()

def get_next_cut_number(parent_folder):
    """Find the next cut_X number based on existing folders."""
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
        return 1
    cut_nums = []
    for d in os.listdir(parent_folder):
        m = re.match(r'^cut_(\d+)$', d)
        if m:
            cut_nums.append(int(m.group(1)))
    if cut_nums:
        return max(cut_nums) + 1
    return 1

async def cut_logging_task(state):
    # ---- Device/SDK Initialization ----
    logger.info("Initializing STDatalog CLI...")
    tui_flags = HSDInfo.TUIFlags(
        output_folder=OUTPUT_FOLDER,
        sub_datetime_folder=True,
        acq_name="CLI_Log",
        acq_desc="CLI periodic logging",
        file_config=DEVICE_CONFIG_PATH,
        ucf_file="",
        ispu_out_fmt="",
        time_sec=-1,
        interactive_mode=False,
    )

    logger.info("Creating HSDInfo instance...")
    try:
        # Run device detection in a thread to avoid blocking the async loop
        def create_hsd_info():
            return HSDInfo(tui_flags)
        
        # Use asyncio to run the blocking call with a timeout
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_hsd_info)
            try:
                hsd_info = await asyncio.get_event_loop().run_in_executor(None, lambda: future.result(timeout=30))
                logger.info("HSDInfo created successfully!")
            except concurrent.futures.TimeoutError:
                logger.error("ERROR: Device detection timeout after 30 seconds!")
                logger.error("Please check that your STMicroelectronics device is connected and try again.")
                state["command"] = "exit"
                return
    except Exception as e:
        logger.error(f"ERROR: Failed to initialize device connection: {e}")
        logger.error("Please check that your STMicroelectronics device is connected and try again.")
        state["command"] = "exit"
        return

    if len(hsd_info.device_list) == 0:
        logger.error("No compatible devices connected! Please connect a device and try again.")
        state["command"] = "exit"
        return

    if len(hsd_info.device_list) > 1:
        logger.warning(f"Multiple devices found ({len(hsd_info.device_list)}). Using the first one.")

    if hsd_info.selected_device_id is None:
        hsd_info.selected_device_id = 0

    pres_res = HSDLink.get_device_presentation_string(hsd_info.hsd_link, hsd_info.selected_device_id)
    if pres_res is not None:
        board_id = hex(pres_res["board_id"])
        fw_id = hex(pres_res["fw_id"])
        hsd_info.load_device_template(board_id, fw_id)

    hsd_info.update_fw_info()
    hsd_info.update_acq_params()
    hsd_info.upload_device_conf_file()
    hsd_info.update_sensor_list()
    hsd_info.init_sensor_data_counters()
    hsd_info.update_ai_sensor_list()
    hsd_info.update_tag_list()
    hsd_info.init_tag_status_list()
    hsd_info.set_rtc()
    hsd_info.check_output_folder()

    logger.info(f"Connected to device: {hsd_info.selected_fw_info}")
    logger.info(f"Active sensors: {len(hsd_info.sensor_list) if hsd_info.sensor_list else 0}")
    logger.info(f"Output folder: {hsd_info.output_acquisition_path}")
    logger.info(f"Acquisition cycle: {ACQ_TIME}s logging, {DELAY}s pause")
    logger.info(f"Waiting for external commands via IPC socket on port {SOCKET_PORT}...")

    cut_number = get_next_cut_number(OUTPUT_FOLDER)

    while not shutdown_event.is_set():
        # Check for shutdown signal first
        if shutdown_event.is_set():
            logger.info("[SHUTDOWN] Graceful shutdown requested.")
            state["command"] = "exit"
            break
            
        # Exit condition
        if state["command"] == "exit":
            logger.info("Exiting program. Goodbye.")
            break

        # Start new cut when commanded and not already running
        if state["command"] == "start" and not state["running"]:
            cut_folder = os.path.join(OUTPUT_FOLDER, f"cut_{cut_number}")
            os.makedirs(cut_folder, exist_ok=True)

            logger.info(f"Starting acquisition cycle {cut_number}")
            logger.info(f"Cut folder: {cut_folder}")

            # Reset output folder to main directory for logging
            hsd_info.tui_flags.output_folder = OUTPUT_FOLDER
            hsd_info.output_acquisition_path = OUTPUT_FOLDER
            hsd_info.update_acq_params()
            hsd_info.check_output_folder()

            logger.info(f"Starting periodic logging: {ACQ_TIME}s log, {DELAY}s pause. Send 'stop' to end safely.")
            state["running"] = True
            state["command"] = None

            while state["running"] and not shutdown_event.is_set():
                # Check for shutdown signal
                if shutdown_event.is_set():
                    logger.info("[SHUTDOWN] Graceful shutdown requested during acquisition.")
                    state["running"] = False
                    state["command"] = "exit"
                    break
                    
                # Get list of existing folders before logging
                existing_folders = set()
                if os.path.exists(OUTPUT_FOLDER):
                    existing_folders = {f for f in os.listdir(OUTPUT_FOLDER) 
                                      if os.path.isdir(os.path.join(OUTPUT_FOLDER, f)) 
                                      and not f.startswith('cut_')}

                logger.info(f"Starting log cycle...")
                hsd_info.start_log()
                await interruptible_sleep(ACQ_TIME)
                hsd_info.stop_log()
                logger.info(f"Log cycle complete.")

                # Check for shutdown again after logging
                if shutdown_event.is_set():
                    logger.info("[SHUTDOWN] Graceful shutdown requested after logging.")
                    state["running"] = False
                    state["command"] = "exit"
                    break
                
                # Find new folders created during logging
                if os.path.exists(OUTPUT_FOLDER):
                    current_folders = {f for f in os.listdir(OUTPUT_FOLDER) 
                                     if os.path.isdir(os.path.join(OUTPUT_FOLDER, f)) 
                                     and not f.startswith('cut_')}
                    
                    new_folders = current_folders - existing_folders
                    
                    # Move new folders to the cut directory
                    for folder_name in new_folders:
                        src_path = os.path.join(OUTPUT_FOLDER, folder_name)
                        dst_path = os.path.join(cut_folder, folder_name)
                        try:
                            logger.info(f"Moving {folder_name} to {cut_folder}")
                            shutil.move(src_path, dst_path)
                        except Exception as e:
                            logger.error(f"Error moving folder {folder_name}: {e}")

                logger.info("Waiting for next cycle...")
                # Wait for DELAY seconds or until a stop command or shutdown signal
                for i in range(DELAY):
                    if state["command"] == "stop" or shutdown_event.is_set():
                        if shutdown_event.is_set():
                            logger.info("[SHUTDOWN] Graceful shutdown requested during delay.")
                            state["command"] = "exit"
                        state["running"] = False
                        state["command"] = None if not shutdown_event.is_set() else "exit"
                        break
                    await interruptible_sleep(1)

            logger.info("Stopping acquisition, cleaning up...")
            if hsd_info.is_log_started:
                hsd_info.stop_log()
            logger.info("Done. Waiting for new command, or send 'exit' to quit.")

            cut_number += 1  # increment for next cycle

        await interruptible_sleep(0.1)
    
    # Final cleanup when exiting the main loop
    logger.info("[SHUTDOWN] Performing final cleanup...")
    try:
        if 'hsd_info' in locals() and hsd_info.is_log_started:
            logger.info("[SHUTDOWN] Stopping any active logging...")
            hsd_info.stop_log()
        logger.info("[SHUTDOWN] HSD cleanup complete.")
    except Exception as e:
        logger.error(f"[ERROR] Error during HSD cleanup: {e}")

async def main():
    state = {"running": False, "command": None, "stop_requested": False}
    try:
        tasks = [
            asyncio.create_task(async_socket_listener(state)),
            asyncio.create_task(cut_logging_task(state))
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
        logger.info("\n[SHUTDOWN] Ctrl+C received, shutting down.")
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
    finally:
        try:
            # Ensure logging is stopped if it was running
            if state.get("running", False):
                logger.info("[SHUTDOWN] Stopping any active logging...")
                # Note: hsd_info cleanup would be handled in cut_logging_task
            logger.info("[SHUTDOWN] Service shutdown complete.")
        except Exception as e:
            logger.error(f"[ERROR] Error during shutdown: {e}")

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("🚀 STDatalog CLI Service Starting...")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path[:3]}...")  # Show first 3 paths
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nExiting by user request.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
