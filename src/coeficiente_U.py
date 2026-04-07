"""
Módulo de cálculo del coeficiente global de transferencia de calor U
=====================================================================
Proyecto P2611 — Tanque de glucosa INGREDION

Modelo de resistencias en serie:
  1/U = 1/h_i + e_w/k_w + 1/h_o

Donde:
  h_i  = coeficiente convectivo interno (agua en media caña) [W/m²·°C]
  e_w  = espesor de pared del tanque SS316L = 0.009 m
  k_w  = conductividad térmica SS316L ≈ 16.3 W/(m·°C)
  h_o  = coeficiente convectivo externo (glucosa, convección natural) [W/m²·°C]

Refs:
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - Perry's Chemical Engineers' Handbook, 8th ed., Sec. 11
  - Kern, Process Heat Transfer, 1950, Cap. 18
"""

import numpy as np
from propiedades_glucosa import (
    mu_agua, rho_agua, Cp_agua, k_agua, Pr_agua,
    mu_glucosa, rho_glucosa, Cp_glucosa, k_glucosa, Pr_glucosa,
    beta_glucosa, K_SS316L
)
from geometria_tanque import (
    diametro_hidraulico_media_cana, area_flujo_media_cana,
    t_HEAD, A_CONTACTO
)


# =============================================================================
# COEFICIENTE INTERNO h_i (LADO AGUA EN LA MEDIA CAÑA)
# =============================================================================

def reynolds_agua(v_agua, T_agua):
    """
    Número de Reynolds del agua en la media caña.
    Re = rho · v · D_h / mu

    Parámetros
    ----------
    v_agua : float — Velocidad del agua en la media caña [m/s]
    T_agua : float — Temperatura media del agua [°C]

    Retorna
    -------
    Re : float — Número de Reynolds
    """
    D_h = diametro_hidraulico_media_cana()
    rho = rho_agua(T_agua)
    mu = mu_agua(T_agua)
    Re = rho * v_agua * D_h / mu
    return Re


def h_interno_sieder_tate(v_agua, T_agua, T_pared=None):
    """
    Coeficiente convectivo del lado del agua (media caña rectangular).
    Correlación de Sieder-Tate para flujo turbulento en conductos:

      Nu = 0.027 · Re^0.8 · Pr^(1/3) · (mu/mu_w)^0.14

    Válida para Re > 10,000 y L/D_h > 10.
    Ref: Incropera et al., 7th ed., Ec. 8.62

    Parámetros
    ----------
    v_agua  : float — Velocidad del agua [m/s]
    T_agua  : float — Temperatura media del agua [°C]
    T_pared : float — Temperatura de la pared [°C] (para corrección mu/mu_w)

    Retorna
    -------
    h_i : float — Coeficiente convectivo [W/m²·°C]
    Re  : float — Número de Reynolds
    Nu  : float — Número de Nusselt
    """
    D_h = diametro_hidraulico_media_cana()
    Re = reynolds_agua(v_agua, T_agua)
    Pr = Pr_agua(T_agua)

    # Corrección por viscosidad en la pared
    if T_pared is None:
        T_pared = T_agua - 5  # Estimación
    mu_bulk = mu_agua(T_agua)
    mu_wall = mu_agua(T_pared)
    corr_mu = (mu_bulk / mu_wall) ** 0.14

    if Re < 10000:
        # Flujo laminar o transición — usar Sieder-Tate laminar
        # Nu = 1.86 · (Re·Pr·D_h/L)^(1/3) · (mu/mu_w)^0.14
        # Para L largo, Nu → 3.66 (mínimo para canal)
        Nu = max(3.66, 0.027 * Re**0.8 * Pr**(1/3) * corr_mu)
    else:
        # Flujo turbulento
        Nu = 0.027 * Re**0.8 * Pr**(1/3) * corr_mu

    k = k_agua(T_agua)
    h_i = Nu * k / D_h
    return h_i, Re, Nu


# =============================================================================
# COEFICIENTE EXTERNO h_o (LADO GLUCOSA — CONVECCIÓN NATURAL)
# =============================================================================

def h_externo_conveccion_natural(T_superficie, T_glucosa, L_car=None):
    """
    Coeficiente convectivo del lado de la glucosa por convección natural.
    Correlación de Churchill-Chu para convección natural sobre superficie caliente:

      Nu_L = [0.825 + 0.387·Ra_L^(1/6) / (1 + (0.492/Pr)^(9/16))^(8/27)]²

    Válida para todo el rango de Ra_L (laminar + turbulento).
    Ref: Churchill & Chu (1975), Int. J. Heat Mass Transfer, 18, 1323.
         Incropera et al., 7th ed., Ec. 9.26

    Parámetros
    ----------
    T_superficie : float — Temperatura de la superficie del tanque [°C]
    T_glucosa    : float — Temperatura bulk de la glucosa [°C]
    L_car        : float — Longitud característica [m] (default: estimación)

    Retorna
    -------
    h_o  : float — Coeficiente convectivo [W/m²·°C]
    Ra   : float — Número de Rayleigh
    Nu_L : float — Número de Nusselt
    """
    # Longitud característica: para fondo toriesférico ≈ altura del fondo
    if L_car is None:
        L_car = 1.0  # ~1 m como longitud representativa

    # Propiedades evaluadas a temperatura de película
    T_film = (T_superficie + T_glucosa) / 2
    Delta_T = abs(T_superficie - T_glucosa)

    if Delta_T < 0.1:
        # Sin diferencia de temperatura, h_o mínimo
        return 1.0, 0.0, 0.825**2

    rho = rho_glucosa(T_film)
    mu = mu_glucosa(T_film)
    Cp = Cp_glucosa(T_film)
    k = k_glucosa(T_film)
    beta = beta_glucosa(T_film)
    nu = mu / rho  # Viscosidad cinemática [m²/s]
    alpha = k / (rho * Cp)  # Difusividad térmica [m²/s]
    Pr = nu / alpha

    # Número de Grashof
    g = 9.81  # [m/s²]
    Gr = g * beta * Delta_T * L_car**3 / nu**2

    # Número de Rayleigh
    Ra = Gr * Pr

    # Churchill-Chu
    denom = (1 + (0.492 / Pr)**(9.0/16))**(8.0/27)
    Nu_L = (0.825 + 0.387 * Ra**(1.0/6) / denom)**2

    h_o = Nu_L * k / L_car
    return h_o, Ra, Nu_L


