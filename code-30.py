from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_mac_one_block(key: bytes, block: bytes) -> bytes:
    """
    CBC-MAC of a single block (IV = 0). Equivalent to AES-ECB encrypt of the block.
    """
    assert len(block) == BLOCK_SIZE
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

def cbc_mac_multi_block(key: bytes, blocks: list[bytes]) -> bytes:
    """
    CBC-MAC of multiple blocks with IV = 0.
    blocks: list of bytes objects, each of length BLOCK_SIZE
    """
    cipher = AES.new(key, AES.MODE_ECB)
    prev = bytes(BLOCK_SIZE)
    for blk in blocks:
        assert len(blk) == BLOCK_SIZE
        x = xor_bytes(blk, prev)
        prev = cipher.encrypt(x)
    return prev

def demo():
    key = get_random_bytes(BLOCK_SIZE)
    X = get_random_bytes(BLOCK_SIZE)
    T = cbc_mac_one_block(key, X)
    X_xor_T = xor_bytes(X, T)
    tag_two_block = cbc_mac_multi_block(key, [X, X_xor_T])

    print("Key:            ", key.hex())
    print("X (hex):        ", X.hex())
    print("T = MAC(K, X):  ", T.hex())
    print("X ⊕ T (hex):    ", X_xor_T.hex())
    print("MAC(K, X||X⊕T): ", tag_two_block.hex())

    print("\nForgery succeeded?" , "YES" if tag_two_block == T else "NO")

if __name__ == "__main__":
    demo()
