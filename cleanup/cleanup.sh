#!/bin/bash

echo "🚀 Mobile Development Cleanup Script"
echo "This will clear Xcode & Android caches to free up disk space."
echo "-------------------------------------------------------------"

# Show initial disk usage
echo "📊 Disk space before cleanup:"
df -h /

echo "-------------------------------------------------------------"

read -p "Do you want to clear Xcode DerivedData? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/Library/Developer/Xcode/DerivedData/*
    echo "✅ Cleared Xcode DerivedData"
fi

read -p "Do you want to clear iOS Simulator data? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/Library/Developer/CoreSimulator/*
    echo "✅ Cleared iOS Simulator data"
fi

read -p "Do you want to clear Xcode Archives? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/Library/Developer/Xcode/Archives/*
    echo "✅ Cleared Xcode Archives"
fi

read -p "Do you want to clear Xcode DeviceSupport files? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/Library/Developer/Xcode/iOS\ DeviceSupport/*
    echo "✅ Cleared Device Support files"
fi

read -p "Do you want to clear Gradle caches? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/.gradle/caches/
    echo "✅ Cleared Gradle caches"
fi

read -p "Do you want to clear Android build-cache? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/.android/build-cache/
    echo "✅ Cleared Android build-cache"
fi

read -p "Do you want to clear Android Emulator AVDs? (y/n): " confirm
if [[ $confirm == [yY] ]]; then
    rm -rf ~/.android/avd/*
    echo "✅ Cleared Android Emulator data"
fi

echo "-------------------------------------------------------------"
# Show final disk usage
echo "📊 Disk space after cleanup:"
df -h /

echo "🎉 Cleanup complete!"
