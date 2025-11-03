def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    cipher = ""
    for ch in text.upper():
        if ch.isalpha():
            cipher += chr(((a * (ord(ch) - 65) + b) % 26) + 65)
        else:
            cipher += ch
    return cipher

def affine_decrypt(cipher, a, b):
    plain = ""
    inv = mod_inverse(a, 26)
    for ch in cipher:
        if ch.isalpha():
            plain += chr(((inv * ((ord(ch) - 65) - b)) % 26) + 65)
        else:
            plain += ch
    return plain

if __name__ == "__main__":
    plaintext = "HELLOWORLD"
    a, b = 5, 8
    if gcd(a, 26) != 1:
        print("Invalid key, 'a' must be coprime with 26.")
    else:
        cipher = affine_encrypt(plaintext, a, b)
        decrypted = affine_decrypt(cipher, a, b)
        print("Plaintext:", plaintext)
        print("Ciphertext:", cipher)
        print("Decrypted:", decrypted)
