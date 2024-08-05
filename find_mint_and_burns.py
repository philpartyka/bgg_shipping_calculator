from web3 import Web3
import json

# Connect to a Mantle node (replace with the correct RPC endpoint)
w3 = Web3(Web3.HTTPProvider('https://rpc.mantle.xyz'))

# Contract address (converted to checksum address)
contract_address = Web3.to_checksum_address('0x4b4a22d4848eb7413ca6630d502a0d73c5b48445')

# ABI for the Mint and Burn events
abi = json.loads('''
[
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "int24",
                "name": "tickLower",
                "type": "int24"
            },
            {
                "indexed": true,
                "internalType": "int24",
                "name": "tickUpper",
                "type": "int24"
            },
            {
                "indexed": false,
                "internalType": "uint128",
                "name": "amount",
                "type": "uint128"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount0",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount1",
                "type": "uint256"
            }
        ],
        "name": "Mint",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "int24",
                "name": "tickLower",
                "type": "int24"
            },
            {
                "indexed": true,
                "internalType": "int24",
                "name": "tickUpper",
                "type": "int24"
            },
            {
                "indexed": false,
                "internalType": "uint128",
                "name": "amount",
                "type": "uint128"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount0",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount1",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    }
]
''')

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Get the latest block number
latest_block = w3.eth.block_number

# Define the block range (e.g., last 100000 blocks, adjust as needed)
from_block = max(0, latest_block - 10000)
to_block = latest_block

# Fetch Mint and Burn events
mint_filter = contract.events.Mint.create_filter(fromBlock=from_block, toBlock=to_block)
burn_filter = contract.events.Burn.create_filter(fromBlock=from_block, toBlock=to_block)

mint_events = mint_filter.get_all_entries()
burn_events = burn_filter.get_all_entries()

# Process events
positions = {}

def update_position(event, is_mint):
    args = event['args']
    position_key = (args['owner'], args['tickLower'], args['tickUpper'])
    
    if position_key not in positions:
        positions[position_key] = {
            'owner': args['owner'],
            'tickLower': args['tickLower'],
            'tickUpper': args['tickUpper'],
            'amount': 0,
            'amount0': 0,
            'amount1': 0
        }
    
    multiplier = 1 if is_mint else -1
    positions[position_key]['amount'] += multiplier * args['amount']
    positions[position_key]['amount0'] += multiplier * args['amount0']
    positions[position_key]['amount1'] += multiplier * args['amount1']

# Process Mint and Burn events
for event in mint_events:
    update_position(event, True)

for event in burn_events:
    update_position(event, False)

# Filter out closed positions
active_positions = {k: v for k, v in positions.items() if v['amount'] > 0}

# Display results
print(f"Active positions found in blocks {from_block} to {latest_block}:")
for position in active_positions.values():
    print(f"Owner: {position['owner']}")
    print(f"  Tick Range: {position['tickLower']} to {position['tickUpper']}")
    print(f"  Liquidity: {position['amount']}")
    print(f"  Token 0 Amount: {position['amount0']}")
    print(f"  Token 1 Amount: {position['amount1']}")
    print()

print(f"Total number of active positions: {len(active_positions)}")