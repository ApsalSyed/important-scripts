import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os
import sys
import re
from collections import defaultdict, Counter

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
TRACKING_FOLDER = "Tracking"  # Base folder for all reports
OBSIDIAN_FOLDER = os.path.join(TRACKING_FOLDER, "Daily Reports")  # Daily reports subfolder
REPORT_FILENAME = "Daily_Progress_Report.md"  # Single file that gets appended to
MONTHLY_REPORTS_FOLDER = os.path.join(TRACKING_FOLDER, "Monthly Reports")  # Monthly reports subfolder

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
    
    # Extract unique labels from all issues
    labels = set()
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        fields = issue.get("fields", {})
        issue_labels = fields.get("labels", [])
        if issue_labels:
            # Labels are strings directly, not objects
            for label in issue_labels:
                if label:
                    labels.add(label)
    
    # Display labels or fallback to "From Jira Board"
    if labels:
        label_list = ", ".join(sorted(labels))
        markdown += f"**{label_list}**\n\n"
    else:
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

def parse_daily_report_file(filepath):
    """Parse the daily report file and extract all daily entries"""
    if not os.path.exists(filepath):
        return [], ""
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by date headers (format: "# Month Day, Year - Daily Progress Report")
    date_pattern = r'# (\w+ \d+, \d+) - Daily Progress Report'
    
    entries = []
    sections = re.split(date_pattern, content)
    
    # Skip first empty section if exists
    if sections and not sections[0].strip():
        sections = sections[1:]
    
    # Process pairs: (date, content)
    for i in range(0, len(sections) - 1, 2):
        if i + 1 < len(sections):
            date_str = sections[i]
            entry_content = sections[i + 1]
            entries.append({
                'date': date_str,
                'content': entry_content
            })
    
    return entries, content

def extract_issues_from_entry(entry_content):
    """Extract issue information from a daily report entry"""
    issues = []
    labels = set()
    
    # Extract module/labels (between ## 📦 Module and ## 🧩 What I Did Today)
    module_match = re.search(r'## 📦 Module\n\n\*\*(.*?)\*\*', entry_content, re.DOTALL)
    if module_match:
        module_text = module_match.group(1).strip()
        if module_text and module_text != "From Jira Board":
            labels.update([l.strip() for l in module_text.split(',')])
    
    # Extract issues (format: "  - KEY: Summary (Status)")
    issue_pattern = r'  - ([A-Z]+-\d+): (.+?) \(([^)]+)\)'
    issue_matches = re.findall(issue_pattern, entry_content)
    
    for key, summary, status in issue_matches:
        issues.append({
            'key': key,
            'summary': summary.strip(),
            'status': status.strip()
        })
    
    return issues, labels

def remove_month_entries_from_daily_report(filepath, target_month, target_year):
    """Remove all entries for a specific month from the daily report file"""
    if not os.path.exists(filepath):
        return False
    
    entries, _ = parse_daily_report_file(filepath)
    
    # Filter out entries for the target month
    remaining_entries = []
    for entry in entries:
        try:
            entry_date = datetime.strptime(entry['date'], "%B %d, %Y")
            if not (entry_date.month == target_month and entry_date.year == target_year):
                remaining_entries.append(entry)
        except ValueError:
            # Keep entries we can't parse (shouldn't happen, but be safe)
            remaining_entries.append(entry)
    
    # Reconstruct the file with remaining entries
    new_content = ""
    for entry in remaining_entries:
        new_content += f"# {entry['date']} - Daily Progress Report\n"
        new_content += entry['content']
    
    # Write back to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True

