#!/usr/bin/env python3
import os
import re
import time
import asyncio
import shutil
import getpass
import zipfile
import fcntl
import errno
from contextlib import contextmanager
from pathlib import Path

# Resolve acquisition_data relative to this file:
SCRIPT_DIR = Path(__file__).resolve().parent          # .../thread
PROJECT_ROOT = SCRIPT_DIR.parent                      # project root

# =================== Configuration ===================

ACQ_FOLDER = str((PROJECT_ROOT / "acquisition_data").resolve())
POLL_INTERVAL = 4  # seconds
TRANSFER_TRACK_FILE = "transferred.txt"
MIN_CUT_FOLDERS = 1  # always keep at least X folders in acquisition_data
LOCKFILE_PATH = "/tmp/usb_transfer.lock"

# Safety margin: require free space >= zip_size + max(64 MiB, 5% of zip_size)
ABS_MARGIN_BYTES = 64 * 1024 * 1024
REL_MARGIN = 0.05

# Optional: minimum headroom on ACQ_FOLDER before we start (to avoid odd failures)
MIN_SRC_HEADROOM = 64 * 1024 * 1024  # 64 MiB

# =====================================================

def find_usb_mounts():
    """Find all USB drives mounted under /media/<username>/ (Linux desktop norm)."""
    base_media = f"/media/{getpass.getuser()}"
    if os.path.isdir(base_media):
        return [os.path.join(base_media, d) for d in os.listdir(base_media)
                if os.path.ismount(os.path.join(base_media, d))]
    return []

def get_cut_number(folder_name):
    m = re.match(r'cut_(\d+)', folder_name)
    return int(m.group(1)) if m else float('inf')

