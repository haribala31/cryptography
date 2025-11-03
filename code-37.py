from collections import Counter

def frequency_attack(ciphertext, top_n=10):
    freq_english = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    freq_cipher = [item[0] for item in Counter(ciphertext.replace(" ", "").upper()).most_common()]
    mappings = dict(zip(freq_cipher, freq_english))
    guesses = []
    for i in range(top_n):
        guess = ''.join(mappings.get(ch, ch) for ch in ciphertext.upper())
        guesses.append(guess)
    return guesses

if __name__ == "__main__":
    ciphertext = "GSRH RH Z HVXIVG NVHHZTV"
    guesses = frequency_attack(ciphertext)
    print("Ciphertext:", ciphertext)
    print("\nTop Guesses:")
    for i, g in enumerate(guesses, 1):
        print(f"{i}. {g}")
