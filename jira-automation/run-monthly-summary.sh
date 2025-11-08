#!/bin/bash
# Monthly Summary Generator

cd "$(dirname "$0")"

# Load environment variables
if [ -f .env ]; then
    source .env
fi

source venv/bin/activate

# Check if --force flag is passed
if [ "$1" == "--force" ] || [ "$1" == "-f" ]; then
    python3 fetch_jira_tasks.py --monthly --force
else
    python3 fetch_jira_tasks.py --monthly
fi

