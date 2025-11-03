from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

def left_shift_1bit(data: bytes) -> bytes:
    """Shift a byte string left by one bit."""
    shifted = int.from_bytes(data, 'big') << 1
    shifted &= (1 << (len(data) * 8)) - 1
    return shifted.to_bytes(len(data), 'big')

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def generate_cmac_subkeys(key: bytes, block_size_bits: int):
    """Generate CMAC subkeys K1, K2 for AES (128-bit) or DES (64-bit)."""
    if block_size_bits == 128:
        cipher = AES.new(key, AES.MODE_ECB)
        Rb = 0x87
    elif block_size_bits == 64:
        cipher = DES.new(key, DES.MODE_ECB)
        Rb = 0x1B
    else:
        raise ValueError("Unsupported block size; use 64 or 128 bits")

    block_size_bytes = block_size_bits // 8
    zero_block = bytes(block_size_bytes)
    L = cipher.encrypt(zero_block)
    if (L[0] & 0x80) == 0:
        K1 = left_shift_1bit(L)
    else:
        K1 = xor_bytes(left_shift_1bit(L),
                       (Rb).to_bytes(block_size_bytes, 'big'))
    if (K1[0] & 0x80) == 0:
        K2 = left_shift_1bit(K1)
    else:
        K2 = xor_bytes(left_shift_1bit(K1),
                       (Rb).to_bytes(block_size_bytes, 'big'))

    return K1, K2
if __name__ == "__main__":
    print("CMAC Subkey Generation Demo\n")
    key_aes = get_random_bytes(16)
    K1_aes, K2_aes = generate_cmac_subkeys(key_aes, 128)
    print("AES-128 CMAC Subkeys:")
    print("K1 =", K1_aes.hex())
    print("K2 =", K2_aes.hex())
    key_des = get_random_bytes(8)
    K1_des, K2_des = generate_cmac_subkeys(key_des, 64)
    print("\nDES-64 CMAC Subkeys:")
    print("K1 =", K1_des.hex())
    print("K2 =", K2_des.hex())
