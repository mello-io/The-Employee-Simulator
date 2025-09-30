import subprocess
import os
import datetime
from logger import log

from modules import apps, websites

# --- List loading ---

apps_list = apps.load_apps()
websites_list = websites.load_websites()


# --- Chocolatey Check ---
def check_chocolatey():
    """Check if Chocolatey is installed"""
    try:
        subprocess.check_output("choco -v", shell=True)
        log("[+] Chocolatey is installed.")
        return True
    except subprocess.CalledProcessError:
        log("[-] Chocolatey is NOT installed. (Bootstrap code available but skipped)")
        return False
    except FileNotFoundError:
        log("[-] Chocolatey command not found. (Bootstrap code available but skipped)")
        return False

# --- Chocolatey Bootstrap ---
def install_chocolatey():
    # Install Chocolatey if it’s missing (production use)
    try:
        subprocess.check_output("choco -v", shell=True)
        log("[+] Chocolatey already installed.")
    except subprocess.CalledProcessError:
        log("[*] Installing Chocolatey...")
        install_cmd = (
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = "
            "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", install_cmd],
            check=True
        )
        log("[+] Chocolatey installation complete.")


# --- App Installation Check ---
def check_or_install_apps(apps_file="data/apps.txt"):
    """Check and install apps listed in apps.txt"""
    if not os.path.exists(apps_file):
        log(f"[!] Apps file {apps_file} not found.")
        return

    with open(apps_file, "r") as f:
        apps = [line.strip() for line in f if line.strip()]

    for app in apps:
        try:
            # Check if app is already installed via Chocolatey
            subprocess.check_output(f"choco list {app}", shell=True, text=True)
            log(f"[=] {app} is already installed.")
            continue
        except subprocess.CalledProcessError:
            log(f"[*] {app} not installed. Installing...")
            try:
                subprocess.run(f"choco install {app} -y", shell=True, check=True)
                log(f"[+] Successfully installed {app}.")
            except subprocess.CalledProcessError:
                log(f"[!] Failed to install {app}.")

# --- Website List Check ---
def check_websites(websites_file="data/websites.txt"):
    """Check if websites.txt exists and log the list"""
    if not os.path.exists(websites_file):
        log(f"[!] Websites file {websites_file} not found.")
        return []

    with open(websites_file, "r") as f:
        websites = [line.strip() for line in f if line.strip()]

    log(f"[+] Found {len(websites)} websites in {websites_file}.")
    return websites

# --- Entry Point for Startup Check ---
def run_startup_check():
    """Run baseline checks before starting simulations"""
    log("=== Running Startup Check ===")
    if check_chocolatey():
        check_or_install_apps()
        # Uncomment below if you want auto-installation of Chocolatey in prod
        # install_chocolatey()
    log(f"Loaded {len(apps_list)} applications from data/apps.txt")
    log(f"Loaded {len(websites_list)} websites from data/websites.txt")    
    log("=== Startup Check Complete ===")
