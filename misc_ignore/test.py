import asyncio
import struct
import csv
from datetime import datetime
from bleak import BleakClient

DEVICE_MAC_ADDRESS = "DE:6D:5D:2A:BD:58"
VELOCITY_CHAR_UUID = "2772836b-8bb0-4d0f-a52c-254b5d1fa438"

recording = False
current_state = None  # "Going down" or "Going up"
csv_file = None
csv_writer = None
should_exit = False

def parse_float32_le(b):
    return struct.unpack('<f', b)[0]

async def user_input_loop():
    global recording, current_state, should_exit
    print("Type D (Enter) for 'Going down', U (Enter) for 'Going up', E (Enter) to exit.")
    while not should_exit:
        user_input = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        user_input = user_input.strip().upper()
        if user_input == "D":
            print("[INFO] Recording started (state: Going down)")
            recording = True
            current_state = "Going down"
        elif user_input == "U":
            if recording:
                print("[INFO] State changed: Going up")
                current_state = "Going up"
            else:
                print("[INFO] Start recording first with D.")
        elif user_input == "E":
            print("[INFO] Exiting and saving CSV.")
            should_exit = True
        else:
            print("[INFO] Unknown input. Use D (down), U (up), or E (exit).")

async def main():
    global csv_file, csv_writer, recording, current_state, should_exit

    # Prepare CSV
    csv_file = open("feedrate_log.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["timestamp", "velocity_in_min", "state"])

    print("Connecting to Feedrate BLE device...")
    async with BleakClient(DEVICE_MAC_ADDRESS) as client:
        if not client.is_connected:
            print("Could not connect!")
            csv_file.close()
            return
        print("Connected! Listening for velocity notifications...")
        print("Type D (Enter) for 'Going down', U (Enter) for 'Going up', E (Enter) to exit.")

        def notification_handler(sender, data):
            global recording, current_state, csv_writer
            raw_v = parse_float32_le(data)
            v_in_min = round(raw_v * 39.3701 * 60, 3)
            timestamp = datetime.now().isoformat(timespec='seconds')
            state_str = current_state if recording else ""
            print(f"{timestamp} | {v_in_min} in/min {state_str}")
            if recording and state_str:
                csv_writer.writerow([timestamp, v_in_min, state_str])
                csv_file.flush()

        await client.start_notify(VELOCITY_CHAR_UUID, notification_handler)

        # Start user input loop in parallel
        await asyncio.gather(
            user_input_loop(),
            # BLE notifications run as long as main runs
            *(asyncio.sleep(0.1) for _ in range(1000000))  # just to keep main alive; notifications handled by Bleak
        )

    csv_file.close()
    print("CSV file saved. Exiting.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"Error: {e}")
