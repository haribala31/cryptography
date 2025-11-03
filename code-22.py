def permute(bits, pattern):
    return [bits[p - 1] for p in pattern]
def left_shift(bits, n):
    return bits[n:] + bits[:n]
S0 = [[1,0,3,2],
      [3,2,1,0],
      [0,2,1,3],
      [3,1,3,2]]

S1 = [[0,1,2,3],
      [2,0,1,3],
      [3,0,1,0],
      [2,1,0,3]]
def to_bits(s):
    return [int(x) for x in s]

def to_str(b):
    return ''.join(str(x) for x in b)
def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]
def generate_keys(key10):
    P10 = [3,5,2,7,4,10,1,9,8,6]
    P8 = [6,3,7,4,8,5,10,9]
    key = permute(key10, P10)
    left, right = key[:5], key[5:]
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    K1 = permute(left + right, P8)
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    K2 = permute(left + right, P8)
    return K1, K2
def fk(bits, key):
    EP = [4,1,2,3,2,3,4,1]
    P4 = [2,4,3,1]
    left, right = bits[:4], bits[4:]
    temp = permute(right, EP)
    temp = xor(temp, key)
    l = temp[:4]
    r = temp[4:]
    row1 = (l[0] << 1) + l[3]
    col1 = (l[1] << 1) + l[2]
    row2 = (r[0] << 1) + r[3]
    col2 = (r[1] << 1) + r[2]
    s0val = S0[row1][col1]
    s1val = S1[row2][col2]
    s_output = [ (s0val & 0b10) >> 1, s0val & 0b1,
                 (s1val & 0b10) >> 1, s1val & 0b1 ]
    s_output = permute(s_output, P4)
    return xor(left, s_output) + right
def sdes_encrypt(bits8, K1, K2):
    IP = [2,6,3,1,4,8,5,7]
    IPinv = [4,1,3,5,7,2,8,6]
    bits = permute(bits8, IP)
    temp = fk(bits, K1)
    temp = temp[4:] + temp[:4]
    temp = fk(temp, K2)
    return permute(temp, IPinv)

def sdes_decrypt(bits8, K1, K2):
    IP = [2,6,3,1,4,8,5,7]
    IPinv = [4,1,3,5,7,2,8,6]
    bits = permute(bits8, IP)
    temp = fk(bits, K2)
    temp = temp[4:] + temp[:4]
    temp = fk(temp, K1)
    return permute(temp, IPinv)
def cbc_encrypt(plaintext, K1, K2, IV):
    blocks = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
    prev = IV
    ciphertext = []
    for block in blocks:
        block = xor(block, prev)
        c = sdes_encrypt(block, K1, K2)
        ciphertext += c
        prev = c
    return ciphertext

def cbc_decrypt(ciphertext, K1, K2, IV):
    blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]
    prev = IV
    plaintext = []
    for block in blocks:
        p = sdes_decrypt(block, K1, K2)
        p = xor(p, prev)
        plaintext += p
        prev = block
    return plaintext
IV = to_bits("10101010")
key10 = to_bits("0111111101")
plaintext = to_bits("0000000100100011")

K1, K2 = generate_keys(key10)

ciphertext = cbc_encrypt(plaintext, K1, K2, IV)
decrypted = cbc_decrypt(ciphertext, K1, K2, IV)

print("IV:          ", to_str(IV))
print("Key:         ", to_str(key10))
print("Plaintext:   ", to_str(plaintext))
print("Ciphertext:  ", to_str(ciphertext))
print("Decrypted:   ", to_str(decrypted))
