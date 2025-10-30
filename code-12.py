import numpy as np
def char_to_num(ch):
    return ord(ch.upper()) - ord('A')
def num_to_char(n):
    return chr((n % 26) + ord('A'))
def prepare_text(text, block_size):
    text = text.replace(" ", "").upper()
    while len(text) % block_size != 0:
        text += 'X'
    return text
def hill_encrypt(plaintext, key):
    n = key.shape[0]
    text = prepare_text(plaintext, n)
    cipher = ""
    print("\n--- Encryption Steps ---")
    for i in range(0, len(text), n):
        block = text[i:i+n]
        vec = np.array([char_to_num(c) for c in block])
        print(f"\nPlain Block: {block} → {vec}")
        enc = np.dot(key, vec) % 26
        print(f"Encrypted Block: {enc} → {[num_to_char(x) for x in enc]}")
        cipher += ''.join(num_to_char(x) for x in enc)
    return cipher
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
def hill_decrypt(cipher, key):
    n = key.shape[0]
    det = int(np.round(np.linalg.det(key)))
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError("Key matrix is not invertible mod 26!")
    key_inv = (det_inv * np.round(det * np.linalg.inv(key)).astype(int)) % 26
    print("\nInverse Key Matrix (mod 26):\n", key_inv)
    plaintext = ""
    print("\n--- Decryption Steps ---")
    for i in range(0, len(cipher), n):
        block = cipher[i:i+n]
        vec = np.array([char_to_num(c) for c in block])
        print(f"\nCipher Block: {block} → {vec}")
        dec = np.dot(key_inv, vec) % 26
        print(f"Decrypted Block: {dec} → {[num_to_char(x) for x in dec]}")
        plaintext += ''.join(num_to_char(x) for x in dec)
    return plaintext
print("=== HILL CIPHER (2x2) ===")
key_matrix = np.array([[9, 4],
                       [5, 7]])
plaintext = "meet me at the usual place at ten rather than eight oclock"
cipher_text = hill_encrypt(plaintext, key_matrix)
print("\nCipher Text:", cipher_text)
decrypted_text = hill_decrypt(cipher_text, key_matrix)
print("\nDecrypted Text:", decrypted_text)
