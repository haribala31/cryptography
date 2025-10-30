from collections import Counter
import math
EN_FREQ = {'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,'F':0.02228,'G':0.02015,
           'H':0.06094,'I':0.06966,'J':0.00153,'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,
           'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,'U':0.02758,
           'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,'Z':0.00074}

def decrypt(text, shift):
    res = ""
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            res += chr((ord(ch)-ord(base)-shift)%26 + ord(base))
        else:
            res += ch
    return res

def score(text):
    letters = [c.upper() for c in text if c.isalpha()]
    if not letters: return -999
    cnt = Counter(letters)
    total = sum(cnt.values())
    return sum(cnt[L]*math.log(EN_FREQ.get(L,1e-6)) for L in cnt)/total
cipher = input("Enter ciphertext: ").strip()
top_n = int(input("Show top how many possible plaintexts? "))

candidates = []
for s in range(26):
    pt = decrypt(cipher, s)
    candidates.append((s, pt, score(pt)))

candidates.sort(key=lambda x: x[2], reverse=True)

print("\nTop possible plaintexts:")
for i, (s, pt, sc) in enumerate(candidates[:top_n], 1):
    print(f"{i}. shift={s:2d} → {pt}")
