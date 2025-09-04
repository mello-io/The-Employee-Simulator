import random
from logger import log

def run_action():
    """Simulate basic system-level actions like volume/brightness"""
    actions = ["adjust_volume", "adjust_brightness", "open_settings", "close_settings"]
    action = random.choice(actions)

    # Just log them (no real system control for now)
    log(f"[SYSTEM ACTION] Performed: {action}")
