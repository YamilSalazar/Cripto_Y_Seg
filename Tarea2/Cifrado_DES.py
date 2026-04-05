# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:58:20 2026

@author: Pedro Yamil Salazar Gonzalez
"""

import base64

# =========================
# TABLAS DES
# =========================

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

FP = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,
    29,12,28,17,
    1,15,23,26,
    5,18,31,10,
    2,8,24,14,
    32,27,3,9,
    19,13,30,6,
    22,11,4,25
]

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

KEY_SHIFT = [
    1,1,2,2,2,2,2,2,
    1,2,2,2,2,2,2,1
]

S_BOXES = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ],
]


def permute(block, table, bits):
    result = 0
    for p in table:
        result = (result << 1) | ((block >> (bits - p)) & 1)
    return result

def left_rotate(val, shift, size):
    return ((val << shift) & ((1 << size) - 1)) | (val >> (size - shift))

def sbox_substitution(block):
    result = 0
    for i in range(8):
        chunk = (block >> (42 - 6 * i)) & 0x3F
        row = ((chunk & 0x20) >> 4) | (chunk & 1)
        col = (chunk >> 1) & 0x0F
        result = (result << 4) | S_BOXES[i][row][col]
    return result

def pkcs5_pad(data):
    pad_len = 8 - (len(data) % 8)
    if pad_len == 0:
        pad_len = 8
    return data + bytes([pad_len] * pad_len)

def pkcs5_unpad(data):
    if not data or len(data) % 8 != 0:
        raise ValueError("Datos inválidos para quitar padding.")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Padding inválido.")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Padding inválido.")
    return data[:-pad_len]

# =========================
# GENERACIÓN DE SUBCLAVES
# =========================

def generate_keys(key):
    keys = []
    key = permute(key, PC1, 64)

    left = (key >> 28) & 0x0FFFFFFF
    right = key & 0x0FFFFFFF

    for shift in KEY_SHIFT:
        left = left_rotate(left, shift, 28)
        right = left_rotate(right, shift, 28)
        combined = (left << 28) | right
        round_key = permute(combined, PC2, 56)
        keys.append(round_key)

    return keys

# =========================
# CIFRADO/DECIFRADO DE BLOQUE
# =========================

def des_block(block, keys):
    block = permute(block, IP, 64)

    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF

    for k in keys:
        temp = right
        expanded = permute(right, E, 32)
        xored = expanded ^ k
        substituted = sbox_substitution(xored)
        permuted = permute(substituted, P, 32)
        right = left ^ permuted
        left = temp

    combined = (right << 32) | left
    return permute(combined, FP, 64)

# =========================
# ECB
# =========================

def des_encrypt_ecb(data, key_int):
    keys = generate_keys(key_int)
    data = pkcs5_pad(data)
    result = b""

    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        enc = des_block(block, keys)
        result += enc.to_bytes(8, "big")

    return result

def des_decrypt_ecb(data, key_int):
    keys = generate_keys(key_int)
    keys.reverse()
    result = b""

    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        dec = des_block(block, keys)
        result += dec.to_bytes(8, "big")

    return pkcs5_unpad(result)

# =========================
# BASE64
# =========================

def encrypt_to_base64(message_text, key_text):
    if len(key_text.encode("utf-8")) != 8:
        raise ValueError("La clave DES debe tener exactamente 8 bytes.")
    message = message_text.encode("utf-8")
    key_int = int.from_bytes(key_text.encode("utf-8"), "big")
    cipher_bytes = des_encrypt_ecb(message, key_int)
    return base64.b64encode(cipher_bytes).decode("ascii")

def decrypt_from_base64(cipher_b64, key_text):
    if len(key_text.encode("utf-8")) != 8:
        raise ValueError("La clave DES debe tener exactamente 8 bytes.")
    cipher_bytes = base64.b64decode(cipher_b64)
    key_int = int.from_bytes(key_text.encode("utf-8"), "big")
    plain_bytes = des_decrypt_ecb(cipher_bytes, key_int)
    return plain_bytes.decode("utf-8")

def decrypt_raw_from_base64(cipher_b64, key_text):
    if len(key_text.encode("utf-8")) != 8:
        raise ValueError("La clave DES debe tener exactamente 8 bytes.")
    cipher_bytes = base64.b64decode(cipher_b64)
    key_int = int.from_bytes(key_text.encode("utf-8"), "big")

    keys = generate_keys(key_int)
    keys.reverse()

    result = b""
    for i in range(0, len(cipher_bytes), 8):
        block = int.from_bytes(cipher_bytes[i:i+8], "big")
        dec = des_block(block, keys)
        result += dec.to_bytes(8, "big")

    return result


if __name__ == "__main__":
    m = "noche697"
    k = "data7Qa="

    c = encrypt_to_base64(m, k)
    print("Mensaje original:", m)
    print("Clave:", k)
    print("Cifrado Base64:", c)

    m_recuperado = decrypt_from_base64(c, k)
    print("Descifrado:", m_recuperado)
    
    # ======================
    # Ejercicio 7 parte 1
    # ======================
    print("\nEjercicio 7:")
    
    archivo_claves = "words.txt"
    cipher_objetivo = "h+F7XMoHpF0="
    
    def es_texto_legible(data):
        return all(32 <= b <= 126 for b in data)
    
    resultados = []
    
    with open(archivo_claves, "r", encoding="utf-8") as f:
        claves = [line.strip() for line in f if line.strip()]
    
    print("\n--- Iniciando ataque por diccionario ---\n")
    print(f"Total de claves a probar: {len(claves)}\n")
    
    for clave in claves:
        if len(clave.encode("utf-8")) != 8:
            continue
    
        try:
            plain_bytes = decrypt_raw_from_base64(cipher_objetivo, clave)
    
            if es_texto_legible(plain_bytes):
                texto = plain_bytes.decode("ascii", errors="ignore")
                print(f"[POSIBLE] Clave: {clave} -> Texto: {texto}")
                resultados.append(f"{clave} -> {texto}")
    
        except Exception:
            continue
    
    with open("resultados.txt", "w", encoding="utf-8") as f:
        for r in resultados:
            f.write(r + "\n")
    
    print("\n--- RESULTADOS GUARDADOS EN resultados.txt ---")
    