#!/usr/bin/env python3
"""
Simulación de ciclo de descargas — Proyecto W2605
==================================================
Caso: chaqueta de 14 m², agua a 65 °C / 75 °C, doble entrada, velocidad 2,5 m/s.

Objetivo:
  Evaluar la factibilidad de realizar 5 descargas diarias de 24 ton
  (≈ 17,1 m³ a 55 °C) con un flujo de descarga de 12 ton/h (≈ 8,5 m³/h a 55 °C),
  dejando entre descargas únicamente tiempo de calentamiento.

Modelo:
  - Tanque precalentado al nivel inicial (% de capacidad) a 60 °C.
  - Durante descarga:
      * Entra glucosa a 55 °C a 12 ton/h (≈ 8,5 m³/h).
      * Sale glucosa hacia el carrotanque a la temperatura del tanque.
      * Volumen/masa del tanque se mantiene aproximadamente constante.
      * Balance energético: chaqueta + aporte de glucosa entrante - pérdidas.
  - Entre descargas:
      * Calentamiento puro con chaqueta, compensando pérdidas.
      * La siguiente descarga comienza a los 4,8 h desde el inicio de la
        anterior (ciclo de 5 descargas/día) o cuando se recupera 60 °C,
        lo que ocurra primero.

Escenarios evaluados:
  - Nivel inicial 80 %, agua 75 °C (caso oficial).
  - Nivel inicial 80 %, agua 65 °C.
  - Nivel inicial 50 %, agua 75 °C.
  - Nivel inicial 50 %, agua 65 °C.
  - Arranque desde 40 °C con agua 75 °C hasta primera descarga a 57 °C.

Referencias:
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - Kern, Process Heat Transfer, Cap. 18 (Jacketed Vessels).
  - Perry's Chemical Engineers' Handbook, 8th ed., Sec. 11.
"""

import os
import sys
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from coeficiente_U import coeficiente_U
from geometria_tanque import volumen_total
from perdidas_termicas_real import calcular_perdidas


# =============================================================================
# CONFIGURACIÓN DE GRÁFICAS
# =============================================================================

COLOR_GLUCOSA = '#2E5AAC'
COLOR_AGUA = '#C44E28'
COLOR_DESCARGA = '#3A7D44'
COLOR_BANDA = '#F4A261'
COLOR_REJILLA = '#E5E5E5'
COLOR_TEXTO = '#333333'
COLOR_BLOQUE = '#F7F7F7'
COLOR_BORDE = '#555555'

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
# PARÁMETROS DEL CICLO
# =============================================================================

A_TRANSFERENCIA = 14.0      # m² (chaqueta según requerimiento)
V_AGUA = 2.5                # m/s
T_ENTRADA_GLUCOSA = 55.0    # °C (glucosa de alimentación)
M_DOT_DESCARGA = 12000.0 / 3600.0  # kg/s (12 ton/h)
MASA_POR_DESCARGA = 24000.0 # kg (24 ton)
N_DESCARGAS = 5
T_TOTAL = 24.0              # h
T_OBJETIVO = 60.0           # °C
T_MIN_DESPACHO = 57.0       # °C
T_MAX_CONTROL = 60.0        # °C (termostato máximo)
T_AMBIENTE = 26.5           # °C

# Volumen por descarga
VOLUMEN_DESCARGA = MASA_POR_DESCARGA / rho_glucosa(T_ENTRADA_GLUCOSA)  # m³
Q_VOL_DESCARGA = M_DOT_DESCARGA / rho_glucosa(T_ENTRADA_GLUCOSA) * 3600.0  # m³/h
T_DESCARGA = VOLUMEN_DESCARGA / Q_VOL_DESCARGA  # h

# Flujo másico de entrada durante descarga (kg/s)
M_DOT_IN = M_DOT_DESCARGA

# Período entre inicios de descarga si se distribuyen 5 en 24 h
T_CICLO = T_TOTAL / N_DESCARGAS  # h


# =============================================================================
# FUNCIONES DEL MODELO
# =============================================================================

def perdidas_termicas(T_g):
    """Pérdidas térmicas [W] en función de T_g [°C]."""
    res = calcular_perdidas(T_g)
    return res['Q_W']


def parametros_iniciales(nivel_inicial, T_inicial):
    """Calcula masa y volumen iniciales del tanque."""
    V_tanque = volumen_total() * nivel_inicial
    rho_inicial = rho_glucosa(T_inicial)
    masa_inicial = V_tanque * rho_inicial
    return V_tanque, masa_inicial


