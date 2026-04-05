# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:03:34 2026

@author: Pedro Yamil Salazar Gonzalez
"""

import math
import random
from math import gcd
import matplotlib.pyplot as plt


# ============================================================
# Utilidades RSA
# ============================================================

def lcm(a: int, b: int) -> int:
    """mcm(a, b)"""
    return (a * b) // gcd(a, b)


def extended_gcd(a: int, b: int):
    """Algoritmo de Euclides extendido."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def modinv(a: int, m: int) -> int:
    """Inverso modular de a mod m."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No existe inverso modular de {a} mod {m}")
    return x % m


def build_rsa(p: int, q: int, e: int):
    """
    Construye parámetros RSA.
    Regresa n, phi(n), lambda(n), d.
    """
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")

    n = p * q
    phi = (p - 1) * (q - 1)
    lam = lcm(p - 1, q - 1)

    if gcd(e, lam) != 1:
        raise ValueError(f"e={e} no es coprimo con lambda(n)={lam}")

    d = modinv(e, lam)
    return n, phi, lam, d


def rsa_encrypt(m: int, e: int, n: int) -> int:
    """Cifrado RSA: c = m^e mod n"""
    return pow(m, e, n)


# ============================================================
# Fórmulas de la paradoja del cumpleaños
# ============================================================

def collision_probability_theoretical(d: int, space_size: int) -> float:
    """
    Aproximación:
    P(colisión) ≈ 1 - exp(-d(d-1)/(2m))
    donde m = tamaño del espacio.
    """
    if space_size <= 0:
        return 0.0
    exponent = - (d * (d - 1)) / (2 * space_size)
    return 1.0 - math.exp(exponent)


def threshold_50_percent(space_size: int) -> float:
    """
    Umbral aproximado para P(colisión) > 1/2:
    d ≈ 1/2 (1 + sqrt(1 + 8 m ln 2))
    """
    return 0.5 * (1 + math.sqrt(1 + 8 * space_size * math.log(2)))


def inflection_point(space_size: int) -> float:
    """
    Punto de inflexión matemático de:
    P(d) = 1 - exp(-d(d-1)/(2m))
    Aproximadamente:
    d ≈ 1/2 + sqrt(m)
    """
    return 0.5 + math.sqrt(space_size)


def practical_threshold(space_size: int, target_prob: float = 0.99) -> int:
    """
    Menor d tal que la probabilidad teórica sea al menos target_prob.
    """
    d = 1
    while collision_probability_theoretical(d, space_size) < target_prob:
        d += 1
    return d


# ============================================================
# Simulación empírica
# ============================================================

def simulate_birthday_attack_rsa(
    n: int,
    e: int,
    lam: int,
    max_messages: int = 200,
    trials: int = 2000,
    use_lambda_as_message_space: bool = True,
):
    """
    Simula interceptar mensajes y observar si aparece alguna colisión.

    use_lambda_as_message_space=True:
        los mensajes aleatorios se toman en [0, lambda(n)-1]
        para que la simulación quede más alineada con la idea del problema.

    Si se pone False:
        los mensajes se toman en [0, n-1].
    """
    empirical_hits = [0] * max_messages

    message_upper = lam if use_lambda_as_message_space else n

    for _ in range(trials):
        seen_ciphertexts = set()
        collision_already_happened = False

        for d in range(1, max_messages + 1):
            m = random.randrange(message_upper)
            c = rsa_encrypt(m, e, n)

            if c in seen_ciphertexts:
                collision_already_happened = True

            seen_ciphertexts.add(c)

            if collision_already_happened:
                empirical_hits[d - 1] += 1

    empirical_probs = [x / trials for x in empirical_hits]
    theoretical_probs = [
        collision_probability_theoretical(d, lam)
        for d in range(1, max_messages + 1)
    ]

    return empirical_probs, theoretical_probs


# ============================================================
# Graficación y reporte
# ============================================================

def run_experiment(
    p: int,
    q: int,
    e: int,
    max_messages: int = 200,
    trials: int = 2000,
    target_prob: float = 0.99,
):
    n, phi, lam, d_priv = build_rsa(p, q, e)

    empirical_probs, theoretical_probs = simulate_birthday_attack_rsa(
        n=n,
        e=e,
        lam=lam,
        max_messages=max_messages,
        trials=trials,
        use_lambda_as_message_space=True,
    )

    d_values = list(range(1, max_messages + 1))

    d_50 = threshold_50_percent(lam)
    d_inflection = inflection_point(lam)
    d_practical = practical_threshold(lam, target_prob=target_prob)

    print("=" * 60)
    print("PARÁMETROS RSA")
    print("=" * 60)
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = p*q = {n}")
    print(f"phi(n) = (p-1)(q-1) = {phi}")
    print(f"lambda(n) = mcm(p-1, q-1) = {lam}")
    print(f"e = {e}")
    print(f"d = e^(-1) mod lambda(n) = {d_priv}")
    print(f"gcd(p-1, q-1) = {gcd(p-1, q-1)}")
    print()

    print("=" * 60)
    print("ANÁLISIS DEL BIRTHDAY ATTACK")
    print("=" * 60)
    print(f"Espacio efectivo usado en la simulación: lambda(n) = {lam}")
    print(f"Mensajes máximos interceptados simulados: {max_messages}")
    print(f"Número de experimentos (trials): {trials}")
    print()
    print(f"Umbral teórico para P(colisión) ≈ 0.5 : d ≈ {d_50:.2f}")
    print(f"Punto de inflexión matemático       : d ≈ {d_inflection:.2f}")
    print(f"Umbral práctico para P(colisión) ≥ {target_prob:.2f}: d = {d_practical}")

    if d_practical <= max_messages:
        print(f"Con ~{d_practical} mensajes interceptados la probabilidad ya es muy cercana a 1.")
    else:
        print(
            f"No se alcanzó P ≥ {target_prob:.2f} dentro de max_messages={max_messages}. "
            f"Incrementa max_messages."
        )

    # -------- Gráfica --------
    plt.figure(figsize=(10, 6))
    plt.plot(d_values, theoretical_probs, label="Probabilidad teórica", linewidth=2)
    plt.plot(d_values, empirical_probs, label="Probabilidad empírica", linewidth=2, linestyle="--")

    # Líneas verticales de referencia
    plt.axvline(d_50, linestyle=":", label=f"50% ≈ {d_50:.1f}")
    plt.axvline(d_inflection, linestyle=":", label=f"Inflexión ≈ {d_inflection:.1f}")

    if d_practical <= max_messages:
        plt.axvline(d_practical, linestyle="-.", label=f"P ≥ {target_prob:.2f} en d={d_practical}")

    plt.title("Birthday attack aplicado a RSA")
    plt.xlabel("Número de mensajes interceptados")
    plt.ylabel("Probabilidad de colisión")
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# Ejecución principal
# ============================================================

if __name__ == "__main__":
    """
    Elegimos un ejemplo didáctico donde p-1 y q-1 comparten muchos factores,
    para que lambda(n) sea relativamente pequeño frente a phi(n).
    """

    # Ejemplo:
    # p-1 = 1008 = 2^4 * 3^2 * 7
    # q-1 = 2016 = 2^5 * 3^2 * 7
    # gcd grande => lambda(n) = mcm(1008, 2016) = 2016
    p = 1009
    q = 2017
    e = 5

    run_experiment(
        p=p,
        q=q,
        e=e,
        max_messages=200,
        trials=3000,
        target_prob=0.99,
    )