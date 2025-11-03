def mod_exp(base, exp, mod):
    """Modular exponentiation"""
    return pow(base, exp, mod)
q = 353
a = 3

print("Public parameters:")
print(f"q = {q}, a = {a}")
print("-" * 40)
xA = 97
xB = 233
print("Correct Diffie–Hellman Protocol")

YA = mod_exp(a, xA, q)
YB = mod_exp(a, xB, q)
KA = mod_exp(YB, xA, q)
KB = mod_exp(YA, xB, q)

print(f"Alice sends YA = {YA}")
print(f"Bob sends   YB = {YB}")
print(f"Alice computes key = {KA}")
print(f"Bob computes   key = {KB}")
print(f"Shared key match? {'Yes' if KA == KB else 'No'}")
print("-" * 40)
print("Wrong Version: Sending x^a instead of a^x")

MA = (xA ** a) % q
MB = (xB ** a) % q
KA_wrong = (MB ** xA) % q
KB_wrong = (MA ** xB) %**_
