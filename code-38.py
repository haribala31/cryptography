import numpy as np

def mod_inv_matrix(matrix, modulus):
    det = int(round(np.linalg.det(matrix))) % modulus
    det_inv = pow(det, -1, modulus)
    return (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus) % modulus

def hill_encrypt(matrix, plaintext):
    block = [ord(ch) - 65 for ch in plaintext]
    block = np.array(block).reshape(len(block)//2, 2)
    result = (block.dot(matrix) % 26).flatten()
    return ''.join(chr(r + 65) for r in result)

if __name__ == "__main__":
    key_matrix = np.array([[3, 3], [2, 5]])
    plaintext = "HELP"
    cipher = hill_encrypt(key_matrix, plaintext)
    print("Ciphertext:", cipher)
    P = np.array([[7, 4], [11, 15]])
    C = np.array([[cipher[0], cipher[1]], [cipher[2], cipher[3]]])
    C = np.vectorize(lambda x: ord(x) - 65)(C)
    K = (mod_inv_matrix(P, 26).dot(C)) % 26
    print("\nRecovered Key Matrix:")
    print(K)
