def generate_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for c in key:
        if c not in matrix and c.isalpha():
            matrix.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in matrix:
            matrix.append(c)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    plaintext = plaintext.upper().replace("J", "I")
    text = ""
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = 'X'
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
        else:
            i += 1
        text += a + b
    ciphertext = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            ciphertext += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            ciphertext += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
        else:
            ciphertext += matrix[r1][c2] + matrix[r2][c1]
    return ciphertext

key = input("Enter key: ")
plaintext = input("Enter plaintext: ")
print("Ciphertext:", playfair_encrypt(plaintext, key))
