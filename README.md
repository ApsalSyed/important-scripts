Perfect 👍 Let’s create a **README.md** that explains what the script does, how to install, and how to use it.
You can keep this alongside your `cleanup.sh` so others on your team (or future you) know exactly what it does.

---

# 📦 Mobile Development Cleanup Script

This repository contains a **shell script** (`cleanup.sh`) to free up disk space by clearing caches and build artifacts created by **Xcode** (iOS) and **Android Studio / Gradle** during mobile app development.

Over time, these caches can consume **tens of gigabytes** of space. This script makes it easy to clear them with confirmation prompts.

---

## ✨ Features

- Clear **Xcode caches**:

  - DerivedData
  - iOS Simulator data
  - Archives
  - Device Support files
  - Crash logs & module cache (optional)

- Clear **Android caches**:

  - Gradle cache
  - Android build-cache
  - Emulator AVDs & system images
  - Android Studio logs (optional)

- Shows **disk usage before & after cleanup**

- Interactive mode (asks before deleting each category)

- Optional **extended cleanup** (system logs, user caches, etc.)

---

## 📂 File Structure

```
.
├── cleanup.sh   # The cleanup script
└── README.md    # Documentation
```

---

## ⚙️ Setup

1. Clone or copy this repository.
2. Make the script executable:

   ```bash
   chmod +x cleanup.sh
   ```

---

## 🚀 Usage

Run the script from terminal:

```bash
./cleanup.sh
```

- The script will show **disk space before cleanup**.
- For each type of cache, it will ask:

  ```
  Do you want to clear Xcode DerivedData? (y/n):
  ```

- Type `y` to confirm, or `n` to skip.
- At the end, you’ll see **disk space after cleanup**.

---

## 🛠️ Optional Extended Cleanup

If you want to also clear:

- macOS user caches (`~/Library/Caches`)
- Temporary system files (`/private/var/folders/`)
- Trash (`~/.Trash`)

👉 You can add these to the script under an **extended mode**.
_(By default, they’re not included to keep things safe.)_

---

## ⚠️ Notes

- These commands **permanently delete files**.
- The **first build** after cleanup will take longer because caches are rebuilt.
- Run this occasionally (e.g., once a month) to keep disk usage under control.

---

## 🧑‍💻 Example

```bash
$ ./cleanup.sh

🚀 Mobile Development Cleanup Script
📊 Disk space before cleanup:
Filesystem   Size  Used  Avail Capacity iused      ifree %iused  Mounted on
/dev/disk1s5 466G  350G   95G    79% 1234567  987654321    2%   /

Do you want to clear Xcode DerivedData? (y/n): y
✅ Cleared Xcode DerivedData
...
📊 Disk space after cleanup:
Filesystem   Size  Used  Avail Capacity iused      ifree %iused  Mounted on
/dev/disk1s5 466G  320G  125G    72% 1234560  987654328    2%   /

🎉 Cleanup complete!
```

---

## 🔮 Future Improvements

- Add **non-interactive mode** (`./cleanup.sh --all`) to clear everything automatically.
- Add **basic vs extended** cleanup modes.
- Add **logs of deleted sizes** per category.

---
