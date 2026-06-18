"""
Cálculo detallado de calentamiento de glucosa Globe 1130
=========================================================
Proyecto W2605 — Caso de estudio de arranque 40 °C → 60 °C.

Objetivo: Calentar distintas masas de glucosa desde 40 °C hasta 60 °C
utilizando un sistema de media caña con área de transferencia de 14 m².

Se calculan escenarios para:
  - 24 ton (masa de un carrotanque).
  - 50 % del volumen operativo del tanque.
  - 80 % del volumen operativo del tanque.
  - Dos temperaturas de agua de calentamiento: 65 °C y 75 °C.
  - Opcionalmente con pérdidas térmicas al ambiente para los casos de tanque.

El modelo:
  - Actualiza las propiedades termofísicas de la glucosa en cada paso.
  - Calcula el coeficiente global U(T) mediante resistencias en serie.
  - Integra el balance de energía transitorio con solve_ivp (RK45).
  - Registra la tasa de calor Q(t) = U(T)·A·(T_agua − T_glucosa).
  - Las pérdidas térmicas se calculan con src/perdidas_termicas_real.py.

Referencias:
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - Churchill & Chu (1975), Int. J. Heat Mass Transfer, 18, 1323.
  - Choi & Okos (1986), Food Engineering and Process Applications, Vol. 1.
  - Ficha técnica Ingredion Globe 1130 011420.
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
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from propiedades_glucosa import (
    rho_glucosa, Cp_glucosa, mu_glucosa, k_glucosa,
    beta_glucosa, Pr_glucosa
)
from coeficiente_U import coeficiente_U
from geometria_tanque import t_HEAD, volumen_total

# Pérdidas térmicas solo para casos de tanque completo
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from perdidas_termicas_real import calcular_perdidas


# =============================================================================
# CONFIGURACIÓN POR DEFECTO DEL CASO DE ESTUDIO
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

# Paleta corporativa
COLOR_65 = '#2E5AAC'
COLOR_75 = '#C44E28'
COLOR_OBJETIVO = '#3A7D44'
COLOR_REJILLA = '#E5E5E5'
COLOR_TEXTO = '#333333'
COLOR_PERDIDAS = '#C44E28'

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


def masa_desde_nivel(nivel_pct, T):
    """Masa de glucosa [kg] para un nivel de llenado [%] a temperatura T."""
    V = volumen_total() * (nivel_pct / 100.0)
    return V * rho_glucosa(T)


def simular_calentamiento(T_agua_in, masa_kg, T_inicial, T_objetivo,
                          area_m2, v_agua, t_final_h=96.0, dt_min=5,
                          con_perdidas=False):
    """
    Simula el calentamiento de una masa fija de glucosa.

    Parámetros
    ----------
    T_agua_in : float — Temperatura de entrada del agua [°C]
    masa_kg : float — Masa de glucosa [kg]
    T_inicial : float — Temperatura inicial [°C]
    T_objetivo : float — Temperatura objetivo [°C]
    area_m2 : float — Área de transferencia [m²]
    v_agua : float — Velocidad del agua en la media caña [m/s]
    t_final_h : float — Tiempo final [h]
    dt_min : float — Paso de salida [min]
    con_perdidas : bool — Si True, resta pérdidas térmicas al ambiente

    Retorna
    -------
    dict con arrays de tiempo, temperatura, U, Q y propiedades.
    """
    # Volumen inicial a T_inicial (constante para la masa fija)
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
        Q_chaq = U_val * area_m2 * DeltaT
        dT = Q_chaq / (m_g * Cp_g)

        # Pérdidas térmicas al ambiente
        if con_perdidas:
            Q_perd = calcular_perdidas(T_g)['Q_W']
            dT -= Q_perd / (m_g * Cp_g)

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
    Q_perd_hist = np.zeros(n)
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
            if con_perdidas:
                Q_perd_hist[i] = calcular_perdidas(T)['Q_W']
        else:
            # Reutilizar último valor válido
            U_hist[i] = U_hist[max(0, i - 1)]
            h_i_hist[i] = h_i_hist[max(0, i - 1)]
            h_o_hist[i] = h_o_hist[max(0, i - 1)]
            Q_hist[i] = 0.0
            Q_perd_hist[i] = Q_perd_hist[max(0, i - 1)]

        rho_hist[i] = rho_glucosa(T)
        Cp_hist[i] = Cp_glucosa(T)
        mu_hist[i] = mu_glucosa(T)
        k_hist[i] = k_glucosa(T)
        Pr_hist[i] = Pr_glucosa(T)
        beta_hist[i] = beta_glucosa(T)

    # Energía acumulada [MJ]
    dt_arr = np.gradient(sol.t)
    Q_MJ = np.cumsum(Q_hist * dt_arr) / 1e6
    Q_perd_MJ = np.cumsum(Q_perd_hist * dt_arr) / 1e6
    Q_neto_MJ = Q_MJ - Q_perd_MJ

    return {
        't_h': t_h,
        'T_g': T_g,
        'U': U_hist,
        'Q_W': Q_hist,
        'Q_MJ': Q_MJ,
        'Q_perd_W': Q_perd_hist,
        'Q_perd_MJ': Q_perd_MJ,
        'Q_neto_MJ': Q_neto_MJ,
        'h_i': h_i_hist,
        'h_o': h_o_hist,
        'rho': rho_hist,
        'Cp': Cp_hist,
        'mu': mu_hist,
        'k': k_hist,
        'Pr': Pr_hist,
        'beta': beta_hist,
        'T_agua': T_agua_in,
        'masa_kg': masa_kg,
        'V0_m3': V_g0,
        'con_perdidas': con_perdidas,
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
        'Q_perd_W': res['Q_perd_W'],
        'Q_perd_acum_MJ': res['Q_perd_MJ'],
        'Q_neto_acum_MJ': res['Q_neto_MJ'],
        'h_i_W_m2C': res['h_i'],
        'h_o_W_m2C': res['h_o'],
        'rho_kg_m3': res['rho'],
        'Cp_J_kgC': res['Cp'],
        'mu_Pa_s': res['mu'],
        'k_W_mC': res['k'],
        'Pr': res['Pr'],
        'beta_1C': res['beta'],
    })
    path = os.path.join(RESULTS_DIR, f'calentamiento_arranque_{etiqueta}.csv')
    df.to_csv(path, index=False, float_format='%.6e')
    return path


def ejecutar_caso(nombre, masa_kg, con_perdidas, t_final_h=T_FINAL_H):
    """Ejecuta un caso de estudio para ambas temperaturas de agua."""
    print(f"\n--- Caso: {nombre} ---")
    print(f"Masa: {masa_kg/1000:.1f} ton | Volumen a 40 °C: {volumen_desde_masa(40, masa_kg):.3f} m³")
    print(f"Pérdidas térmicas: {'Sí' if con_perdidas else 'No'}")

    resultados = {}
    for T_agua in T_AGUA_OPCIONES:
        etiqueta = f"{nombre}_T{int(T_agua)}"
        res = simular_calentamiento(
            T_agua_in=T_agua,
            masa_kg=masa_kg,
            T_inicial=T_INICIAL,
            T_objetivo=T_OBJETIVO,
            area_m2=AREA_TRANSFERENCIA,
            v_agua=V_AGUA,
            t_final_h=t_final_h,
            dt_min=DT_MIN,
            con_perdidas=con_perdidas,
        )
        resultados[etiqueta] = res

        t_60 = tiempo_para_alcanzar(res['t_h'], res['T_g'], T_OBJETIVO)
        if t_60:
            print(f"  Agua {T_agua:.0f} °C: alcanza 60 °C en {t_60:.2f} h ({t_60/24:.2f} días)")
            idx = np.argmin(np.abs(res['t_h'] - t_60))
            E_total = res['Q_MJ'][idx]
            E_perd = res['Q_perd_MJ'][idx]
            E_neto = res['Q_neto_MJ'][idx]
        else:
            print(f"  Agua {T_agua:.0f} °C: no alcanza 60 °C en {t_final_h:.0f} h")
            E_total = res['Q_MJ'][-1]
            E_perd = res['Q_perd_MJ'][-1]
            E_neto = res['Q_neto_MJ'][-1]

        print(f"    Q máx: {np.max(res['Q_W'])/1000:.2f} kW | U inicial: {res['U'][0]:.2f} W/(m²·°C)")
        print(f"    Energía chaqueta: {E_total:.2f} MJ | Pérdidas: {E_perd:.2f} MJ | Neto: {E_neto:.2f} MJ")

        csv_path = guardar_csv(res, etiqueta)
        print(f"    CSV: {csv_path}")

    return resultados


# =============================================================================
# GRÁFICAS
# =============================================================================

def graficar_comparativa_todos(casos, t_final_h=T_FINAL_H):
    """Genera figuras comparativas de todos los casos."""
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Figura 1: T vs t comparativa
    fig, ax = plt.subplots(figsize=(12, 7))
    for nombre, resultados in casos.items():
        for etiqueta, color in [(f"{nombre}_T65", COLOR_65), (f"{nombre}_T75", COLOR_75)]:
            if etiqueta in resultados:
                res = resultados[etiqueta]
                linestyle = '-' if not res['con_perdidas'] else '--'
                ax.plot(res['t_h'], res['T_g'], color=color, linewidth=2,
                        linestyle=linestyle, label=f"{nombre} — {res['T_agua']:.0f} °C")

    ax.axhline(y=T_OBJETIVO, color=COLOR_OBJETIVO, linestyle='--', linewidth=1.5,
               label=f"Objetivo: {T_OBJETIVO:.0f} °C")
    ax.axhline(y=T_INICIAL, color=COLOR_TEXTO, linestyle=':', alpha=0.5,
               label=f"Inicial: {T_INICIAL:.0f} °C")

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura de la glucosa [°C]')
    ax.set_title('Curvas de arranque 40 °C → 60 °C — comparación de casos')
    ax.legend(loc='lower right', framealpha=0.95, fontsize=8)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, t_final_h)
    ax.set_ylim(T_INICIAL - 2, max(T_AGUA_OPCIONES) + 2)

    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_T_vs_t_comparativa.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_T_vs_t_comparativa.pdf'))
    plt.close(fig)
    print("  Guardada: curva_arranque_T_vs_t_comparativa.pdf/.png")

    # Figura 2: Q vs t comparativa
    fig, ax = plt.subplots(figsize=(12, 7))
    for nombre, resultados in casos.items():
        for etiqueta, color in [(f"{nombre}_T65", COLOR_65), (f"{nombre}_T75", COLOR_75)]:
            if etiqueta in resultados:
                res = resultados[etiqueta]
                linestyle = '-' if not res['con_perdidas'] else '--'
                ax.plot(res['t_h'], res['Q_W'] / 1000, color=color, linewidth=2,
                        linestyle=linestyle, label=f"{nombre} — {res['T_agua']:.0f} °C")

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Flujo de calor [kW]')
    ax.set_title('Flujo de calor transferido — comparación de casos')
    ax.legend(loc='upper right', framealpha=0.95, fontsize=8)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, t_final_h)

    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_Q_vs_t_comparativa.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_Q_vs_t_comparativa.pdf'))
    plt.close(fig)
    print("  Guardada: curva_arranque_Q_vs_t_comparativa.pdf/.png")

    # Figura 3: panel por caso, T vs t
    n_casos = len(casos)
    fig, axes = plt.subplots(1, n_casos, figsize=(5 * n_casos, 5), sharey=True)
    if n_casos == 1:
        axes = [axes]

    for ax, (nombre, resultados) in zip(axes, casos.items()):
        for etiqueta, color in [(f"{nombre}_T65", COLOR_65), (f"{nombre}_T75", COLOR_75)]:
            if etiqueta in resultados:
                res = resultados[etiqueta]
                ax.plot(res['t_h'], res['T_g'], color=color, linewidth=2,
                        label=f"Agua {res['T_agua']:.0f} °C")
        ax.axhline(y=T_OBJETIVO, color=COLOR_OBJETIVO, linestyle='--', linewidth=1.5)
        ax.set_xlabel('Tiempo [h]')
        ax.set_title(nombre)
        ax.legend(loc='lower right', framealpha=0.95)
        ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
        ax.set_xlim(0, t_final_h)

    axes[0].set_ylabel('Temperatura [°C]')
    fig.suptitle('Curvas de arranque por caso')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_por_caso.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_por_caso.pdf'))
    plt.close(fig)
    print("  Guardada: curva_arranque_por_caso.pdf/.png")

    # Figura 4: energía acumulada neta (chaqueta − pérdidas)
    fig, ax = plt.subplots(figsize=(12, 7))
    for nombre, resultados in casos.items():
        for etiqueta, color in [(f"{nombre}_T65", COLOR_65), (f"{nombre}_T75", COLOR_75)]:
            if etiqueta in resultados and resultados[etiqueta]['con_perdidas']:
                res = resultados[etiqueta]
                ax.plot(res['t_h'], res['Q_neto_MJ'], color=color, linewidth=2,
                        linestyle='-', label=f"{nombre} — {res['T_agua']:.0f} °C")

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Energía neta acumulada [MJ]')
    ax.set_title('Energía neta aprovechada (chaqueta − pérdidas) — casos con pérdidas')
    ax.legend(loc='lower right', framealpha=0.95, fontsize=8)
    ax.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax.set_xlim(0, t_final_h)

    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_E_neta_acum.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'curva_arranque_E_neta_acum.pdf'))
    plt.close(fig)
    print("  Guardada: curva_arranque_E_neta_acum.pdf/.png")


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == '__main__':
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("=" * 80)
    print("CALENTAMIENTO DE ARRANQUE — Glucosa Globe 1130: 40 °C -> 60 °C")
    print(f"Área de transferencia: {AREA_TRANSFERENCIA} m²")
    print(f"Velocidad del agua: {V_AGUA} m/s")
    print("=" * 80)

    # Definición de casos
    casos = {}

    # Caso 1: 24 ton (carrotanque) — sin pérdidas (referencia ideal)
    casos['24ton'] = ejecutar_caso(
        nombre='24ton',
        masa_kg=24_000.0,
        con_perdidas=False,
        t_final_h=T_FINAL_H,
    )

    # Caso 2: 50 % del tanque — con pérdidas
    masa_50 = masa_desde_nivel(50.0, T_INICIAL)
    casos['50pct'] = ejecutar_caso(
        nombre='50pct',
        masa_kg=masa_50,
        con_perdidas=True,
        t_final_h=T_FINAL_H,
    )

    # Caso 3: 80 % del tanque — con pérdidas
    masa_80 = masa_desde_nivel(80.0, T_INICIAL)
    casos['80pct'] = ejecutar_caso(
        nombre='80pct',
        masa_kg=masa_80,
        con_perdidas=True,
        t_final_h=T_FINAL_H,
    )

    # Generar figuras comparativas
    print("\n" + "=" * 80)
    print("Generando figuras comparativas...")
    print("=" * 80)
    graficar_comparativa_todos(casos, t_final_h=T_FINAL_H)

    print("\n" + "=" * 80)
    print("Simulaciones completadas. Figuras guardadas en:", FIGURES_DIR)
    print("=" * 80)
