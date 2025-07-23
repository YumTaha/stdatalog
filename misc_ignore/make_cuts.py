import os
import sys

# --- CONFIG ---
ACQ_FOLDER = "/home/kirwinr/Desktop/stdatalog/acquisition_data"
N = 15  # Number of folders to create; change as needed

if len(sys.argv) > 1:
    N = int(sys.argv[1])

os.makedirs(ACQ_FOLDER, exist_ok=True)

for i in range(1, N + 1):
    folder = os.path.join(ACQ_FOLDER, f"cut_{i}")
    try:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")
    except Exception as e:
        print(f"Error creating {folder}: {e}")
