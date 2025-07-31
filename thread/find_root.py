#!/usr/bin/env python3
import os
import json
import subprocess

ROOT_HINT_FILENAME = "stdatalog_root.json"

def find_stdatalog_root():
    """Search for the 'stdatalog' root folder based on exact directory name."""
    try:
        print("🔍 Searching for 'stdatalog' directory across filesystem...")
        result = subprocess.run(
            ["find", "/", "-type", "d", "-name", "stdatalog"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        matches = result.stdout.strip().split('\n')
        for match in matches:
            if os.path.basename(match.strip()) == "stdatalog":
                return os.path.abspath(match)
    except Exception as e:
        print(f"❌ Error during search: {e}")
    return None

def get_hint_file_path(root_path=None):
    """Return the full path to stdatalog_root.json inside the stdatalog directory."""
    if root_path is None:
        root_path = load_root_path()
    return os.path.join(root_path, ROOT_HINT_FILENAME) if root_path else ROOT_HINT_FILENAME

def save_root_path(root_path):
    """Save the root path to stdatalog_root.json inside the stdatalog folder."""
    try:
        hint_path = get_hint_file_path(root_path)
        with open(hint_path, "w") as f:
            json.dump({"stdatalog_root": root_path}, f)
        print(f"✅ STDatalog root path saved to {hint_path}")
    except Exception as e:
        print(f"❌ Failed to save root path: {e}")

def load_root_path():
    """Load the root path from stdatalog_root.json inside the stdatalog directory."""
    # Try standard relative path first (if running inside stdatalog)
    cwd = os.getcwd()
    local_hint = os.path.join(cwd, ROOT_HINT_FILENAME)
    if os.path.exists(local_hint):
        print(f"[DEBUG] Found local hint file at {local_hint}")
        with open(local_hint, "r") as f:
            return json.load(f).get("stdatalog_root")

    # Try one level up (if script is inside stdatalog/services or similar)
    parent = os.path.abspath(os.path.join(cwd, ".."))
    fallback_hint = os.path.join(parent, ROOT_HINT_FILENAME)
    if os.path.exists(fallback_hint):
        print(f"[DEBUG] Found fallback hint file at {fallback_hint}")
        with open(fallback_hint, "r") as f:
            return json.load(f).get("stdatalog_root")

    print("[DEBUG] No stdatalog_root.json found in expected locations.")
    return None

def find_subfolder(name):
    """Find a named subfolder anywhere inside the STDatalog root."""
    root = load_root_path()
    if not root:
        print("⚠️ Root path not found. Run this script once to detect and save it.")
        return None

    for dirpath, dirnames, _ in os.walk(root):
        if name in dirnames:
            full_path = os.path.join(dirpath, name)
            print(f"📁 Found '{name}': {full_path}")
            return full_path

    print(f"❌ Subfolder '{name}' not found inside {root}")
    return None

if __name__ == "__main__":
    print("🔧 Running STDatalog root finder...")

    # Only try to detect root if not already cached
    if not load_root_path():
        root = find_stdatalog_root()
        if root:
            save_root_path(root)
            print(f"📁 STDatalog root is: {root}")
        else:
            print("❌ Could not find STDatalog root.")
    else:
        print("ℹ️ Root already saved. No need to re-scan.")
