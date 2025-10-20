# Clasher Engine

Like a chess engine but for Clash Royale - A mobile overlay application that runs when Clash Royale is open.

## Overview

Clasher Engine is an Android application that provides a mobile overlay that appears when the Clash Royale game is running. The app monitors for Clash Royale in the foreground and displays an overlay view that can be used for game assistance, analysis, or other features.

## Features

- **Automatic Detection**: Continuously monitors running apps to detect when Clash Royale is active
- **Overlay Display**: Shows a customizable overlay on top of Clash Royale when the game is running
- **Foreground Service**: Runs as a persistent foreground service to ensure reliable monitoring
- **Permission Management**: Handles all necessary Android permissions (Overlay, Usage Stats, Foreground Service)

## Technical Implementation

### Architecture

The app consists of three main components:

1. **MainActivity**: The main entry point that handles permission requests and service management
2. **OverlayService**: A foreground service that monitors for Clash Royale and manages the overlay view
3. **Overlay Layout**: A customizable UI that appears when Clash Royale is detected

### Required Permissions

- `SYSTEM_ALERT_WINDOW`: Required to draw overlay on top of other apps
- `FOREGROUND_SERVICE`: Required to run the monitoring service persistently
- `FOREGROUND_SERVICE_SPECIAL_USE`: Required for API 34+ foreground services
- `PACKAGE_USAGE_STATS`: Required to detect which app is currently in the foreground
- `POST_NOTIFICATIONS`: Required for the foreground service notification

### How It Works

1. The app starts a foreground service when the user grants permissions and starts the service
2. The service checks every second which app is in the foreground using UsageStatsManager
3. When Clash Royale (package: `com.supercell.clashroyale`) is detected, the overlay is displayed
4. When the user switches away from Clash Royale, the overlay is automatically hidden
5. The service continues running until explicitly stopped by the user

## Building the App

### Prerequisites

- Android Studio (latest version recommended)
- Android SDK with API level 34
- Gradle 8.0+

### Build Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/bbyrum-del/clasher-engine.git
   cd clasher-engine
   ```

2. Open the project in Android Studio or build from command line:
   ```bash
   ./gradlew build
   ```

3. Install on device:
   ```bash
   ./gradlew installDebug
   ```

## Usage

1. Install and launch the app
2. Grant overlay permission when prompted
3. Grant usage stats permission when prompted (Settings → Usage Access)
4. Tap "Start Overlay Service" button
5. Launch Clash Royale - the overlay will appear automatically
6. The overlay will hide when you exit Clash Royale

## File Structure

```
clasher-engine/
├── app/
│   ├── src/main/
│   │   ├── java/com/clasher/engine/
│   │   │   ├── MainActivity.java          # Main activity for UI and permission handling
│   │   │   └── OverlayService.java        # Service for monitoring and overlay display
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml      # Main activity layout
│   │   │   │   └── overlay_layout.xml     # Overlay view layout
│   │   │   ├── values/
│   │   │   │   ├── colors.xml             # Color definitions
│   │   │   │   ├── strings.xml            # String resources
│   │   │   │   └── styles.xml             # App theme
│   │   │   └── drawable/
│   │   │       └── ic_launcher.xml        # App icon
│   │   └── AndroidManifest.xml            # App manifest with permissions
│   ├── build.gradle                        # App-level build configuration
│   └── proguard-rules.pro                  # ProGuard rules
├── build.gradle                            # Project-level build configuration
├── settings.gradle                         # Project settings
└── gradle.properties                       # Gradle properties
```

## Customization

### Modifying the Overlay

To customize the overlay appearance, edit `app/src/main/res/layout/overlay_layout.xml`:
- Change dimensions, colors, or add new UI elements
- Update `OverlayService.java` to add interactive features

### Changing Detection Frequency

Modify the `CHECK_INTERVAL` constant in `OverlayService.java` (default: 1000ms):
```java
private static final long CHECK_INTERVAL = 1000; // milliseconds
```

### Overlay Position

Adjust the overlay position in `OverlayService.showOverlay()` method:
```java
params.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
params.y = 100; // Distance from top in pixels
```

## License

This project is open source and available for educational purposes.

## Disclaimer

This app is not affiliated with, endorsed by, or sponsored by Supercell. Clash Royale is a trademark of Supercell.
