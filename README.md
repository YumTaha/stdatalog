# STDatalog - Industrial Data Collection System

Welcome to STDatalog! This is a **smart data collection system** that automatically records sensor data from industrial machines (like cutting tools) using STMicroelectronics hardware and wireless sensors.

## 🎯 What This Project Does (In Simple Terms)

Imagine you have a machine (like a cutting tool) and you want to **automatically record data** only when it's actually working. This system:

1. **👀 Watches** wireless sensors (Bluetooth) to know when your machine is working
2. **🔄 Automatically starts/stops** data recording based on machine activity  
3. **💾 Saves** all the data to organized folders
4. **📀 Backs up** data to USB drives when you plug them in
5. **🌐 Shows** you everything happening through a web dashboard

**The Cool Part:** It's smart! It knows the difference between when your machine is:
- 🟢 **Actually cutting** (records data)
- 🟡 **Just running but not cutting** (doesn't record)
- 🔴 **Completely stopped** (doesn't record)

## 🗂️ Project Structure

```
stdatalog/
├── 📁 services/          ← Makes everything run automatically (Linux services)
├── 📁 thread/            ← Core scripts (BLE sensors, USB transfer)
├── 📁 stdatalog_core/    ← Main STDatalog software 
├── 📁 stdatalog_gui/     ← Graphical interface
├── 📁 stdatalog_pnpl/    ← PnP Like configuration library
├── 📁 stdatalog_dtk/     ← Data Toolkit for processing
├── 📁 stdatalog_examples/ ← Example code and tutorials
├── 📁 acquisition_data/  ← Where your recorded data gets saved
├── 📁 linux_setup/      ← USB permission setup for Linux
├── 📁 .venv/            ← Python virtual environment (created by global_setup.sh)
├── 📄 global_setup.sh   ← One-command installation script
└── 📄 README.md          ← This file
```

## 🚀 Quick Start Guide

### One-Command Installation (New Users):

**For STWINBX1 on Linux - Complete Setup:**
```bash
# Clone this repository first:
git clone https://github.com/YumTaha/stdatalog.git
cd stdatalog

# Run the global setup (installs everything automatically):
./global_setup.sh
```

**What the global setup does:**
- ✅ Checks system requirements (Python 3.10+)
- ✅ Installs system dependencies (audio, GUI, USB drivers)
- ✅ Creates Python virtual environment
- ✅ Installs all STDATALOG-PYSDK packages
- ✅ Configures USB drivers for STWINBX1
- ✅ Tests the installation

**After global setup:**
```bash
# Reboot is recommended for USB drivers to work properly
sudo reboot
```

**Global setup options:**
```bash
./global_setup.sh --help          # Show all options
./global_setup.sh --no-gui        # Install without GUI (headless systems)
./global_setup.sh --skip-usb      # Skip USB driver setup
./global_setup.sh --proxy http://proxy:8080  # Use with corporate proxy
```

### After Installation - Setup Services:

1. **Activate the virtual environment** (required):
   ```bash
   source .venv/bin/activate
   ```

2. **Set up the automatic services** (makes everything run in the background):
   ```bash
   cd services/
   ./setup_services.sh
   ```

3. **Open the web dashboard** to see what's happening:
   ```
   http://localhost:8080
   ```

4. **Connect your STDatalog hardware** (the actual sensor board)

5. **Start data collection** when ready:
   ```bash
   cd services/
   ./stdatalog-services start cli
   ```

### For Daily Use:

**Important:** Always activate the virtual environment first:
```bash
source .venv/bin/activate
```

Then use these commands:
- **Web Dashboard**: http://localhost:8080 (your control center)
- **Start recording**: `cd services && ./stdatalog-services start cli`
- **Stop recording**: `cd services && ./stdatalog-services stop cli`  
- **Check what's happening**: `cd services && ./stdatalog-services status`
- **Plug in USB**: Data automatically copies over

## 📋 How The System Works

### The Hardware:
- **STDatalog Board**: Main sensor data collector (connects via USB)
- **BLE Feedrate Sensor**: Measures how fast something moves (in/min)
- **BLE Speed Sensor**: Measures rotational speed (rad/s)

### The Software Flow:
1. **BLE Service** watches both wireless sensors
2. When **both sensors are active** → Tells CLI "start recording!"
3. When **not cutting** → Tells CLI "stop recording!"
4. **CLI Service** does the actual data recording from the STDatalog board
5. **USB Service** automatically backs up data when you plug in a USB drive
6. **Web Dashboard** shows you everything that's happening

### Smart Logic:
- **Cutting** = Speed sensor active AND feedrate sensor moving down → ✅ Record
- **Blade Reset** = Speed sensor active BUT feedrate moving up → ❌ Don't record  
- **Machine Idle** = No speed sensor activity → ❌ Don't record

### Advanced Features:
- **Smart Disconnect Handling**: If the speed sensor disconnects, the system waits 1 minute before stopping data collection (in case it's just a temporary connection issue)
- **Disconnect Logging**: All speed sensor disconnections are logged with timestamps to `acquisition_data/speed_sensor_disconnections.txt` for troubleshooting
- **Auto-Reconnection**: Both BLE sensors automatically try to reconnect forever if disconnected
- **Automated Installation**: The `global_setup.sh` script automatically installs all dependencies including:
  - System libraries (audio, USB, GUI support)
  - Python packages (numpy, matplotlib, pandas, bleak, colorlog)
  - STDATALOG-PYSDK components (core, GUI, examples, PnPL, DTK)
  - USB drivers and permissions for STWINBX1

## 🔧 Main Components

### 🗂️ For Detailed Information:

- **📁 `services/` folder** → [Read the Services README](services/README.md)
  - How to set up automatic background services
  - Web dashboard usage
  - Troubleshooting service issues

- **📁 `thread/` folder** → [Read the Thread README](thread/README.md)
  - BLE sensor monitoring scripts
  - USB transfer functionality  
  - Configuration and thresholds

### Key Scripts You'll Use:
- **`services/stdatalog-services`** - Main control script (start/stop everything)
- **`thread/ble_service.py`** - Dual BLE sensor monitoring
- **`thread/usb_transfer.py`** - Automatic USB backup

## 🌐 Web Dashboard

Open http://localhost:8080 to see:
- ✅ Which services are running (green = good, red = problem)
- 📊 Real-time machine status (cutting/idle/resetting)
- 💾 Data folder information
- 📀 USB drive detection and transfer status
- 🔘 Buttons to start/stop services
- 📋 Recent log messages

## 📁 Data Organization

Your recorded data gets saved like this:
```
acquisition_data/
├── cut_001/                    ← First cutting session
│   ├── (sensor data files)
├── cut_002/                    ← Second cutting session  
│   ├── (sensor data files)
├── cut_003/                    ← And so on...
│   ├── (sensor data files)
└── speed_sensor_disconnections.txt ← Speed sensor disconnect log (timestamps)
```

### Log Files:
- **`speed_sensor_disconnections.txt`**: Tracks when the speed sensor loses connection for maintenance/troubleshooting

## 🛠️ Common Tasks

### Daily Operation:
```bash
# FIRST: Always activate the virtual environment
source .venv/bin/activate

# See what's running
cd services/
./stdatalog-services status

# Start data collection (after connecting hardware)
./stdatalog-services start cli

# Stop data collection  
./stdatalog-services stop cli

# Restart if something's stuck
./stdatalog-services restart ble
```

### Data Management:
- **USB Backup**: Just plug in a USB drive - automatic!
- **Check Data**: Look in `acquisition_data/` folder
- **Free Up Space**: USB service keeps newest data, removes oldest

### Troubleshooting:
```bash
# Check what went wrong
./stdatalog-services logs cli
./stdatalog-services logs ble

# Nuclear option - restart everything
./stdatalog-services stop all
./stdatalog-services start all
```

## 🚨 Troubleshooting Quick Fixes

### "Nothing is working!"
1. **Check virtual environment**: `source .venv/bin/activate`
2. Check web dashboard: http://localhost:8080
3. Restart everything: `cd services && ./stdatalog-services restart all`
4. Check logs: `./stdatalog-services logs cli`

### "Command not found" or "Module not found"
1. **Make sure virtual environment is active**: `source .venv/bin/activate`
2. If still broken, reinstall: `./global_setup.sh`
3. Check Python version: `python --version` (should be 3.10+)

### "BLE sensors not connecting"
1. Make sure sensors are powered on and nearby
2. Check the MAC addresses in `thread/ble_service.py`
3. Restart BLE service: `./stdatalog-services restart ble`
4. **Check disconnect log**: Look at `acquisition_data/speed_sensor_disconnections.txt` to see if there's a pattern of sensor issues

### "Speed sensor keeps disconnecting"
1. **Check the disconnect log**: `cat acquisition_data/speed_sensor_disconnections.txt`
2. Look for patterns (same time every day? after long runs?)
3. Check sensor battery/power supply
4. Verify sensor is within BLE range (typically 10-30 feet)
5. **System is designed to handle brief disconnects** - it waits 1 minute before stopping recording

### "Data not recording"
1. Make sure CLI service is started: `./stdatalog-services start cli`
2. Check if STDatalog hardware is connected via USB
3. Verify BLE sensors are triggering: check web dashboard

### "USB backup not working"  
1. Make sure USB is properly mounted: `ls /media/$USER/`
2. Check if USB has enough free space
3. Restart USB service: `./stdatalog-services restart usb`

## 📝 For Future You/Someone Taking Over

### Most Important Things:
1. **Web dashboard** (http://localhost:8080) is your best friend
2. **Services folder** has the main control scripts
3. **Thread folder** has the core BLE and USB logic
4. **Configuration** is mostly in the Python files (MAC addresses, thresholds)

### Key Files to Understand:
- `services/stdatalog-services` - Your main control tool
- `thread/ble_service.py` - The brain that watches sensors
- `services/service_monitor.py` - The web dashboard code

### When You Need to Change Things:
- **Different sensors?** → Update MAC addresses in `thread/ble_service.py`
- **Different thresholds?** → Update values in `thread/ble_service.py`
- **Different machine behavior?** → Modify the logic in `ble_service.py`

### Questions to Ask When Debugging:
1. What does the web dashboard show?
2. Are the BLE sensors powered and connected?
3. Is the STDatalog hardware connected via USB?
4. What do the log files say?
5. Did someone change the sensor MAC addresses or thresholds?


---

**Need more details?** Check out the folder-specific README files:
- 📁 [Services README](services/README.md) - For setup and service management
- 📁 [Thread README](thread/README.md) - For BLE sensors and USB transfer
- [STDATALOG-PYSDK Repository](https://github.com/STMicroelectronics/stdatalog-pysdk) - For STD Communication

Good luck, and may your data collection be ever automatic! 🎯
