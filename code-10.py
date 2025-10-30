def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for ch in key:
        if ch.isalpha() and ch not in matrix:
            matrix.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in matrix:
            matrix.append(ch)
    matrix_5x5 = [matrix[i:i+5] for i in range(0, 25, 5)]
    return matrix_5x5
key = input("Enter the Playfair key: ")

matrix = generate_playfair_matrix(key)

print("\n--- Playfair 5x5 Matrix ---")
for row in matrix:
    print(" ".join(row))
