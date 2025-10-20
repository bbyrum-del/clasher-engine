# Quick Start Guide

Get Clasher Engine running on your Android device in 5 minutes!

## Prerequisites

- Android device running Android 7.0 (API 24) or higher
- USB cable (for installation) or ability to download APK
- Clash Royale installed on your device

## Installation

### Method 1: Build from Source (Recommended)

1. **Install Android Studio**
   - Download from [developer.android.com](https://developer.android.com/studio)
   - Install and run initial setup

2. **Clone the Repository**
   ```bash
   git clone https://github.com/bbyrum-del/clasher-engine.git
   cd clasher-engine
   ```

3. **Open in Android Studio**
   - File → Open → Select the `clasher-engine` folder
   - Wait for Gradle sync to complete

4. **Connect Your Device**
   - Enable USB Debugging on your Android device:
     - Settings → About Phone → Tap "Build Number" 7 times
     - Settings → Developer Options → Enable "USB Debugging"
   - Connect via USB and authorize the computer

5. **Build and Install**
   - Click the green "Run" button in Android Studio
   - OR from command line: `./gradlew installDebug`

### Method 2: Install APK (If Available)

1. Download the APK file
2. Enable "Install from Unknown Sources" in Android Settings
3. Open the APK file on your device
4. Follow installation prompts

## First-Time Setup

### Step 1: Grant Overlay Permission

When you first open the app:

1. Tap "Grant Permission" when prompted for overlay permission
2. You'll be taken to Android Settings
3. Find "Clasher Engine" in the list
4. Toggle "Allow display over other apps" to ON
5. Press Back to return to the app

### Step 2: Grant Usage Stats Permission

1. Tap "Grant Permission" when prompted for usage stats
2. You'll be taken to "Usage access" settings
3. Find "Clasher Engine" in the list
4. Toggle the switch to ON
5. Confirm the warning dialog
6. Press Back to return to the app

### Step 3: Start the Service

1. Once both permissions are granted, tap "Start Overlay Service"
2. You should see a notification: "Clasher Engine is monitoring for Clash Royale"
3. The button will change to "Stop Overlay Service"

## Using the Overlay

### Activate the Overlay

1. With the service running, press Home or switch apps
2. Open Clash Royale
3. Within 1-2 seconds, the overlay will appear at the top center of your screen
4. The overlay shows: "Clasher Engine - Clash Royale Detected!"

### Deactivate the Overlay

The overlay automatically disappears when you:
- Close Clash Royale
- Switch to another app
- Return to the home screen

### Stop the Service

1. Open Clasher Engine app
2. Tap "Stop Overlay Service"
3. The monitoring will stop and the overlay will no longer appear

## Troubleshooting

### Overlay Not Appearing

**Problem:** Overlay doesn't show when Clash Royale is open

**Solutions:**
1. Check that both permissions are granted:
   - Settings → Apps → Clasher Engine → Permissions
   - Ensure "Display over other apps" is allowed
   - Settings → Apps → Special access → Usage access
   - Ensure Clasher Engine is enabled

2. Verify the service is running:
   - Open Clasher Engine app
   - Check that button says "Stop Overlay Service"
   - Look for notification in notification shade

3. Try restarting the service:
   - Tap "Stop Overlay Service"
   - Tap "Start Overlay Service"
   - Try opening Clash Royale again

### Service Stops Unexpectedly

**Problem:** Service notification disappears

**Solutions:**
1. Disable battery optimization:
   - Settings → Apps → Clasher Engine → Battery
   - Select "Unrestricted" or "Don't optimize"

2. Check that Android isn't killing the service:
   - Some manufacturers (Xiaomi, Huawei, Samsung) aggressively kill background services
   - Look for battery/power management settings for your device
   - Add Clasher Engine to the "protected apps" list

### App Won't Install

**Problem:** Installation fails or app won't open

**Solutions:**
1. Check Android version:
   - Settings → About Phone
   - Ensure Android version is 7.0 or higher

2. Clear previous installation:
   - Settings → Apps → Clasher Engine → Uninstall
   - Reinstall the app

3. Check storage space:
   - Ensure you have at least 50MB free

### Permissions Keep Getting Revoked

**Problem:** Need to grant permissions repeatedly

**Solutions:**
1. Some Android versions automatically revoke permissions for unused apps
   - Settings → Apps → Clasher Engine → Permissions
   - Look for option to "Allow all the time" or "Don't ask again"

2. Update to latest Android version if possible

## Usage Tips

### Battery Life
- Stop the service when not actively playing Clash Royale
- The 1-second polling does use battery, though minimally
- Consider using battery saver mode when not gaming

### Notifications
- Don't dismiss the service notification - it keeps the service alive
- You can minimize it by swiping it away partially on Android 8+

### Multi-User Devices
- Each user profile needs to install and configure separately
- Permissions are per-user, not device-wide

### Customization
- The overlay is currently display-only
- See DEVELOPMENT.md for how to customize appearance
- See README.md for changing overlay position

## Next Steps

### Explore Documentation
- **README.md** - Full feature list and customization
- **DEVELOPMENT.md** - Technical details for developers
- **ARCHITECTURE.md** - System design and diagrams
- **SECURITY.md** - Privacy and security information

### Customize Your Experience
- Edit overlay position in `OverlayService.java`
- Change colors in `res/values/colors.xml`
- Modify text in `res/values/strings.xml`
- Adjust layout in `res/layout/overlay_layout.xml`

### Report Issues
- Create a GitHub issue with:
  - Your Android version
  - Device model
  - Steps to reproduce the problem
  - Screenshots if applicable

## Frequently Asked Questions

### Q: Is this safe to use?
**A:** Yes, the app is open source, uses no network access, and stores no data. It only displays an overlay when Clash Royale is open.

### Q: Will I get banned from Clash Royale?
**A:** The app only displays information and doesn't modify the game. However, check Supercell's Terms of Service. Use at your own discretion.

### Q: Why does it need so many permissions?
**A:** Only two special permissions are needed:
- Overlay permission: To display on top of Clash Royale
- Usage stats: To detect when Clash Royale is running
Both are required for the core functionality.

### Q: Can I run this on iOS?
**A:** No, this is Android-only. iOS doesn't allow overlay apps due to system restrictions.

### Q: Does it work on emulators?
**A:** Yes, it works on Android emulators (Android Studio, BlueStacks, etc.) as long as you can install both this app and Clash Royale.

### Q: How much battery does it use?
**A:** Minimal - approximately 2-3% per hour when actively monitoring. The service only polls every second and doesn't perform heavy operations.

### Q: Can I move the overlay?
**A:** Currently no, but you can modify the code to change its position. See DEVELOPMENT.md for instructions.

### Q: Does it collect my data?
**A:** No, the app has no internet permission and cannot transmit data. All processing is local to your device.

## Getting Help

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check README.md and DEVELOPMENT.md
- **Source Code:** Review the code for how it works

## Success!

You should now have Clasher Engine running with an overlay appearing when Clash Royale is active. Enjoy using the app!

---

**Need more help?** Check the full documentation or create a GitHub issue.
