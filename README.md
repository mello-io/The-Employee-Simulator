# 🖥️ User Simulation Framework

A modular Python framework to simulate normal employee behavior on Windows endpoints for EDR baseline research and testing.

This project helps researchers create repeatable, controllable, and realistic user activity patterns (apps, websites, breaks, browsing, system actions) for evaluating endpoint security solutions such as Palo Alto Cortex.

---

## 📌 Features

- 🎲 Randomized App Usage\
  Opens and closes applications from a defined list at random intervals (1–4 min).
- 🌐 Website Browsing Simulation\
  Visits websites (work & personal) in a browser with realistic durations.
- ☕ Idle Breaks\
  Simulates user micro/lunch breaks (up to 10 min).
- 📑 Detailed Logging\
  Every action is logged in ` logs/<log-<date>.txt ` with timestamps and durations.
- 🛠️ Modular Design\
  Extend functionality easily by adding new modules (e.g., system interactions, file usage).
- ⏳ Continuous Simulation\
  Runs until stopped, logging termination events (` Ctrl+C `).

---

## 🗂️ Project Structure

```
User-Simulation-Framework/
│
├── main.py                # Entry point for simulation
|
├── data/                  # Data folder (containing the simulation worksflow lists)
│   ├── apps.txt           # List of app executable paths
│   └── websites.txt           # List of websites for browsing
|
├── requirements.txt       # Python dependencies for User Simulation Framework
|
├── logs/                  # Logs folder (auto-created per run)
│   └── log-<date>.txt
│
├── modules/               # Modular simulation features
│   ├── apps.py            # Application open/close logic
│   ├── websites.py        # Browser website simulation
│   ├── breaks.py          # Idle/lunch break simulation
│   ├── browsing.py        # Advanced browser features (multi-tabs, surfing)
│   ├── system_actions.py  # System-level actions (volume, settings)
│   └── __init__.py
└── .gitignore             # Avoid clutter like cache files, logs, and system-specific junk.

```

---

## 📖 Roadmap

## ✅ Phase 1 (Completed)

- Random app usage (open/close with duration).
- Website browsing (open/close with duration).
- Idle breaks (up to 10 minutes).
- Logging (log-<date>.txt) with timestamps & durations.
- Modular architecture.
- Fixed app/browser closing via PID tracking.
- Continuous execution until stopped.

⚠️ : Comprehensive Phase 1 documentation to be released soon.



## 🚀 Phase 2 (Planned)

- 🖱️ System Interactions: adjust volume, brightness, open/close settings panels.
- 🌐 Advanced Browsing: multi-tab browsing, random surfing (e.g., YouTube, TryHackMe, Spotify, VirusTotal, home decor sites).
- 📂 File Interactions: open/edit/close documents, PDFs, spreadsheets.
- 🎵 Media Player Simulation: play/pause music or video apps.
- 📊 Analytics/Export: structured JSON/CSV logs for timeline analysis.
- ⚡ Error Handling Hooks: resilient execution (no crash on one module failure).

---

## 📋 Usage

1. Clone the repo:
```
git clone https://github.com/mello-io/user-simulation-framework.git
cd user-simulation-framework
```
2. Install requirements:
```
pip install -r requirements.txt
```
3. Edit ` apps.txt ` and ` websites.txt ` with your environment.
4. Run the simulation:
```
python main.py
```
5. Logs will be saved to logs/log-<date>.txt.

---

## 📝 Development Notes

This repository is structured to keep the focus on simulation scripts and configurations.
To ensure clean commits and version control, a .gitignore file is included with the following rules:
- Logs ignored → All runtime logs (` logs/ `, ` log-*.txt `) are excluded from Git history.
- Virtual environments ignored → ` venv/ `, ` .venv/ `, or ` env/ ` folders are excluded to avoid bulky, system-specific files.
- Cache files ignored → Python ` __pycache__/ ` and ` .pyc ` files are ignored.
- System/IDE files ignored → macOS ` .DS_Store `, Windows ` Thumbs.db `, and IDE configs (` .vscode/ `, ` .idea/ `) are excluded.

This keeps the repo lightweight and portable, focusing only on:
- Simulation modules (` apps.py `, ` websites.py `, ` browsing.py `, ` breaks.py `, ` system_actions.py `)
- The main orchestration script (` main.py `)
- Configuration files (` apps.txt `, ` websites.txt `)
- Documentation (` README.md `, roadmaps, and future notes)

---

⚠️ Disclaimer

This framework is built for research and education purposes only.
Run it only in controlled environments where you have authorization.

---
✨ Developed & Maintained by @mello-io
