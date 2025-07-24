import os
import time
import asyncio
import shutil
import re
import getpass
import zipfile

ACQ_FOLDER = "/home/kirwinr/Desktop/stdatalog/acquisition_data"
POLL_INTERVAL = 4  # seconds
TRANSFER_TRACK_FILE = "transferred.txt"
MIN_CUT_FOLDERS = 1  # always keep at least X folders in acquisition_data

def find_usb_mounts():
    """Find all USB drives mounted under /media/<username>/"""
    base_media = f"/media/{getpass.getuser()}"
    if os.path.isdir(base_media):
        # List all subdirs (mounted USBs)
        return [os.path.join(base_media, d) for d in os.listdir(base_media)
                if os.path.ismount(os.path.join(base_media, d))]
    return []

def get_cut_number(folder_name):
    match = re.match(r'cut_(\d+)', folder_name)
    return int(match.group(1)) if match else float('inf')

def get_folder_size(folder_path):
    """Calculate total size of a folder in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
    except Exception as e:
        print(f"[USB] Warning: Error calculating folder size for {folder_path}: {e}")
    return total_size

async def monitor_usb():
    while True:
        usb_mounts = find_usb_mounts()
        if usb_mounts:
            for usb_mount in usb_mounts:
                print(f"[USB] USB stick detected at {usb_mount}")
                total, used, free = shutil.disk_usage(usb_mount)
                print(f"[USB] Free space: {free // (1024*1024)} MB")

                track_path = os.path.join(usb_mount, TRANSFER_TRACK_FILE)
                if not os.path.exists(track_path):
                    print("[USB] Creating transferred.txt on USB.")
                    with open(track_path, "w") as f:
                        pass

                with open(track_path, "r") as f:
                    transferred = {line.strip() for line in f if line.strip()}

                # List and sort all cut_* folders by their number
                cut_folders = [f for f in os.listdir(ACQ_FOLDER)
                               if f.startswith("cut_") and os.path.isdir(os.path.join(ACQ_FOLDER, f))]
                cut_folders_sorted = sorted(cut_folders, key=get_cut_number)
                print(f"[USB] All cut folders: {cut_folders_sorted}")

                # Only start transfer if we have more than MIN_CUT_FOLDERS
                if len(cut_folders_sorted) > MIN_CUT_FOLDERS:
                    # Find folders not yet transferred, sorted
                    to_transfer = [f for f in cut_folders_sorted if f not in transferred]
                    print(f"[USB] Not yet transferred: {to_transfer}")

                    if to_transfer:
                        folder = to_transfer[0]  # always the oldest
                        src = os.path.join(ACQ_FOLDER, folder)
                        dst = os.path.join(usb_mount, folder)
                        
                        folder_size = get_folder_size(src)
                        if folder_size > free:
                            print(f"[USB] Not enough space for {folder} ({folder_size // (1024*1024)} MB needed, {free // (1024*1024)} MB free). Waiting...")
                        print(f"[USB] Zipping {folder}...")
                        zip_name = folder + ".zip"
                        zip_path = os.path.join(ACQ_FOLDER, zip_name)

                        try:
                            # Create the zip file in the acquisition folder
                            shutil.make_archive(os.path.splitext(zip_path)[0], 'zip', src)
                            print(f"[USB] Zip created: {zip_path}")

                            # Move zip file to USB
                            usb_zip_path = os.path.join(usb_mount, zip_name)
                            shutil.move(zip_path, usb_zip_path)
                            print(f"[USB] Zip moved to USB: {usb_zip_path}")

                            # Record in transferred.txt
                            with open(track_path, "a") as f:
                                f.write(folder + "\n")

                            # Delete original folder
                            shutil.rmtree(src)
                            print(f"[USB] Deleted folder: {src}")

                        except Exception as e:
                            print(f"[USB] Error in zipping/copying {folder}: {e}")
                    else:
                        print("[USB] No new folders to transfer.")
                else:
                    print(f"[USB] Only {len(cut_folders_sorted)} cut folders found. Waiting until more than {MIN_CUT_FOLDERS} to start transfer.")
                
                # Only process the first USB found to avoid conflicts
                break
        else:
            print("[USB] No USB stick detected. Waiting...")
        await asyncio.sleep(POLL_INTERVAL)

async def main():
    await monitor_usb()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user.")
