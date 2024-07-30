from web3 import Web3
import json
import time
import winsound
import datetime

# Mantle RPC URL (replace with an actual Mantle RPC endpoint)
mantle_rpc_url = "https://rpc.mantle.xyz"

# The pool address
pool_address = "0x4b4a22d4848eb7413ca6630d502a0d73c5b48445"

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(mantle_rpc_url))

# Convert the address to checksum format
checksum_address = Web3.to_checksum_address(pool_address)

# ABI for the slot0 function
abi = json.loads('''
[
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {
                "internalType": "uint160",
                "name": "sqrtPriceX96",
                "type": "uint160"
            },
            {
                "internalType": "int24",
                "name": "tick",
                "type": "int24"
            },
            {
                "internalType": "uint16",
                "name": "observationIndex",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "observationCardinality",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "observationCardinalityNext",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "feeProtocol",
                "type": "uint8"
            },
            {
                "internalType": "bool",
                "name": "unlocked",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

# Create contract instance
contract = w3.eth.contract(address=checksum_address, abi=abi)

def play_sound():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

def get_tick():
    slot0_data = contract.functions.slot0().call()
    return slot0_data[1]  # The tick is the second element in the returned tuple

def monitor_tick():
    print(f"Starting to monitor tick for pool: {pool_address}")
    play_sound()  # Play sound at the start
    previous_tick = None
    
    while True:
        try:
            current_tick = get_tick()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if previous_tick is None:
                print(f"{current_time} - Initial tick: {current_tick}")
            elif current_tick != previous_tick:
                print(f"{current_time} - Tick changed from {previous_tick} to {current_tick}")
                if current_tick > 100000:
                    play_sound()  # Play sound when tick changes and is above 85000
            
            previous_tick = current_tick
            time.sleep(6)  # Wait for 30 seconds before the next check
        
        except Exception as e:
            print(f"{current_time} - An error occurred: {e}")
            time.sleep(30)  # If there's an error, wait 30 seconds before retrying

if __name__ == "__main__":
    monitor_tick()