````markdown
# 🚀 Git Helper Scripts

This repository provides two shell scripts to make Git setup and usage easier.  
Perfect for **beginners setting up Git for the first time** and for **developers who want handy Git shortcuts**.

---

## 🔧 1. One-Time Git Setup (`git-setup.sh`)

A script to quickly configure Git on a fresh machine. Run it once and you’re good to go.

### ✨ Features

- Configure Git username & email
- Set default branch to `main`
- Enable colorized output
- Safe defaults for push/pull behavior
- Useful Git aliases: `st`, `co`, `br`, `cm`, `lg`
- Create a global `.gitignore`
- Generate an SSH key if missing and display the public key

### ▶️ Usage

```sh
chmod +x git-setup.sh
./git-setup.sh
```
````

---

## 🛠️ 2. Git Helper Script (`git-helper.sh`)

An interactive menu for ongoing Git tasks. Use it anytime you need quick Git actions.

### ✨ Features

- Set Git username & email
- Add Git aliases
- Create global `.gitignore`
- Generate SSH key (if not exists)
- Show current Git config
- Cleanup merged branches

### ▶️ Usage

```sh
chmod +x git-helper.sh
./git-helper.sh
```

---

## 🖼️ Demo (Preview)

When you run `./git-helper.sh`, you’ll see a menu like this:

```
========================
     Git Helper Menu
========================
1. Set Git username & email
2. Add Git aliases
3. Create global .gitignore
4. Generate SSH key
5. Show current Git config
6. Cleanup merged branches
0. Exit
========================
Choose an option:
```

---

## 📂 Files

- `git-setup.sh` → One-time Git setup script (run once on a new machine)
- `git-helper.sh` → Interactive Git helper menu (use anytime)

---

## 💡 Notes

- Works on **macOS** and **Linux**.
- Windows users can run via **Git Bash** or **WSL**.
- Scripts are **idempotent**: safe to run multiple times.
- You can extend the scripts with your own aliases or tasks.

```
---
```
