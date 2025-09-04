# modules/browsing.py
import os
import random
import tempfile
import shutil
import time

from logger import log
from . import process_utils as pu
from .websites import _find_browser  # reuse the same detector

def simulate_multi_tab_browsing(websites_list):
    browser = _find_browser()
    if not browser:
        log("[BROWSING][ERROR] No supported browser found.")
        return

    num_tabs = min(len(websites_list), random.randint(2, 4))
    urls = random.sample(websites_list, num_tabs)
    duration = random.randint(60, 240)  # 1–4 minutes
    profile_dir = tempfile.mkdtemp(prefix="sim_browser_profile_")

    log(f"[BROWSING] Opening {num_tabs} tabs for {duration//60}m {duration%60}s via {os.path.basename(browser)}")
    for u in urls:
        log(f"[BROWSING]  - {u}")

    args = [
        "--new-window",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ] + urls

    try:
        proc = pu.launch_process(browser, args=args, new_console=False)
    except Exception as e:
        log(f"[BROWSING][ERROR] Launch failed: {e}")
        shutil.rmtree(profile_dir, ignore_errors=True)
        return

    time.sleep(duration)

    try:
        pu.terminate_tree(proc.pid, timeout=5.0, force=True)
        log("[BROWSING] Closed multi-tab session")
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)
