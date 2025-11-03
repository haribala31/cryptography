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
p, q = 59, 61
n = p * q
phi = (p - 1) * (q - 1)
e = 31
_, x, _ = extended_gcd(e, phi)
d = x % phi

print("Original RSA Keys:")
print(f"Public Key (e, n): ({e}, {n})")
print(f"Private Key (d, n): ({d}, {n})")
print("\nBob leaks his private key...")
kphi = d * e - 1
phi_recovered = None
for k in range(2, e * 10):
    if kphi % k == 0:
        phi_guess = kphi // k
        a = 1
        b = -(n + 1 - phi_guess)
        c = n
        disc = b*b - 4*a*c
        if disc >= 0:
            sqrt_disc = int(disc**0.5)
            if sqrt_disc * sqrt_disc == disc:
                p_guess = (-(b) + sqrt_disc)//2
                q_guess = n // p_guess
                if p_guess * q_guess == n:
                    phi_recovered = phi_guess
                    break

if phi_recovered:
    print(f"\nAttacker recovers φ(n) = {phi_recovered}")
    print(f"Recovered factors: p = {p_guess}, q = {q_guess}")
else:
    print("\nAttack failed to recover φ(n).")
e2 = 17
d2 = mod_inverse(e2, phi)
print(f"\nBob’s NEW keys using same n:")
print(f"New Public Key (e2, n): ({e2}, {n})")
print(f"New Private Key (d2, n): ({d2}, {n})")
if phi_recovered:
    d2_recovered = mod_inverse(e2, phi_recovered)
    print(f"\nAttacker also computes Bob’s new d2 = {d2_recovered}")
    if d2_recovered == d2:
        print("New key compromised! Reusing n is NOT safe.")
    else:
        print("Something went wrong in recovery.")