def ode_descarga(t, y, T_agua):
    """ODE durante descarga: entra glucosa fría, sale glucosa caliente."""
    T_g = y[0]
    m_g = y[1]

    if m_g < 1000.0:
        return [0.0, 0.0]

    Cp_g = Cp_glucosa(T_g)

    # Aporte de la chaqueta (termostato: apaga si ya se alcanzó 60 °C)
    if T_g < T_MAX_CONTROL:
        U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g)
        Q_chaq = U_val * A_TRANSFERENCIA * (T_agua - T_g)
    else:
        Q_chaq = 0.0

    # Aporte (negativo) de la glucosa de alimentación a 55 °C
    Cp_in = Cp_glucosa(T_ENTRADA_GLUCOSA)
    Q_mezcla = M_DOT_IN * Cp_in * (T_ENTRADA_GLUCOSA - T_g)

    # Pérdidas al ambiente
    Q_perd = perdidas_termicas(T_g)

    dT_dt = (Q_chaq + Q_mezcla - Q_perd) / (m_g * Cp_g)
    # Masa aproximadamente constante (entra y sale el mismo volumen)
    dm_dt = 0.0
    return [dT_dt, dm_dt]


def ode_calentamiento(t, y, T_agua):
    """ODE entre descargas: calentamiento puro."""
    T_g = y[0]
    m_g = y[1]

    if m_g < 1000.0 or T_g >= T_MAX_CONTROL:
        return [0.0, 0.0]

    Cp_g = Cp_glucosa(T_g)
    U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g)

    Q_chaq = U_val * A_TRANSFERENCIA * (T_agua - T_g)
    Q_perd = perdidas_termicas(T_g)

    dT_dt = (Q_chaq - Q_perd) / (m_g * Cp_g)
    dm_dt = 0.0
    return [dT_dt, dm_dt]


def simular_ciclo(T_agua, nivel_inicial, T_inicial, tiempo_max_h=None, n_descargas=None):
    """
    Simula el ciclo completo de 24 h.

    Parámetros
    ----------
    T_agua : float — temperatura del agua de calentamiento [°C]
    nivel_inicial : float — nivel inicial del tanque (0–1)
    T_inicial : float — temperatura inicial de la glucosa [°C]
    tiempo_max_h : float — tiempo máximo de simulación [h]; si None, 24 h
    n_descargas : int — número de descargas a simular; si None, 5

    Retorna
    -------
    t_eventos : array — tiempo acumulado [h]
    estados : array — [T_g, m_g]
    fases : list — 'calentamiento' o 'descarga'
    ganancia_tiempos_muertos : list — energía neta por intervalo [MJ]
    """
    if tiempo_max_h is None:
        tiempo_max_h = T_TOTAL
    if n_descargas is None:
        n_descargas = N_DESCARGAS

    t_ciclo = tiempo_max_h / n_descargas

    _, MASA_INICIAL = parametros_iniciales(nivel_inicial, T_inicial)

    t_eventos = []
    estados = []
    fases = []
    ganancia_tiempos_muertos = []

    y0 = [T_inicial, MASA_INICIAL]
    t_actual = 0.0

    # Registrar punto inicial
    t_eventos.append(t_actual)
    estados.append(y0.copy())
    fases.append('calentamiento')

    for i in range(n_descargas):
        # --- Fase de descarga ---
        t_fin_descarga = t_actual + T_DESCARGA
        if t_fin_descarga > tiempo_max_h:
            t_fin_descarga = tiempo_max_h
        sol = solve_ivp(lambda t, y: ode_descarga(t, y, T_agua),
                        [t_actual * 3600, t_fin_descarga * 3600], y0,
                        method='RK45', max_step=60, rtol=1e-6, atol=1e-9)
        t_eventos.extend(list(sol.t / 3600.0))
        estados.extend([[T, m] for T, m in zip(sol.y[0], sol.y[1])])
        fases.extend(['descarga'] * len(sol.t))

        y0 = [sol.y[0][-1], sol.y[1][-1]]
        t_actual = t_fin_descarga

        if t_actual >= tiempo_max_h:
            break

        # --- Fase de calentamiento hasta el siguiente ciclo o hasta 60 °C ---
        t_inicio_calentamiento = t_actual
        t_max_calentamiento = (i + 1) * t_ciclo
        duracion_max = max(0.0, t_max_calentamiento - t_inicio_calentamiento)

        # Si ya estamos en 60 °C, mantener hasta el siguiente evento
        if y0[0] >= T_OBJETIVO - 0.01:
            t_eventos.extend([t_actual, t_max_calentamiento])
            estados.extend([y0.copy(), y0.copy()])
            fases.extend(['calentamiento', 'calentamiento'])
            t_actual = t_max_calentamiento
            ganancia_tiempos_muertos.append(0.0)
            continue

        t_fin_cal = t_inicio_calentamiento + duracion_max
        if t_fin_cal > tiempo_max_h:
            t_fin_cal = tiempo_max_h

        sol_cal = solve_ivp(lambda t, y: ode_calentamiento(t, y, T_agua),
                            [t_inicio_calentamiento * 3600, t_fin_cal * 3600],
                            y0, method='RK45', max_step=60, rtol=1e-6, atol=1e-9)

        # Calcular ganancia térmica neta en este tiempo muerto
        Q_chaq_arr = []
        Q_perd_arr = []
        for T in sol_cal.y[0]:
            if T < T_MAX_CONTROL:
                U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T)
                Q_chaq_arr.append(U_val * A_TRANSFERENCIA * (T_agua - T))
            else:
                Q_chaq_arr.append(0.0)
            Q_perd_arr.append(perdidas_termicas(T))
        dt_arr = np.gradient(sol_cal.t)
        ganancia_MJ = np.sum((np.array(Q_chaq_arr) - np.array(Q_perd_arr)) * dt_arr) / 1e6
        ganancia_tiempos_muertos.append(ganancia_MJ)

        t_eventos.extend(list(sol_cal.t / 3600.0))
        estados.extend([[T, m] for T, m in zip(sol_cal.y[0], sol_cal.y[1])])
        fases.extend(['calentamiento'] * len(sol_cal.t))

        y0 = [sol_cal.y[0][-1], sol_cal.y[1][-1]]
        t_actual = t_fin_cal

        if t_actual >= tiempo_max_h:
            break

    return np.array(t_eventos), np.array(estados), fases, ganancia_tiempos_muertos


