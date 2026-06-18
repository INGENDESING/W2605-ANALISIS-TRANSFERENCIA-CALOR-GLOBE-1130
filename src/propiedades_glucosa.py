"""
Módulo de propiedades termofísicas — Proyecto W2605
====================================================
Propiedades de la glucosa Globe 1130 (Ingredion 011420) y del agua
en función de la temperatura.

Las correlaciones para glucosa se basan en la ficha técnica oficial
del fabricante (Ingredion, 2017) y datos complementarios de literatura:
  - Densidad: Ficha técnica Ingredion 011420 (3 puntos), ajuste lineal
  - Viscosidad: Modelo VFT calibrado a ficha técnica Ingredion 011420
  - Cp y k: Choi & Okos (1986), correlaciones ASHRAE
  - Agua: IAPWS-IF97 simplificadas (Incropera, Apéndice A)

Ficha técnica Ingredion Globe 1130 011420:
  - Dry Substance: 79.7-81.5% (nominal ~80.6%)
  - DE: 40.5-46.5
  - Densidad y viscosidad a 80, 100, 120 °F

Nota: A temperaturas bajas es extremadamente viscosa (>74,000 cP a 26.7°C).
Se comporta como fluido newtoniano a temperaturas por encima de ~40°C.
"""

import numpy as np


# =============================================================================
# PROPIEDADES DE LA GLUCOSA Globe 1130 (Ingredion 011420)
# =============================================================================

# Concentración de sólidos (ficha técnica: 79.7-81.5% DS)
BRIX_GLUCOSA = 80.6  # °Brix (valor nominal medio de la ficha técnica)
X_SOLIDOS = BRIX_GLUCOSA / 100.0  # Fracción másica de sólidos


def rho_glucosa(T):
    """
    Densidad del jarabe de glucosa en función de la temperatura.
    Correlación lineal ajustada a los 3 puntos de la ficha técnica
    Ingredion 011420 (Globe 1130, 79.7-81.5% DS).

    Datos de la ficha técnica:
      rho(26.7°C) = 1421 kg/m³  (80°F)
      rho(37.8°C) = 1415 kg/m³  (100°F)
      rho(48.9°C) = 1409 kg/m³  (120°F)

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    rho : float — Densidad [kg/m³]
    """
    # rho = a - b·T  (ajuste lineal a ficha técnica Ingredion)
    rho = 1435.4 - 0.540 * T
    return rho


def mu_glucosa(T):
    """
    Viscosidad dinámica del jarabe de glucosa vs temperatura.
    Modelo Vogel-Fulcher-Tammann (VFT) calibrado a ficha técnica
    Ingredion 011420 (Globe 1130, 79.7-81.5% DS, nominal 80.6%).

    Correlación VFT: ln(mu) = A + B / (T_C + C)
      A = -9.349980
      B = 1277.988
      C = 66.898
      T_C = temperatura en °C
      mu en Pa·s

    Datos de la ficha técnica Ingredion 011420:
      mu(26.7°C) = 74,000 cP  (74.0 Pa·s)   — 80°F   ← ajuste exacto
      mu(37.8°C) = 17,400 cP  (17.4 Pa·s)   — 100°F  ← ajuste exacto
      mu(48.9°C) =  5,400 cP  (5.40 Pa·s)   — 120°F  ← ajuste exacto

    Valores del modelo VFT calibrado:
      mu(20°C) ≈ 212,000 cP (212.0 Pa·s)  — extrapolación
      mu(30°C) ≈  46,500 cP  (46.5 Pa·s)
      mu(40°C) ≈  13,500 cP  (13.5 Pa·s)
      mu(50°C) ≈   4,870 cP  (4.87 Pa·s)
      mu(60°C) ≈   2,060 cP  (2.06 Pa·s)
      mu(70°C) ≈     986 cP  (0.986 Pa·s)  — extrapolación
      mu(80°C) ≈     522 cP  (0.522 Pa·s)  — extrapolación

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    mu : float — Viscosidad dinámica [Pa·s]
    """
    # Modelo VFT calibrado a 3 puntos de ficha técnica Ingredion 011420.
    # Ajuste exacto (residuales ~10^-15). Rango interpolación: 26.7-48.9°C.
    A_vft = -9.349980
    B_vft = 1277.988
    C_vft = 66.898
    mu = np.exp(A_vft + B_vft / (T + C_vft))
    return mu


def mu_glucosa_tabular(T):
    """
    Viscosidad dinámica del jarabe de glucosa — interpolación tabular.
    Opción B: Interpolación log-lineal sobre datos de ficha técnica
    Ingredion 011420 + extrapolaciones del modelo VFT calibrado.
    Usar como verificación cruzada del modelo VFT.

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    mu : float — Viscosidad dinámica [Pa·s]
    """
    # 3 puntos de ficha técnica Ingredion 011420 + extensiones VFT calibrado
    T_data = np.array([20.0, 26.7, 37.8, 48.9, 60.0, 70.0, 80.0])
    mu_data = np.array([212.0, 74.0, 17.4, 5.40, 2.06, 0.986, 0.522])  # Pa·s

    # Interpolación log-lineal (log(mu) vs T es casi lineal)
    log_mu = np.interp(T, T_data, np.log(mu_data))
    return np.exp(log_mu)


