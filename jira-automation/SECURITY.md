# Security Guide - Jira Automation

## 🔐 Credentials are Now Secured!

Your API token and credentials are now stored safely using environment variables.

## ✅ What Was Done

### 1. Created `.env` file
- Contains your Jira credentials
- File permissions set to `600` (only you can read/write)
- Added to `.gitignore` to prevent accidental commits

### 2. Updated `fetch_jira_tasks.py`
- Reads credentials from environment variables
- Falls back to defaults if not set
- Shows helpful error if API token is missing

### 3. Updated run scripts
- Automatically load `.env` before running
- No manual steps needed

### 4. Created `.gitignore`
- Prevents sensitive files from being committed to git
- Includes `.env`, logs, and other sensitive files

## 📁 File Structure

```
jira-automation/
├── .env              # ← Your credentials (secure, not in git)
├── .gitignore        # ← Prevents .env from being committed
├── fetch_jira_tasks.py
└── ... other files
```

## 🔒 Security Features

| Feature | Status | Description |
|---------|--------|-------------|
| **.env file** | ✅ | Credentials in separate file |
| **File permissions** | ✅ | Only you can read (chmod 600) |
| **.gitignore** | ✅ | Won't be committed to git |
| **Environment variables** | ✅ | Loaded at runtime |
| **Error handling** | ✅ | Alerts if token missing |

## 🚨 Important Security Tips

### 1. Never commit `.env` to git
```bash
# Always check before committing
git status

# If .env appears, it's a problem!
# It should be in .gitignore
```

### 2. Regenerate token if exposed
If you accidentally commit your token:
1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Revoke the old token
3. Create a new token
4. Update `.env` file

### 3. File permissions are correct
```bash
# .env should show: -rw------- (600)
ls -la .env

# If not, fix it:
chmod 600 .env
```

### 4. Backup your `.env` securely
- Don't email it
- Don't store it in cloud storage unencrypted
- Use a password manager or encrypted backup

## 📝 Manual Setup (if needed)

If you need to recreate the `.env` file:

```bash
cd /Users/mohammedsayeethapsals/workspace/Swivl/jira-automation

cat > .env << 'EOF'
export JIRA_EMAIL="your-email@domain.com"
export JIRA_API_TOKEN="your-token-here"
export JIRA_DOMAIN="your-domain.atlassian.net"
EOF

chmod 600 .env
```

## 🔄 How It Works

1. **Run scripts automatically load `.env`**
   ```bash
   ./run:daily-report  # Loads .env, then runs script
   ```

2. **Script reads environment variables**
   ```python
   EMAIL = os.getenv("JIRA_EMAIL")
   API_TOKEN = os.getenv("JIRA_API_TOKEN")
   DOMAIN = os.getenv("JIRA_DOMAIN")
   ```

3. **Launchd automation also works**
   - Environment variables are loaded by the run scripts
   - Automation runs at 7 PM as usual

## ✅ Verification

Test that security is working:

```bash
# This should work (loads .env)
./run:daily-report

# This should fail with error (no .env loaded)
python3 fetch_jira_tasks.py
```

## 🎯 Best Practices

1. ✅ Keep `.env` file permissions at `600`
2. ✅ Never share `.env` file
3. ✅ Don't commit `.env` to git
4. ✅ Rotate API tokens periodically
5. ✅ Use different tokens for different environments

## 🆘 Troubleshooting

### Error: "JIRA_API_TOKEN environment variable not set!"

**Solution:**
```bash
# Load environment variables
source .env

# Or use the run scripts (they do this automatically)
./run:daily-report
```

### `.env` file is missing

Recreate it using the manual setup steps above.

### Token expired or invalid

1. Generate new token at [Atlassian](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Update `.env` file with new token
3. Test: `./run:daily-report`

---

**Your credentials are now secure! 🔐**

