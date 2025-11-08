# Jira Daily Progress Report Automation

This folder contains the automated Jira daily progress report system.

## 📂 Contents

- `fetch_jira_tasks.py` - Main script that fetches Jira tasks
- `run:daily-report` - Convenience script (force run, works on weekends)
- `run:report` - Convenience script (normal run, skips weekends)
- `run-daily-report.sh` - Shell script (force run)
- `run-report.sh` - Shell script (normal run)
- `README.md` - This file (quick reference)
- `README_JIRA_AUTOMATION.md` - Complete documentation
- `venv/` - Python virtual environment with dependencies
- `jira_script.log` - Execution logs
- `jira_script_error.log` - Error logs

## 🚀 Quick Start

### Using convenience scripts (easiest):

```bash
cd /Users/mohammedsayeethapsals/workspace/Swivl/scripts/jira-automation

# Force run (works on weekends)
./run:daily-report

# Normal run (skips weekends)
./run:report
```

### Manual Run

```bash
cd /Users/mohammedsayeethapsals/workspace/Swivl/scripts/jira-automation
source venv/bin/activate
python3 fetch_jira_tasks.py
```

### Force Run (weekends)

```bash
python3 fetch_jira_tasks.py --force
```

## 📖 Full Documentation

See [README_JIRA_AUTOMATION.md](./README_JIRA_AUTOMATION.md) for complete documentation including:

- Installation instructions
- Configuration options
- Automation setup
- Troubleshooting
- Customization

## ⚙️ Automation Status

The script runs automatically at **7 PM daily** (Monday-Friday).

Check status:

```bash
launchctl list | grep jira
```

## 📁 Output Location

Reports are appended to:

```
/Users/mohammedsayeethapsals/Documents/Obsidian Vault/Daily Reports/Daily_Progress_Report.md
```
