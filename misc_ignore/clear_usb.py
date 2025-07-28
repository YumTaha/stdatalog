import os
import shutil

USB_MOUNT_PATH = "/media/kirwinr/AA19-6A98"

if not os.path.ismount(USB_MOUNT_PATH):
    print(f"WARNING: {USB_MOUNT_PATH} does not appear to be mounted. Proceeding anyway...")

for name in os.listdir(USB_MOUNT_PATH):
    path = os.path.join(USB_MOUNT_PATH, name)
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            print(f"Deleted file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Deleted folder: {path}")
    except Exception as e:
        print(f"Failed to delete {path}: {e}")

print("USB stick cleared.")
