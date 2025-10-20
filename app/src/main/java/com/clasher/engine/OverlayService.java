package com.clasher.engine;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.app.usage.UsageStats;
import android.app.usage.UsageStatsManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import androidx.core.app.NotificationCompat;

import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;

public class OverlayService extends Service {

    private static final String CHANNEL_ID = "OverlayServiceChannel";
    private static final int NOTIFICATION_ID = 1;
    private static final long CHECK_INTERVAL = 1000; // Check every second
    private static final String CLASH_ROYALE_PACKAGE = "com.supercell.clashroyale";

    private WindowManager windowManager;
    private View overlayView;
    private Handler handler;
    private Runnable checkRunnable;
    private boolean isOverlayVisible = false;
    private String lastForegroundApp = "";

    @Override
    public void onCreate() {
        super.onCreate();
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
        handler = new Handler(Looper.getMainLooper());
        
        createNotificationChannel();
        startForeground(NOTIFICATION_ID, createNotification());
        
        startMonitoring();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel serviceChannel = new NotificationChannel(
                    CHANNEL_ID,
                    "Overlay Service Channel",
                    NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                manager.createNotificationChannel(serviceChannel);
            }
        }
    }

    private Notification createNotification() {
        return new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle(getString(R.string.app_name))
                .setContentText(getString(R.string.service_running))
                .setSmallIcon(R.drawable.ic_launcher)
                .build();
    }

    private void startMonitoring() {
        checkRunnable = new Runnable() {
            @Override
            public void run() {
                String foregroundApp = getForegroundApp();
                
                if (foregroundApp != null && foregroundApp.equals(CLASH_ROYALE_PACKAGE)) {
                    if (!isOverlayVisible) {
                        showOverlay();
                    }
                } else {
                    if (isOverlayVisible) {
                        hideOverlay();
                    }
                }
                
                lastForegroundApp = foregroundApp;
                handler.postDelayed(this, CHECK_INTERVAL);
            }
        };
        handler.post(checkRunnable);
    }

    private String getForegroundApp() {
        String foregroundApp = null;
        UsageStatsManager usageStatsManager = (UsageStatsManager) getSystemService(Context.USAGE_STATS_SERVICE);
        
        if (usageStatsManager != null) {
            long currentTime = System.currentTimeMillis();
            // Query usage stats for the last 1 second
            List<UsageStats> stats = usageStatsManager.queryUsageStats(
                    UsageStatsManager.INTERVAL_DAILY,
                    currentTime - 1000 * 2,
                    currentTime
            );

            if (stats != null && !stats.isEmpty()) {
                SortedMap<Long, UsageStats> sortedStats = new TreeMap<>();
                for (UsageStats usageStats : stats) {
                    sortedStats.put(usageStats.getLastTimeUsed(), usageStats);
                }
                
                if (!sortedStats.isEmpty()) {
                    foregroundApp = sortedStats.get(sortedStats.lastKey()).getPackageName();
                }
            }
        }
        
        return foregroundApp;
    }

    private void showOverlay() {
        if (overlayView == null) {
            overlayView = LayoutInflater.from(this).inflate(R.layout.overlay_layout, null);

            WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                    WindowManager.LayoutParams.WRAP_CONTENT,
                    WindowManager.LayoutParams.WRAP_CONTENT,
                    Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                            ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                            : WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                    PixelFormat.TRANSLUCENT
            );

            params.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
            params.y = 100;

            windowManager.addView(overlayView, params);
            isOverlayVisible = true;
        }
    }

    private void hideOverlay() {
        if (overlayView != null && isOverlayVisible) {
            windowManager.removeView(overlayView);
            overlayView = null;
            isOverlayVisible = false;
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (handler != null && checkRunnable != null) {
            handler.removeCallbacks(checkRunnable);
        }
        hideOverlay();
    }
}
