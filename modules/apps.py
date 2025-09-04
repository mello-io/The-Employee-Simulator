# modules/apps.py
import os
import random
import time
from logger import log
from . import process_utils as pu

def load_apps(file_path="data/apps.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

def simulate_apps_usage(apps_list):
    app_path = random.choice(apps_list)
    duration = random.randint(60, 240)  # 1–4 minutes
    exe_name = os.path.basename(app_path)

    log(f"[APP] Launching: {app_path} (for {duration//60}m {duration%60}s)")
    try:
        # Prefer absolute .exe paths here; .lnk is unreliable for PID tracking
        proc = pu.launch_process(app_path, args=[], new_console=False)
    except Exception as e:
        log(f"[APP][ERROR] Failed to start '{app_path}': {e}")
        return

    time.sleep(duration)

    # Try clean termination of the full tree
    try:
        pu.terminate_tree(proc.pid, timeout=5.0, force=True)
        log(f"[APP] Closed: {exe_name}")
    except Exception as e:
        log(f"[APP][WARN] Tree terminate failed for PID {proc.pid}: {e}; trying image-name kill")
        pu.kill_by_image_name(exe_name)
