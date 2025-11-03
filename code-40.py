from collections import Counter

def frequency_attack_mono(ciphertext, top_n=10):
    english_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    cipher_freq = [item[0] for item in Counter(ciphertext.replace(" ", "").upper()).most_common()]
    mapping = dict(zip(cipher_freq, english_freq))
    guesses = []
    for i in range(top_n):
        guess = ''.join(mapping.get(ch, ch) for ch in ciphertext.upper())
        guesses.append(guess)
    return guesses

if __name__ == "__main__":
    ciphertext = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"
    guesses = frequency_attack_mono(ciphertext)
    print("Ciphertext:", ciphertext)
    for i, g in enumerate(guesses, 1):
        print(f"{i}. {g}")
