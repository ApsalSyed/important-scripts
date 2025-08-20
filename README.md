# ��️Development Scripts

A collection of useful shell scripts for mobile development and Git workflow automation. This repository contains two main script collections designed to streamline your development process.

## 📁 Repository Structure

```
scripts/
├── cleanup/           # Mobile development cleanup utilities
│   ├── cleanup.sh     # Xcode & Android cache cleanup script
│   └── README.md      # Detailed cleanup documentation
└── git-helpers/       # Git workflow automation tools
    ├── git-setup.sh   # One-time Git configuration script
    ├── git-helper.sh  # Interactive Git helper menu
    └── README.md      # Git helpers documentation
```

## 🧹 Cleanup Scripts

### Mobile Development Cleanup (`cleanup/`)

Free up disk space by clearing caches and build artifacts from mobile development tools.

**Features:**

- 🤖 **Xcode cleanup**: DerivedData, Simulator data, Archives, Device Support
- 🤖 **Android cleanup**: Gradle cache, build-cache, Emulator AVDs
- 📊 **Disk usage tracking**: Shows before/after space savings
- ⚡ **Interactive mode**: Confirms each cleanup step

**Quick Start:**

```bash
cd cleanup/
chmod +x cleanup.sh
./cleanup.sh
```

**Perfect for:** iOS/Android developers who want to reclaim gigabytes of disk space from development caches.

---

## Git Helper Scripts

### Git Workflow Automation (`git-helpers/`)

Streamline your Git setup and daily workflow with interactive tools.

**Two Scripts:**

1. **`git-setup.sh`** - One-time Git configuration

   - Configure username & email
   - Set up useful aliases (`st`, `co`, `br`, `cm`, `lg`)
   - Create global `.gitignore`
   - Generate SSH key

2. **`git-helper.sh`** - Interactive Git helper menu
   - Ongoing Git tasks and configuration
   - Branch cleanup
   - SSH key management
   - Config inspection

**Quick Start:**

```bash
cd git-helpers/
chmod +x git-setup.sh git-helper.sh

# First-time setup
./git-setup.sh

# Daily use
./git-helper.sh
```

**Perfect for:** Developers setting up Git for the first time or wanting convenient Git shortcuts.

---

## 🚀 Getting Started

### Prerequisites

- macOS or Linux (scripts are bash-based)
- Git (for git-helpers)
- Xcode/Android Studio (for cleanup scripts)

### Installation

1. Clone this repository
2. Navigate to the script folder you want to use
3. Make scripts executable: `chmod +x *.sh`
4. Run the scripts as needed

### Usage Examples

**Clean up development caches:**

```bash
cd scripts/cleanup
./cleanup.sh
# Follow the interactive prompts
```

**Set up Git for the first time:**

```bash
cd scripts/git-helpers
./git-setup.sh
# Enter your username and email when prompted
```

**Use Git helper menu:**

```bash
cd scripts/git-helpers
./git-helper.sh
# Choose from the interactive menu
```

---

## Use Cases

### For Mobile Developers

- **Weekly cleanup**: Run `cleanup.sh` to free up 10-50GB of cache space
- **Before releases**: Clear all caches for clean builds
- **Disk emergencies**: Quick space recovery when storage is low

### For Git Users

- **New machine setup**: Use `git-setup.sh` to configure Git from scratch
- **Daily workflow**: Use `git-helper.sh` for common Git tasks
- **Team onboarding**: Share these scripts with new developers

---

## ⚠️ Important Notes

### Cleanup Scripts

- **Permanent deletion**: Files removed cannot be recovered
- **First build slowdown**: Caches will be rebuilt after cleanup
- **Safe by default**: Interactive prompts prevent accidental deletions

### Git Scripts

- **Idempotent**: Safe to run multiple times
- **Global configuration**: Changes affect all Git repositories
- **SSH keys**: Generated keys should be added to your Git hosting service

---

## 🔮 Future Enhancements

### Planned Features

- **Non-interactive mode** for cleanup scripts
- **Configuration files** for custom cleanup paths
- **Cross-platform support** for Windows
- **Integration scripts** combining cleanup + Git helpers
- **Logging and analytics** for cleanup effectiveness

### Contributing

Feel free to extend these scripts with:

- Additional cleanup targets
- New Git aliases and shortcuts
- Platform-specific optimizations
- Integration with other development tools

---

## 📚 Documentation

Each script folder contains detailed documentation:

- [`cleanup/README.md`](cleanup/README.md) - Complete cleanup guide
- [`git-helpers/README.md`](git-helpers/README.md) - Git workflow documentation

---

## 🤝 Support

These scripts are designed to be self-contained and well-documented. If you encounter issues:

1. Check the individual README files for detailed instructions
2. Ensure scripts have execute permissions (`chmod +x *.sh`)
3. Verify you're running on a supported platform (macOS/Linux)

---

**Happy coding! 🎉**

```

This comprehensive README provides:

1. **Overview** of the entire repository structure
2. **Clear categorization** of the two script collections
3. **Quick start guides** for each script type
4. **Use cases** and target audiences
5. **Important warnings** about permanent deletions and global configurations
6. **Future roadmap** for potential enhancements
7. **Cross-references** to the detailed documentation in each folder

The README is structured to be helpful for both new users discovering the repository and existing users looking for quick reference information.
```
