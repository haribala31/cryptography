def generate_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for c in key:
        if c not in matrix and c.isalpha():
            matrix.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in matrix:
            matrix.append(c)
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    ciphertext = ciphertext.upper().replace("J", "I").replace(" ", "")
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
        else:
            plaintext += matrix[r1][c2] + matrix[r2][c1]
    return plaintext

key = "ROYAL NEW ZEALAND NAVY"
ciphertext = """KXJEY UREBE ZWEHE WRYTU HEYFS
KREHE GOYFI WTTTU OLKSY CAJPO
BOTEI ZONTX BYBNT GONEY CUZWR
GDSON SXBOU YWRHE BAAHY USEDQ"""

plaintext = playfair_decrypt(ciphertext, key)
print("Decrypted message:\n", plaintext)
