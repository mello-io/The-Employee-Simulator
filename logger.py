import datetime

def log(message):
    """Central logger for all modules"""
    date = datetime.datetime.now().strftime("%m-%d-%Y")
    logfile = f"log-{date}.txt"
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    with open(logfile, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")
