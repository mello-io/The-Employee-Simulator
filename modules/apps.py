# modules/apps.py

import os
import random
import time
import json
import shutil

from logger import log
from . import process_utils as pu

# --- Common install locations to search ---
COMMON_PATHS = [
    r"C:\\Program Files\\",
    r"C:\\Program Files (x86)\\",
    os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
]

# --- Load apps from apps.txt ---
def load_apps(file_path="data/apps.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

# --- Unifed App map loader ---
def load_apps_map(json_file="data/apps_map.json"):
    if not os.path.exists(json_file):
        log("[APP][WARN] apps_map.json not found. Will try Auto-Detection and PATH.")
        return {}

    with open(json_file, "r") as f:
        apps_map = json.load(f)

    resolved_map = {}
    for key, path in apps_map.items():
        # Expand %USERNAME% and other env vars
        expanded_path = os.path.expandvars(path)
        # Normalize slashes for Windows
        expanded_path = os.path.normpath(expanded_path)
        resolved_map[key] = expanded_path

    return resolved_map


    
# --- Try to auto-locate an executable ---
def auto_locate_app(app_name):
    exe_name = f"{app_name}.exe".lower()
    for base in COMMON_PATHS:
        for root, dirs, files in os.walk(base):
            for f in files:
                if f.lower() == exe_name:
                    return os.path.join(root, f)
    return None


# --- Simulate app usage ---
def simulate_apps_usage(apps_list, apps_map=None):
    if not apps_list:
        log("[APP][ERROR] No apps available to simulate.")
        return
    
    if apps_map is None:
        apps_map = load_apps_map()
        
    # Pick a random app ID (the key from apps.txt, e.g. "sumatrapdf") (without .exe)
    app_id = random.choice(apps_list).lower()
    app_exec = None #apps_map.get(app_id, app_id)  # fall back to PATH if no mapping    
    
    #app_path = random.choice(apps_list)
    #exe_name = os.path.basename(app_path)
    
    # 1. Use mapping if available
    if app_id in apps_map:
        app_exec = apps_map[app_id]

    # 2. Try auto-detection
    if not app_exec:
        app_exec = auto_locate_app(app_id)

    # 3. Fallback: assume it's in PATH (add .exe)
    if not app_exec:
        app_exec = app_id + ".exe"

    
    duration = random.randint(60, 240)  # 1–4 minutes
    log(f"[APP] Launching: {app_id} (for {duration//60}m {duration%60}s)")
    log(f"[APP][DEBUG] PATH: {app_id} executed from location {app_exec}")

    try:
        # Prefer absolute .exe paths here; .lnk is unreliable for PID tracking
        proc = pu.launch_process(app_exec, args=[], new_console=True)
    except Exception as e:
        log(f"[APP][ERROR] Failed to start '{app_exec}': {e}")
        return

    time.sleep(duration)

    # Try clean termination of the full tree
    try:
        pu.terminate_tree(proc.pid, timeout=5.0, force=True)
        log(f"[APP] Closed: {app_id}")
    except Exception as e:
        log(f"[APP][WARN] Tree terminate failed for PID {proc.pid}: {e}; trying image-name kill")
        pu.kill_by_image_name(app_id)
