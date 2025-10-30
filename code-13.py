from typing import List, Tuple
MOD = 26
def egcd(a: int, b: int) -> Tuple[int,int,int]:
    """Extended GCD: returns (g, x, y) such that ax + by = g = gcd(a,b)."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)
def modinv(a: int, m: int) -> int:
    """Modular inverse of a under modulus m. Raises ValueError if none exists."""
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m
def clean_text(s: str) -> str:
    """Keep only letters and convert to uppercase."""
    return ''.join(ch for ch in s.upper() if ch.isalpha())

def text_to_numbers(s: str) -> List[int]:
    return [ord(ch) - ord('A') for ch in s]

def numbers_to_text(nums: List[int]) -> str:
    return ''.join(chr((n % MOD) + ord('A')) for n in nums)

def zeros(rows: int, cols: int) -> List[List[int]]:
    return [[0]*cols for _ in range(rows)]

def mat_mul(A: List[List[int]], B: List[List[int]], mod: int=MOD) -> List[List[int]]:
    r, m = len(A), len(B)
    n = len(B[0])
    C = zeros(r, n)
    for i in range(r):
        for j in range(n):
            s = 0
            for k in range(m):
                s += A[i][k] * B[k][j]
            C[i][j] = s % mod
    return C

def mat_transpose(A: List[List[int]]) -> List[List[int]]:
    return [list(col) for col in zip(*A)]

def mat_from_blocks(blocks: List[List[int]]) -> List[List[int]]:
    """Given k blocks (each length n), form an n x k matrix where each column is a block."""
    if not blocks: return []
    n = len(blocks[0])
    k = len(blocks)
    M = zeros(n, k)
    for col in range(k):
        for row in range(n):
            M[row][col] = blocks[col][row] % MOD
    return M

def mat_copy(A):
    return [row[:] for row in A]

def mat_identity(n: int) -> List[List[int]]:
    I = zeros(n,n)
    for i in range(n):
        I[i][i] = 1
    return I

def mat_inv_mod(A: List[List[int]], mod: int=MOD) -> List[List[int]]:
    """Inverse of matrix A modulo mod using Gauss-Jordan. A must be square and invertible mod."""
    n = len(A)
    aug = [row[:] + Irow[:] for row, Irow in zip(mat_copy(A), mat_identity(n))]

    for col in range(n):
        pivot = None
        for r in range(col, n):
            if aug[r][col] % mod != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Matrix not invertible modulo {}".format(mod))

        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]

        inv_pivot = modinv(aug[col][col], mod)
        aug[col] = [(val * inv_pivot) % mod for val in aug[col]]

        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor % mod != 0:
                aug[r] = [ (aug[r][c] - factor * aug[col][c]) % mod for c in range(2*n) ]

    inv = [row[n:] for row in aug]
    return inv

def encrypt_hill(plaintext: str, K: List[List[int]]) -> str:
    """Encrypt plaintext (letters only) using key matrix K (n x n)."""
    n = len(K)
    pt = clean_text(plaintext)
    while len(pt) % n != 0:
        pt += 'X'
    nums = text_to_numbers(pt)
    cipher_nums = []
    for i in range(0, len(nums), n):
        block = nums[i:i+n]
        res = [ sum(K[row][k] * block[k] for k in range(n)) % MOD for row in range(n) ]
        cipher_nums.extend(res)
    return numbers_to_text(cipher_nums)
def recover_key_known_plaintext(plaintext: str, ciphertext: str, n: int) -> List[List[int]]:
    """
    Recover n x n Hill key given known plaintext and matching ciphertext.
    plaintext and ciphertext should contain only letters (function cleans them).
    Need at least n blocks (i.e., plaintext length >= n*n? actually n blocks -> len >= n*n? careful:)
    We will take the first n blocks (each of length n) as columns.
    """
    pt = clean_text(plaintext)
    ct = clean_text(ciphertext)
    if len(pt) < n*n or len(ct) < n*n:
        raise ValueError(f"Need at least {n} blocks (total length >= {n*n} letters).")

    pt_blocks = []
    ct_blocks = []
    nums_pt = text_to_numbers(pt)
    nums_ct = text_to_numbers(ct)
    for i in range(n):
        start = i*n
        pt_blocks.append(nums_pt[start:start+n])
        ct_blocks.append(nums_ct[start:start+n])

    P = mat_from_blocks(pt_blocks)
    C = mat_from_blocks(ct_blocks)
    P_inv = mat_inv_mod(P, MOD)
    K = mat_mul(C, P_inv, MOD)
    return K

def recover_key_chosen_plaintext(chosen_blocks: List[List[int]], ciphertext_blocks: List[List[int]]) -> List[List[int]]:
    """
    If the attacker chooses plaintext blocks such that the plaintext matrix is invertible (often choose identity basis),
    they can directly solve K = C * P^{-1}. For identity P we have K = C.
    chosen_blocks and ciphertext_blocks are lists of length n with each block length n.
    """
    P = mat_from_blocks(chosen_blocks)
    C = mat_from_blocks(ciphertext_blocks)
    P_inv = mat_inv_mod(P, MOD)
    K = mat_mul(C, P_inv, MOD)
    return K
if __name__ == "__main__":
    K_true = [[9,4],
              [5,7]]
    n = 2
    plaintext = "meet me at the usual place at ten rather than eight oclock"
    print("Plaintext (cleaned):", clean_text(plaintext))
    ciphertext = encrypt_hill(plaintext, K_true)
    print("Ciphertext (generated):", ciphertext)
    try:
        K_recovered = recover_key_known_plaintext(plaintext, ciphertext, n)
        print("\nRecovered key (known-plaintext attack):")
        for row in K_recovered:
            print(row)
    except ValueError as e:
        print("Known-plaintext attack failed:", e)
    chosen_blocks = [[1,0],[0,1]]
    chosen_plaintext = ''.join(numbers_to_text(b) for b in chosen_blocks)
    chosen_ciphertext = encrypt_hill(chosen_plaintext, K_true)
    nums_chosen_ct = text_to_numbers(clean_text(chosen_ciphertext))
    ct_blocks = [ nums_chosen_ct[i*n:(i+1)*n] for i in range(n) ]
    try:
        K_from_chosen = recover_key_chosen_plaintext(chosen_blocks, ct_blocks)
        print("\nRecovered key (chosen-plaintext attack):")
        for row in K_from_chosen:
            print(row)
    except ValueError as e:
        print("Chosen-plaintext attack failed:", e)
    print("\nTrue key:")
    for row in K_true:
        print(row)
