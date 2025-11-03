from collections import Counter

def additive_decrypt(ciphertext, shift):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr(((ord(ch) - 65 - shift) % 26) + 65)
        else:
            result += ch
    return result

def frequency_attack_additive(ciphertext, top_n=10):
    freq = Counter(ciphertext.replace(" ", "").upper())
    most_common_cipher = freq.most_common(1)[0][0]
    most_common_english = 'E'
    shift_guess = (ord(most_common_cipher) - ord(most_common_english)) % 26

    results = []
    for i in range(top_n):
        pt = additive_decrypt(ciphertext, (shift_guess + i) % 26)
        results.append(pt)
    return results

if __name__ == "__main__":
    ciphertext = "KHOORZRUOG"
    guesses = frequency_attack_additive(ciphertext)
    print("Ciphertext:", ciphertext)
    for i, g in enumerate(guesses, 1):
        print(f"{i}. {g}")
