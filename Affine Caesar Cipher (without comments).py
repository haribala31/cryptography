import math

def mod_inverse(a, m):
    """Find modular multiplicative inverse using Extended Euclidean Algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def affine_encrypt(plaintext, a, b):
    """Encrypt plaintext using affine cipher: C = (a*P + b) mod 26"""
    result = ""
    for char in plaintext.upper():
        if char.isalpha():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            result += char
    return result

def affine_decrypt(ciphertext, a, b):
    """Decrypt ciphertext using affine cipher: P = a^-1 * (C - b) mod 26"""
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Decryption not possible (a not invertible mod 26)"
    for char in ciphertext.upper():
        if char.isalpha():
            result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        else:
            result += char
    return result

# Main program
try:
    a = int(input("Enter value of a: "))
    b = int(input("Enter value of b: "))
    plaintext = input("Enter plaintext: ")
    
    if math.gcd(a, 26) != 1:
        print("Invalid key: 'a' must be coprime with 26.")
    else:
        cipher = affine_encrypt(plaintext, a, b)
        print("Ciphertext:", cipher)
        decrypted = affine_decrypt(cipher, a, b)
        print("Decrypted:", decrypted)
except ValueError:
    print("Error: 'a' and 'b' must be integers.")
