def caesar_cipher(text, k):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + k) % 26 + base)
        else:
            result += char
    return result

text = input("Enter plaintext: ")
for k in range(1, 26):
    print("k =", k, ":", caesar_cipher(text, k))
