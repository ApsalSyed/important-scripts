# Important Scripts

A collection of useful scripts for mobile development workflow optimization.

## Mobile Development Cleanup Script

### Overview

The `cleanup.sh` script is a comprehensive tool designed to free up disk space by clearing various caches and temporary files generated during mobile development with Xcode and Android Studio.

### Features

- **Xcode Cleanup**: Removes DerivedData, Simulator data, Archives, and DeviceSupport files
- **Android Cleanup**: Clears Gradle caches, build-cache, and Emulator AVDs
- **Interactive**: Prompts for confirmation before each cleanup operation
- **Disk Usage Monitoring**: Shows before and after disk space usage

### Usage

1. Make the script executable:

   ```bash
   chmod +x cleanup.sh
   ```

2. Run the script:

   ```bash
   ./cleanup.sh
   ```

3. Follow the interactive prompts to select which caches to clear:
   - Xcode DerivedData
   - iOS Simulator data
   - Xcode Archives
   - Xcode DeviceSupport files
   - Gradle caches
   - Android build-cache
   - Android Emulator AVDs

### What Gets Cleaned

#### Xcode Related

- `~/Library/Developer/Xcode/DerivedData/*` - Build artifacts and intermediate files
- `~/Library/Developer/CoreSimulator/*` - iOS Simulator data and apps
- `~/Library/Developer/Xcode/Archives/*` - App archives for distribution
- `~/Library/Developer/Xcode/iOS DeviceSupport/*` - Device support files

#### Android Related

- `~/.gradle/caches/` - Gradle build cache
- `~/.android/build-cache/` - Android build cache
- `~/.android/avd/*` - Android Virtual Device data

### Safety

- The script prompts for confirmation before each cleanup operation
- Only removes cache and temporary files, not source code
- Shows disk usage before and after cleanup

### Requirements

- macOS (for Xcode cleanup features)
- Bash shell
- Appropriate permissions to access the directories

### Tips

- Run this script periodically to maintain optimal disk space
- Consider running before large builds to ensure clean state
- Backup important data before running if you have custom configurations

---

## Contributing

Feel free to add more scripts to this collection for common development tasks.

## License

This project is open source and available under the MIT License.
