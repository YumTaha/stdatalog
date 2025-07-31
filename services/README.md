# Services Folder - Auto-Running Background Programs

This folder contains everything needed to make your STDatalog system run **automatically in the background** like a professional service. Think of these as "background workers" that start when your computer boots up and keep running even if you're not logged in.

## 🎯 What This Does (Simple Explanation)

Instead of manually starting Python scripts every time, this sets up **Linux services** that:

- **🔄 STDatalog CLI Service**: The main data recorder (only starts when you tell it to)
- **🔄 STDatalog BLE Service**: Watches the BLE sensors and tells CLI when to start/stop
- **📀 USB Transfer Service**: Automatically copies data to any USB drive you plug in
- **🌐 Web Dashboard**: A website you can open to see what's happening (http://localhost:8080)
- **📊 Easy Controls**: Simple commands to start/stop everything

## 🚀 Quick Setup (First Time Only)

**Prerequisites:** Make sure you've run the global setup first:
```bash
# From the main stdatalog directory:
./global_setup.sh
source .venv/bin/activate  # Always activate the virtual environment
```

**Step 1:** Install the services (makes them start automatically)
```bash
cd /home/kirwinr/Desktop/stdatalog/services
./setup_services.sh
```

**Step 2:** Open the web dashboard in your browser
```
http://localhost:8080
```

**Step 3:** Use simple commands to control everything
```bash
# Remember: Always activate virtual environment first!
source ../.venv/bin/activate

./stdatalog-services status        # See what's running
./stdatalog-services start cli     # Start the data recorder  
./stdatalog-services start ble     # Start the sensor monitor
./stdatalog-services start usb     # Start USB auto-transfer
./stdatalog-services restart ble   # Restart if something's stuck
./stdatalog-services stop all      # Stop everything
```

## 📋 What Each Service Does (Detailed)

