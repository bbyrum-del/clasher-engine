# Security Considerations

This document outlines the security considerations for the Clasher Engine application.

## Permissions Used

### SYSTEM_ALERT_WINDOW
**Risk Level:** Medium  
**Purpose:** Allows the app to draw overlay windows on top of other applications  
**Security Implications:**
- Could be misused to display fake UI over legitimate apps
- Users must explicitly grant this permission via system settings
- Android displays a warning that this permission allows the app to "draw over other apps"

**Mitigation:**
- Permission is only requested when necessary
- Clear user messaging explains why the permission is needed
- Overlay is only shown when Clash Royale is active

### PACKAGE_USAGE_STATS
**Risk Level:** High  
**Purpose:** Allows monitoring of which apps are currently running  
**Security Implications:**
- Can reveal user behavior and app usage patterns
- Considered a "dangerous" permission requiring explicit user consent
- Must be granted through system settings, not in-app

**Mitigation:**
- Only used to detect Clash Royale, not to collect usage data
- No data is stored or transmitted
- Service runs locally on device only

### FOREGROUND_SERVICE / FOREGROUND_SERVICE_SPECIAL_USE
**Risk Level:** Low  
**Purpose:** Allows running background services that persist  
**Security Implications:**
- Can drain battery if not implemented properly
- Services can continue running even when app is closed

**Mitigation:**
- User can easily stop service from the app
- Foreground notification makes service visible
- Service doesn't perform any network operations

### POST_NOTIFICATIONS
**Risk Level:** Low  
**Purpose:** Required for displaying the foreground service notification (Android 13+)  
**Security Implications:**
- Minimal - only for service notification

## Data Privacy

### What Data is Collected
- **None** - The app does not collect, store, or transmit any user data

### What Data is Accessed
- Current foreground app package name (via UsageStatsManager)
- This data is:
  - Read in real-time
  - Not stored
  - Not transmitted over network
  - Only used for app detection logic

### No Network Access
- The app does not request INTERNET permission
- No data can be transmitted off the device
- All processing is local

## Potential Security Risks

### 1. Overlay Abuse
**Risk:** The overlay could theoretically be used for clickjacking or phishing attacks  
**Mitigation:**
- Overlay is non-interactive (FLAG_NOT_FOCUSABLE)
- Only appears when Clash Royale is active
- Small, transparent overlay at top of screen
- Source code is open for review

### 2. Privacy Monitoring
**Risk:** UsageStatsManager could be used to spy on user behavior  
**Mitigation:**
- Only checks for specific package name (Clash Royale)
- No logging or storage of usage data
- No network transmission capability
- Code is open source and auditable

### 3. Service Persistence
**Risk:** Service could continue running indefinitely without user knowledge  
**Mitigation:**
- Visible foreground notification required
- Easy stop button in main activity
- Can be force stopped from Android Settings
- No automatic restart after user stops it

### 4. Resource Consumption
**Risk:** Continuous polling could drain battery  
**Mitigation:**
- Efficient 1-second polling interval
- Only runs when explicitly started by user
- No wake locks or background processing
- Handler cleanup in onDestroy()

## Best Practices Implemented

### Principle of Least Privilege
- Only requests permissions absolutely necessary
- No INTERNET permission
- No CAMERA or MICROPHONE permissions
- No LOCATION permissions

### User Control
- User must explicitly start the service
- Clear permission request explanations
- Easy service stop functionality
- Visible foreground notification

### Transparency
- Open source code
- Comprehensive documentation
- Clear permission usage explanation
- No hidden functionality

### Secure Coding
- No hardcoded credentials
- No external dependencies beyond AndroidX
- Proper resource cleanup (Handler, WindowManager)
- Null checks and exception handling

## Recommendations for Users

### Before Installing
1. Review the source code on GitHub
2. Understand required permissions
3. Ensure you're downloading from official source

### After Installing
1. Only grant permissions you're comfortable with
2. Review the app's battery usage periodically
3. Stop the service when not needed
4. Uninstall if you no longer use it

### Monitoring the App
1. Check notification tray for service status
2. Use Android's battery optimization settings
3. Review app permissions in Android Settings
4. Monitor which apps have overlay permission

## Security Updates

This app follows secure development practices:
- Regular dependency updates
- Security patch reviews
- Community vulnerability reporting welcome

## Responsible Disclosure

If you discover a security vulnerability:
1. **DO NOT** create a public GitHub issue
2. Contact the maintainers privately
3. Provide detailed reproduction steps
4. Allow time for fix before public disclosure

## Compliance

### Android Security Best Practices
- ✅ Requests permissions at runtime
- ✅ Uses foreground services appropriately
- ✅ No unnecessary permissions
- ✅ Transparent about functionality
- ✅ User-controllable service lifecycle

### Google Play Policies (if published)
- ✅ Clear privacy policy
- ✅ Justification for sensitive permissions
- ✅ No deceptive behavior
- ✅ No malicious code

## Known Limitations

### Cannot Detect
- When Clash Royale is actually active (only when foreground)
- Game events or in-game state
- User credentials or account information

### Does Not
- Modify Clash Royale or any other app
- Provide unfair advantage in gameplay
- Violate Supercell Terms of Service (overlay only)

## Disclaimer

This app is a third-party tool and is not affiliated with Supercell. Users should:
- Review Supercell's Terms of Service
- Understand that overlay tools may be against ToS
- Use at their own risk
- Not use for cheating or unfair advantages

## License and Liability

This software is provided "as is" without warranty. Users are responsible for:
- Understanding the permissions they grant
- Compliance with applicable laws
- Compliance with game Terms of Service
- Any consequences of app usage

---

**Last Updated:** October 2025  
**Version:** 1.0
