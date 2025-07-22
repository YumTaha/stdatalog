# STDatalog Services Setup

This directory contains systemd service files and management tools for running your STDatalog CLI and BLE components as Linux services with web monitoring.

## 🎯 What This Provides

- **🔄 STDatalog CLI Service**: Manual restart only (perfect for post-hardware-reset workflow)
- **🔄 STDatalog BLE Service**: Auto-restart on failure  
- **🌐 Web Dashboard**: Real-time monitoring and control at http://localhost:8080
- **📊 Service Management**: Easy command-line tools for control

## 🚀 Quick Setup

1. **Install the services:**
   ```bash
   cd /home/kirwinr/Desktop/stdatalog/services
   ./setup_services.sh
   ```

2. **Access the web dashboard:**
   ```
   http://localhost:8080
   ```

3. **Use the management script:**
   ```bash
   ./stdatalog-services status
   ./stdatalog-services start cli
   ./stdatalog-services restart ble
   ```

## 📋 Service Descriptions

### STDatalog CLI (`stdatalog-cli`)
- **Purpose**: Periodic sensor data acquisition with IPC socket control
- **Restart Policy**: Manual only (`Restart=no`)
- **Use Case**: Start after hardware reset, stop when board disconnected
- **Log Location**: `/home/kirwinr/logs/stdatalog-cli.log`

### STDatalog BLE (`stdatalog-ble`) 
- **Purpose**: BLE monitoring with rotational velocity thresholds
- **Restart Policy**: Auto-restart on failure (`Restart=on-failure`)
- **Use Case**: Always running, triggers CLI acquisitions
- **Log Location**: `/home/kirwinr/logs/stdatalog-ble.log`

### Service Monitor (`stdatalog-monitor`)
- **Purpose**: Web dashboard for monitoring and control
- **Restart Policy**: Always restart (`Restart=always`)
- **Use Case**: Always available for status checking
- **Log Location**: `/home/kirwinr/logs/service-monitor.log`

## 🛠 Management Commands

### Using the `stdatalog-services` script:

```bash
# Show status of all services
./stdatalog-services status

# Start/stop/restart individual services
./stdatalog-services start cli
./stdatalog-services stop ble  
./stdatalog-services restart monitor

# Control all services at once
./stdatalog-services start all
./stdatalog-services stop all

# View logs
./stdatalog-services logs cli
./stdatalog-services tail ble    # Follow logs in real-time

# Open web dashboard
./stdatalog-services dashboard
```

### Using systemctl directly:

```bash
# Service control
sudo systemctl start stdatalog-cli
sudo systemctl stop stdatalog-cli
sudo systemctl restart stdatalog-ble
sudo systemctl status stdatalog-monitor

# View logs
journalctl -u stdatalog-cli -f
tail -f /home/kirwinr/logs/stdatalog-ble.log

# Enable/disable services
sudo systemctl enable stdatalog-ble
sudo systemctl disable stdatalog-cli
```

## 🌐 Web Dashboard Features

The web dashboard provides:

- **🟢🔴 Visual Status Indicators**: Green/red LEDs for each service
- **📊 System Statistics**: Memory usage, uptime, disk usage
- **📁 Acquisition Monitoring**: Count of acquisition and cut folders
- **🔄 Service Control**: Start/stop/restart buttons
- **📋 Live Logs**: Recent log entries from all services
- **🔄 Auto-refresh**: Updates every 30 seconds

## 📁 File Structure

```
services/
├── stdatalog-cli.service      # CLI service definition
├── stdatalog-ble.service      # BLE service definition  
├── stdatalog-monitor.service  # Web dashboard service
├── service_monitor.py         # Web dashboard application
├── setup_services.sh          # Installation script
├── stdatalog-services         # Management script
└── README.md                  # This file
```

## 🔧 Typical Workflow

1. **Initial Setup**: Run `./setup_services.sh` once
2. **Normal Operation**: 
   - BLE service runs automatically
   - Web dashboard always available
   - Start CLI manually when needed
3. **After Hardware Reset**:
   - Reset your STWIN board
   - Go to web dashboard or run `./stdatalog-services start cli`
   - CLI will connect and resume operation
4. **Monitoring**: Check web dashboard or `./stdatalog-services status`

## 🐛 Troubleshooting

### Service won't start:
```bash
# Check detailed status
systemctl status stdatalog-cli

# Check logs
./stdatalog-services logs cli
```

### Permission issues:
```bash
# Fix log file permissions
sudo chown kirwinr:kirwinr /home/kirwinr/logs/stdatalog-*.log
sudo chmod 664 /home/kirwinr/logs/stdatalog-*.log
```

### Dashboard not accessible:
```bash
# Check if monitor service is running
./stdatalog-services status

# Restart monitor service
./stdatalog-services restart monitor
```

### BLE connection issues:
```bash
# Check Bluetooth status
systemctl status bluetooth

# Restart BLE service
./stdatalog-services restart ble
```

## 🔄 Backup & Recovery

Your original files are backed up in:
```
backup_changes/systemd_services_backup_YYYYMMDD_HHMMSS/
```

To restore original functionality:
```bash
# Stop all services
./stdatalog-services stop all

# Disable services  
sudo systemctl disable stdatalog-cli stdatalog-ble stdatalog-monitor

# Remove service files
sudo rm /etc/systemd/system/stdatalog-*.service

# Reload systemd
sudo systemctl daemon-reload
```

## 📞 Support

If you encounter issues:
1. Check service logs: `./stdatalog-services logs <service>`
2. Verify file permissions in `/home/kirwinr/logs/`
3. Ensure virtual environment is properly set up
4. Check that all Python dependencies are installed

The web dashboard provides real-time diagnostics and is your best starting point for troubleshooting.
