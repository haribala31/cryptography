def playfair_encrypt(message):
    matrix = [['M','F','H','I','K'],
              ['U','N','O','P','Q'],
              ['Z','V','W','X','Y'],
              ['E','L','A','R','G'],
              ['D','S','T','B','C']]
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[matrix[i][j]] = (i, j)

    msg = message.upper().replace('J', 'I')
    msg = ''.join([c for c in msg if c.isalpha()])

    pairs = []
    i = 0
    while i < len(msg):
        a = msg[i]
        b = 'X'
        if i+1 < len(msg) and msg[i+1] != a:
            b = msg[i+1]
            i += 2
        else:
            i += 1
        pairs.append((a, b))

    cipher = ''
    for a, b in pairs:
        r1, c1 = pos[a]
        r2, c2 = pos[b]
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

message = "Must see you over Cadogan West. Coming at once."
print(playfair_encrypt(message))