### STDatalog CLI (`stdatalog-cli`) - The Main Data Recorder
- **What it does**: Records sensor data from your STDatalog hardware to files
- **When to use**: Start this AFTER you've reset/connected your hardware
- **Auto-restart**: NO - you control when it starts/stops
- **Log file**: `/home/kirwinr/logs/stdatalog-cli.log` (check here if something's wrong)
- **Think of it as**: The actual "recording button" for your data

### STDatalog BLE (`stdatalog-ble`) - The Smart Trigger
- **What it does**: Watches your BLE sensors and automatically tells CLI when to record
- **When to use**: Keep this running all the time
- **Auto-restart**: YES - if it crashes, it starts itself again
- **Log file**: `/home/kirwinr/logs/stdatalog-ble.log`
- **Think of it as**: The "smart switch" that knows when your machine is cutting

### USB Transfer (`stdatalog-usboffload`) - The Auto-Backup
- **What it does**: Copies your data to any USB drive you plug in
- **When to use**: Keep this running all the time  
- **Auto-restart**: YES - always stays running
- **Log file**: `/home/kirwinr/logs/stdatalog-usb.log`
- **Think of it as**: Automatic backup whenever you insert a USB stick

### Service Monitor (`stdatalog-monitor`) - The Web Dashboard
- **What it does**: Creates a website where you can see everything that's happening
- **When to use**: Keep this running to use the web dashboard
- **Auto-restart**: YES - always stays running
- **Website**: http://localhost:8080
- **Think of it as**: Your "control panel" in a web browser

## 🛠 How to Control Everything (Management Commands)

### The Easy Way - Use the `stdatalog-services` script:

```bash
# See what's running and what's not
./stdatalog-services status

# Start/stop individual things  
./stdatalog-services start cli      # Start the data recorder
./stdatalog-services start ble      # Start the sensor monitor
./stdatalog-services start usb      # Start USB auto-backup
./stdatalog-services stop ble       # Stop the sensor monitor
./stdatalog-services restart ble    # Restart if it's stuck

# Control everything at once
./stdatalog-services start all      # Start everything
./stdatalog-services stop all       # Stop everything

# Check what went wrong (read the logs)
./stdatalog-services logs cli       # See CLI messages
./stdatalog-services tail ble       # Watch BLE messages in real-time
./stdatalog-services logs usb       # See USB transfer messages

# Open the web dashboard
./stdatalog-services dashboard      # Opens http://localhost:8080
```

## 🌐 Web Dashboard (Super Helpful!)

Open http://localhost:8080 in your web browser to see:
- ✅ Which services are running (green = good, red = problem)
- 📊 Real-time status of your data collection
- 🔘 Buttons to start/stop services without using the terminal
- 📋 Recent log messages (see what's happening)
- 📈 System information (disk space, etc.)

## 🔧 Typical Workflow (How You'll Actually Use This)

### Daily Use:
1. **Turn on your computer** → Services start automatically
2. **Check the web dashboard** → http://localhost:8080  
3. **Connect your STDatalog hardware** → Nothing happens yet (good!)
4. **Start the CLI service** → `./stdatalog-services start cli`
5. **The BLE service watches sensors** → When your machine cuts, data recording starts automatically
6. **Plug in USB stick** → Data gets copied automatically
7. **When done** → `./stdatalog-services stop cli` (BLE and USB keep running)

### If Something Goes Wrong:
1. **Check the web dashboard** → See which service has a problem
2. **Look at the logs** → `./stdatalog-services logs [service-name]`
3. **Restart the problematic service** → `./stdatalog-services restart [service-name]`
4. **If still broken** → `./stdatalog-services stop all` then `./stdatalog-services start all`

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

## � Troubleshooting (When Things Go Wrong)

### "Service won't start" or shows as "failed":
```bash
# Get detailed info about what went wrong
systemctl status stdatalog-cli
./stdatalog-services logs cli
```

### "Permission denied" errors:
```bash
# Fix file permissions
sudo chown kirwinr:kirwinr /home/kirwinr/logs/stdatalog-*.log
sudo chmod 664 /home/kirwinr/logs/stdatalog-*.log
```

### "Can't access web dashboard" (http://localhost:8080 doesn't work):
```bash
# Check if the monitor service is running
./stdatalog-services status
# If it's not running, start it
./stdatalog-services restart monitor
```

### "BLE sensors not connecting":
```bash
# Check if Bluetooth is working on your computer
systemctl status bluetooth
# Restart the BLE service
./stdatalog-services restart ble
```

### "USB stick not being detected":
```bash
# Check if your USB is mounted properly
ls /media/$USER/
# Look for error messages
./stdatalog-services logs usb
# Restart the USB service
./stdatalog-services restart usb
```

## 🗂️ Important Files You Should Know About

```
services/
├── stdatalog-cli.service      # Tells Linux how to run the data recorder
├── stdatalog-ble.service      # Tells Linux how to run the sensor monitor
├── stdatalog-monitor.service  # Tells Linux how to run the web dashboard
├── stdatalog-usboffload.service # Tells Linux how to run USB auto-backup
├── service_monitor.py         # The code for the web dashboard
├── setup_services.sh          # Script that installs everything (run once)
├── stdatalog-services         # The main control script (use this often!)
└── README.md                  # This helpful guide
```

## � Backup & Recovery

Don't worry! When you run the setup, your original files are safely backed up here:
```
backup_changes/systemd_services_backup_YYYYMMDD_HHMMSS/
```

If something breaks, you can always go back to how things were before.

## 📝 For Future You/New Person Taking Over

**Key Things to Remember:**
1. **Web dashboard is your friend** → http://localhost:8080 shows you everything
2. **The `./stdatalog-services` script** does most of what you need
3. **BLE and USB services** should always be running (they auto-restart)
4. **CLI service** you start manually when you want to record data
5. **Log files** in `/home/kirwinr/logs/` tell you what went wrong

**Common Questions:**
- **"Nothing is working!"** → Check the web dashboard first, then restart everything
- **"Data isn't recording!"** → Make sure CLI service is started AND BLE sensors are connected
- **"USB backup not working!"** → Check if USB is properly mounted and has enough space
- **"I changed something and broke it!"** → Use the backup files to restore original settings

**This folder makes your system "professional"** - everything runs automatically in the background like a real product, not just manual Python scripts. Pretty cool! 🚀

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

## Support

If you encounter issues:
1. Check service logs: `./stdatalog-services logs <service>`
2. Verify file permissions in `/home/kirwinr/logs/`
3. Ensure virtual environment is properly set up
4. Check that all Python dependencies are installed

The web dashboard provides real-time diagnostics and is your best starting point for troubleshooting.
