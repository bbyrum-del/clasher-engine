# Development Guide

## Project Overview

Clasher Engine is an Android application that provides a mobile overlay system that activates when Clash Royale is running. This guide covers the technical implementation details.

## Core Components

### 1. MainActivity.java

The main activity serves as the app's entry point and handles:

- **Permission Management**: 
  - Requests SYSTEM_ALERT_WINDOW permission for overlay display
  - Requests PACKAGE_USAGE_STATS permission for app detection
  - Uses Settings intents to direct users to system permission screens

- **Service Control**:
  - Starts/stops the OverlayService
  - Manages service lifecycle based on user interaction
  - Updates UI to reflect service state

**Key Methods:**
- `checkPermissions()`: Validates all required permissions
- `requestOverlayPermission()`: Launches system overlay permission screen
- `requestUsageStatsPermission()`: Launches usage access settings
- `startOverlayService()`: Initiates the monitoring service
- `stopOverlayService()`: Terminates the service

### 2. OverlayService.java

A foreground service that continuously monitors running applications and manages overlay display.

**Functionality:**
- Runs as a foreground service with persistent notification
- Polls UsageStatsManager every second to detect foreground app
- Shows/hides overlay based on Clash Royale detection
- Manages WindowManager for overlay display

**Key Constants:**
- `CLASH_ROYALE_PACKAGE`: "com.supercell.clashroyale" - package to detect
- `CHECK_INTERVAL`: 1000ms - frequency of app checking
- `CHANNEL_ID`: Notification channel identifier

**Key Methods:**
- `startMonitoring()`: Initiates periodic foreground app checking
- `getForegroundApp()`: Uses UsageStatsManager to detect current app
- `showOverlay()`: Creates and displays the overlay view
- `hideOverlay()`: Removes the overlay view

### 3. Layouts

**activity_main.xml:**
- Simple LinearLayout with vertical orientation
- Status TextView showing service state
- Toggle button to start/stop service
- Information text about permissions

