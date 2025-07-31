#!/usr/bin/env python3
"""
STDatalog Service Monitor & Control Dashboard
Enhanced version for STDatalog CLI and BLE services
"""

from flask import Flask, render_template_string, request, jsonify, redirect
import subprocess
import os
import json
import time
import re
from datetime import datetime
import psutil
import sys
from flask import session, abort, url_for
from functools import wraps



# Add the parent of this file’s directory to PYTHONPATH so 'thread' is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from thread.find_root import find_subfolder
ACQ_FOLDER = find_subfolder("acquisition_data")

# Initialize Flask app
app = Flask(__name__)

# === Password Config ===
DASHBOARD_PASSWORD = "qwerty"
app.secret_key = "qwerty"  # Needed for sessions

# Service configuration
SERVICES = {
    'stdatalog-cli': {
        'name': 'STDatalog CLI Logger', 
        'log_file': '/home/kirwinr/logs/stdatalog-cli.log',
        'auto_restart': False
    },
    'stdatalog-ble': {
        'name': 'STDatalog BLE Controller',
        'log_file': '/home/kirwinr/logs/stdatalog-ble.log', 
        'auto_restart': True
    },
    'stdatalog-usboffload': {
        'name': 'USB Data Offload',
        'log_file': '/home/kirwinr/logs/stdatalog-usboffload.log',
        'auto_restart': True,
        'compact': True  # Special flag for compact display
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == DASHBOARD_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return "<h3>Incorrect password</h3><a href='/login'>Try again</a>", 401

    return '''
        <html><head>
        <style>
        body {
            background: #111;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: sans-serif;
        }
        input[type="password"] {
            padding: 10px;
            font-size: 16px;
            width: 200px;
        }
        button {
            padding: 10px;
            font-size: 16px;
            margin-left: 10px;
        }
        </style></head><body>
        <form method="POST">
            <input type="password" name="password" placeholder="Enter password" autofocus/>
            <button type="submit">Login</button>
        </form>
        </body></html>
    '''

def ansi_to_html(text):
    """Convert ANSI color codes to HTML with colors matching colorlog setup"""
    # ANSI color codes mapping to HTML colors
    ansi_colors = {
        # Standard colors
        '\033[30m': '<span style="color: #000000;">',  # black
        '\033[31m': '<span style="color: #ff0000;">',  # red
        '\033[32m': '<span style="color: #00ff00;">',  # green
        '\033[33m': '<span style="color: #ffff00;">',  # yellow
        '\033[34m': '<span style="color: #0000ff;">',  # blue
        '\033[35m': '<span style="color: #ff00ff;">',  # magenta
        '\033[36m': '<span style="color: #00ffff;">',  # cyan
        '\033[37m': '<span style="color: #ffffff;">',  # white
        
        # Bright colors
        '\033[90m': '<span style="color: #808080;">',  # bright black (gray)
        '\033[91m': '<span style="color: #ff6666;">',  # bright red
        '\033[92m': '<span style="color: #66ff66;">',  # bright green
        '\033[93m': '<span style="color: #ffff66;">',  # bright yellow
        '\033[94m': '<span style="color: #6666ff;">',  # bright blue
        '\033[95m': '<span style="color: #ff66ff;">',  # bright magenta
        '\033[96m': '<span style="color: #66ffff;">',  # bright cyan
        '\033[97m': '<span style="color: #ffffff;">',  # bright white
        
        # Bold (colorlog uses this)
        '\033[1m': '<span style="font-weight: bold;">',
        '\033[1;31m': '<span style="color: #ff0000; font-weight: bold;">',  # bold red
        
        # Reset
        '\033[0m': '</span>',
        '\033[39m': '</span>',  # default foreground
        '\033[49m': '</span>',  # default background
    }
    
    # Convert ANSI codes to HTML
    html_text = text
    for ansi_code, html_tag in ansi_colors.items():
        html_text = html_text.replace(ansi_code, html_tag)
    
    # Handle any remaining ANSI codes with a regex (remove unknown codes)
    html_text = re.sub(r'\033\[[0-9;]*m', '', html_text)
    
    # Ensure proper span closing for any unclosed tags
    open_spans = html_text.count('<span')
    close_spans = html_text.count('</span>')
    if open_spans > close_spans:
        html_text += '</span>' * (open_spans - close_spans)
    
    return html_text

def get_recent_logs():
    """Get recent log entries from both services separately with color support"""
    service_logs = {}
    for service_id, config in SERVICES.items():
        # Skip logs for USB service as per requirements
        if config.get('compact', False):
            continue
            
        log_file = config['log_file']
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Get last 25 lines from each service
                    recent = lines[-25:] if len(lines) > 25 else lines
                    if recent:
                        log_text = ''.join(recent)
                        # Convert ANSI color codes to HTML for BLE service
                        if service_id == 'stdatalog-ble':
                            log_text = ansi_to_html(log_text)
                        service_logs[service_id] = log_text
                    else:
                        service_logs[service_id] = "No recent logs available"
            except:
                service_logs[service_id] = "Error reading log file"
        else:
            service_logs[service_id] = "Log file not found"
    return service_logs

# Global state cache for BLE status
LAST_KNOWN_BLE_STATUS = {
    'speed_sensor': {'connected': False, 'status': 'Unknown'},
    'feedrate_sensor': {'connected': False, 'status': 'Unknown'}
}

def get_ble_status():
    global LAST_KNOWN_BLE_STATUS
    
    # First check if the BLE service is running
    ble_service_status = get_service_status('stdatalog-ble')
    if ble_service_status != 'active':
        # If service is not active, return unknown status for both sensors
        return {
            'speed_sensor': {'connected': False, 'status': 'Service not running'},
            'feedrate_sensor': {'connected': False, 'status': 'Service not running'}
        }
    
    try:
        log_file = SERVICES['stdatalog-ble']['log_file']
        if not os.path.exists(log_file):
            return {
                'speed_sensor': {'connected': False, 'status': 'Log not found'},
                'feedrate_sensor': {'connected': False, 'status': 'Log not found'}
            }

        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            recent_text = ''.join(recent_lines)

        updated = False

        if "Speed BLE connected" in recent_text:
            if "Speed BLE disconnected" not in recent_text.split("Speed BLE connected")[-1]:
                LAST_KNOWN_BLE_STATUS['speed_sensor'] = {
                    'connected': True,
                    'status': "Connected and listening"
                }
                updated = True
            else:
                LAST_KNOWN_BLE_STATUS['speed_sensor'] = {
                    'connected': False,
                    'status': "Disconnected, retrying..."
                }
                updated = True

        if "Feedrate BLE connected" in recent_text:
            if "Feedrate BLE disconnected" not in recent_text.split("Feedrate BLE connected")[-1]:
                LAST_KNOWN_BLE_STATUS['feedrate_sensor'] = {
                    'connected': True,
                    'status': "Connected and listening"
                }
                updated = True
            else:
                LAST_KNOWN_BLE_STATUS['feedrate_sensor'] = {
                    'connected': False,
                    'status': "Disconnected, retrying..."
                }
                updated = True

        LAST_KNOWN_BLE_STATUS['speed_sensor']['mac'] = 'F9:51:AC:0F:75:9E'
        LAST_KNOWN_BLE_STATUS['feedrate_sensor']['mac'] = 'DE:6D:5D:2A:BD:58'

        return LAST_KNOWN_BLE_STATUS

    except Exception as e:
        return {
            'speed_sensor': {'connected': False, 'status': f'Error: {str(e)}'},
            'feedrate_sensor': {'connected': False, 'status': f'Error: {str(e)}'}
        }


def get_usb_status():
    """Check if any USB stick is mounted and get info"""
    import getpass
    base_media = f"/media/{getpass.getuser()}"
    
    try:
        if os.path.isdir(base_media):
            # Find all mounted USB drives
            usb_mounts = [os.path.join(base_media, d) for d in os.listdir(base_media)
                         if os.path.ismount(os.path.join(base_media, d))]
            
            if usb_mounts:
                # Use the first USB found
                usb_path = usb_mounts[0]
                # Get disk usage info
                import shutil
                total, used, free = shutil.disk_usage(usb_path)
                free_mb = free // (1024*1024)
                total_mb = total // (1024*1024)
                used_percent = int((used / total) * 100)
                
                return {
                    'connected': True,
                    'free_space_mb': free_mb,
                    'total_space_mb': total_mb,
                    'used_percent': used_percent,
                    'mount_path': usb_path
                }
        
        return {'connected': False}
    except:
        return {'connected': False}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>STDatalog Service Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 20px; 
            background: #f5f5f5;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 { 
            color: #2c3e50; 
            text-align: center; 
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .service-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .service-card { 
            border: 2px solid #ddd; 
            border-radius: 8px; 
            padding: 20px; 
            background: #fafafa;
        }
        .service-card.active { border-color: #27ae60; background: #f8fff8; }
        .service-card.inactive { border-color: #e74c3c; background: #fff8f8; }
        .service-card.compact { 
            grid-column: 1 / -1; /* Span all columns */
            padding: 12px 20px; 
            background: #f8f9fa; 
            border: 1px solid #ddd;
            min-height: auto;
        }
        .service-card.compact.active { border-color: #17a2b8; background: #f0f9ff; }
        .service-card.compact.inactive { border-color: #6c757d; background: #f8f9fa; }
        .compact-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .compact-left {
            display: flex;
            align-items: center;
            flex: 1;
        }
        .compact-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .usb-info { 
            font-size: 12px; 
            color: #6c757d; 
            margin-top: 8px;
        }
        .usb-status { 
            display: inline-block; 
            padding: 2px 6px; 
            border-radius: 3px; 
            font-size: 11px; 
            font-weight: bold;
        }
        .usb-connected { background: #d4edda; color: #155724; }
        .usb-disconnected { background: #f8d7da; color: #721c24; }
        .ble-info { 
            font-size: 12px; 
            color: #6c757d; 
            margin-top: 8px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .ble-sensor { 
            display: flex; 
            align-items: center; 
            gap: 6px;
        }
        .ble-led { 
            width: 8px; 
            height: 8px; 
            border-radius: 50%; 
            flex-shrink: 0;
        }
        .ble-led.connected { background: #28a745; }
        .ble-led.disconnected { background: #dc3545; }
        .ble-led.unknown { background: #6c757d; }
        .ble-sensor-text {
            font-size: 11px;
            line-height: 1.2;
        }
        .ble-mac {
            color: #999;
            font-size: 10px;
        }
        .service-header { 
            display: flex; 
            align-items: center; 
            margin-bottom: 15px;
        }
        .led { 
            width: 20px; 
            height: 20px; 
            border-radius: 50%; 
            margin-right: 15px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        .led.green { background: #27ae60; box-shadow: 0 0 15px #27ae60; }
        .led.red { background: #e74c3c; box-shadow: 0 0 15px #e74c3c; }
        .service-name { 
            font-weight: bold; 
            font-size: 18px; 
            color: #2c3e50;
        }
        .service-status { 
            font-size: 14px; 
            margin-top: 5px;
        }
        .status-active { color: #27ae60; font-weight: bold; }
        .status-inactive { color: #e74c3c; font-weight: bold; }
        .btn { 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 14px; 
            margin: 5px; 
            transition: all 0.3s;
        }
        .btn-restart { background: #3498db; color: white; }
        .btn-restart:hover { background: #2980b9; }
        .btn-stop { background: #e74c3c; color: white; }
        .btn-stop:hover { background: #c0392b; }
        .btn-start { background: #27ae60; color: white; }
        .btn-start:hover { background: #229954; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 15px; 
            margin-top: 20px;
        }
        .stat-card { 
            background: #ecf0f1; 
            padding: 15px; 
            border-radius: 5px; 
            text-align: center;
        }
        .stat-value { 
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
        }
        .stat-label { 
            font-size: 12px; 
            color: #7f8c8d; 
            margin-top: 5px;
        }
        .log-section { 
            margin-top: 30px; 
            padding: 20px; 
            background: #2c3e50; 
            border-radius: 8px; 
            color: #ecf0f1;
        }
        .log-content { 
            font-family: 'Courier New', monospace; 
            background: #34495e; 
            padding: 15px; 
            border-radius: 5px; 
            max-height: 300px; 
            overflow-y: auto; 
            white-space: pre-wrap; 
            font-size: 12px;
            line-height: 1.4;
        }
        .logs-container {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        .log-column {
            flex: 1;
            background: #2c3e50;
            border-radius: 8px;
            padding: 15px;
        }
        .log-column h4 {
            margin: 0 0 15px 0;
            color: #f39c12;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            border-bottom: 2px solid #f39c12;
            padding: 8px 0;
            background: #34495e;
            border-radius: 4px;
        }
        .refresh-notice { 
            background: #f39c12; 
            color: white; 
            padding: 10px; 
            border-radius: 5px; 
            text-align: center; 
            margin-bottom: 20px;
        }
    </style>
    <script>
    function updateDashboard() {
        fetch("/api/status")
            .then(response => response.json())
            .then(data => {
                try {
                    // Update service status
                    for (const [service_id, info] of Object.entries(data.services)) {
                        // Uptime
                        const uptimeEl = document.getElementById(service_id + "-uptime");
                        if (uptimeEl) uptimeEl.textContent = info.uptime;
                        
                        // Memory
                        const memoryEl = document.getElementById(service_id + "-memory");
                        if (memoryEl) memoryEl.textContent = info.memory;
                        
                        // Status LED
                        let led = document.getElementById(service_id + "-led");
                        if (led) led.className = "led " + (info.status === "active" ? "green" : "red");
                        
                        // Status Text
                        let statusText = document.getElementById(service_id + "-status");
                        if (statusText) {
                            statusText.textContent = info.status.toUpperCase() + (info.auto_restart ? " (Auto-restart)" : " (Manual)");
                            statusText.className = "service-status " + (info.status === "active" ? "status-active" : "status-inactive");
                        }
                        
                        // Update buttons dynamically based on service status
                        const buttonContainer = document.querySelector(`[data-service="${service_id}"]`);
                        if (buttonContainer) {
                            const isActive = info.status === "active";
                            const isCompact = buttonContainer.classList.contains('compact-buttons');
                            
                            // Create the appropriate buttons HTML
                            let buttonsHTML;
                            if (isActive) {
                                // Service is active - show restart and stop buttons
                                if (isCompact) {
                                    buttonsHTML = `
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="restart">
                                            <button type="submit" class="btn btn-restart" style="padding: 8px 12px; font-size: 12px;">🔄</button>
                                        </form>
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="stop">
                                            <button type="submit" class="btn btn-stop" style="padding: 8px 12px; font-size: 12px;">⏹️</button>
                                        </form>
                                    `;
                                } else {
                                    buttonsHTML = `
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="restart">
                                            <button type="submit" class="btn btn-restart">🔄 Restart</button>
                                        </form>
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="stop">
                                            <button type="submit" class="btn btn-stop">⏹️ Stop</button>
                                        </form>
                                    `;
                                }
                            } else {
                                // Service is inactive - show restart and start buttons
                                if (isCompact) {
                                    buttonsHTML = `
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="restart">
                                            <button type="submit" class="btn btn-restart" style="padding: 8px 12px; font-size: 12px;">🔄</button>
                                        </form>
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="start">
                                            <button type="submit" class="btn btn-start" style="padding: 8px 12px; font-size: 12px;">▶️</button>
                                        </form>
                                    `;
                                } else {
                                    buttonsHTML = `
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="restart">
                                            <button type="submit" class="btn btn-restart">🔄 Restart</button>
                                        </form>
                                        <form method="post" action="/control/${service_id}" style="display: inline;">
                                            <input type="hidden" name="action" value="start">
                                            <button type="submit" class="btn btn-start">▶️ Start</button>
                                        </form>
                                    `;
                                }
                            }
                            buttonContainer.innerHTML = buttonsHTML;
                        }
                    }
                } catch (error) {
                    console.error("Error updating services:", error);
                }

                try {
                    // Update system stats
                    const acqFoldersEl = document.getElementById("acq_folders");
                    if (acqFoldersEl) acqFoldersEl.textContent = data.system.acquisition_folders;
                    
                    const cutFoldersEl = document.getElementById("cut_folders");
                    if (cutFoldersEl) cutFoldersEl.textContent = data.system.cut_folders;
                    
                    const diskUsageEl = document.getElementById("disk_usage");
                    if (diskUsageEl) diskUsageEl.textContent = data.system.disk_usage + "%";
                } catch (error) {
                    console.error("Error updating system stats:", error);
                }

                try {
                    // Update USB status
                    if (data.system.usb_status) {
                        const usbStatusEl = document.getElementById("usb-status");
                        const usbInfoEl = document.getElementById("usb-info");
                        
                        if (usbStatusEl && usbInfoEl) {
                            if (data.system.usb_status.connected) {
                                usbStatusEl.textContent = "CONNECTED";
                                usbStatusEl.className = "usb-status usb-connected";
                                usbInfoEl.textContent = `${data.system.usb_status.free_space_mb} MB free (${data.system.usb_status.used_percent}% used)`;
                            } else {
                                usbStatusEl.textContent = "NOT DETECTED";
                                usbStatusEl.className = "usb-status usb-disconnected";
                                usbInfoEl.textContent = "Insert USB stick to begin data transfer";
                            }
                        }
                    }
                } catch (error) {
                    console.error("Error updating USB status:", error);
                }

                try {
                    // Update logs per service
                    if (data.system.logs) {
                        for (const [service_id, log_content] of Object.entries(data.system.logs)) {
                            const logDiv = document.getElementById(service_id + "-log");
                            if (logDiv) {
                                // Use innerHTML for BLE service to render HTML colors, textContent for others
                                if (service_id === 'stdatalog-ble') {
                                    logDiv.innerHTML = log_content;
                                } else {
                                    logDiv.textContent = log_content;
                                }
                            }
                        }
                    }
                } catch (error) {
                    console.error("Error updating logs:", error);
                }

                try {
                    // Update BLE sensor status
                    if (data.system.ble_status) {
                        // Speed sensor
                        const speedLed = document.getElementById("speed-sensor-led");
                        const speedStatus = document.getElementById("speed-sensor-status");
                        if (speedLed && speedStatus) {
                            // Check if service is not running
                            if (data.system.ble_status.speed_sensor.status === "Service not running") {
                                speedLed.className = "ble-led unknown";
                                speedStatus.textContent = "Service not running";
                            } else {
                                speedLed.className = "ble-led " + (data.system.ble_status.speed_sensor.connected ? "connected" : "disconnected");
                                speedStatus.textContent = data.system.ble_status.speed_sensor.status;
                            }
                        }
                        
                        // Feedrate sensor
                        const feedrateLed = document.getElementById("feedrate-sensor-led");
                        const feedrateStatus = document.getElementById("feedrate-sensor-status");
                        if (feedrateLed && feedrateStatus) {
                            // Check if service is not running
                            if (data.system.ble_status.feedrate_sensor.status === "Service not running") {
                                feedrateLed.className = "ble-led unknown";
                                feedrateStatus.textContent = "Service not running";
                            } else {
                                feedrateLed.className = "ble-led " + (data.system.ble_status.feedrate_sensor.connected ? "connected" : "disconnected");
                                feedrateStatus.textContent = data.system.ble_status.feedrate_sensor.status;
                            }
                        }
                    }
                } catch (error) {
                    console.error("Error updating BLE status:", error);
                }

                try {
                    // Update timestamp
                    const timestampEl = document.getElementById("timestamp");
                    if (timestampEl) timestampEl.textContent = (new Date(data.system.timestamp)).toLocaleString();
                } catch (error) {
                    console.error("Error updating timestamp:", error);
                }
            })
            .catch(error => {
                console.error("Dashboard update failed:", error);
            });
    }

    // Update every second
    setInterval(updateDashboard, 1000);
    </script>
</head>
<body>
    <div class="container">
        <h1>🔧 STDatalog Service Monitor</h1>
        
        <div class="refresh-notice">
            ⏱️ Live updates | Last updated: <span id="timestamp">{{ timestamp }}</span>
        </div>
        
        <div class="service-grid">
            {% for service_id, service_info in services.items() %}
            {% if service_info.config.get('compact', False) %}
            <!-- Compact USB Service -->
            <div class="service-card compact {{ 'active' if service_info.status == 'active' else 'inactive' }}">
                <div class="compact-content">
                    <div class="compact-left">
                        <div class="led {{ 'green' if service_info.status == 'active' else 'red' }}" id="{{ service_id }}-led"></div>
                        <div style="margin-right: 20px;">
                            <div class="service-name">📀 {{ service_info.config.name }}</div>
                            <div class="service-status {{ 'status-active' if service_info.status == 'active' else 'status-inactive' }}" id="{{ service_id }}-status">
                                {{ service_info.status.upper() }}{% if service_info.config.auto_restart %} (Auto-restart){% else %} (Manual){% endif %}
                            </div>
                        </div>
                        <div class="usb-info">
                            USB: <span class="usb-status usb-disconnected" id="usb-status">NOT DETECTED</span>
                            <small id="usb-info" style="display: block; margin-top: 2px;">Insert USB stick to begin data transfer</small>
                        </div>
                    </div>
                    <div class="compact-right" data-service="{{ service_id }}" class="compact-buttons">
                        <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                            <input type="hidden" name="action" value="restart">
                            <button type="submit" class="btn btn-restart" style="padding: 8px 12px; font-size: 12px;">🔄</button>
                        </form>
                        {% if service_info.status == 'active' %}
                        <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                            <input type="hidden" name="action" value="stop">
                            <button type="submit" class="btn btn-stop" style="padding: 8px 12px; font-size: 12px;">⏹️</button>
                        </form>
                        {% else %}
                        <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                            <input type="hidden" name="action" value="start">
                            <button type="submit" class="btn btn-start" style="padding: 8px 12px; font-size: 12px;">▶️</button>
                        </form>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% else %}
            <!-- Regular Service -->
            <div class="service-card {{ 'active' if service_info.status == 'active' else 'inactive' }}">
                <div class="service-header">
                    <div class="led {{ 'green' if service_info.status == 'active' else 'red' }}" id="{{ service_id }}-led"></div>
                    <div style="flex: 1;">
                        <div class="service-name">{{ service_info.config.name }}</div>
                        <div class="service-status {{ 'status-active' if service_info.status == 'active' else 'status-inactive' }}" id="{{ service_id }}-status">
                            {{ service_info.status.upper() }}{% if service_info.config.auto_restart %} (Auto-restart){% else %} (Manual){% endif %}
                        </div>
                        
                        {% if service_id == 'stdatalog-ble' %}
                        <div class="ble-info" id="ble-status-info">
                            <div class="ble-sensor">
                                <div class="ble-led unknown" id="speed-sensor-led"></div>
                                <div class="ble-sensor-text">
                                    <strong>Speed:</strong> <span id="speed-sensor-status">Checking...</span><br>
                                    <span class="ble-mac" id="speed-sensor-mac">F9:51:AC:0F:75:9E</span>
                                </div>
                            </div>
                            <div class="ble-sensor">
                                <div class="ble-led unknown" id="feedrate-sensor-led"></div>
                                <div class="ble-sensor-text">
                                    <strong>Feedrate:</strong> <span id="feedrate-sensor-status">Checking...</span><br>
                                    <span class="ble-mac" id="feedrate-sensor-mac">DE:6D:5D:2A:BD:58</span>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                    </div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="{{ service_id }}-uptime">{{ service_info.uptime }}</div>
                        <div class="stat-label">Uptime</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="{{ service_id }}-memory">{{ service_info.memory }}</div>
                        <div class="stat-label">Memory</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px;" data-service="{{ service_id }}">
                    <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                        <input type="hidden" name="action" value="restart">
                        <button type="submit" class="btn btn-restart">🔄 Restart</button>
                    </form>
                    
                    {% if service_info.status == 'active' %}
                    <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                        <input type="hidden" name="action" value="stop">
                        <button type="submit" class="btn btn-stop">⏹️ Stop</button>
                    </form>
                    {% else %}
                    <form method="post" action="/control/{{ service_id }}" style="display: inline;">
                        <input type="hidden" name="action" value="start">
                        <button type="submit" class="btn btn-start">▶️ Start</button>
                    </form>
                    {% endif %}
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="acq_folders">{{ acq_folders }}</div>
                <div class="stat-label">Acquisition Folders</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="cut_folders">{{ cut_folders }}</div>
                <div class="stat-label">Cut Folders</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="disk_usage">{{ disk_usage }}%</div>
                <div class="stat-label">Disk Usage</div>
            </div>
        </div>
        
        {% if recent_logs %}
        <div class="log-section">
            <h3>📋 Recent Logs (Last 25 lines per service)</h3>
            <div class="logs-container">
                {% for service_id, log_content in recent_logs.items() %}
                <div class="log-column">
                    <h4>🔧 {{ services[service_id]['config']['name'] if service_id in services else service_id }} ({{ service_id }})</h4>
                    {% if service_id == 'stdatalog-ble' %}
                    <div class="log-content" id="{{ service_id }}-log">{{ log_content|safe }}</div>
                    {% else %}
                    <div class="log-content" id="{{ service_id }}-log">{{ log_content }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_service_status(service_name):
    """Get systemd service status"""
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return 'unknown'

def get_service_info(service_name):
    """Get detailed service information"""
    try:
        # Get basic status
        status = get_service_status(service_name)
        
        # Get uptime and memory info if running
        uptime = "N/A"
        memory = "N/A"
        
        if status == 'active':
            try:
                # Get process info
                result = subprocess.run(['systemctl', 'show', service_name, 
                                       '--property=MainPID'], 
                                      capture_output=True, text=True)
                pid_line = result.stdout.strip()
                if pid_line.startswith('MainPID='):
                    pid = int(pid_line.split('=')[1])
                    if pid > 0:
                        try:
                            proc = psutil.Process(pid)
                            # Uptime
                            create_time = proc.create_time()
                            uptime_seconds = int(time.time() - create_time)
                            hours, remainder = divmod(uptime_seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            uptime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                            
                            # Memory
                            memory_mb = proc.memory_info().rss / 1024 / 1024
                            memory = f"{memory_mb:.1f} MB"
                        except psutil.NoSuchProcess:
                            pass
            except:
                pass
        
        return {
            'status': status,
            'uptime': uptime,
            'memory': memory
        }
    except:
        return {
            'status': 'unknown',
            'uptime': 'N/A', 
            'memory': 'N/A'
        }

def get_acquisition_stats():
    """Get acquisition folder statistics"""
    try:
        if not os.path.exists(ACQ_FOLDER):
            return 0, 0
        
        folders = [d for d in os.listdir(ACQ_FOLDER) 
                  if os.path.isdir(os.path.join(ACQ_FOLDER, d))]
        
        # Count cut_* folders
        cut_folders = [f for f in folders if f.startswith('cut_')]
        cut_folder_count = len(cut_folders)
        
        # Count all subfolders inside cut_* folders
        total_acquisition_folders = 0
        for cut_folder in cut_folders:
            cut_folder_path = os.path.join(ACQ_FOLDER, cut_folder)
            try:
                subfolders = [d for d in os.listdir(cut_folder_path) 
                             if os.path.isdir(os.path.join(cut_folder_path, d))]
                total_acquisition_folders += len(subfolders)
            except:
                # Skip if we can't read the cut folder
                continue
        
        return total_acquisition_folders, cut_folder_count
    except:
        return 0, 0

def get_disk_usage():
    """Get disk usage percentage for the workspace"""
    try:
        usage = psutil.disk_usage('/home/kirwinr/Desktop/stdatalog')
        return int(usage.percent)
    except:
        return 0



@app.route("/")
@login_required
def dashboard():
    # Get service information
    services = {}
    for service_id, config in SERVICES.items():
        info = get_service_info(service_id)
        services[service_id] = {
            'config': config,
            'status': info['status'],
            'uptime': info['uptime'],
            'memory': info['memory']
        }
    
    # Get system stats
    acq_folders, cut_folders = get_acquisition_stats()
    disk_usage = get_disk_usage()
    recent_logs = get_recent_logs()
    usb_status = get_usb_status()
    ble_status = get_ble_status()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template_string(HTML_TEMPLATE, 
                                services=services,
                                acq_folders=acq_folders,
                                cut_folders=cut_folders,
                                disk_usage=disk_usage,
                                recent_logs=recent_logs,
                                usb_status=usb_status,
                                ble_status=ble_status,
                                timestamp=timestamp)

@app.route("/control/<service_id>", methods=["POST"])
@login_required
def control_service(service_id):
    if service_id not in SERVICES:
        return "Service not found", 404
    
    action = request.form.get('action')
    if action not in ['start', 'stop', 'restart']:
        return "Invalid action", 400
    
    try:
        # Clear the log file before performing the action
        log_file = SERVICES[service_id]['log_file']
        if os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write(f"=== Log cleared - {action} action at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        
        subprocess.run(['sudo', 'systemctl', action, service_id], check=True)
        return redirect('/')
    except subprocess.CalledProcessError as e:
        return f"Failed to {action} service: {e}", 500

@app.route("/api/status")
def api_status():
    services = {}
    for service_id, config in SERVICES.items():
        info = get_service_info(service_id)
        services[service_id] = {
            'name': config['name'],
            'status': info['status'],
            'uptime': info['uptime'],
            'memory': info['memory'],
            'auto_restart': config['auto_restart']
        }
    
    acq_folders, cut_folders = get_acquisition_stats()
    logs = get_recent_logs() 
    usb_status = get_usb_status()
    ble_status = get_ble_status()

    return jsonify({
        'services': services,
        'system': {
            'acquisition_folders': acq_folders,
            'cut_folders': cut_folders,
            'disk_usage': get_disk_usage(),
            'timestamp': datetime.now().isoformat(),
            'logs': logs,
            'usb_status': usb_status,
            'ble_status': ble_status
        }
    })

if __name__ == "__main__":
    # Create log directory if it doesn't exist
    os.makedirs('/home/kirwinr/logs', exist_ok=True)
    
    print("🌐 STDatalog Service Monitor starting...")
    print("📊 Dashboard available at: http://10.0.71.110:8080/")
    print("🔌 API endpoint available at: http://10.0.71.110:8080/api/status")
    
    app.run(host="0.0.0.0", port=8080, debug=False)
