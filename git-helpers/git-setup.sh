#!/bin/bash
# =========================================
# Git One-Time Setup Script
# =========================================

echo "🔧 Starting Git Setup..."

# 1. Ask for user details
read -p "👤 Enter your Git username: " git_username
read -p "📧 Enter your Git email: " git_email

git config --global user.name "$git_username"
git config --global user.email "$git_email"

# 2. Basic settings
git config --global init.defaultBranch main
git config --global color.ui auto
git config --global pull.rebase false
git config --global push.default current
git config --global help.autocorrect 1

echo "✅ Basic Git config applied!"

# 3. Aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm "commit -m"
git config --global alias.lg "log --oneline --graph --decorate --all"

echo "✅ Git aliases added!"

# 4. Global ignore file
IGNORE_FILE=~/.gitignore_global

if [ ! -f "$IGNORE_FILE" ]; then
  cat <<EOL > $IGNORE_FILE
# Global gitignore
.DS_Store
node_modules
*.log
.env
dist
build
EOL
  git config --global core.excludesfile $IGNORE_FILE
  echo "✅ Global gitignore created at $IGNORE_FILE"
else
  echo "ℹ️ Global gitignore already exists"
fi

# 5. SSH key setup
if [ ! -f ~/.ssh/id_rsa.pub ]; then
  echo "🔑 No SSH key found, generating one..."
  ssh-keygen -t rsa -b 4096 -C "$git_email" -f ~/.ssh/id_rsa -N ""
  echo "✅ SSH key generated!"
else
  echo "ℹ️ SSH key already exists"
fi

echo "📋 Your SSH public key is:"
cat ~/.ssh/id_rsa.pub

echo "🚀 Git setup complete!"
