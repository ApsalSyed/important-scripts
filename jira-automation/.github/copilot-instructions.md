# AI Agent Instructions for Jira Automation Scripts

## 🏗️ Project Overview

This is a Jira task automation system that generates daily progress reports by fetching in-progress tasks from Jira and formatting them into Markdown reports.

## 🔑 Key Components

- `fetch_jira_tasks.py`: Main Python script that handles Jira API interaction and report generation
- Shell scripts for different execution modes:
  - `run:daily-report` / `run-daily-report.sh`: Force run (works on weekends)
  - `run:report` / `run-report.sh`: Normal run (skips weekends)

## 💡 Important Patterns & Conventions

### Environment Setup

- Required environment variables:
  ```
  JIRA_EMAIL
  JIRA_API_TOKEN
  JIRA_DOMAIN (defaults to wormsconnect.atlassian.net)
  ```
- Python virtual environment expected in `venv/` directory

### Data Flow

1. Script fetches "In Progress" tasks via Jira API v3
2. Processes and formats tasks into Markdown
3. Appends to `/Users/mohammedsayeethapsals/Documents/Obsidian Vault/Daily Reports/Daily_Progress_Report.md`

### Error Handling

- Environment variable checks with descriptive error messages
- Weekend execution protection (unless --force flag used)
- API response validation with status code checks
- Logging to `jira_script.log` and `jira_script_error.log`

## 🛠️ Development Workflow

1. Always work within the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Test changes with force run:
   ```bash
   python3 fetch_jira_tasks.py --force
   ```
3. Check logs in `jira_script.log` for execution details

## 🔄 Integration Points

- Jira API v3 (`/rest/api/3/search/jql` endpoint)
- Local filesystem (Obsidian vault for report storage)
- System launchd for automation (runs 7 PM daily, Mon-Fri)

## ⚠️ Common Pitfalls

- Not sourcing `.env` file before running script
- Running outside virtual environment
- Modifying report format without updating Obsidian links/references
- Running on weekends without --force flag
