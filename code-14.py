import random
def char_to_num(ch):
    return ord(ch.upper()) - ord('A')
def num_to_char(n):
    return chr((n % 26) + ord('A'))
def generate_random_key(length):
    return [random.randint(0, 25) for _ in range(length)]
def otp_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()
    ciphertext = ""
    print("\n--- Encryption Steps ---")
    for i, ch in enumerate(plaintext):
        p = char_to_num(ch)
        k = key[i]
        c = (p + k) % 26
        print(f"Plaintext: {ch} ({p}) + Key: {k} → Cipher: {num_to_char(c)} ({c})")
        ciphertext += num_to_char(c)
    return ciphertext
def otp_decrypt(ciphertext, key):
    plaintext = ""
    print("\n--- Decryption Steps ---")
    for i, ch in enumerate(ciphertext):
        c = char_to_num(ch)
        k = key[i]
        p = (c - k) % 26
        print(f"Cipher: {ch} ({c}) - Key: {k} → Plaintext: {num_to_char(p)} ({p})")
        plaintext += num_to_char(p)
    return plaintext
print("=== ONE-TIME PAD (Vigenère Cipher Version) ===")

plaintext = "HELLO WORLD"
plaintext = plaintext.replace(" ", "").upper()

key = generate_random_key(len(plaintext))

print("\nPlaintext:", plaintext)
print("Random Key Stream:", key)

ciphertext = otp_encrypt(plaintext, key)
print("\nCiphertext:", ciphertext)

decrypted_text = otp_decrypt(ciphertext, key)
print("\nDecrypted Text:", decrypted_text)
