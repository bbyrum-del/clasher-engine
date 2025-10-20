package com.clasher.engine;

import android.app.AppOpsManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private static final int REQUEST_CODE_OVERLAY_PERMISSION = 1001;
    private static final int REQUEST_CODE_USAGE_STATS_PERMISSION = 1002;
    
    private Button toggleServiceButton;
    private TextView statusText;
    private boolean serviceRunning = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        toggleServiceButton = findViewById(R.id.toggleServiceButton);
        statusText = findViewById(R.id.statusText);

        // Check and request necessary permissions
        checkPermissions();

        toggleServiceButton.setOnClickListener(v -> {
            if (!checkPermissions()) {
                Toast.makeText(this, "Please grant all permissions", Toast.LENGTH_SHORT).show();
                return;
            }

            if (serviceRunning) {
                stopOverlayService();
            } else {
                startOverlayService();
            }
        });
    }

    private boolean checkPermissions() {
        boolean hasOverlayPermission = checkOverlayPermission();
        boolean hasUsageStatsPermission = checkUsageStatsPermission();

        if (!hasOverlayPermission) {
            requestOverlayPermission();
            return false;
        }

        if (!hasUsageStatsPermission) {
            requestUsageStatsPermission();
            return false;
        }

        return true;
    }

    private boolean checkOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            return Settings.canDrawOverlays(this);
        }
        return true;
    }

    private void requestOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:" + getPackageName()));
            startActivityForResult(intent, REQUEST_CODE_OVERLAY_PERMISSION);
        }
    }

    private boolean checkUsageStatsPermission() {
        AppOpsManager appOps = (AppOpsManager) getSystemService(Context.APP_OPS_SERVICE);
        int mode = appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS,
                android.os.Process.myUid(), getPackageName());
        return mode == AppOpsManager.MODE_ALLOWED;
    }

    private void requestUsageStatsPermission() {
        Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
        startActivityForResult(intent, REQUEST_CODE_USAGE_STATS_PERMISSION);
    }

    private void startOverlayService() {
        Intent serviceIntent = new Intent(this, OverlayService.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent);
        } else {
            startService(serviceIntent);
        }
        serviceRunning = true;
        updateUI();
        Toast.makeText(this, R.string.service_started, Toast.LENGTH_SHORT).show();
    }

    private void stopOverlayService() {
        Intent serviceIntent = new Intent(this, OverlayService.class);
        stopService(serviceIntent);
        serviceRunning = false;
        updateUI();
        Toast.makeText(this, R.string.service_stopped, Toast.LENGTH_SHORT).show();
    }

    private void updateUI() {
        if (serviceRunning) {
            toggleServiceButton.setText(R.string.stop_service);
            statusText.setText("Service is running");
        } else {
            toggleServiceButton.setText(R.string.start_service);
            statusText.setText("Service is stopped");
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_OVERLAY_PERMISSION || 
            requestCode == REQUEST_CODE_USAGE_STATS_PERMISSION) {
            checkPermissions();
        }
    }
}
