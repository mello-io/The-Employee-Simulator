# modules/process_utils.py
# Cross-cutting helpers for launching and terminating processes reliably on Windows.

import os
import shutil
import subprocess
import time
from typing import List, Optional

import psutil

TRACKED_PIDS = set()

def register_pid(pid: int) -> None:
    """Remember a PID so we can clean it up on exit."""
    if pid:
        TRACKED_PIDS.add(pid)

def launch_process(exe_path: str, args: Optional[List[str]] = None, new_console: bool = False) -> subprocess.Popen:
    """
    Launch a process WITHOUT shell=True so we get the true child PID.
    If you pass a .lnk or a verb-only command, resolution may fail — prefer absolute .exe paths.
    """
    if args is None:
        args = []
    creationflags = 0
    # Note: CREATE_NEW_CONSOLE is Windows-only; if you ever want a new console, uncomment next line.
    # creationflags |= subprocess.CREATE_NEW_CONSOLE

    # Ensure we pass a list so shell=False works even with spaces in path
    proc = subprocess.Popen([exe_path] + args, shell=False, creationflags=creationflags)
    register_pid(proc.pid)
    return proc

def terminate_tree(pid: int, timeout: float = 5.0, force: bool = True) -> None:
    """
    Gracefully terminate a process and all of its children; escalate to kill if needed.
    Works better than proc.terminate() for GUI apps and browsers that spawn children.
    """
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    # Collect full tree
    children = p.children(recursive=True)

    # Try terminate
    for c in children:
        try:
            c.terminate()
        except psutil.Error:
            pass
    try:
        p.terminate()
    except psutil.Error:
        pass

    # Wait a bit
    gone, alive = psutil.wait_procs(children + [p], timeout=timeout)

    if alive and force:
        # Escalate with kill and Windows taskkill as a last resort
        for a in alive:
            try:
                a.kill()
            except psutil.Error:
                pass
        try:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        except Exception:
            pass

def kill_by_image_name(image_name: str) -> None:
    """Best-effort: kill all processes whose .name() matches image_name (case-insensitive)."""
    low = image_name.lower()
    for p in psutil.process_iter(["name", "pid"]):
        try:
            if p.info["name"] and p.info["name"].lower() == low:
                terminate_tree(p.info["pid"], timeout=2.0, force=True)
        except psutil.Error:
            continue

def cleanup_all_tracked() -> None:
    """Kill all PIDs we launched (plus their trees)."""
    for pid in list(TRACKED_PIDS):
        try:
            terminate_tree(pid, timeout=3.0, force=True)
        except Exception:
            pass
    TRACKED_PIDS.clear()
