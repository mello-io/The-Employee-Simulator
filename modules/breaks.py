import random, time
from logger import log

def take_break():
    """Simulate short idle/lunch breaks (max 10 minutes)"""
    duration = random.randint(60, 120)  # 1–5 minutes ; can be increased later
    log(f"[BREAK] Taking a break for {duration//60}m {duration%60}s")
    time.sleep(duration)
    log("[BREAK] Break finished, back to work !!")