**overlay_layout.xml:**
- Compact LinearLayout (200dp width)
- Semi-transparent background (#CC000000)
- App title and detection message
- Positioned at top-center of screen

## Android API Usage

### UsageStatsManager

Used to detect which app is currently in the foreground:

```java
UsageStatsManager usageStatsManager = 
    (UsageStatsManager) getSystemService(Context.USAGE_STATS_SERVICE);
    
List<UsageStats> stats = usageStatsManager.queryUsageStats(
    UsageStatsManager.INTERVAL_DAILY,
    currentTime - 2000,
    currentTime
);
```

**Why it's needed:** Android doesn't provide a direct API to get the foreground app. UsageStatsManager is the recommended approach for API 21+.

### WindowManager

Manages the overlay view display:

```java
WindowManager.LayoutParams params = new WindowManager.LayoutParams(
    WindowManager.LayoutParams.WRAP_CONTENT,
    WindowManager.LayoutParams.WRAP_CONTENT,
    WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, // API 26+
    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
    PixelFormat.TRANSLUCENT
);
```

**Flag details:**
- `TYPE_APPLICATION_OVERLAY`: Required for API 26+, overlays all apps
- `FLAG_NOT_FOCUSABLE`: Allows touch events to pass through to underlying app

### Foreground Service

Required for persistent background monitoring:

```java
startForeground(NOTIFICATION_ID, createNotification());
```

**Android 14+ requirements:**
- Must declare `foregroundServiceType` in manifest
- Must provide ongoing notification
- Special use type requires explanation in manifest

## Permissions Explained

### SYSTEM_ALERT_WINDOW
- Allows app to draw over other applications
- User must explicitly grant via system settings
- Checked using `Settings.canDrawOverlays()`

### PACKAGE_USAGE_STATS
- Special permission requiring system settings access
- Needed to query which apps are running
- Checked using `AppOpsManager.checkOpNoThrow()`

### FOREGROUND_SERVICE
- Normal permission (automatically granted)
- Required for all foreground services

### FOREGROUND_SERVICE_SPECIAL_USE
- Required for Android 14+ (API 34)
- Must be declared with explanation in manifest

## Build System

### Gradle Configuration

**Project-level (build.gradle):**
- Android Gradle Plugin 8.1.0
- Uses Google's Maven repository
- Configured for Kotlin DSL compatibility

**App-level (app/build.gradle):**
- compileSdk: 34 (Android 14)
- minSdk: 24 (Android 7.0)
- targetSdk: 34
- Dependencies: AndroidX AppCompat, Material Design

### ProGuard
Currently disabled (`minifyEnabled false`) for easier debugging. 
For production releases, enable and add rules to preserve:
- Service classes
- UsageStatsManager reflection
- Any AIDL interfaces

## Testing Considerations

### Manual Testing

1. **Permission Flow:**
   - Launch app on fresh install
   - Verify overlay permission request appears
   - Verify usage stats permission request appears
   - Confirm both permissions are granted

2. **Detection Logic:**
   - Start service
   - Open Clash Royale
   - Verify overlay appears within 1-2 seconds
   - Switch to another app
   - Verify overlay disappears

3. **Service Persistence:**
   - Start service
   - Navigate away from app
   - Check notification tray for service notification
   - Verify service continues running

4. **Edge Cases:**
   - Quickly switch between apps
   - Rotate device while overlay is visible
   - Put device to sleep and wake
   - Low memory scenarios

### Potential Issues

**Overlay not appearing:**
- Check if permission is actually granted
- Verify Clash Royale package name matches
- Check logcat for WindowManager exceptions

**High battery drain:**
- CHECK_INTERVAL may need adjustment
- Consider using JobScheduler for longer intervals
- Implement battery optimization exemptions

**Service being killed:**
- Android may kill foreground services under memory pressure
- Implement restart strategy in onStartCommand (START_STICKY)
- Consider persistent notification importance

## Future Enhancements

### Suggested Features

1. **Interactive Overlay:**
   - Add buttons/controls to overlay
   - Implement drag-to-reposition
   - Resizable overlay option

2. **Game Analysis:**
   - Screenshot capture when events occur
   - Card/troop recognition using ML
   - Strategy suggestions

3. **Statistics Tracking:**
   - Win/loss record
   - Card usage frequency
   - Battle duration tracking

4. **Customization:**
   - Theme options
   - Overlay size/position preferences
   - Custom notification icons

5. **Performance:**
   - Reduce CHECK_INTERVAL during gameplay
   - Implement smart detection (only check when screen changes)
   - Battery optimization modes

## Known Limitations

1. **Detection Delay:** 1-second polling means up to 1-second delay in showing overlay
2. **Battery Impact:** Continuous polling uses battery (optimizable)
3. **Permission Requirements:** Requires two special permissions which users may deny
4. **Package Name Dependency:** Hardcoded Clash Royale package name may change
5. **No Interaction:** Current overlay is display-only, doesn't handle touch events

## Debugging Tips

### Enable Verbose Logging

Add logging to service:
```java
private static final String TAG = "OverlayService";
Log.d(TAG, "Checking foreground app: " + foregroundApp);
```

### Monitor Service State

```bash
adb shell dumpsys activity services com.clasher.engine
```

### Check Permissions

```bash
adb shell appops get com.clasher.engine SYSTEM_ALERT_WINDOW
adb shell appops get com.clasher.engine GET_USAGE_STATS
```

### Force Stop Service

```bash
adb shell am force-stop com.clasher.engine
```

### View Logs

```bash
adb logcat | grep -E "(OverlayService|MainActivity)"
```

## Contributing Guidelines

1. Follow existing code style (Java conventions)
2. Add comments for complex logic
3. Test on multiple Android versions (especially 7.0, 10.0, 14.0)
4. Update documentation for new features
5. Consider battery and performance impact
