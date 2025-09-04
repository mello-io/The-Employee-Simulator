# modules/websites.py
import os
import random
import tempfile
import shutil
import time

from logger import log
from . import process_utils as pu

CANDIDATE_BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
]

def _find_browser():
    for p in CANDIDATE_BROWSERS:
        if os.path.exists(p):
            return p
    return None

def load_websites(file_path="data/websites.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

def simulate_website_usage(websites_list):
    browser = _find_browser()
    if not browser:
        log("[WEB][ERROR] No supported browser found. Update CANDIDATE_BROWSERS with your path.")
        return

    url = random.choice(websites_list)
    duration = random.randint(60, 240)  # 1–4 minutes
    profile_dir = tempfile.mkdtemp(prefix="sim_browser_profile_")

    log(f"[WEB] Opening: {url} (for {duration//60}m {duration%60}s) via {os.path.basename(browser)}")
    args = [
        "--new-window",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]

    try:
        proc = pu.launch_process(browser, args=args, new_console=False)
    except Exception as e:
        log(f"[WEB][ERROR] Launch failed: {e}")
        shutil.rmtree(profile_dir, ignore_errors=True)
        return

    time.sleep(duration)

    # Close browser tree and remove temp profile
    try:
        pu.terminate_tree(proc.pid, timeout=5.0, force=True)
        log("[WEB] Closed browser session")
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)
