#!/bin/bash
# =========================================
# Git Helper Script (Menu-based)
# =========================================

while true; do
  clear
  echo "========================"
  echo "     Git Helper Menu    "
  echo "========================"
  echo "1. Set Git username & email"
  echo "2. Add Git aliases"
  echo "3. Create global .gitignore"
  echo "4. Generate SSH key"
  echo "5. Show current Git config"
  echo "6. Cleanup merged branches"
  echo "0. Exit"
  echo "========================"
  read -p "Choose an option: " choice

  case $choice in
    1)
      read -p "👤 Enter Git username: " git_username
      read -p "📧 Enter Git email: " git_email
      git config --global user.name "$git_username"
      git config --global user.email "$git_email"
      echo "✅ Git username and email set!"
      read -p "Press Enter to continue..."
      ;;
    2)
      git config --global alias.st status
      git config --global alias.co checkout
      git config --global alias.br branch
      git config --global alias.cm "commit -m"
      git config --global alias.lg "log --oneline --graph --decorate --all"
      echo "✅ Git aliases added!"
      read -p "Press Enter to continue..."
      ;;
    3)
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
      read -p "Press Enter to continue..."
      ;;
    4)
      if [ ! -f ~/.ssh/id_rsa.pub ]; then
        read -p "📧 Enter email for SSH key: " ssh_email
        ssh-keygen -t rsa -b 4096 -C "$ssh_email" -f ~/.ssh/id_rsa -N ""
        echo "✅ SSH key generated!"
      else
        echo "ℹ️ SSH key already exists"
      fi
      echo "📋 Your SSH public key is:"
      cat ~/.ssh/id_rsa.pub
      read -p "Press Enter to continue..."
      ;;
    5)
      echo "📌 Current Git Config:"
      git config --list
      read -p "Press Enter to continue..."
      ;;
    6)
      echo "🧹 Cleaning up merged branches..."
      git branch --merged | egrep -v "(^\*|main|master|develop)" | xargs -r git branch -d
      echo "✅ Merged branches cleaned!"
      read -p "Press Enter to continue..."
      ;;
    0)
      echo "👋 Exiting Git Helper. Bye!"
      exit 0
      ;;
    *)
      echo "❌ Invalid choice, try again!"
      read -p "Press Enter to continue..."
      ;;
  esac
done