# =============================================================================
# COEFICIENTE GLOBAL U
# =============================================================================

def coeficiente_U(v_agua, T_agua_media, T_glucosa, T_pared=None, L_car=None):
    """
    Coeficiente global de transferencia de calor U.

    1/U = 1/h_i + e_w/k_w + 1/h_o

    Parámetros
    ----------
    v_agua       : float — Velocidad del agua en la media caña [m/s]
    T_agua_media : float — Temperatura media del agua [°C]
    T_glucosa    : float — Temperatura bulk de la glucosa [°C]
    T_pared      : float — Temperatura estimada de la pared [°C]
    L_car        : float — Longitud característica para h_o [m]

    Retorna
    -------
    U    : float — Coeficiente global [W/m²·°C]
    h_i  : float — Coeficiente interno [W/m²·°C]
    h_o  : float — Coeficiente externo [W/m²·°C]
    info : dict  — Información detallada del cálculo
    """
    e_w = t_HEAD  # Espesor de pared [m]
    k_w = K_SS316L  # Conductividad SS316L [W/m·°C]

    # Temperatura de pared estimada (promedio agua-glucosa)
    if T_pared is None:
        T_pared = (T_agua_media + T_glucosa) / 2

    # Lado agua (interno)
    h_i, Re_agua, Nu_agua = h_interno_sieder_tate(v_agua, T_agua_media, T_pared)

    # Lado glucosa (externo — convección natural)
    T_sup = T_pared  # Temperatura de la superficie del tanque
    h_o, Ra, Nu_gluc = h_externo_conveccion_natural(T_sup, T_glucosa, L_car)

    # Resistencias
    R_i = 1.0 / h_i
    R_w = e_w / k_w
    R_o = 1.0 / h_o
    R_total = R_i + R_w + R_o

    U = 1.0 / R_total

    info = {
        'h_i': h_i, 'h_o': h_o, 'U': U,
        'Re_agua': Re_agua, 'Nu_agua': Nu_agua,
        'Ra_glucosa': Ra, 'Nu_glucosa': Nu_gluc,
        'R_i': R_i, 'R_w': R_w, 'R_o': R_o, 'R_total': R_total,
        'pct_R_i': R_i/R_total*100, 'pct_R_w': R_w/R_total*100,
        'pct_R_o': R_o/R_total*100,
        'T_pared': T_pared,
        'mu_glucosa_film': mu_glucosa((T_sup + T_glucosa)/2)
    }
    return U, h_i, h_o, info


# =============================================================================
# RESUMEN
# =============================================================================

if __name__ == "__main__":
    print("=" * 75)
    print("CALCULO DEL COEFICIENTE U — Proyecto P2611")
    print("=" * 75)

    # --- Escenario 1: Q = 30.9 m³/h → v = 1.34 m/s ---
    print("\n--- ESCENARIO 1: v_agua = 1.34 m/s ---")
    temps_glucosa = [20, 30, 40, 50, 60]
    T_agua_in = 65.0  # Estimación para escenario 1

    print(f"{'T_gluc':>8} {'T_agua':>8} {'h_i':>10} {'h_o':>10} {'U':>10} "
          f"{'Re':>10} {'Ra':>12} {'%R_i':>6} {'%R_w':>6} {'%R_o':>6}")
    print("-" * 95)
    for T_g in temps_glucosa:
        T_w = T_agua_in
        U, h_i, h_o, info = coeficiente_U(1.338, T_w, T_g)
        print(f"{T_g:>8.0f} {T_w:>8.0f} {h_i:>10.1f} {h_o:>10.2f} {U:>10.2f} "
              f"{info['Re_agua']:>10.0f} {info['Ra_glucosa']:>12.1e} "
              f"{info['pct_R_i']:>6.1f} {info['pct_R_w']:>6.1f} {info['pct_R_o']:>6.1f}")

    # --- Escenarios 2/3: v = 2.5 m/s ---
    for T_agua_esc, esc_name in [(65, "ESCENARIO 2: agua 65°C"), (75, "ESCENARIO 3: agua 75°C")]:
        print(f"\n--- {esc_name}, v_agua = 2.5 m/s ---")
        print(f"{'T_gluc':>8} {'T_agua':>8} {'h_i':>10} {'h_o':>10} {'U':>10} "
              f"{'Re':>10} {'Ra':>12} {'%R_i':>6} {'%R_w':>6} {'%R_o':>6}")
        print("-" * 95)
        for T_g in temps_glucosa:
            U, h_i, h_o, info = coeficiente_U(2.5, T_agua_esc, T_g)
            print(f"{T_g:>8.0f} {T_agua_esc:>8.0f} {h_i:>10.1f} {h_o:>10.2f} {U:>10.2f} "
                  f"{info['Re_agua']:>10.0f} {info['Ra_glucosa']:>12.1e} "
                  f"{info['pct_R_i']:>6.1f} {info['pct_R_w']:>6.1f} {info['pct_R_o']:>6.1f}")
