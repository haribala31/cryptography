from math import gcd
from random import randrange
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n**0.5)
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def gen_small_prime(start=100, end=500):
    while True:
        p = randrange(start, end)
        if is_prime(p):
            return p

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m
def generate_rsa_keypair():
    p = gen_small_prime(200, 500)
    q = gen_small_prime(500, 900)
    while p == q:
        q = gen_small_prime(500, 900)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if gcd(e, phi) != 1:
        for cand in range(3, phi, 2):
            if gcd(cand, phi) == 1:
                e = cand
                break
    d = modinv(e, phi)
    return (e, d, n, p, q)
def char_to_int(c):
    return ord(c) - ord('A')

def int_to_char(i):
    return chr(i + ord('A'))

def encrypt_single_values(vals, e, n):
    return [pow(m, e, n) for m in vals]

def decrypt_single_values(cipher_vals, d, n):
    return [pow(c, d, n) for c in cipher_vals]
def attacker_recover(cipher_blocks, e, n):
    table = {pow(m, e, n): m for m in range(26)}
    recovered = []
    for c in cipher_blocks:
        if c in table:
            recovered.append(table[c])
        else:
            recovered.append(None)
    return recovered
if __name__ == "__main__":
    e, d, n, p, q = generate_rsa_keypair()
    print("Demo RSA parameters (small primes used for clarity):")
    print("p =", p, "q =", q, "n =", n)
    print("Public exponent e =", e)
    print("Private exponent d =", d)
    print()

    plaintext_str = "HELLOALICE"
    plaintext_vals = [char_to_int(c) for c in plaintext_str]
    print("Plaintext letters:", plaintext_str)
    print("Plaintext values:", plaintext_vals)
    ciphertext = encrypt_single_values(plaintext_vals, e, n)
    print("Ciphertext blocks:", ciphertext)
    recovered_vals = attacker_recover(ciphertext, e, n)
    recovered_text = ''.join(int_to_char(v) for v in recovered_vals)
    print("Attacker-recovered values:", recovered_vals)
    print("Attacker-recovered text  :", recovered_text)
    decrypted_vals = decrypt_single_values(ciphertext, d, n)
    decrypted_text = ''.join(int_to_char(v) for v in decrypted_vals)
    print("Owner-decrypted text     :", decrypted_text)
    print("\nCONCLUSION: Because the plaintext space is tiny (26 values), an attacker can precompute")
    print("E(0..25) under the public key and recover any ciphertext immediately. This is insecure.")