def resumen_ciclo(t, estados, t_ciclo=None):
    """Genera tabla de resultados por descarga."""
    if t_ciclo is None:
        t_ciclo = T_CICLO

    T = estados[:, 0]

    resultados = []
    for i in range(N_DESCARGAS):
        t_ini = i * t_ciclo
        t_fin = t_ini + T_DESCARGA
        if t_ini > t[-1]:
            break
        idx_ini = np.argmin(np.abs(t - t_ini))
        idx_fin = np.argmin(np.abs(t - t_fin))
        T_ini = T[idx_ini]
        T_fin = T[idx_fin]
        resultados.append({
            'descarga': i + 1,
            't_ini_h': t_ini,
            't_fin_h': t_fin,
            'T_ini_C': T_ini,
            'T_fin_C': T_fin,
            'delta_T_C': T_fin - T_ini,
            'cumple_min': T_fin >= T_MIN_DESPACHO,
        })

    return resultados


# =============================================================================
# GENERACIÓN DE GRÁFICAS
# =============================================================================

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')


def graficar_ciclo(t, estados, fases, T_agua, nivel_inicial, nombre_base):
    """Gráfica de temperatura y nivel vs tiempo."""
    T = estados[:, 0]
    m = estados[:, 1]
    _, MASA_INICIAL = parametros_iniciales(nivel_inicial, T[0] if len(T) > 0 else 60.0)
    nivel = m / (MASA_INICIAL / nivel_inicial * volumen_total()) * 100.0

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                             gridspec_kw={'height_ratios': [2, 1]})

    ax1 = axes[0]
    ax1.plot(t, T, color=COLOR_GLUCOSA, linewidth=2.2, label='Temperatura de la glucosa')
    ax1.axhline(T_OBJETIVO, color=COLOR_DESCARGA, linestyle='--', linewidth=1.5,
                label=f'Objetivo {T_OBJETIVO:.0f} °C')
    ax1.axhline(T_MIN_DESPACHO, color=COLOR_BANDA, linestyle='--', linewidth=1.5,
                label=f'Mínimo despacho {T_MIN_DESPACHO:.0f} °C')

    # Bandas de descarga
    for i in range(N_DESCARGAS):
        t_ini = i * T_CICLO
        t_fin = t_ini + T_DESCARGA
        if t_ini > t[-1]:
            break
        ax1.axvspan(t_ini, t_fin, color=COLOR_DESCARGA, alpha=0.15)
        if t_fin <= t[-1]:
            ax1.text((t_ini + t_fin) / 2, 61.5, f'D{i+1}',
                     ha='center', va='bottom', fontsize=9, color=COLOR_DESCARGA,
                     fontweight='bold')

    ax1.set_ylabel('Temperatura [°C]')
    ax1.set_title(f'Ciclo de descargas: {nivel_inicial*100:.0f} %, agua {T_agua:.0f} °C, 12 ton/h')
    ax1.legend(loc='lower left', framealpha=0.95)
    ax1.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax1.set_ylim(54, 63)

    ax2 = axes[1]
    ax2.plot(t, nivel, color=COLOR_AGUA, linewidth=2.0, label='Nivel del tanque')
    for i in range(N_DESCARGAS):
        t_ini = i * T_CICLO
        t_fin = t_ini + T_DESCARGA
        if t_ini > t[-1]:
            break
        ax2.axvspan(t_ini, t_fin, color=COLOR_DESCARGA, alpha=0.15)
    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('Nivel [%]')
    ax2.legend(loc='lower left', framealpha=0.95)
    ax2.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax2.set_ylim(nivel_inicial * 100 - 10, nivel_inicial * 100 + 5)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_T_vs_t.png'))
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_T_vs_t.pdf'))
    plt.close(fig)


