# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 15:56:17 2026

@author: Pedro Yamil Salazar Gonzalez
"""
import re

# ============================================================
# CLAVE OBTENIDA DEL EJERCICIO ANTERIOR
# ============================================================

KEY = "PEgAsuzs"

# ============================================================
# CRIPTOGRAMA
# ============================================================

CIPHERTEXT = """
SHPETXSQZNSPLBMBWFFKCEBRBQMVQSEGOLRBLGXPPSUXHWLGXPDL-
SZSNAZINELFTEQRGTSRIFWKBRGZVNPWKBQPGPBMZOMGEQMXPHGUF
DIKBSCMGQMSHVZXTQMFXFOGPSHBWIOSNOQNPWKKCOQMFAVSHSM-
FOSNDKHGMVSZHQPIYSQAVPNEGCERZQBQOKSSCOFOHPYQSBKQOZSHP
FKEGKCRLSNQOIKOQOWPSTDPSBRAVGMVZQZKGFRZVVPZVSHPG-
VAOHRBGEZVEQHGWMKSNSZSRZPHZVPSZSIRIDLSNAZINDLOBFWSKGPZS
MZQZOWMCAVSHGRMPXGNSPGFPKFHBMGSQSGPEKGQSFSSNOW-
BLPYSQKBSQBRQSEFSGKSKSUXHWLGXYZSZSNSZKRGFZQPOQDVSXTFRZQ
MPQRGXECNZPCEGLBQNQPCMESNOWBLPYSCGSOHQPFSRIFWKBQB-
DTQOQNDOZVMIZPUFDIKBSCNGRYCYBLQGBQOQZAMRZPBRPESNGRQEPE
SNVPVZBKZVUPPSKSSPQBKGKBQOBKWHKDZVYMNGMQZLKEIOEQGLBR-
WHUXFOSPZSGPFGQQGKAV
"""

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def clean_text(text):
    text = text.upper()
    text = text.replace("J", "I")
    text = re.sub(r"[^A-Z]", "", text)
    return text

def normalize_key(key):
    key = clean_text(key)
    result = []
    seen = set()

    for ch in key:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)

    return "".join(result)

def build_matrix_from_key(key):
    key = normalize_key(key)

    used = set(key)
    rest = "".join(ch for ch in ALPHABET if ch not in used)
    full = key + rest

    matrix = [list(full[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def build_positions(matrix):
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[matrix[i][j]] = (i, j)
    return pos

def decrypt_pair(a, b, matrix, pos):
    ra, ca = pos[a]
    rb, cb = pos[b]

    # misma fila -> izquierda
    if ra == rb:
        return matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5]

    # misma columna -> arriba
    if ca == cb:
        return matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb]

    # rectángulo
    return matrix[ra][cb] + matrix[rb][ca]

def playfair_decrypt(ciphertext, matrix):
    pos = build_positions(matrix)
    text = clean_text(ciphertext)

    if len(text) % 2 != 0:
        text = text[:-1]

    plain = []
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        plain.append(decrypt_pair(a, b, matrix, pos))

    return "".join(plain)

def matrix_to_string(matrix):
    return "\n".join(" ".join(row) for row in matrix)



if __name__ == "__main__":
    matrix = build_matrix_from_key(KEY)
    plaintext = playfair_decrypt(CIPHERTEXT, matrix)

    print("Clave original:", KEY)
    print("Clave normalizada:", normalize_key(KEY))
    print("\nMatriz Playfair:")
    print(matrix_to_string(matrix))

    print("\nTexto descifrado (inicio):")
    print(plaintext[:1000])

    with open("playfair_descifrado.txt", "w", encoding="utf-8") as f:
        f.write("Clave original: " + KEY + "\n")
        f.write("Clave normalizada: " + normalize_key(KEY) + "\n\n")
        f.write("Matriz Playfair:\n")
        f.write(matrix_to_string(matrix) + "\n\n")
        f.write("Texto descifrado:\n")
        f.write(plaintext)

    print("\nSe guardó el resultado en 'playfair_descifrado.txt'.")