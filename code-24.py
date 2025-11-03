def find_factors(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    return None, None
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd == 1:
        return x % phi
    else:
        return None
e = 31
n = 3599

p, q = find_factors(n)
print(f"Step 1: Factors of n = {n} are p = {p}, q = {q}")
phi = (p - 1) * (q - 1)
print(f"Step 2: φ(n) = (p-1)*(q-1) = {phi}")
d = mod_inverse(e, phi)
print(f"Step 3: Private key d = {d}")
print("\n--- RSA Key Pair ---")
print(f"Public Key (e, n): ({e}, {n})")
print(f"Private Key (d, n): ({d}, {n})")
