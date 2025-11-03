from math import gcd
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g == 1:
        return x % phi
    else:
        return None
n = 3599
e = 31
M = 59 
g = gcd(M, n)
print(f"Step 1: gcd(M, n) = gcd({M}, {n}) = {g}")
if g != 1 and g != n:
    p = g
    q = n // g
    print(f"Step 2: We found the factors! p = {p}, q = {q}")
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)

    print(f"Step 3: φ(n) = {phi}")
    print(f"Step 4: Private key d = {d}")

    print("\n--- RSA Key Recovered ---")
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")
else:
    print("No common factor found — attack fails.")