def get_folder_size(folder_path):
    """Approximate total logical size of a folder in bytes (sum of file sizes)."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    st = os.stat(fp, follow_symlinks=False)
                    if not os.path.islink(fp):
                        total_size += st.st_size
                except FileNotFoundError:
                    # file disappeared during traversal
                    pass
    except Exception as e:
        print(f"[USB] Warning: error calculating folder size for {folder_path}: {e}")
    return total_size

def is_vfat_mount(mount_point):
    """Detect if mount point is FAT32/vfat by inspecting /proc/mounts."""
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3:
                    mnt = parts[1]
                    fstype = parts[2]
                    if mnt == mount_point and fstype.lower() in ("vfat", "fat", "msdos"):
                        return True
    except Exception:
        pass
    return False

def safety_margin(bytes_size):
    return max(ABS_MARGIN_BYTES, int(bytes_size * REL_MARGIN))

def format_mb(b):
    return b // (1024 * 1024)

def now_ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")

@contextmanager
def single_instance_lock(lockfile_path):
    """Ensure only one instance runs at a time using an advisory file lock."""
    fd = os.open(lockfile_path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.write(fd, str(os.getpid()).encode("ascii"))
        yield
    except BlockingIOError:
        raise RuntimeError("Another instance is already running.")
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except Exception:
            pass
        os.close(fd)
        try:
            os.remove(lockfile_path)
        except Exception:
            pass

def ensure_track_file(usb_mount):
    track_path = os.path.join(usb_mount, TRANSFER_TRACK_FILE)
    if not os.path.exists(track_path):
        print(f"[USB] Creating {TRANSFER_TRACK_FILE} on USB.")
        with open(track_path, "w"):
            pass
    return track_path

def read_transferred(track_path):
    try:
        with open(track_path, "r") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

def write_transferred(track_path, folder):
    with open(track_path, "a") as f:
        f.write(folder + "\n")

def estimate_clearly_insufficient(folder_size, tgt_free):
    """
    Abort early if it's clearly impossible:
    We assume worst case zip_size ~ folder_size + safety overhead.
    This is conservative for already-compressed data (zip may be ~same size).
    """
    worst_zip = folder_size + safety_margin(folder_size)
    return worst_zip > tgt_free

def zip_directory_stream_to_usb(src_dir, usb_mount, final_zip_name, is_vfat):
    """
    Stream a ZIP of src_dir directly to the USB device as <final_zip_name>.part,
    then rename to <final_zip_name> upon success.

    Returns: absolute path to final zip, and its size in bytes.
    Raises OSError on ENOSPC or other IO errors. Cleans up partial on failure.
    """
    part_path = os.path.join(usb_mount, final_zip_name + ".part")
    final_path = os.path.join(usb_mount, final_zip_name)

    # Open target as a file object, and give it to ZipFile
    # Use DEFLATED if available; fallback to ZIP_STORED for safety.
    compression = zipfile.ZIP_DEFLATED
    if not zipfile.is_zipfile.__doc__:  # no good check; keep default
        pass

    # Build a stable list of files first (so we can zip in deterministic order)
    files = []
    src_dir = os.path.abspath(src_dir)
    for dirpath, _, filenames in os.walk(src_dir):
        for name in sorted(filenames):
            abs_path = os.path.join(dirpath, name)
            if os.path.islink(abs_path):
                # skip symlinks for safety
                continue
            files.append(abs_path)

    # Ensure we start with enough space for metadata + margin
    _, _, free0 = shutil.disk_usage(usb_mount)
    if free0 < ABS_MARGIN_BYTES:
        raise OSError(errno.ENOSPC, "Not enough initial free space on USB.")

    # Create/overwrite .part
    # If a previous partial exists, remove it
    try:
        if os.path.exists(part_path):
            os.remove(part_path)
    except Exception:
        pass

    bytes_written_last_check = 0
    try:
        with open(part_path, "wb") as fobj:
            with zipfile.ZipFile(fobj, mode="w", compression=compression, allowZip64=True) as zf:
                for abs_path in files:
                    rel_arcname = os.path.relpath(abs_path, start=os.path.dirname(src_dir))
                    # Write file into the zip
                    zf.write(abs_path, arcname=rel_arcname)

                    # Optional progress-space checks
                    # Check how big the .part file is becoming
                    try:
                        current_size = fobj.tell()
                    except Exception:
                        current_size = os.path.getsize(part_path)

                    # If VFAT (FAT32), enforce < 4 GiB single-file limit
                    if is_vfat and current_size >= (4 * 1024**3):
                        raise OSError(errno.EFBIG, "FAT32 limit: single file must be < 4 GiB.")

                    # Avoid spamming disk_usage; check when growth exceeds 64 MiB since last check
                    if current_size - bytes_written_last_check >= ABS_MARGIN_BYTES:
                        _, _, free_now = shutil.disk_usage(usb_mount)
                        if free_now <= ABS_MARGIN_BYTES:
                            # We are about to run out; force an error so we can cleanly abort
                            raise OSError(errno.ENOSPC, "USB nearly out of space during write.")
                        bytes_written_last_check = current_size

            # Ensure all data is flushed to the device
            fobj.flush()
            os.fsync(fobj.fileno())

        # Final size of the .part
        zip_size = os.path.getsize(part_path)

        # One more free-space check (not strictly necessary for rename, but explicit)
        _, _, free_after = shutil.disk_usage(usb_mount)
        required_margin = safety_margin(zip_size)
        if free_after < required_margin:
            # We *could* still rename, but we honor the policy and keep headroom
            raise OSError(errno.ENOSPC, f"Free space {format_mb(free_after)} MB below safety margin.")

        # Crash-safe publish: atomic rename
        os.replace(part_path, final_path)
        print(f"[USB] {now_ts()} ZIP complete: {final_path} ({format_mb(zip_size)} MB)")
        return final_path, zip_size

    except Exception as e:
        # Clean up partial
        try:
            if os.path.exists(part_path):
                os.remove(part_path)
        except Exception:
            pass
        raise

async def monitor_usb():
    while True:
        usb_mounts = find_usb_mounts()
        if usb_mounts:
            # Only process the first USB found to avoid conflicts
            usb_mount = usb_mounts[0]
            print(f"[USB] {now_ts()} USB stick detected at {usb_mount}")

            # Ensure tracking file on USB
            track_path = ensure_track_file(usb_mount)
            transferred = read_transferred(track_path)

            # Summarize space
            total, used, free = shutil.disk_usage(usb_mount)
            print(f"[USB] Free space on USB: {format_mb(free)} MB")

            # List and sort cut_* folders (oldest first)
            cut_folders = [f for f in os.listdir(ACQ_FOLDER)
                           if f.startswith("cut_") and os.path.isdir(os.path.join(ACQ_FOLDER, f))]
            cut_folders_sorted = sorted(cut_folders, key=get_cut_number)
            print(f"[USB] All cut folders: {cut_folders_sorted}")

            if len(cut_folders_sorted) > MIN_CUT_FOLDERS:
                # Find not-yet-transferred
                to_transfer = [f for f in cut_folders_sorted if f not in transferred]
                print(f"[USB] Not yet transferred: {to_transfer}")

                if to_transfer:
                    folder = to_transfer[0]  # oldest first
                    src = os.path.join(ACQ_FOLDER, folder)
                    final_zip_name = folder + ".zip"

                    # Check source headroom (not strictly required for streaming, but requested)
                    _, _, src_free = shutil.disk_usage(ACQ_FOLDER)
                    if src_free < MIN_SRC_HEADROOM:
                        print(f"[USB] Not enough free space on source drive (need >= {format_mb(MIN_SRC_HEADROOM)} MB). Waiting...")
                        await asyncio.sleep(POLL_INTERVAL)
                        continue

                    # Pre-check: if clearly insufficient, skip (continue)
                    folder_size = get_folder_size(src)
                    _, _, tgt_free = shutil.disk_usage(usb_mount)
                    if estimate_clearly_insufficient(folder_size, tgt_free):
                        print(f"[USB] Clearly insufficient space for {folder} "
                              f"(folder ~{format_mb(folder_size)} MB, free {format_mb(tgt_free)} MB incl. margin). Waiting...")
                        await asyncio.sleep(POLL_INTERVAL)
                        continue

                    # Filesystem type check for FAT32
                    vfat = is_vfat_mount(usb_mount)
                    if vfat:
                        print("[USB] Detected FAT32/vfat on USB (single file must be < 4 GiB).")

                    # Stream zip directly to USB as .part
                    print(f"[USB] {now_ts()} Zipping (stream) {folder} -> USB (.part then rename)...")
                    try:
                        final_path, zip_size = zip_directory_stream_to_usb(
                            src_dir=src,
                            usb_mount=usb_mount,
                            final_zip_name=final_zip_name,
                            is_vfat=vfat
                        )
                    except OSError as e:
                        if e.errno in (errno.ENOSPC, errno.EFBIG):
                            print(f"[USB] Space/size error while zipping {folder}: {e}. Will retry later.")
                        else:
                            print(f"[USB] I/O error while zipping {folder}: {e}.")
                        # Do not mark transferred; do not delete src
                        await asyncio.sleep(POLL_INTERVAL)
                        continue
                    except Exception as e:
                        print(f"[USB] Unexpected error while zipping {folder}: {e}")
                        await asyncio.sleep(POLL_INTERVAL)
                        continue

                    # At this point the .zip is fully written on the USB and renamed atomically
                    # Record in transferred.txt
                    write_transferred(track_path, folder)

                    # Delete original folder
                    try:
                        shutil.rmtree(src)
                        print(f"[USB] Deleted source folder: {src}")
                    except Exception as e:
                        print(f"[USB] Warning: could not delete source folder {src}: {e}")

                else:
                    print("[USB] No new folders to transfer.")
            else:
                print(f"[USB] Only {len(cut_folders_sorted)} cut folders found. Waiting for > {MIN_CUT_FOLDERS} to start.")
        else:
            print(f"[USB] {now_ts()} No USB stick detected. Waiting...")

        await asyncio.sleep(POLL_INTERVAL)

async def main():
    # Single-instance guard
    try:
        with single_instance_lock(LOCKFILE_PATH):
            await monitor_usb()
    except RuntimeError as e:
        print(f"[USB] {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user.")
