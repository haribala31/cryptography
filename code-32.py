from Crypto.PublicKey import RSA, DSA
from Crypto.Signature import pkcs1_15, DSS
from Crypto.Hash import SHA256

def hexsig(b):
    return b.hex()

def demo():
    message = b"Attack at dawn - demonstrate signature differences"
    rsa_key = RSA.generate(2048)
    rsa_pub = rsa_key.publickey()
    h1 = SHA256.new(message)
    rsa_sig1 = pkcs1_15.new(rsa_key).sign(h1)

    h2 = SHA256.new(message)
    rsa_sig2 = pkcs1_15.new(rsa_key).sign(h2)
    dsa_key = DSA.generate(2048)
    dsa_pub = dsa_key.publickey()

    h1 = SHA256.new(message)
    dsa_sig1 = DSS.new(dsa_key, 'fips-186-3').sign(h1)

    h2 = SHA256.new(message)
    dsa_sig2 = DSS.new(dsa_key, 'fips-186-3').sign(h2)
    print("Message:", message.decode())
    print("\n--- RSA (PKCS#1 v1.5) signatures ---")
    print("RSA sig 1 (hex):", hexsig(rsa_sig1))
    print("RSA sig 2 (hex):", hexsig(rsa_sig2))
    print("RSA signatures identical?", rsa_sig1 == rsa_sig2)

    print("\n--- DSA (FIPS 186-3) signatures ---")
    print("DSA sig 1 (hex):", hexsig(dsa_sig1))
    print("DSA sig 2 (hex):", hexsig(dsa_sig2))
    print("DSA signatures identical?", dsa_sig1 == dsa_sig2)
    try:
        pkcs1_15.new(rsa_pub).verify(SHA256.new(message), rsa_sig1)
        print("\nRSA signature 1 verification: OK")
    except (ValueError, TypeError):
        print("\nRSA signature 1 verification: FAILED")

    try:
        pkcs1_15.new(rsa_pub).verify(SHA256.new(message), rsa_sig2)
        print("RSA
