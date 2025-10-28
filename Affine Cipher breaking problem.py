import math

def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_decrypt(ciphertext, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    for c in ciphertext.upper():
        if c.isalpha():
            p = (a_inv * ((ord(c) - 65 - b)) % 26)
            result += chr(p + 65)
        else:
            result += c
    return result

def solve_for_keys():
    p1, c1 = 4, 1   # E -> B
    p2, c2 = 19, 20 # T -> U
    a = ((c2 - c1) * mod_inverse((p2 - p1) % 26, 26)) % 26
    b = (c1 - a * p1) % 26
    return a, b

ciphertext = input("Enter ciphertext: ")
a, b = solve_for_keys()
print("Possible keys: a =", a, ", b =", b)
print("Decrypted text:", affine_decrypt(ciphertext, a, b))
