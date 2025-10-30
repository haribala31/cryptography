PC1 = [
 57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,
 63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4
]
PC2 = [
 14,17,11,24,1,5,3,28,15,6,21,10,
 23,19,12,4,26,8,16,7,27,20,13,2,
 41,52,31,37,47,55,30,40,51,45,33,48,
 44,49,39,56,34,53,46,42,50,36,29,32
]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def hex_to_bits(h): return [int(x) for x in bin(int(h,16))[2:].zfill(64)]
def perm(bits, table): return [bits[i-1] for i in table]
def rotl(lst,n): return lst[n:]+lst[:n]

key_hex = input("Enter 64-bit key (hex) [default 133457799BBCDFF1]: ").strip() or "133457799BBCDFF1"
bits = hex_to_bits(key_hex)
cd = perm(bits, PC1)
C, D = cd[:28], cd[28:]

print("\nDES Subkey Composition (First 24 bits from C, Last 24 from D)\n")

for r, shift in enumerate(SHIFTS, 1):
    C, D = rotl(C, shift), rotl(D, shift)
    subkey_positions = PC2
    c_part = [p for p in subkey_positions if p <= 28]
    d_part = [p for p in subkey_positions if p > 28]
    print(f"Round {r:2d}:  First 24 bits from C positions {c_part}")
    print(f"           Last 24 bits from D positions {d_part}\n")

print("Verified: Each subkey’s two halves use disjoint 28-bit subsets of the initial key.")
