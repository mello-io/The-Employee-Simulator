import datetime
import os

# --- Setup log folder ---
LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# --- Centralized log function ---
def log(message, verbose=True):
    """
    Logs a message to console and a daily log file.
    
    Args:
        message (str): Message to log.
        verbose (bool): If True, prints to console.
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    # Print to console if verbose
    if verbose:
        print(log_message)

    # Append to daily log file
    log_file = os.path.join(LOG_FOLDER, f"log-{now.strftime('%Y-%m-%d')}.txt")
    try:
        with open(log_file, "a") as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to write to log file: {e}")