def grafico_barras_resultados(resumen, nombre_base):
    """Gráfico de barras con temperatura final por descarga."""
    descargas = [r['descarga'] for r in resumen]
    T_fin = [r['T_fin_C'] for r in resumen]

    fig, ax = plt.subplots(figsize=(10, 5))
    colores = [COLOR_DESCARGA if t >= T_MIN_DESPACHO else COLOR_BANDA for t in T_fin]
    bars = ax.bar(descargas, T_fin, color=colores, edgecolor=COLOR_TEXTO, linewidth=1.2)
    ax.axhline(T_MIN_DESPACHO, color=COLOR_BANDA, linestyle='--', linewidth=1.5,
               label=f'Mínimo despacho {T_MIN_DESPACHO:.0f} °C')
    ax.axhline(T_OBJETIVO, color=COLOR_DESCARGA, linestyle='--', linewidth=1.5,
               label=f'Objetivo {T_OBJETIVO:.0f} °C')

    for bar, t in zip(bars, T_fin):
        ax.text(bar.get_x() + bar.get_width()/2, t + 0.1,
                f'{t:.2f} °C', ha='center', va='bottom', fontsize=10,
                color=COLOR_TEXTO, fontweight='bold')

    ax.set_xlabel('Descarga')
    ax.set_ylabel('Temperatura final [°C]')
    ax.set_title('Temperatura del tanque al finalizar cada descarga')
    ax.set_ylim(54, 61)
    ax.legend(loc='lower left', framealpha=0.95)
    ax.grid(True, axis='y', linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_barras_Tfin.png'))
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_barras_Tfin.pdf'))
    plt.close(fig)


def graficar_ganancia_tiempos_muertos(ganancias, nombre_base):
    """Gráfico de barras de ganancia térmica neta por tiempo muerto."""
    fig, ax = plt.subplots(figsize=(10, 5))
    intervalos = [f'TM{i+1}' for i in range(len(ganancias))]
    colores = [COLOR_DESCARGA if g > 0 else COLOR_BANDA for g in ganancias]
    bars = ax.bar(intervalos, ganancias, color=colores, edgecolor=COLOR_TEXTO, linewidth=1.2)

    for bar, g in zip(bars, ganancias):
        ax.text(bar.get_x() + bar.get_width()/2, g + (0.5 if g > 0 else -1.5),
                f'{g:.1f} MJ', ha='center', va='bottom' if g > 0 else 'top',
                fontsize=10, color=COLOR_TEXTO, fontweight='bold')

    ax.axhline(0, color=COLOR_TEXTO, linewidth=0.8)
    ax.set_xlabel('Intervalo entre descargas')
    ax.set_ylabel('Ganancia térmica neta [MJ]')
    ax.set_title('Energía neta aprovechada en tiempos muertos (chaqueta − pérdidas)')
    ax.grid(True, axis='y', linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_ganancia_tiempos_muertos.png'))
    fig.savefig(os.path.join(FIGURES_DIR, f'{nombre_base}_ganancia_tiempos_muertos.pdf'))
    plt.close(fig)


def exportar_resumen_csv(resumen, ganancias, T_agua, nivel_inicial, nombre_base):
    """Exporta tabla resumen del ciclo a CSV."""
    filas = []
    for r, g in zip(resumen, ganancias + [None]):
        filas.append({
            'descarga': r['descarga'],
            't_ini_h': r['t_ini_h'],
            't_fin_h': r['t_fin_h'],
            'T_ini_C': r['T_ini_C'],
            'T_fin_C': r['T_fin_C'],
            'cumple_min': r['cumple_min'],
            'ganancia_tiempo_muerto_MJ': g,
        })
    df = pd.DataFrame(filas)
    path = os.path.join(RESULTS_DIR, f'{nombre_base}_resumen.csv')
    df.to_csv(path, index=False)
    return path


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == '__main__':
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("=" * 80)
    print("CICLO DE DESCARGAS — Chaqueta 14 m², 12 ton/h, con pérdidas térmicas")
    print("=" * 80)
    print(f"Volumen por descarga: {VOLUMEN_DESCARGA:.2f} m³")
    print(f"Duración descarga:    {T_DESCARGA:.3f} h ({T_DESCARGA*60:.1f} min)")
    print(f"Período de ciclo:     {T_CICLO:.2f} h")
    print(f"Tiempo de calentamiento disponible: {T_CICLO - T_DESCARGA:.2f} h")
    print()

    escenarios = [
        {'T_agua': 75.0, 'nivel_inicial': 0.80, 'T_inicial': 60.0, 'nombre': 'ciclo_80pct_75C'},
        {'T_agua': 65.0, 'nivel_inicial': 0.80, 'T_inicial': 60.0, 'nombre': 'ciclo_80pct_65C'},
        {'T_agua': 75.0, 'nivel_inicial': 0.50, 'T_inicial': 60.0, 'nombre': 'ciclo_50pct_75C'},
        {'T_agua': 65.0, 'nivel_inicial': 0.50, 'T_inicial': 60.0, 'nombre': 'ciclo_50pct_65C'},
    ]

    resultados_totales = {}

    for esc in escenarios:
        T_agua = esc['T_agua']
        nivel = esc['nivel_inicial']
        T_ini = esc['T_inicial']
        nombre = esc['nombre']

        print(f"\n--- Escenario: {nombre} ---")
        V0, M0 = parametros_iniciales(nivel, T_ini)
        print(f"Masa inicial: {M0/1000:.1f} ton | Nivel: {nivel*100:.0f} % | T inicial: {T_ini:.0f} °C | T agua: {T_agua:.0f} °C")

        t, estados, fases, ganancias = simular_ciclo(T_agua, nivel, T_ini)
        resumen = resumen_ciclo(t, estados, t_ciclo=T_TOTAL / N_DESCARGAS)

        print(f"\n{'Desc':>5} {'t_ini[h]':>10} {'t_fin[h]':>10} {'T_ini[C]':>12} {'T_fin[C]':>12} {'Cumple':>8} {'Ganancia[MJ]':>14}")
        for r, g in zip(resumen, ganancias + [None]):
            g_str = f'{g:.1f}' if g is not None else '—'
            print(f"{r['descarga']:>5} {r['t_ini_h']:>10.2f} {r['t_fin_h']:>10.2f} "
                  f"{r['T_ini_C']:>12.2f} {r['T_fin_C']:>12.2f} "
                  f"{'Sí' if r['cumple_min'] else 'No':>8} {g_str:>14}")

        T_final = estados[-1, 0]
        T_min_ciclo = np.min(estados[:, 0])
        print(f"\nT mínima del ciclo: {T_min_ciclo:.2f} °C")
        print(f"T final del tanque: {T_final:.2f} °C")
        print(f"Factibilidad (T_min >= {T_MIN_DESPACHO:.0f} °C): {'SÍ' if T_min_ciclo >= T_MIN_DESPACHO else 'NO'}")

        graficar_ciclo(t, estados, fases, T_agua, nivel, nombre)
        grafico_barras_resultados(resumen, nombre)
        if any(g != 0.0 for g in ganancias):
            graficar_ganancia_tiempos_muertos(ganancias, nombre)
        csv_path = exportar_resumen_csv(resumen, ganancias, T_agua, nivel, nombre)
        print(f"CSV guardado: {csv_path}")

        resultados_totales[nombre] = {
            't': t, 'estados': estados, 'fases': fases,
            'resumen': resumen, 'ganancias': ganancias,
        }

    print("\n" + "=" * 80)
    print("Simulaciones de ciclos completadas. Figuras guardadas en:", FIGURES_DIR)
    print("=" * 80)
