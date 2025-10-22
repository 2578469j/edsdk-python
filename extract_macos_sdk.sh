#!/bin/bash

# Script to extract macOS EDSDK and set up dependencies
# Usage: ./extract_macos_sdk.sh

set -e

echo "=== EDSDK macOS Extraction Script ==="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Warning: This script is designed for macOS."
    echo "For Linux/WSL, please follow the manual extraction steps in MACOS_SETUP.md"
    echo ""
fi

# Check for DMG file
DMG_ZIP="EDSDKv131910M/Macintosh/Macintosh.dmg.zip"
if [ ! -f "$DMG_ZIP" ]; then
    echo "Error: Could not find $DMG_ZIP"
    echo "Please ensure you have downloaded the EDSDK from Canon and placed it in EDSDKv131910M/Macintosh/"
    exit 1
fi

echo "Found $DMG_ZIP"
echo ""

# Extract the zip if DMG doesn't exist
if [ ! -f "EDSDKv131910M/Macintosh/Macintosh.dmg" ]; then
    echo "Extracting DMG from zip..."
    cd EDSDKv131910M/Macintosh
    unzip -o Macintosh.dmg.zip
    cd ../..
    echo "Extraction complete."
    echo ""
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS-specific extraction
    echo "Mounting DMG..."
    DMG_MOUNT=$(hdiutil attach EDSDKv131910M/Macintosh/Macintosh.dmg | grep Volumes | awk '{print $3}')

    if [ -z "$DMG_MOUNT" ]; then
        echo "Error: Failed to mount DMG"
        exit 1
    fi

    echo "DMG mounted at: $DMG_MOUNT"
    echo ""

    # Create directories
    echo "Creating dependencies directories..."
    mkdir -p dependencies/EDSDK/Header
    mkdir -p dependencies/EDSDK_Mac/Framework
    echo ""

    # Copy headers
    echo "Copying header files..."
    cp "$DMG_MOUNT/Header/"*.h dependencies/EDSDK/Header/
    echo "Headers copied: $(ls dependencies/EDSDK/Header/)"
    echo ""

    # Copy framework
    echo "Copying EDSDK.framework..."
    cp -R "$DMG_MOUNT/Framework/EDSDK.framework" dependencies/EDSDK_Mac/Framework/
    echo "Framework copied."
    echo ""

    # Unmount
    echo "Unmounting DMG..."
    hdiutil detach "$DMG_MOUNT"
    echo ""

    echo "=== Extraction Complete ==="
    echo ""
    echo "Next steps:"
    echo "1. Modify dependencies/EDSDK/Header/EDSDKTypes.h (change 'Unknown' to 'UNKNOWN')"
    echo "2. Run: pip install ."
    echo "3. (Optional) Install framework system-wide: sudo cp -R dependencies/EDSDK_Mac/Framework/EDSDK.framework /Library/Frameworks/"
    echo ""
    echo "See MACOS_SETUP.md for detailed instructions."

else
    echo "For Linux/WSL extraction, please follow these steps manually:"
    echo ""
    echo "1. Install dmg2img: sudo apt-get install dmg2img"
    echo "2. Extract DMG:"
    echo "   cd EDSDKv131910M/Macintosh"
    echo "   bunzip2 -k Macintosh.dmg"
    echo "   dmg2img Macintosh.dmg.out"
    echo "   mkdir -p extracted"
    echo "   sudo mount -o loop Macintosh.img extracted/"
    echo ""
    echo "3. Copy files:"
    echo "   mkdir -p ../../dependencies/EDSDK/Header"
    echo "   mkdir -p ../../dependencies/EDSDK_Mac/Framework"
    echo "   cp extracted/Header/*.h ../../dependencies/EDSDK/Header/"
    echo "   cp -R extracted/Framework/EDSDK.framework ../../dependencies/EDSDK_Mac/Framework/"
    echo ""
    echo "4. Unmount: sudo umount extracted/"
    echo ""
    echo "See MACOS_SETUP.md for complete instructions."
fi
