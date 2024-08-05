from web3 import Web3
import json

# Connect to Mantle network
w3 = Web3(Web3.HTTPProvider('https://rpc.mantle.xyz'))  # Replace with the correct RPC URL if different

# Contract address
contract_address = Web3.to_checksum_address('0xf79c37b8344c58467ec88c01b82c2fd8fccdbbd0')

# ABI (you'll need to get the correct ABI for this contract)
abi = json.loads('''[
    {
        "inputs": [
            {"name": "key", "type": "bytes32"}
        ],
        "name": "positions",
        "outputs": [
            {"name": "liquidity", "type": "uint128"},
            {"name": "feeGrowthInside0LastX128", "type": "uint256"},
            {"name": "feeGrowthInside1LastX128", "type": "uint256"},
            {"name": "tokensOwed0", "type": "uint128"},
            {"name": "tokensOwed1", "type": "uint128"},
            {"name": "attachedVeNFTId", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]''')

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Parameters for positionHash
owner = Web3.to_checksum_address('0xAAA78E8C4241990B4ce159E105dA08129345946A')  # Your address
index = 26273
tick_lower = 194970
tick_upper = 197240

# Generate the position hash (key)
position_key = w3.solidity_keccak(
    ['address', 'uint256', 'int24', 'int24'],
    [owner, index, tick_lower, tick_upper]
)

# Call the positions function
try:
    result = contract.functions.positions(position_key).call()
    print(f"Liquidity: {result[0]}")
    print(f"Fee growth of token0: {result[1]}")
    print(f"Fee growth of token1: {result[2]}")
    print(f"Token0 owed: {result[3]}")
    print(f"Token1 owed: {result[4]}")
    print(f"Attached veNFT tokenId: {result[5]}")
except Exception as e:
    print(f"Error: {e}")