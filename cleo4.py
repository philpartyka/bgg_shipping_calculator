from web3 import Web3

# Connect to Mantle network
w3 = Web3(Web3.HTTPProvider('https://rpc.mantle.xyz'))

# Contract address (converted to checksum)
contract_address = Web3.to_checksum_address('0x4b4a22d4848eb7413ca6630d502a0d73c5b48445')

# ABI (Add the necessary functions from the contract ABI)
abi = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Given values
liquidity = 141716927253310204138559
tick_lower = 79014
tick_upper = 79284

# Get current sqrt price and tick
slot0 = contract.functions.slot0().call()
sqrt_price_x96 = slot0[0]
current_tick = slot0[1]

print(f"Current tick: {current_tick}")
print(f"Current sqrt price: {sqrt_price_x96}")

def get_sqrt_ratio_at_tick(tick):
    # Implementation from TickMath.sol
    abs_tick = abs(tick)
    ratio = 0x100000000000000000000000000000000
    if abs_tick & 0x1 != 0: ratio = (ratio * 0xfffcb933bd6fad37aa2d162d1a594001) >> 128
    if abs_tick & 0x2 != 0: ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128
    if abs_tick & 0x4 != 0: ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128
    if abs_tick & 0x8 != 0: ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128
    if abs_tick & 0x10 != 0: ratio = (ratio * 0xffcb9843d60f6159c9db58835c926644) >> 128
    if abs_tick & 0x20 != 0: ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128
    if abs_tick & 0x40 != 0: ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128
    if abs_tick & 0x80 != 0: ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128
    if abs_tick & 0x100 != 0: ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128
    if abs_tick & 0x200 != 0: ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128
    if abs_tick & 0x400 != 0: ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128
    if abs_tick & 0x800 != 0: ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128
    if abs_tick & 0x1000 != 0: ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128
    if abs_tick & 0x2000 != 0: ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128
    if abs_tick & 0x4000 != 0: ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128
    if abs_tick & 0x8000 != 0: ratio = (ratio * 0x31be135f97d08fd981231505542fcfa6) >> 128
    if abs_tick & 0x10000 != 0: ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128
    if abs_tick & 0x20000 != 0: ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128
    if abs_tick & 0x40000 != 0: ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128
    if abs_tick & 0x80000 != 0: ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128
    if tick > 0: ratio = (2**256 - 1) // ratio
    return int(((ratio >> 32) + 1) // 2)

# Implementing relevant functions from SqrtPriceMath.sol and LiquidityAmounts.sol
def get_amount0_delta(sqrt_ratio_a, sqrt_ratio_b, liquidity, round_up):
    if sqrt_ratio_a > sqrt_ratio_b:
        sqrt_ratio_a, sqrt_ratio_b = sqrt_ratio_b, sqrt_ratio_a
    numerator1 = liquidity << 96
    numerator2 = sqrt_ratio_b - sqrt_ratio_a
    if round_up:
        return -((numerator1 * numerator2 + (sqrt_ratio_b << 96) - 1) // (sqrt_ratio_b << 96))
    else:
        return -(numerator1 * numerator2 // (sqrt_ratio_b << 96))

def get_amount1_delta(sqrt_ratio_a, sqrt_ratio_b, liquidity, round_up):
    if sqrt_ratio_a > sqrt_ratio_b:
        sqrt_ratio_a, sqrt_ratio_b = sqrt_ratio_b, sqrt_ratio_a
    if round_up:
        return (liquidity * (sqrt_ratio_b - sqrt_ratio_a) + (1 << 96) - 1) // (1 << 96)
    else:
        return liquidity * (sqrt_ratio_b - sqrt_ratio_a) // (1 << 96)

# Calculate sqrt ratios
sqrt_ratio_current = int(sqrt_price_x96)
sqrt_ratio_lower = get_sqrt_ratio_at_tick(tick_lower)
sqrt_ratio_upper = get_sqrt_ratio_at_tick(tick_upper)

print(f"sqrt_ratio_current: {sqrt_ratio_current}")
print(f"sqrt_ratio_lower: {sqrt_ratio_lower}")
print(f"sqrt_ratio_upper: {sqrt_ratio_upper}")

# Calculate amounts
if current_tick < tick_lower:
    amount0 = get_amount0_delta(sqrt_ratio_lower, sqrt_ratio_upper, liquidity, False)
    amount1 = 0
elif current_tick < tick_upper:
    amount0 = get_amount0_delta(sqrt_ratio_current, sqrt_ratio_upper, liquidity, False)
    amount1 = get_amount1_delta(sqrt_ratio_lower, sqrt_ratio_current, liquidity, False)
else:
    amount0 = 0
    amount1 = get_amount1_delta(sqrt_ratio_lower, sqrt_ratio_upper, liquidity, False)

print(f"Calculated amount0: {amount0}")
print(f"Calculated amount1: {amount1}")

# Expected values
expected_amount0 = 29052677209174533
expected_amount1 = 99999999999999997547409

print(f"Difference in amount0: {amount0 - expected_amount0}")
print(f"Difference in amount1: {amount1 - expected_amount1}")