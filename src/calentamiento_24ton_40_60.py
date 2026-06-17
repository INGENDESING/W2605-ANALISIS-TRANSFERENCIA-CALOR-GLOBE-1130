"""
Cálculo detallado de calentamiento de 24 ton de glucosa Globe 42 DE
=====================================================================
Proyecto W2605 — Caso de estudio adicional

Objetivo: Calentar 24 toneladas de glucosa desde 40 °C hasta 60 °C
utilizando un sistema de media caña con área de transferencia de 14 m².

Se calculan dos escenarios de temperatura de agua de calentamiento:
  - Escenario A: agua a 65 °C
  - Escenario B: agua a 75 °C

El modelo:
  - Actualiza las propiedades termofísicas de la glucosa en cada paso.
  - Calcula el coeficiente global U(T) mediante resistencias en serie.
  - Integra el balance de energía transitorio con solve_ivp (RK45).
  - Registra la tasa de calor Q(t) = U(T)·A·(T_agua – T_glucosa).
  - No incluye pérdidas térmicas al ambiente (tanque ideal aislado).

Referencias:
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - Churchill & Chu (1975), Int. J. Heat Mass Transfer, 18, 1323.
  - Choi & Okos (1986), Food Engineering and Process Applications, Vol. 1.
  - Ficha técnica Ingredion Globe 42 DE 011420.
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Importar módulos del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from propiedades_glucosa import (
    rho_glucosa, Cp_glucosa, mu_glucosa, k_glucosa,
    beta_glucosa, Pr_glucosa
)
from coeficiente_U import coeficiente_U
from geometria_tanque import t_HEAD


# =============================================================================
# CONFIGURACIÓN DEL CASO DE ESTUDIO
# =============================================================================
MASA_KG = 24_000.0          # Masa de glucosa [kg]
T_INICIAL = 40.0            # Temperatura inicial [°C]
T_OBJETIVO = 60.0           # Temperatura objetivo [°C]
AREA_TRANSFERENCIA = 14.0   # Área de transferencia [m²]
V_AGUA = 2.5                # Velocidad del agua en media caña [m/s]
T_AGUA_OPCIONES = [65.0, 75.0]  # Temperaturas de agua a evaluar [°C]
T_FINAL_H = 96.0            # Tiempo máximo de simulación [h]
DT_MIN = 5                  # Paso de salida [min]

# Directorios de salida
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Paleta corporativa
COLOR_65 = '#2E5AAC'
COLOR_75 = '#C44E28'
COLOR_OBJETIVO = '#3A7D44'
COLOR_REJILLA = '#E5E5E5'
COLOR_TEXTO = '#333333'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'axes.edgecolor': COLOR_TEXTO,
    'axes.labelcolor': COLOR_TEXTO,
    'xtick.color': COLOR_TEXTO,
    'ytick.color': COLOR_TEXTO,
    'text.color': COLOR_TEXTO,
})


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def volumen_desde_masa(T, masa_kg):
    """Volumen de glucosa [m³] para una masa dada a temperatura T."""
    return masa_kg / rho_glucosa(T)


def simular_calentamiento(T_agua_in, masa_kg, T_inicial, T_objetivo,
                          area_m2, v_agua, t_final_h=96.0, dt_min=5):
    """
    Simula el calentamiento de una masa fija de glucosa.

    Parámetros
    ----------
    T_agua_in : float — Temperatura de entrada del agua [°C]
    masa_kg : float — Masa de glucosa [kg]
    T_inicial : float — Temperatura inicial [°C]
    T_objetivo : float — Temperatura objetivo [°C]
    area_m2 : float — Área de transferencia [m²]
    v_agua : float — Velocidad del agua [m/s]
    t_final_h : float — Tiempo final [h]
    dt_min : float — Paso de salida [min]

    Retorna
    -------
    dict con arrays de tiempo, temperatura, U, Q y propiedades.
    """
    # Volumen inicial a T_inicial
    V_g0 = volumen_desde_masa(T_inicial, masa_kg)

    def dTdt(t, T_g_arr):
        T_g = T_g_arr[0]
        if T_g >= T_agua_in - 0.05:
            return [0.0]

        # Propiedades a temperatura actual
        rho_g = rho_glucosa(T_g)
        Cp_g = Cp_glucosa(T_g)
        m_g = rho_g * V_g0  # Masa constante

        # Coeficiente global U(T)
        U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T_g)

        # Tasa de calor al tanque
        DeltaT = T_agua_in - T_g
        dT = U_val * area_m2 * DeltaT / (m_g * Cp_g)
        return [dT]

    t_span = (0, t_final_h * 3600)
    t_eval = np.arange(0, t_final_h * 3600 + 1, dt_min * 60)

    sol = solve_ivp(dTdt, t_span, [T_inicial], t_eval=t_eval,
                    method='RK45', max_step=300, rtol=1e-6, atol=1e-9)

    t_h = sol.t / 3600.0
    T_g = sol.y[0]

    # Calcular variables secundarias en cada punto
    n = len(T_g)
    U_hist = np.zeros(n)
    Q_hist = np.zeros(n)
    h_i_hist = np.zeros(n)
    h_o_hist = np.zeros(n)
    rho_hist = np.zeros(n)
    Cp_hist = np.zeros(n)
    mu_hist = np.zeros(n)
    k_hist = np.zeros(n)
    Pr_hist = np.zeros(n)
    beta_hist = np.zeros(n)

    for i, T in enumerate(T_g):
        if T < T_agua_in - 0.05:
            U_val, h_i, h_o, info = coeficiente_U(v_agua, T_agua_in, T)
            U_hist[i] = U_val
            h_i_hist[i] = h_i
            h_o_hist[i] = h_o
            Q_hist[i] = U_val * area_m2 * (T_agua_in - T)
        else:
            # Reutilizar último valor válido
            U_hist[i] = U_hist[max(0, i - 1)]
            h_i_hist[i] = h_i_hist[max(0, i - 1)]
            h_o_hist[i] = h_o_hist[max(0, i - 1)]
            Q_hist[i] = 0.0

        rho_hist[i] = rho_glucosa(T)
        Cp_hist[i] = Cp_glucosa(T)
        mu_hist[i] = mu_glucosa(T)
        k_hist[i] = k_glucosa(T)
        Pr_hist[i] = Pr_glucosa(T)
        beta_hist[i] = beta_glucosa(T)

    # Energía acumulada [MJ]
    Q_MJ = np.cumsum(Q_hist * np.gradient(sol.t)) / 1e6

    return {
        't_h': t_h,
        'T_g': T_g,
        'U': U_hist,
        'Q_W': Q_hist,
        'Q_MJ': Q_MJ,
        'h_i': h_i_hist,
        'h_o': h_o_hist,
        'rho': rho_hist,
        'Cp': Cp_hist,
        'mu': mu_hist,
        'k': k_hist,
        'Pr': Pr_hist,
        'beta': beta_hist,
        'T_agua': T_agua_in,
    }


def tiempo_para_alcanzar(t_h, T_g, T_objetivo):
    """Interpola el tiempo [h] para alcanzar T_objetivo."""
    idx = np.where(T_g >= T_objetivo)[0]
    if len(idx) > 0:
        return t_h[idx[0]]
    return None


def guardar_csv(res, etiqueta):
    """Exporta resultados a CSV."""
    df = pd.DataFrame({
        't_h': res['t_h'],
        'T_glucosa_C': res['T_g'],
        'U_W_m2C': res['U'],
        'Q_W': res['Q_W'],
        'Q_acum_MJ': res['Q_MJ'],
        'h_i_W_m2C': res['h_i'],
        'h_o_W_m2C': res['h_o'],
        'rho_kg_m3': res['rho'],
        'Cp_J_kgC': res['Cp'],
        'mu_Pa_s': res['mu'],
        'k_W_mC': res['k'],
        'Pr': res['Pr'],
        'beta_1C': res['beta'],
    })
    path = os.path.join(RESULTS_DIR, f'calentamiento_24ton_40_60_{etiqueta}.csv')
    df.to_csv(path, index=False, float_format='%.6e')
    return path


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == '__main__':
    print("=" * 80)
    print("CALENTAMIENTO DE 24 TON DE GLUCOSA GLOBE 42 DE: 40 °C -> 60 °C")
    print(f"Área de transferencia: {AREA_TRANSFERENCIA} m²")
    print(f"Velocidad del agua: {V_AGUA} m/s")
    print("=" * 80)

    # Volumen inicial
    V0 = volumen_desde_masa(T_INICIAL, MASA_KG)
    print(f"\nMasa de glucosa: {MASA_KG/1000:.1f} ton")
    print(f"Volumen a {T_INICIAL:.0f} °C: {V0:.3f} m³")
    print(f"Densidad a {T_INICIAL:.0f} °C: {rho_glucosa(T_INICIAL):.1f} kg/m³")
    print(f"Densidad a {T_OBJETIVO:.0f} °C: {rho_glucosa(T_OBJETIVO):.1f} kg/m³")

    resultados = {}
    for T_agua in T_AGUA_OPCIONES:
        etiqueta = f"T{int(T_agua)}"
        print(f"\n--- Escenario agua a {T_agua:.0f} °C ---")
        res = simular_calentamiento(
            T_agua_in=T_agua,
            masa_kg=MASA_KG,
            T_inicial=T_INICIAL,
            T_objetivo=T_OBJETIVO,
            area_m2=AREA_TRANSFERENCIA,
            v_agua=V_AGUA,
            t_final_h=T_FINAL_H,
            dt_min=DT_MIN,
        )
        resultados[etiqueta] = res

        t_60 = tiempo_para_alcanzar(res['t_h'], res['T_g'], T_OBJETIVO)
        print(f"Tiempo para alcanzar {T_OBJETIVO:.0f} °C: {t_60:.2f} h "
              f"({t_60/24:.2f} días)" if t_60 else "No alcanza 60 °C")

        # Energía total hasta 60 °C
        if t_60:
            idx = np.argmin(np.abs(res['t_h'] - t_60))
            E_total = res['Q_MJ'][idx]
        else:
            E_total = res['Q_MJ'][-1]
        print(f"Energía total transferida: {E_total:.2f} MJ")
        print(f"Q máximo: {np.max(res['Q_W'])/1000:.2f} kW")
        print(f"U a {T_INICIAL:.0f} °C: {res['U'][0]:.2f} W/(m²·°C)")
        print(f"U a {T_OBJETIVO:.0f} °C: {res['U'][-1]:.2f} W/(m²·°C)")

        csv_path = guardar_csv(res, etiqueta)
        print(f"CSV guardado: {csv_path}")

    # =============================================================================
    # GRÁFICA 1: Curva de calentamiento T vs t (ambos escenarios)
    # =============================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    for etiqueta, color in [('T65', COLOR_65), ('T75', COLOR_75)]:
        res = resultados[etiqueta]
        ax.plot(res['t_h'], res['T_g'], color=color, linewidth=2,
                label=f"Agua a {res['T_agua']:.0f} °C")

    ax.axhline(y=T_OBJETIVO, color=COLOR_OBJETIVO, linestyle='--', linewidth=1.5,
               label=f"Objetivo: {T_OBJETIVO:.0f} °C")
    ax.axhline(y=T_INICIAL, color=COLOR_TEXTO, linestyle=':', alpha=0.5,
               label=f"Inicial: {T_INICIAL:.0f} °C")

    # Anotaciones de tiempo objetivo
    for etiqueta, color in [('T65', COLOR_65), ('T75', COLOR_75)]:
        res = resultados[etiqueta]
        t_60 = tiempo_para_alcanzar(res['t_h'], res['T_g'], T_OBJETIVO)
        if t_60:
            ax.plot(t_60, T_OBJETIVO, 'o', color=color, markersize=8)
            ax.annotate(f"{t_60:.1f} h", xy=(t_60, T_OBJETIVO),
                        xytext=(t_60 + 2, T_OBJETIVO + (2 if etiqueta == 'T65' else -3)),
                        fontsize=9, color=color,
                        arrowprops=dict(arrowstyle='->', color=color, lw=0.8))

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura de la glucosa [°C]')
    ax.set_title('Calentamiento de 24 ton de glucosa Globe 42 DE (40 °C a 60 °C)')
    ax.legend(loc='lower right', framealpha=0.95)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, min(T_FINAL_H, max([tiempo_para_alcanzar(r['t_h'], r['T_g'], T_OBJETIVO) or T_FINAL_H
                                        for r in resultados.values()]) * 1.3))
    ax.set_ylim(T_INICIAL - 2, max(T_AGUA_OPCIONES) + 2)

    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_T_vs_t.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_T_vs_t.pdf'))
    plt.close(fig)

    # =============================================================================
    # GRÁFICA 2: Flujo de calor Q vs t
    # =============================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    for etiqueta, color in [('T65', COLOR_65), ('T75', COLOR_75)]:
        res = resultados[etiqueta]
        ax.plot(res['t_h'], res['Q_W'] / 1000, color=color, linewidth=2,
                label=f"Agua a {res['T_agua']:.0f} °C")

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Flujo de calor [kW]')
    ax.set_title('Flujo de calor transferido a la glucosa (propiedades variables)')
    ax.legend(loc='upper right', framealpha=0.95)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, min(T_FINAL_H, max([tiempo_para_alcanzar(r['t_h'], r['T_g'], T_OBJETIVO) or T_FINAL_H
                                        for r in resultados.values()]) * 1.3))

    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_Q_vs_t.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_Q_vs_t.pdf'))
    plt.close(fig)

    # =============================================================================
    # GRÁFICA 3: Coeficiente global U vs t
    # =============================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    for etiqueta, color in [('T65', COLOR_65), ('T75', COLOR_75)]:
        res = resultados[etiqueta]
        ax.plot(res['t_h'], res['U'], color=color, linewidth=2,
                label=f"Agua a {res['T_agua']:.0f} °C")

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('U [W/(m²·°C)]')
    ax.set_title('Coeficiente global de transferencia de calor U(T)')
    ax.legend(loc='lower right', framealpha=0.95)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, min(T_FINAL_H, max([tiempo_para_alcanzar(r['t_h'], r['T_g'], T_OBJETIVO) or T_FINAL_H
                                        for r in resultados.values()]) * 1.3))

    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_U_vs_t.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_U_vs_t.pdf'))
    plt.close(fig)

    # =============================================================================
    # GRÁFICA 4: Propiedades termofísicas de la glucosa vs temperatura
    # =============================================================================
    T_range = np.linspace(T_INICIAL, T_OBJETIVO, 100)
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))

    ax = axes[0, 0]
    ax.plot(T_range, rho_glucosa(T_range), color=COLOR_65, linewidth=2)
    ax.set_xlabel('T [°C]')
    ax.set_ylabel(r'$\rho$ [kg/m³]')
    ax.set_title('Densidad de la glucosa')
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)

    ax = axes[0, 1]
    ax.plot(T_range, Cp_glucosa(T_range), color=COLOR_65, linewidth=2)
    ax.set_xlabel('T [°C]')
    ax.set_ylabel(r'$C_p$ [J/(kg·°C)]')
    ax.set_title('Calor específico de la glucosa')
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)

    ax = axes[1, 0]
    ax.semilogy(T_range, mu_glucosa(T_range) * 1000, color=COLOR_65, linewidth=2)
    ax.set_xlabel('T [°C]')
    ax.set_ylabel(r'$\mu$ [cP]')
    ax.set_title('Viscosidad dinámica de la glucosa')
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)

    ax = axes[1, 1]
    ax.plot(T_range, k_glucosa(T_range), color=COLOR_65, linewidth=2)
    ax.set_xlabel('T [°C]')
    ax.set_ylabel(r'$k$ [W/(m·°C)]')
    ax.set_title('Conductividad térmica de la glucosa')
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)

    fig.suptitle('Propiedades termofísicas de la glucosa Globe 42 DE (40–60 °C)')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_propiedades.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'calentamiento_24ton_propiedades.pdf'))
    plt.close(fig)

    print("\n" + "=" * 80)
    print("Figuras guardadas en:", FIGURES_DIR)
    print("=" * 80)
