# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:34:26 2026

@author: Admin
"""

CUADRO = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O'],
    ['P', 'Q', 'R', 'S', 'T'],
    ['U', 'V', 'W', 'X', 'Y']
]

# Diccionarios para cifrar y descifrar
letra_a_codigo = {}
codigo_a_letra = {}

for fila in range(5):
    for col in range(5):
        letra = CUADRO[fila][col]
        codigo = f"{fila+1}{col+1}"
        letra_a_codigo[letra] = codigo
        codigo_a_letra[codigo] = letra


def cifrar_polibio(texto):
    resultado = []

    texto = texto.upper()

    for char in texto:
        if char == ' ':
            resultado.append(' / ')  # separador visual de palabras
        elif char in letra_a_codigo:
            resultado.append(letra_a_codigo[char])
        else:
            # Ignora caracteres no válidos o podrías lanzar error
            pass

    return ' '.join(resultado).replace('/ ', '/').replace(' /', '/')


def descifrar_polibio(codigo):
    resultado = []
    bloques = codigo.split()

    for bloque in bloques:
        if bloque == '/':
            resultado.append(' ')
        elif bloque in codigo_a_letra:
            resultado.append(codigo_a_letra[bloque])

    return ''.join(resultado)

def main():

    print("===== CUADRADO DE POLIBIO =====\n")

    # --- DESENCRIPTAR MENSAJE DEL EJERCICIO ---
    mensaje_cifrado = "15 32 45 24 15 33 41 35 34 35 15 44 41 15 43 11 11 34 11 14 24 15"

    print("Mensaje cifrado:")
    print(mensaje_cifrado)

    mensaje_descifrado = descifrar_polibio(mensaje_cifrado)

    print("\nMensaje descifrado:")
    print(mensaje_descifrado)


    # --- CIFRAR FRASE DEL EJERCICIO ---
    frase = "Si la felicidad tuviera una forma, tendría forma de cristal, porque puede estar a tu alrededor sin que la notes. Pero si cambias de perspectiva, puede reflejar una luz capaz de iluminarlo todo."

    cifrado = cifrar_polibio(frase)

    print("\nFrase original:")
    print(frase)

    print("\nFrase cifrada:")
    print(cifrado)


if __name__ == "__main__":
    main()