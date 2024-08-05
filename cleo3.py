from web3 import Web3

def get_tick_bitmap():
    # Connect to the Mantle network
    w3 = Web3(Web3.HTTPProvider('https://rpc.mantle.xyz'))

    # Ensure we're connected
    if not w3.is_connected():
        print("Not connected to Mantle network")
        return

    # The pool contract address (converted to checksum format)
    pool_address = Web3.to_checksum_address('0x4b4a22d4848eb7413ca6630d502a0d73c5b48445')

    # The ABI for the tickBitmap function
    abi = [
        {
            "inputs": [{"internalType": "int16", "name": "wordPosition", "type": "int16"}],
            "name": "tickBitmap",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    # Create a contract instance
    contract = w3.eth.contract(address=pool_address, abi=abi)

    # Calculate the word position for tick 79269
    word_position = 78160 // 256

    try:
        # Call the tickBitmap function
        bitmap = contract.functions.tickBitmap(word_position).call()
        print(f"Bitmap for word position {word_position} (tick ~79269): {bitmap}")
        return bitmap
    except Exception as e:
        print(f"Error calling tickBitmap: {e}")

if __name__ == "__main__":
    get_tick_bitmap()