def Cp_glucosa(T):
    """
    Calor específico del jarabe de glucosa.
    Correlación de Choi & Okos (1986) para soluciones de carbohidratos:
      Cp = Cp_agua · (1 - Xs) + Cp_solido · Xs
    donde Cp_solido(carbohidrato) ≈ 1548.8 + 1.962·T - 5.939e-3·T²

    Ref: Choi, Y. & Okos, M.R. (1986). Effects of Temperature and
         Composition on the Thermal Properties of Foods. Food Engineering
         and Process Applications, Vol. 1, pp. 93-101.

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    Cp : float — Calor específico [J/(kg·°C)]
    """
    Cp_agua = 4182.0 - 0.3 * T  # Simplificación para rango 20-80°C
    Cp_solido = 1548.8 + 1.962 * T - 5.939e-3 * T**2
    Cp = Cp_agua * (1 - X_SOLIDOS) + Cp_solido * X_SOLIDOS
    return Cp


def k_glucosa(T):
    """
    Conductividad térmica del jarabe de glucosa.
    Correlación basada en Choi & Okos (1986) y datos ASHRAE.

    Para jarabe de glucosa a 83 Brix:
      k(20°C) ≈ 0.35 W/(m·°C)
      k(60°C) ≈ 0.38 W/(m·°C)
      k(80°C) ≈ 0.40 W/(m·°C)

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    k : float — Conductividad térmica [W/(m·°C)]
    """
    # k_agua ≈ 0.569 + 0.0019·T - 8e-6·T² (20-80°C)
    k_agua = 0.569 + 0.0019 * T - 8e-6 * T**2
    # k_solido(carbohidrato) ≈ 0.2015 + 1.385e-3·T - 4.331e-6·T²
    k_solido = 0.2015 + 1.385e-3 * T - 4.331e-6 * T**2
    k = k_agua * (1 - X_SOLIDOS) + k_solido * X_SOLIDOS
    return k


def beta_glucosa(T):
    """
    Coeficiente de expansión térmica volumétrica de la glucosa.
    Estimado a partir de la derivada de la densidad con T.
    beta = -(1/rho) * (drho/dT)

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    beta : float — Coeficiente de expansión [1/°C]
    """
    rho = rho_glucosa(T)
    drho_dT = -0.540  # Pendiente de la correlación lineal (ficha técnica Ingredion)
    beta = -drho_dT / rho
    return beta


def Pr_glucosa(T):
    """
    Número de Prandtl de la glucosa.
    Pr = Cp · mu / k

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    Pr : float — Número de Prandtl (adimensional)
    """
    return Cp_glucosa(T) * mu_glucosa(T) / k_glucosa(T)


# =============================================================================
# PROPIEDADES DEL AGUA (lado caliente de la media caña)
# =============================================================================

def rho_agua(T):
    """
    Densidad del agua en función de la temperatura.
    Ajuste polinomial simplificado (Incropera, Apéndice A).

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    rho : float — Densidad [kg/m³]
    """
    return 1000.6 - 0.0128 * T**1.76


def mu_agua(T):
    """
    Viscosidad dinámica del agua vs temperatura.
    Correlación exponencial simplificada.

    Parámetros
    ----------
    T : float — Temperatura [°C]

    Retorna
    -------
    mu : float — Viscosidad dinámica [Pa·s]
    """
    return 2.414e-5 * 10**(247.8 / (T + 133.15))


def Cp_agua(T):
    """
    Calor específico del agua [J/(kg·°C)].
    Prácticamente constante en el rango 20-80°C.
    """
    return 4182.0 - 0.3 * T


def k_agua(T):
    """
    Conductividad térmica del agua [W/(m·°C)].
    """
    return 0.569 + 0.0019 * T - 8e-6 * T**2


def Pr_agua(T):
    """
    Número de Prandtl del agua.
    """
    return Cp_agua(T) * mu_agua(T) / k_agua(T)


# =============================================================================
# PROPIEDADES DEL ACERO SS316L
# =============================================================================

K_SS316L = 16.3  # Conductividad térmica del SS316L [W/(m·°C)] a ~100°C
                  # Ref: ASME Section II Part D, Table TCD


# =============================================================================
# RESUMEN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PROPIEDADES TERMOFISICAS - Proyecto W2605")
    print("=" * 70)

    temps = [20, 30, 40, 50, 60, 70, 80]

    print("\n--- Glucosa Globe 1130 (Ingredion 011420, ~80.6 Brix) ---")
    print(f"{'T [°C]':>8} {'rho [kg/m3]':>12} {'mu [Pa·s]':>12} {'mu [cP]':>12} "
          f"{'Cp [J/kg°C]':>12} {'k [W/m°C]':>10} {'Pr':>10}")
    print("-" * 78)
    for T in temps:
        mu_val = mu_glucosa(T)
        print(f"{T:>8} {rho_glucosa(T):>12.1f} {mu_val:>12.4f} {mu_val*1000:>12.1f} "
              f"{Cp_glucosa(T):>12.1f} {k_glucosa(T):>10.4f} {Pr_glucosa(T):>10.0f}")

    print("\n--- Agua (fluido de calentamiento) ---")
    print(f"{'T [°C]':>8} {'rho [kg/m3]':>12} {'mu [Pa·s]':>12} {'mu [cP]':>12} "
          f"{'Cp [J/kg°C]':>12} {'k [W/m°C]':>10} {'Pr':>10}")
    print("-" * 78)
    for T in temps:
        mu_val = mu_agua(T)
        print(f"{T:>8} {rho_agua(T):>12.1f} {mu_val:>12.6f} {mu_val*1000:>12.3f} "
              f"{Cp_agua(T):>12.1f} {k_agua(T):>10.4f} {Pr_agua(T):>10.2f}")

    print(f"\nConductividad térmica SS316L: {K_SS316L} W/(m·°C)")
