import random, math
from collections import Counter

EN_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
COMMON = (" the and that have for not with you this but his from they which are "
          "are were their will what there been one all any out about who get when").split()
DIGRAM = {"TH":2.7,"HE":2.3,"IN":2.0,"ER":1.8,"AN":1.6,"RE":1.4,"ND":1.3,"AT":1.25,"ON":1.2,"NT":1.17,
          "HA":1.0,"ES":0.99,"ST":0.98,"EN":0.93,"ED":0.92,"TO":0.91,"IT":0.89,"OU":0.84,"EA":0.82,"HI":0.71}
MIN_D = 0.01

def clean(s): return ''.join(ch for ch in s.upper() if ch.isalpha() or ch.isspace())

def freq_init(ct):
    letters = [c for c in ct if c.isalpha()]
    most = [p for p,_ in Counter(letters).most_common()]
    for c in (chr(ord('A')+i) for i in range(26)):
        if c not in most: most.append(c)
    return {c:p for c,p in zip(most, EN_ORDER)}

def decrypt(ct, key):
    out=[]
    for ch in ct:
        if ch.isalpha(): out.append(key.get(ch, '?'))
        else: out.append(ch)
    return ''.join(out)

def score(pt):
    L=[c for c in pt if c.isalpha()]
    if not L: return -1e9
    s=0.0
    for i in range(len(L)-1):
        s += math.log(DIGRAM.get(L[i]+L[i+1], MIN_D))
    s /= max(1,len(L)-1)
    lw=pt.lower()
    bonus = sum(0.5*(lw.count(" "+w+" ")+lw.startswith(w+" ")+lw.endswith(" "+w)) for w in COMMON)
    toks=[t for t in lw.split() if any(c.isalpha() for c in t)]
    if toks:
        bonus += 0.1*sum(1 for t in toks if len(t)>1)/len(toks)
    return s+bonus

def swap_key(k):
    a,b = random.sample([chr(ord('A')+i) for i in range(26)], 2)
    nk = k.copy(); nk[a], nk[b] = nk[b], nk[a]; return nk

def climb(ct, start, iters=1200):
    best = start.copy(); best_pt = decrypt(ct,best); best_sc = score(best_pt)
    cur, cur_sc = best, best_sc; temp=1.0
    for i in range(iters):
        cand = swap_key(cur)
        cand_pt = decrypt(ct,cand); cand_sc = score(cand_pt)
        if cand_sc>cur_sc or random.random() < math.exp((cand_sc-cur_sc)/max(1e-9,temp)):
            cur, cur_sc = cand, cand_sc
            if cand_sc>best_sc: best, best_sc = cand.copy(), cand_sc
        temp *= 0.995
    return best, best_sc

def attack(ct, restarts=12, iters=1200, top_n=10):
    ct = clean(ct)
    cand_list=[]
    # frequency start
    km = freq_init(ct)
    k, sc = climb(ct, km, iters); cand_list.append((sc, decrypt(ct,k), k))
    for _ in range(restarts-1):
        letters = list(EN_ORDER); random.shuffle(letters)
        rand_map = {chr(ord('A')+i): letters[i] for i in range(26)}
        k, sc = climb(ct, rand_map, iters); cand_list.append((sc, decrypt(ct,k), k))
    # unique and sort
    seen = {}
    for sc,pt,k in cand_list:
        if pt not in seen or sc>seen[pt][0]: seen[pt]=(sc,k)
    ordered = sorted(((v[0],pt,v[1]) for pt,v in seen.items()), key=lambda x:x[0], reverse=True)
    return ordered[:top_n]

def main():
    print("Paste ciphertext (end input with empty line):")
    lines=[]
    while True:
        try:
            l=input()
        except EOFError: break
        if not l.strip(): break
        lines.append(l)
    if not lines:
        print("No input."); return
    ct="\n".join(lines)
    try:
        top_n = int(input("Show top how many? [10] ").strip() or "10")
    except:
        top_n=10
    print("Working... (may take a few seconds)")
    results = attack(ct, restarts=20, iters=1800, top_n=top_n)
    for i,(sc,pt,k) in enumerate(results,1):
        keystr=''.join(k[chr(ord('A')+j)] for j in range(26))
        print(f"\nRank {i} — score={sc:.4f}\nKey(A->Z): {keystr}\nPlaintext:\n{pt}\n{'-'*60}")

if __name__=="__main__":
    main()
