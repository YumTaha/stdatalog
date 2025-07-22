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
from datetime import datetime
import psutil

app = Flask(__name__)

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
    }
}

# Acquisition folder monitoring
ACQ_FOLDER = "/home/kirwinr/Desktop/stdatalog/acquisition_data"

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
                // Update service status
                for (const [service_id, info] of Object.entries(data.services)) {
                    // Uptime
                    document.getElementById(service_id + "-uptime").textContent = info.uptime;
                    // Memory
                    document.getElementById(service_id + "-memory").textContent = info.memory;
                    // Status LED
                    let led = document.getElementById(service_id + "-led");
                    led.className = "led " + (info.status === "active" ? "green" : "red");
                    // Status Text
                    let statusText = document.getElementById(service_id + "-status");
                    statusText.textContent = info.status.toUpperCase() + (info.auto_restart ? " (Auto-restart)" : " (Manual)");
                    statusText.className = "service-status " + (info.status === "active" ? "status-active" : "status-inactive");
                }

                // Update system stats
                document.getElementById("acq_folders").textContent = data.system.acquisition_folders;
                document.getElementById("cut_folders").textContent = data.system.cut_folders;
                document.getElementById("disk_usage").textContent = data.system.disk_usage + "%";

                // Update logs per service
                for (const [service_id, log_content] of Object.entries(data.system.logs)) {
                    const logDiv = document.getElementById(service_id + "-log");
                    if (logDiv) logDiv.textContent = log_content;
                }

                // Update timestamp
                document.getElementById("timestamp").textContent = (new Date(data.system.timestamp)).toLocaleString();
            })
            .catch(error => {
                // Optional: handle fetch error
                console.log("AJAX fetch failed", error);
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
            ⏱️ Live updates (every 1 second) | Last updated: <span id="timestamp">{{ timestamp }}</span>
        </div>
        
        <div class="service-grid">
            {% for service_id, service_info in services.items() %}
            <div class="service-card {{ 'active' if service_info.status == 'active' else 'inactive' }}">
                <div class="service-header">
                    <!-- ADD id to LED -->
                    <div class="led {{ 'green' if service_info.status == 'active' else 'red' }}" id="{{ service_id }}-led"></div>
                    <div>
                        <div class="service-name">{{ service_info.config.name }}</div>
                        <!-- ADD id to status -->
                        <div class="service-status {{ 'status-active' if service_info.status == 'active' else 'status-inactive' }}" id="{{ service_id }}-status">
                            {{ service_info.status.upper() }}{% if service_info.config.auto_restart %} (Auto-restart){% else %} (Manual){% endif %}
                        </div>
                    </div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <!-- ADD id to uptime -->
                        <div class="stat-value" id="{{ service_id }}-uptime">{{ service_info.uptime }}</div>
                        <div class="stat-label">Uptime</div>
                    </div>
                    <div class="stat-card">
                        <!-- ADD id to memory -->
                        <div class="stat-value" id="{{ service_id }}-memory">{{ service_info.memory }}</div>
                        <div class="stat-label">Memory</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
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
                    <div class="log-content" id="{{ service_id }}-log">{{ log_content }}</div>
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
        
        total_folders = len(folders)
        cut_folders = len([f for f in folders if f.startswith('cut_')])
        
        return total_folders, cut_folders
    except:
        return 0, 0

def get_disk_usage():
    """Get disk usage percentage for the workspace"""
    try:
        usage = psutil.disk_usage('/home/kirwinr/Desktop/stdatalog')
        return int(usage.percent)
    except:
        return 0

def get_recent_logs():
    """Get recent log entries from both services separately"""
    service_logs = {}
    for service_id, config in SERVICES.items():
        log_file = config['log_file']
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Get last 25 lines from each service
                    recent = lines[-25:] if len(lines) > 25 else lines
                    service_logs[service_id] = ''.join(recent) if recent else "No recent logs available"
            except:
                service_logs[service_id] = "Error reading log file"
        else:
            service_logs[service_id] = "Log file not found"
    
    return service_logs

@app.route("/")
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
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template_string(HTML_TEMPLATE, 
                                services=services,
                                acq_folders=acq_folders,
                                cut_folders=cut_folders,
                                disk_usage=disk_usage,
                                recent_logs=recent_logs,
                                timestamp=timestamp)

@app.route("/control/<service_id>", methods=["POST"])
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

    return jsonify({
        'services': services,
        'system': {
            'acquisition_folders': acq_folders,
            'cut_folders': cut_folders,
            'disk_usage': get_disk_usage(),
            'timestamp': datetime.now().isoformat(),
            'logs': logs
        }
    })

if __name__ == "__main__":
    # Create log directory if it doesn't exist
    os.makedirs('/home/kirwinr/logs', exist_ok=True)
    
    print("🌐 STDatalog Service Monitor starting...")
    print("📊 Dashboard available at: http://localhost:8080")
    print("🔌 API endpoint available at: http://localhost:8080/api/status")
    
    app.run(host="0.0.0.0", port=8080, debug=False)
