import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os
import sys

# 🧩 Your Jira details - Loaded from environment variables
EMAIL = os.getenv("JIRA_EMAIL", "apsal@swivl.tech")
API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
DOMAIN = os.getenv("JIRA_DOMAIN", "wormsconnect.atlassian.net")

# Check if API token is set
if not API_TOKEN:
    print("❌ Error: JIRA_API_TOKEN environment variable not set!")
    print("💡 Run: source .env")
    exit(1)

# 📁 Obsidian vault configuration
OBSIDIAN_VAULT_PATH = "/Users/mohammedsayeethapsals/Documents/Obsidian Vault"
OBSIDIAN_FOLDER = "Daily Reports"  # Optional: folder name inside vault (set to "" if you want root)
REPORT_FILENAME = "Daily_Progress_Report.md"  # Single file that gets appended to

# 🔍 JQL query – fetch only "In Progress" tasks assigned to you
JQL_QUERY = "assignee=currentUser() AND status = \"In Progress\" ORDER BY created DESC"

def fetch_jira_tasks():
    # Use the new /rest/api/3/search/jql endpoint (required migration)
    url = f"https://{DOMAIN}/rest/api/3/search/jql"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    # The new endpoint requires POST with JQL in the body
    payload = {
        "jql": JQL_QUERY,
        "maxResults": 20
    }

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN), json=payload)
    
    # Check for errors
    if response.status_code != 200:
        print(f"❌ Error: API returned status code {response.status_code}")
        print(f"Response: {response.text}")
        return []
    
    data = response.json()
    
    # The new /search/jql endpoint returns issue IDs in 'issues' array
    issue_data_list = data.get("issues", [])
    
    # Extract actual issue IDs (they come as dicts with 'id' key)
    issue_ids = []
    for item in issue_data_list:
        if isinstance(item, dict) and "id" in item:
            issue_ids.append(item["id"])
        elif isinstance(item, (str, int)):
            issue_ids.append(item)
    
    # Fetch full issue details for each ID
    issues = []
    headers = {"Accept": "application/json"}
    
    print(f"📊 Found {len(issue_ids)} in-progress task(s)")
    for issue_id in issue_ids[:20]:  # Limit to 20 issues
        issue_url = f"https://{DOMAIN}/rest/api/3/issue/{issue_id}"
        issue_response = requests.get(issue_url, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN))
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
            issues.append(issue_data)
            
            # Print issue info
            key = issue_data.get("key", "UNKNOWN")
            fields = issue_data.get("fields", {})
            summary = fields.get("summary", "No summary")
            status_obj = fields.get("status", {})
            if isinstance(status_obj, dict):
                status = status_obj.get("name", "Unknown")
            else:
                status = str(status_obj)
            print(f"   - {key}: {summary} ({status})")
        else:
            print(f"   ⚠️  Failed to fetch issue {issue_id}: {issue_response.status_code}")
    
    return issues

def generate_daily_report(issues):
    """Generate the daily progress report in the exact format specified"""
    today = datetime.now()
    # Format: "November 4, 2025" (without leading zero on day)
    day = today.day
    current_date = today.strftime(f"%B {day}, %Y")
    
    # Build the markdown content
    markdown = f"# {current_date} - Daily Progress Report\n\n"
    markdown += "## 📦 Module\n\n"
    markdown += "**From Jira Board**\n\n"
    markdown += "## 🧩 What I Did Today\n\n"
    markdown += "* Picked and worked on the following Jira issues:\n\n"
    
    # Add each issue
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        
        # Handle different possible field names
        key = issue.get("key") or issue.get("issueKey") or issue.get("id", "UNKNOWN")
        fields = issue.get("fields", {})
        summary = fields.get("summary", "No summary")
        status_obj = fields.get("status", {})
        if isinstance(status_obj, dict):
            status = status_obj.get("name", "Unknown")
        else:
            status = str(status_obj)
        
        markdown += f"  - {key}: {summary} ({status})\n\n"
    
    # Add separator at the end
    markdown += "---\n\n"
    
    return markdown

def save_report(content):
    """Append the report to the Obsidian vault file"""
    # Create full path to Obsidian vault
    if OBSIDIAN_FOLDER:
        obsidian_dir = os.path.join(OBSIDIAN_VAULT_PATH, OBSIDIAN_FOLDER)
        os.makedirs(obsidian_dir, exist_ok=True)
        filepath = os.path.join(obsidian_dir, REPORT_FILENAME)
    else:
        filepath = os.path.join(OBSIDIAN_VAULT_PATH, REPORT_FILENAME)
    
    # Append to file (create if doesn't exist)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)
    
    return filepath

if __name__ == "__main__":
    # Check for --force flag to bypass weekend check
    force_run = "--force" in sys.argv or "-f" in sys.argv
    
    # Skip execution on weekends (Saturday = 5, Sunday = 6) unless forced
    today = datetime.now()
    weekday = today.weekday()  # Monday = 0, Sunday = 6
    
    if weekday >= 5 and not force_run:  # Saturday (5) or Sunday (6)
        print("⏭️  Skipping report generation on weekends (Saturday/Sunday)")
        print("💡 Tip: Use --force or -f to run manually on weekends")
        exit(0)
    
    if force_run and weekday >= 5:
        print("🚀 Force run enabled - generating report on weekend")
    
    print("🔄 Fetching Jira tasks...")
    issues = fetch_jira_tasks()
    
    if issues:
        report = generate_daily_report(issues)
        filename = save_report(report)
        print(f"✅ Report saved to: {filename}")
    else:
        # Still create a report even if no issues
        report = generate_daily_report([])
        filename = save_report(report)
        print(f"✅ Report saved to: {filename} (no tasks found)")
