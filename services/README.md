# STDatalog Services Setup

This directory contains systemd service files and management tools for running your STDatalog CLI and BLE components as Linux services with web monitoring.

## 🎯 What This Provides

- **🔄 STDatalog CLI Service**: Manual restart only (perfect for post-hardware-reset workflow)
- **🔄 STDatalog BLE Service**: Auto-restart on failure  
- **📀 USB Data Offload Service**: Automatic transfer of acquisition data to USB drives
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
   ./stdatalog-services start usb
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

### USB Data Offload (`stdatalog-usboffload`)
- **Purpose**: Automatically transfers acquisition data to any inserted USB drive
- **Restart Policy**: Auto-restart on failure (`Restart=always`)
- **Use Case**: Runs continuously, monitors for USB drives and transfers cut folders
- **Features**: Detects any USB drive, maintains transfer history, keeps minimum folders
- **Log Location**: `/home/kirwinr/logs/stdatalog-usboffload.log`

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
./stdatalog-services start usb

# Control all services at once
./stdatalog-services start all
./stdatalog-services stop all

# View logs
./stdatalog-services logs cli
./stdatalog-services tail ble    # Follow logs in real-time
./stdatalog-services logs usb

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
sudo systemctl start stdatalog-usboffload

# View logs
journalctl -u stdatalog-cli -f
tail -f /home/kirwinr/logs/stdatalog-ble.log
tail -f /home/kirwinr/logs/stdatalog-usboffload.log

# Enable/disable services
sudo systemctl enable stdatalog-ble
sudo systemctl disable stdatalog-cli
sudo systemctl enable stdatalog-usboffload
```

## 🌐 Web Dashboard Features

The web dashboard provides:

- **🟢🔴 Visual Status Indicators**: Green/red LEDs for each service
- **📊 System Statistics**: Memory usage, uptime, disk usage
- **📁 Acquisition Monitoring**: Count of acquisition folders (inside cut_* folders) and cut folders
- **📀 USB Status**: Real-time USB drive detection and space information
- **🔄 Service Control**: Start/stop/restart buttons for all services
- **📋 Live Logs**: Recent log entries from CLI and BLE services (USB logs excluded)
- **🔄 Auto-refresh**: Updates every 1 second for real-time monitoring

## 📁 File Structure

```
services/
├── stdatalog-cli.service      # CLI service definition
├── stdatalog-ble.service      # BLE service definition  
├── stdatalog-monitor.service  # Web dashboard service
├── stdatalog-usboffload.service # USB data transfer service
├── service_monitor.py         # Web dashboard application
├── setup_services.sh          # Installation script
├── stdatalog-services         # Management script
└── README.md                  # This file
```

## 🔧 Typical Workflow

1. **Initial Setup**: Run `./setup_services.sh` once
2. **Normal Operation**: 
   - BLE service runs automatically
   - USB offload service runs automatically (transfers data when USB inserted)
   - Web dashboard always available
   - Start CLI manually when needed
3. **USB Data Transfer**:
   - Insert any USB drive
   - Service automatically detects and transfers oldest cut folders
   - Maintains transfer history to avoid duplicates
   - Always keeps minimum number of folders on local storage
4. **After Hardware Reset**:
   - Reset your STWIN board
   - Go to web dashboard or run `./stdatalog-services start cli`
   - CLI will connect and resume operation
5. **Monitoring**: Check web dashboard or `./stdatalog-services status`

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

### USB offload not working:
```bash
# Check USB service status
./stdatalog-services status

# Check if USB is detected
ls /media/$USER/

# Check USB service logs
./stdatalog-services logs usb

# Restart USB service
./stdatalog-services restart usb
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
