PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,
       41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def hex_to_bits(h):
    h = h.strip().replace("0x","").zfill(16)
    b = bin(int(h,16))[2:].zfill(64)
    return [int(x) for x in b]

def bits_to_hex(bits):
    s = ''.join(str(b) for b in bits)
    return hex(int(s,2))[2:].upper().zfill(len(s)//4)

def perm(bits, table): return [bits[i-1] for i in table]
def rotl(lst,n): return lst[n:]+lst[:n]
def rotr(lst,n): return lst[-n:]+lst[:-n]

def gen_subkeys(hexkey):
    bits = hex_to_bits(hexkey)
    cd = perm(bits, PC1)
    C, D = cd[:28], cd[28:]
    keys=[]
    for s in SHIFTS:
        C, D = rotl(C,s), rotl(D,s)
        keys.append(perm(C+D, PC2))
    return keys 

def decr_by_reversal(hexkey):
    return list(reversed(gen_subkeys(hexkey)))

def decr_direct(hexkey):
    bits = hex_to_bits(hexkey)
    cd = perm(bits, PC1)
    C, D = cd[:28], cd[28:]
    # advance to C16,D16
    for s in SHIFTS:
        C, D = rotl(C,s), rotl(D,s)
    decr=[]
    for s in reversed(SHIFTS):
        decr.append(perm(C+D, PC2))
        C, D = rotr(C,s), rotr(D,s)
    return decr

if __name__ == "__main__":
    k = input("64-bit key hex [133457799BBCDFF1]: ").strip() or "133457799BBCDFF1"
    enc = gen_subkeys(k)
    dec_rev = decr_by_reversal(k)
    dec_dir = decr_direct(k)
    print("\nK1..K16 (enc):")
    for i,b in enumerate(enc,1): print(f"K{i:2d}: {bits_to_hex(b)}")
    print("\nK16..K1 (decryption by reversal):")
    for i,b in enumerate(dec_rev,1): print(f"K{17-i:2d}: {bits_to_hex(b)}")
    print("\nK16..K1 (decryption direct):")
    for i,b in enumerate(dec_dir,1): print(f"K{17-i:2d}: {bits_to_hex(b)}")
    print("\nMatch:", dec_rev==dec_dir)
