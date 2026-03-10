# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:10:48 2026

@author: Admin
"""

from collections import defaultdict, Counter


def limpiar_texto(texto):
    texto = texto.upper()
    limpio = ""
    for c in texto:
        if c.isalpha():
            limpio += c
    return limpio


def encontrar_repeticiones(texto, longitud=3):
    
    repeticiones = defaultdict(list)

    for i in range(len(texto) - longitud + 1):
        secuencia = texto[i:i+longitud]
        repeticiones[secuencia].append(i)

    # solo dejar las que aparecen más de una vez
    repeticiones = {k:v for k,v in repeticiones.items() if len(v) > 1}

    return repeticiones


def calcular_distancias(repeticiones):

    distancias = defaultdict(list)

    for secuencia, posiciones in repeticiones.items():

        for i in range(len(posiciones)-1):
            distancia = posiciones[i+1] - posiciones[i]
            distancias[secuencia].append(distancia)

    return distancias


def factorizar(n):

    factores = []

    for i in range(2, n+1):
        if n % i == 0:
            factores.append(i)

    return factores


def kasiski(texto):

    print("\n==============================")
    print(" TEST DE KASISKI ")
    print("==============================\n")

    texto = limpiar_texto(texto)

    print("Texto analizado:")
    print(texto)
    print("\nLongitud del texto:", len(texto))


    print("\n--- Buscando secuencias repetidas ---")

    repeticiones = encontrar_repeticiones(texto)

    for secuencia, posiciones in repeticiones.items():
        print(secuencia, "-> posiciones", posiciones)


    print("\n--- Calculando distancias ---")

    distancias = calcular_distancias(repeticiones)

    todas_distancias = []

    for secuencia, dists in distancias.items():
        print(secuencia, "-> distancias", dists)
        todas_distancias.extend(dists)


    print("\n--- Factorizando distancias ---")

    todos_factores = []

    for d in todas_distancias:

        factores = factorizar(d)

        print(f"Distancia {d} -> factores {factores}")

        todos_factores.extend(factores)


    print("\n--- Frecuencia de factores ---")

    conteo = Counter(todos_factores)

    for factor, freq in conteo.most_common():
        print(f"Factor {factor} aparece {freq} veces")


    print("\n--- Longitudes probables de clave ---")

    candidatos = [f for f,_ in conteo.most_common(10)]

    print("Candidatos:", candidatos[:5])


def main():

    texto = """
    ECISCRVSWVLGDDWUEFHFNGESXUVTICOKQOTAJPHWAKFBNA
    EUONOJFHONCPHRZNSCOKEWLSUFPFEEUWOMHPQFAEEOLDB
    QROKFZLNQBSXVMFZZNMQQSACESDDVMONHBROUEBGMOCVI
    SLZAOXDGTJDAQVZLDRTOVAKDDWOKJTFEJBBFNHBGLCRJRLS
    KVEVUDBXOPVDVZADBSLCPOKUVWSJCRQWCOLFOKUC
    """

    kasiski(texto)


if __name__ == "__main__":
    main()