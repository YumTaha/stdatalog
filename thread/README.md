# Thread Folder - BLE and Data Management Scripts

This folder contains the core Python scripts that handle **Bluetooth Low Energy (BLE) sensors** and **USB data transfer**. Think of these as the "workers" that do the actual monitoring and data handling.

## 🎯 What's In This Folder

### 📡 BLE Scripts (Bluetooth Sensors)
- **`ble_service.py`** - **MAIN DUAL SENSOR SCRIPT** (feedrate + speed sensors together)
- **`ble_feed.py`** - Single feedrate sensor monitoring (older version)
- **`ble_speed.py`** - Single speed sensor monitoring (older version)

### 💾 Data Transfer Scripts
- **`usb_transfer.py`** - Automatically copies data to USB drives when plugged in

## 🔧 How It Works (Simple Explanation)

### The Main Script: `ble_service.py`
This is the **most important** script. It connects to **two BLE sensors**:

1. **Feedrate Sensor** (`DE:6D:5D:2A:BD:58`) - Measures how fast something moves down (in inches per minute)
2. **Speed Sensor** (`F9:51:AC:0F:75:9E`) - Measures rotational speed (in radians per second)

**The Logic:**
- When **BOTH** sensors are active → Machine is **CUTTING** → Sends "start" command
- When **ONLY speed** sensor is active → Machine is **RESETTING** → Sends "stop" command  
- When **NEITHER** sensor is active → Machine is **STOPPED** → Sends "stop" command

**Communication:**
- Talks to the main data logging system through a **socket connection** on port `8888`
- Sends simple commands: `start` or `stop`

### USB Transfer Script: `usb_transfer.py`
- **Watches** for USB drives being plugged in
- **Automatically copies** data from `acquisition_data/` folder to the USB
- **Zips up** the data to save space
- **Keeps track** of what's already been copied (won't copy duplicates)

## 🚦 Status Indicators

### BLE Connection States
- **"Connected to [Sensor] BLE"** = Good! Sensor is working
- **"[Sensor] BLE disconnected"** = Sensor lost connection, will try to reconnect
- **"Starting 1-minute timer before sending stop command"** = Speed sensor disconnected, waiting to see if it reconnects
- **"Speed sensor reconnected - cancelled disconnect timer"** = Speed sensor came back online during the 1-minute grace period
- **"1 minute passed since speed disconnect - sending 'stop' command"** = Speed sensor was offline too long, stopping data collection
- **"Criteria met: Sending 'start'"** = Both sensors active, telling system to record data
- **"Criteria NOT met: Sending 'stop'"** = Sensors not meeting cutting criteria

### Machine States (from ble_service.py)
- **"CUTTING (blade running, moving down)"** = Recording data ✅
- **"BLADE RESETTING (blade running, moving up)"** = Not recording 🔄
- **"BLADE STOPPED (no spinning)"** = Machine idle ⏹️

## 🔧 Configuration (Important Numbers)

### In `ble_service.py`:
```python
DOWN_THRESHOLD_IN_MIN = -15    # Feedrate must be less than -15 in/min (moving down)
START_THRESHOLD_SP = 0.5       # Speed must be at least 0.5 rad/s (spinning)
SOCKET_PORT = 8888             # How it talks to the main system

# Advanced Features:
# - Speed sensor disconnect grace period: 60 seconds
# - Disconnect logging: acquisition_data/speed_sensor_disconnections.txt
# - Auto-reconnection: Both sensors try to reconnect forever
```

### In `usb_transfer.py`:
```python
POLL_INTERVAL = 4              # Check for USB every 4 seconds
MIN_CUT_FOLDERS = 1            # Always keep at least 1 folder on the computer
```

## 🏃‍♂️ How to Run

### Run the main BLE service:
```bash
cd /home/kirwinr/Desktop/stdatalog/thread
python3 ble_service.py --log INFO
```

### Run USB transfer monitoring:
```bash
cd /home/kirwinr/Desktop/stdatalog/thread  
python3 usb_transfer.py
```

### For debugging (see all the detailed messages):
```bash
python3 ble_service.py --log DEBUG
```

## 🛠️ Troubleshooting

### "Connection timed out" or "device not found"
- Check if BLE sensors are **powered on** and **nearby**
- Make sure the **MAC addresses** in the script match your actual sensors
- Try scanning for devices: `bluetoothctl scan on`

### "CLI logger not available"
- The main STDatalog system isn't running
- Start it first, then run this BLE script

### USB transfer not working
- Check if USB is properly mounted under `/media/[username]/`
- Make sure there's enough **free space** on the USB drive
- Check the console output for error messages

### Speed sensor frequent disconnections
- **Check the disconnect log**: `cat ../acquisition_data/speed_sensor_disconnections.txt`
- Look for patterns in disconnect times
- Verify sensor battery/power and BLE range
- **System waits 1 minute** before stopping recording, so brief disconnects won't interrupt data collection

## 🆕 Recent Features Added

### Smart Speed Sensor Disconnect Handling
- **1-Minute Grace Period**: When speed sensor disconnects, system waits 60 seconds before sending stop command
- **Automatic Logging**: All disconnections logged with timestamps to `acquisition_data/speed_sensor_disconnections.txt`
- **Smart Recovery**: If sensor reconnects during the 1-minute window, stop command is cancelled
- **Maintenance Aid**: Disconnect log helps identify sensor reliability issues

**Example disconnect log:**
```
2025-07-29 09:33:16 - Speed sensor disconnected
2025-07-29 09:33:56 - Speed sensor disconnected
2025-07-29 09:35:34 - Speed sensor disconnected
```

## 📝 For Future You/New Person

1. **Most important file**: `ble_service.py` - this does the main work
2. **The thresholds** (like -15 in/min) might need adjustment for different machines
3. **MAC addresses** will be different if you change sensors
4. **Socket port 8888** must match what the main STDatalog system expects
5. The **acquisition_data folder** path must match between all scripts
6. **Disconnect logging** helps with sensor maintenance and troubleshooting

**Questions to ask when debugging:**
- Are both sensors connected and sending data?
- Is the main STDatalog CLI running and listening on port 8888?
- Do the threshold values make sense for your machine?
- Are the sensor MAC addresses correct?

Good luck! 🚀
