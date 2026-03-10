# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:17:16 2026

@author: Admin
"""

from collections import Counter

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"

def descifrar_cesar(texto, shift):
    resultado = []

    for char in texto:
        c = char.lower()

        if c in ALFABETO:
            pos = ALFABETO.index(c)
            nueva_pos = (pos - shift) % len(ALFABETO)
            nueva_letra = ALFABETO[nueva_pos]

            if char.isupper():
                nueva_letra = nueva_letra.upper()

            resultado.append(nueva_letra)
        else:
            resultado.append(char)

    return "".join(resultado)

def fuerza_bruta(texto):
    for s in range(len(ALFABETO)):
        print(f"{s:2d}: {descifrar_cesar(texto, s)}")


def ataque_frecuencias_top3(texto):
    
    letras = [c.lower() for c in texto if c.lower() in ALFABETO]

    conteo = Counter(letras)

    mas_frecuentes = [letra for letra, _ in conteo.most_common(3)]

    letras_comunes_es = ['e', 'a', 'o']

    candidatos = []

    for i in range(3):
        shift = (ALFABETO.index(mas_frecuentes[i]) - ALFABETO.index(letras_comunes_es[i])) % len(ALFABETO)
        descifrado = descifrar_cesar(texto, shift)
        candidatos.append((shift, descifrado))

    return candidatos
print("Fuerza bruta de la primera cadena:\n")

texto1 = "Nc xkfc gu dgnnc"
fuerza_bruta(texto1)
print()

print("Corrimiento de 15 con César:\n")
texto2 = "Zo qgweidugotío sh jb hsqgsid"
resultado_cesar = descifrar_cesar(texto2,15)
print(f"Mensaje: {resultado_cesar}")
print()

print("Descifrado de la tercera cadena:\n")

texto3 = "Jx qzd kfhnp mjwnw f ptx ijqfx xnr ifwxj hzjryf xtgwj ytit hzfrit jwjx ñtajr"

resultados = ataque_frecuencias_top3(texto3)

print("Top 3 candidatos:\n")

for i, (shift, mensaje) in enumerate(resultados, 1):
    print(f"Candidato {i}")
    print(f"Clave: {shift}")
    print(f"Mensaje: {mensaje}")
    print()
