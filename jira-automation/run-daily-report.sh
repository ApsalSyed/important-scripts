#!/bin/bash
# Daily Report Generator - Force Run (works on weekends)

cd "$(dirname "$0")"

# Load environment variables
if [ -f .env ]; then
    source .env
fi

source venv/bin/activate
python3 fetch_jira_tasks.py --force

