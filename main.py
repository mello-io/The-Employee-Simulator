import random
import time
import signal
import sys
import pyfiglet
import os
import subprocess

from logger import log
from modules import apps, websites, breaks, browsing, system_action
from modules import process_utils as pu
from modules.startup_check import run_startup_check as full_check


# --- ASCII Banner ---
def print_banner():
    """Prints a ASCII banner for the User Simulator."""
    ascii_banner = pyfiglet.figlet_format("The Employee \nSimulator v1.2")
    print(ascii_banner)
    print("By - @mello-io")
    print("-" * 30 + "\n")

# Load data files
def load_list(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

# --- List loading ---
apps_list = apps.load_apps()
websites_list = websites.load_websites()


# --- Graceful exit handler (Ctrl+C logging) ---
def handle_exit(sig, frame):
    log("[SYSTEM] Ctrl+C detected. Cleaning up tracked processes...")
    try:
        pu.cleanup_all_tracked()
    finally:
        log("[SYSTEM] Exiting now.")
        sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# --- Main loop ---
def main():
    print_banner()
    log("[SYSTEM] Simulation started")
    full_check()
    #apps_list, websites_list = full_check()

    try:
        
        while True:
            # Randomly choose an activity
            activity = random.choice(["apps", "website", "break", "browsing", "system_action"])

            apps_list = apps.load_apps()
            apps_map = apps.load_apps_map()
            
            if activity == "apps":
                apps.simulate_apps_usage(apps_list)

            elif activity == "website":
                websites.simulate_website_usage(websites_list)

            elif activity == "break":
                breaks.take_break()

            elif activity == "browsing":
                browsing.simulate_multi_tab_browsing(websites_list)

            elif activity == "system_action":
                system_action.run_action()

            # No wait time between actions (per your last request)
    
    except KeyboardInterrupt:
        handle_exit(None, None)
    finally:
        # belt & suspenders cleanup
        pu.cleanup_all_tracked()    

if __name__ == "__main__":
    main()
