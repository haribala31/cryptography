from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def bit_padding(data: bytes, block_size=8):
    bits = ''.join(format(b, '08b') for b in data) + '1'
    while len(bits) % (block_size * 8) != 0:
        bits += '0'
    return int(bits, 2).to_bytes(len(bits)//8, 'big')

def des_encrypt(mode, key, data, iv=None):
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv, segment_size=8)
    else:
        raise ValueError("Mode must be ECB, CBC, or CFB")
    return cipher.encrypt(data)

def des_decrypt(mode, key, data, iv=None):
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv, segment_size=8)
    else:
        raise ValueError("Mode must be ECB, CBC, or CFB")
    return cipher.decrypt(data)

if __name__ == "__main__":
    key = get_random_bytes(8)
    iv = get_random_bytes(8)
    plaintext = b"HELLO DES MODE TEST"
    padded = bit_padding(plaintext)

    for mode in ['ECB', 'CBC', 'CFB']:
        ct = des_encrypt(mode, key, padded, iv)
        pt = des_decrypt(mode, key, ct, iv)
        print(f"\n{mode} Mode:")
        print("Ciphertext:", ct.hex())
        print("Decrypted:", pt)
