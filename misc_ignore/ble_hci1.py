import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_MAC_ADDRESS = "DE:6D:5D:2A:BD:58"  # Replace with your BLE device's MAC address

async def check_ble_adapter():
    # List all available Bluetooth adapters
    adapters = await BleakScanner.discover()
    print("Available Bluetooth adapters:")
    for adapter in adapters:
        print(f"Address: {adapter.address}, Name: {adapter.name}")
    
    # Attempt to connect using the TP-Link Bluetooth adapter (hci1)
    client = BleakClient(DEVICE_MAC_ADDRESS, adapter="hci1")
    
    try:
        print("Connecting to BLE device...")
        await client.connect()
        if client.is_connected:
            print(f"Connected to {DEVICE_MAC_ADDRESS} via hci1")
            print("Using TP-Link Bluetooth adapter (hci1).")
        else:
            print(f"Failed to connect to {DEVICE_MAC_ADDRESS}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()

async def main():
    await check_ble_adapter()

if __name__ == "__main__":
    asyncio.run(main())

