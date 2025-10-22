# macOS Setup Guide for edsdk-python

This guide explains how to set up and build edsdk-python on macOS.

## Prerequisites

1. **macOS version**: macOS 13 or later (based on EDSDK v13.19.10 support)
2. **Xcode Command Line Tools**: Required for C++ compilation
   ```bash
   xcode-select --install
   ```
3. **Python**: Version 3.8 or later
4. **EDSDK for macOS**: Downloaded from Canon (EDSDKv131910M or later)

## Step 1: Extract the EDSDK for macOS

You should have received `Macintosh.dmg.zip` from Canon.

### Option A: On macOS (Recommended)

1. Extract the zip file:
   ```bash
   cd EDSDKv131910M/Macintosh
   unzip Macintosh.dmg.zip
   ```

2. Mount the DMG:
   ```bash
   hdiutil attach Macintosh.dmg
   ```

3. The EDSDK will be mounted (typically at `/Volumes/EDSDK`). Navigate to it and you should see:
   - `Header/` folder containing:
     - `EDSDK.h`
     - `EDSDKTypes.h`
     - `EDSDKErrors.h`
   - `Framework/` folder containing:
     - `EDSDK.framework`

### Option B: On Linux/WSL

If you're on Linux/WSL and need to extract the DMG, you can use these tools:

1. Install dmg2img:
   ```bash
   sudo apt-get install dmg2img  # Ubuntu/Debian
   # or
   brew install dmg2img          # if using Homebrew
   ```

2. Convert and extract:
   ```bash
   cd EDSDKv131910M/Macintosh
   unzip Macintosh.dmg.zip
   dmg2img Macintosh.dmg
   mkdir -p extracted
   sudo mount -o loop Macintosh.img extracted/
   ```

## Step 2: Copy EDSDK Files to Dependencies Folder

Create the required directory structure in the project's `dependencies` folder:

```bash
cd /path/to/edsdk-python

# Create directories
mkdir -p dependencies/EDSDK/Header
mkdir -p dependencies/EDSDK_Mac/Framework
```

### From the mounted EDSDK (on macOS):

```bash
# Copy headers (same as Windows)
cp /Volumes/EDSDK/Header/*.h dependencies/EDSDK/Header/

# Copy framework
cp -R /Volumes/EDSDK/Framework/EDSDK.framework dependencies/EDSDK_Mac/Framework/

# Unmount when done
hdiutil detach /Volumes/EDSDK
```

### From extracted location (on Linux):

```bash
# Copy headers
cp extracted/Header/*.h dependencies/EDSDK/Header/

# Copy framework
cp -R extracted/Framework/EDSDK.framework dependencies/EDSDK_Mac/Framework/

# Unmount when done
sudo umount extracted/
```

Your dependencies folder structure should look like this:

```
dependencies/
├── EDSDK/
│   └── Header/
│       ├── EDSDK.h
│       ├── EDSDKErrors.h
│       └── EDSDKTypes.h
└── EDSDK_Mac/
    └── Framework/
        └── EDSDK.framework/
            ├── EDSDK (binary)
            ├── Headers/
            ├── Resources/
            └── Versions/
```

## Step 3: Modify EDSDKTypes.h (Required)

This is the same fix needed for Windows. Open `dependencies/EDSDK/Header/EDSDKTypes.h` and find the `EdsObjectFormat` enum:

```c
typedef enum
{
    Unknown   = 0x00000000,  // <- This line needs to be changed
    Jpeg      = 0x3801,
    CR2       = 0xB103,
    MP4       = 0xB982,
    CR3       = 0xB108,
    HEIF_CODE = 0xB10B,
} EdsObjectFormat;
```

Change `Unknown` to `UNKNOWN` or comment it out:

```c
typedef enum
{
    // Unknown   = 0x00000000,  // Commented out to avoid collision
    UNKNOWN   = 0x00000000,     // Or rename it
    Jpeg      = 0x3801,
    CR2       = 0xB103,
    MP4       = 0xB982,
    CR3       = 0xB108,
    HEIF_CODE = 0xB10B,
} EdsObjectFormat;
```

## Step 4: Build the Library

On macOS, run:

```bash
pip install .
```

Or for development mode:

```bash
pip install -e .
```

## Step 5: Runtime Setup

The EDSDK.framework needs to be accessible at runtime. You have several options:

### Option A: Install Framework System-Wide (Recommended for Development)

```bash
sudo cp -R dependencies/EDSDK_Mac/Framework/EDSDK.framework /Library/Frameworks/
```

### Option B: Use DYLD_FRAMEWORK_PATH (For Testing)

```bash
export DYLD_FRAMEWORK_PATH=/path/to/edsdk-python/dependencies/EDSDK_Mac/Framework:$DYLD_FRAMEWORK_PATH
python your_script.py
```

### Option C: Bundle with Your Application

For distribution, you can bundle the framework with your application using tools like `py2app` or by including it in your application bundle.

## Troubleshooting

### Error: "framework not found EDSDK"

This means the linker cannot find the EDSDK.framework during compilation. Make sure:
1. The framework exists at `dependencies/EDSDK_Mac/Framework/EDSDK.framework`
2. The path in `setup.py` is correct

### Error: "dyld: Library not loaded"

This is a runtime error meaning the framework cannot be found. Use one of the runtime setup options above.

### Error: "Unknown: redefinition"

You forgot to modify `EDSDKTypes.h`. See Step 3.

### Compilation errors with C++ standard

If you get C++11 related errors, make sure you have Xcode Command Line Tools installed:
```bash
xcode-select --install
```

## Differences from Windows

1. **Library format**: macOS uses `.framework` instead of `.dll`/`.lib`
2. **Additional frameworks**: macOS requires linking to `CoreFoundation` and `IOKit` frameworks
3. **Compiler flags**: Uses GCC/Clang flags instead of MSVC flags
4. **No pywin32 dependency**: The Windows-specific `pywin32` package is not needed on macOS

## Testing

After installation, test the library:

```python
import edsdk

# Initialize the SDK
edsdk.EdsInitializeSDK()

# Get camera list
camera_list = edsdk.EdsGetCameraList()
count = edsdk.EdsGetChildCount(camera_list)
print(f"Found {count} camera(s)")

# Clean up
edsdk.EdsTerminateSDK()
```

## Additional Resources

- [EDSDK API Documentation](EDSDKv131910M/Document/EDSDK_API_EN.pdf)
- [Canon Developer Community](https://developercommunity.usa.canon.com)
- [Original Repository](https://github.com/jiloc/edsdk-python)