def generate_monthly_summary(target_month=None, target_year=None, force=False):
    """Generate a monthly summary from all daily reports and remove those entries"""
    today = datetime.now()
    
    # Use provided month/year or default to current month
    if target_month and target_year:
        month_name = datetime(target_year, target_month, 1).strftime("%B")
        year = target_year
        month_num = target_month
    else:
        month_name = today.strftime("%B")
        year = today.year
        month_num = today.month
    
    # Get the daily report file path (for reading)
    if OBSIDIAN_FOLDER:
        obsidian_dir = os.path.join(OBSIDIAN_VAULT_PATH, OBSIDIAN_FOLDER)
        daily_report_path = os.path.join(obsidian_dir, REPORT_FILENAME)
    else:
        daily_report_path = os.path.join(OBSIDIAN_VAULT_PATH, REPORT_FILENAME)
    
    # Get the monthly reports folder path (for saving summaries)
    monthly_reports_dir = os.path.join(OBSIDIAN_VAULT_PATH, MONTHLY_REPORTS_FOLDER)
    os.makedirs(monthly_reports_dir, exist_ok=True)
    monthly_summary_path = os.path.join(monthly_reports_dir, f"{month_name}_{year}_Monthly_Summary.md")
    
    # Check if summary already exists (unless force is True)
    if os.path.exists(monthly_summary_path) and not force:
        print(f"ℹ️  Monthly summary for {month_name} {year} already exists")
        print("💡 Tip: Use --force or -f to regenerate the summary")
        # Still remove entries if they exist
        removed = remove_month_entries_from_daily_report(daily_report_path, month_num, year)
        if removed:
            print(f"🗑️  Removed {month_name} {year} entries from daily report")
        return monthly_summary_path
    
    if force and os.path.exists(monthly_summary_path):
        print(f"🔄 Force mode: Regenerating monthly summary for {month_name} {year}...")
    
    # Parse all daily entries
    all_entries, _ = parse_daily_report_file(daily_report_path)
    
    # Filter entries for target month
    month_entries = []
    for entry in all_entries:
        try:
            # Parse date like "November 4, 2025"
            entry_date = datetime.strptime(entry['date'], "%B %d, %Y")
            if entry_date.month == month_num and entry_date.year == year:
                month_entries.append(entry)
        except ValueError:
            continue
    
    if not month_entries:
        print(f"⚠️  No daily reports found for {month_name} {year}")
        return None
    
    # Aggregate data
    all_issues = []
    all_labels = set()
    issues_by_date = defaultdict(list)
    issue_keys_seen = set()
    
    for entry in month_entries:
        issues, labels = extract_issues_from_entry(entry['content'])
        all_issues.extend(issues)
        all_labels.update(labels)
        issues_by_date[entry['date']] = issues
        
        # Track unique issue keys
        for issue in issues:
            issue_keys_seen.add(issue['key'])
    
    # Generate summary markdown
    markdown = f"# {month_name} {year} - Monthly Summary\n\n"
    markdown += f"*Generated on {today.strftime('%B %d, %Y')}*\n\n"
    
    # Statistics section
    markdown += "## 📊 Statistics\n\n"
    markdown += f"- **Total Days Worked**: {len(month_entries)}\n"
    markdown += f"- **Total Issues Worked On**: {len(all_issues)}\n"
    markdown += f"- **Unique Issues**: {len(issue_keys_seen)}\n"
    markdown += f"- **Modules/Labels**: {', '.join(sorted(all_labels)) if all_labels else 'None'}\n\n"
    
    # Status breakdown
    status_counter = Counter(issue['status'] for issue in all_issues)
    if status_counter:
        markdown += "### Status Breakdown\n\n"
        for status, count in status_counter.most_common():
            markdown += f"- **{status}**: {count}\n"
        markdown += "\n"
    
    # Daily breakdown
    markdown += "## 📅 Daily Breakdown\n\n"
    for date in sorted(issues_by_date.keys(), key=lambda x: datetime.strptime(x, "%B %d, %Y")):
        issues = issues_by_date[date]
        markdown += f"### {date}\n\n"
        
        # Get labels for this day
        entry = next((e for e in month_entries if e['date'] == date), None)
        if entry:
            _, day_labels = extract_issues_from_entry(entry['content'])
            if day_labels:
                markdown += f"**Modules**: {', '.join(sorted(day_labels))}\n\n"
        
        if issues:
            markdown += "**Issues**:\n"
            for issue in issues:
                markdown += f"- {issue['key']}: {issue['summary']} ({issue['status']})\n"
        else:
            markdown += "*No issues recorded*\n"
        markdown += "\n"
    
    # All unique issues list
    markdown += "## 🎯 All Issues Worked On\n\n"
    unique_issues_dict = {}
    for issue in all_issues:
        key = issue['key']
        if key not in unique_issues_dict:
            unique_issues_dict[key] = issue
    
    for key in sorted(unique_issues_dict.keys()):
        issue = unique_issues_dict[key]
        markdown += f"- **{key}**: {issue['summary']} ({issue['status']})\n"
    
    markdown += "\n---\n\n"
    
    # Save monthly summary to Monthly Reports folder
    with open(monthly_summary_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    # Remove entries for this month from daily report
    removed = remove_month_entries_from_daily_report(daily_report_path, month_num, year)
    if removed:
        print(f"🗑️  Removed {month_name} {year} entries from daily report")
    
    return monthly_summary_path

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
    
    # Check for --monthly flag to manually generate monthly summary
    if "--monthly" in sys.argv or "--summary" in sys.argv:
        force_monthly = force_run  # Use the same force flag for monthly summaries
        if force_monthly:
            print("📊 Generating monthly summary (force mode)...")
        else:
            print("📊 Generating monthly summary...")
        summary_path = generate_monthly_summary(force=force_monthly)
        if summary_path:
            print(f"✅ Monthly summary saved to: {summary_path}")
        exit(0)
    
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
    
    # Auto-generate monthly summary on the last day of the month (works for EVERY month)
    from calendar import monthrange
    last_day = monthrange(today.year, today.month)[1]
    
    if today.day == last_day:
        print(f"\n📊 Last day of {today.strftime('%B')} detected - generating monthly summary...")
        summary_path = generate_monthly_summary()
        if summary_path:
            print(f"✅ Monthly summary saved to: {summary_path}")
    # Also generate for previous month if it's the 1st of the month (backup in case script wasn't run on last day)
    elif today.day == 1:
        print("\n📊 First day of month detected - generating previous month's summary...")
        # Get previous month
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        summary_path = generate_monthly_summary(prev_month, prev_year)
        if summary_path:
            print(f"✅ Monthly summary saved to: {summary_path}")
