#!/usr/bin/env python3
"""
Simulación de ciclo de descargas a 12 m³/h — Proyecto W2605
===========================================================
Caso: chaqueta de 14 m², agua a 75 °C, doble entrada, velocidad 2,5 m/s.

Objetivo:
  Evaluar la factibilidad de realizar 5 descargas diarias de 24 ton
  (≈ 17,1 m³ a 55 °C) con un flujo de descarga de 12 m³/h, dejando
  entre descargas únicamente tiempo de calentamiento.

Modelo:
  - Tanque precalentado al 80 % de su capacidad (~250 ton) a 60 °C.
  - Durante descarga:
      * Entra glucosa a 55 °C a 12 m³/h.
      * Sale glucosa hacia el carrotanque a la temperatura del tanque.
      * Volumen/masa del tanque se mantiene aproximadamente constante.
      * Balance energético: chaqueta + aporte de glucosa entrante - pérdidas.
  - Entre descargas:
      * Calentamiento puro con chaqueta, compensando pérdidas.
      * La siguiente descarga comienza a los 4,8 h desde el inicio de la
        anterior (ciclo de 5 descargas/día) o cuando se recupera 60 °C,
        lo que ocurra primero.

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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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
T_AGUA = 75.0               # °C
T_ENTRADA_GLUCOSA = 55.0    # °C (glucosa de alimentación)
Q_VOL_DESCARGA = 12.0       # m³/h
MASA_POR_DESCARGA = 24000.0 # kg (24 ton)
N_DESCARGAS = 5
T_TOTAL = 24.0              # h
NIVEL_INICIAL = 0.80
T_INICIAL = 60.0            # °C
T_OBJETIVO = 60.0           # °C
T_MIN_DESPACHO = 57.0       # °C
T_MAX_CONTROL = 60.0        # °C (termostato máximo)
T_AMBIENTE = 26.5           # °C

# Volumen y masa iniciales
V_TANQUE_80 = volumen_total() * NIVEL_INICIAL
RHO_INICIAL = rho_glucosa(T_INICIAL)
MASA_INICIAL = V_TANQUE_80 * RHO_INICIAL  # kg

# Duración de cada descarga
VOLUMEN_DESCARGA = MASA_POR_DESCARGA / rho_glucosa(T_ENTRADA_GLUCOSA)  # m³
T_DESCARGA = VOLUMEN_DESCARGA / Q_VOL_DESCARGA  # h

# Flujo másico de entrada durante descarga (kg/s)
M_DOT_IN = rho_glucosa(T_ENTRADA_GLUCOSA) * (Q_VOL_DESCARGA / 3600.0)

# Período entre inicios de descarga si se distribuyen 5 en 24 h
T_CICLO = T_TOTAL / N_DESCARGAS  # h


def perdidas_termicas(T_g):
    """Pérdidas térmicas [W] en función de T_g [°C]."""
    res = calcular_perdidas(T_g)
    return res['Q_W']


def ode_descarga(t, y):
    """ODE durante descarga: entra glucosa fría, sale glucosa caliente."""
    T_g = y[0]
    m_g = y[1]

    if m_g < 1000.0:
        return [0.0, 0.0]

    Cp_g = Cp_glucosa(T_g)

    # Aporte de la chaqueta (termostato: apaga si ya se alcanzó 60 °C)
    if T_g < T_MAX_CONTROL:
        U_val, _, _, _ = coeficiente_U(V_AGUA, T_AGUA, T_g)
        Q_chaq = U_val * A_TRANSFERENCIA * (T_AGUA - T_g)
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


def ode_calentamiento(t, y):
    """ODE entre descargas: calentamiento puro."""
    T_g = y[0]
    m_g = y[1]

    if m_g < 1000.0 or T_g >= T_MAX_CONTROL:
        return [0.0, 0.0]

    Cp_g = Cp_glucosa(T_g)
    U_val, _, _, _ = coeficiente_U(V_AGUA, T_AGUA, T_g)

    Q_chaq = U_val * A_TRANSFERENCIA * (T_AGUA - T_g)
    Q_perd = perdidas_termicas(T_g)

    dT_dt = (Q_chaq - Q_perd) / (m_g * Cp_g)
    dm_dt = 0.0
    return [dT_dt, dm_dt]


def simular_ciclo():
    """Simula el ciclo completo de 24 h."""
    t_eventos = []
    estados = []
    fases = []  # 'calentamiento' o 'descarga'

    y0 = [T_INICIAL, MASA_INICIAL]
    t_actual = 0.0

    # Registrar punto inicial
    t_eventos.append(t_actual)
    estados.append(y0.copy())
    fases.append('calentamiento')

    for i in range(N_DESCARGAS):
        # --- Fase de descarga ---
        t_fin_descarga = t_actual + T_DESCARGA
        sol = solve_ivp(ode_descarga, [t_actual * 3600, t_fin_descarga * 3600], y0,
                        method='RK45', max_step=60, rtol=1e-6, atol=1e-9)
        t_eventos.extend(list(sol.t / 3600.0))
        estados.extend([[T, m] for T, m in zip(sol.y[0], sol.y[1])])
        fases.extend(['descarga'] * len(sol.t))

        y0 = [sol.y[0][-1], sol.y[1][-1]]
        t_actual = t_fin_descarga

        # --- Fase de calentamiento hasta el siguiente ciclo o hasta 60 °C ---
        t_inicio_calentamiento = t_actual
        t_max_calentamiento = (i + 1) * T_CICLO  # inicio de siguiente descarga
        duracion_max = max(0.0, t_max_calentamiento - t_inicio_calentamiento)

        # Si ya estamos en 60 °C, mantener hasta el siguiente evento
        if y0[0] >= T_OBJETIVO - 0.01:
            t_eventos.extend([t_actual, t_max_calentamiento])
            estados.extend([y0.copy(), y0.copy()])
            fases.extend(['calentamiento', 'calentamiento'])
            t_actual = t_max_calentamiento
            continue

        t_fin_cal = t_inicio_calentamiento + duracion_max
        sol_cal = solve_ivp(ode_calentamiento,
                            [t_inicio_calentamiento * 3600, t_fin_cal * 3600],
                            y0, method='RK45', max_step=60, rtol=1e-6, atol=1e-9)
        t_eventos.extend(list(sol_cal.t / 3600.0))
        estados.extend([[T, m] for T, m in zip(sol_cal.y[0], sol_cal.y[1])])
        fases.extend(['calentamiento'] * len(sol_cal.t))

        y0 = [sol_cal.y[0][-1], sol_cal.y[1][-1]]
        t_actual = t_fin_cal

    return np.array(t_eventos), np.array(estados), fases


def resumen_ciclo(t, estados):
    """Genera tabla de resultados por descarga."""
    T = estados[:, 0]
    m = estados[:, 1]

    # Encontrar temperaturas al inicio y fin de cada descarga
    resultados = []
    inicios_descarga = [0]
    for i in range(1, len(t)):
        if i == 1:  # primera descarga inicia en t=0
            continue
        # Detectar inicio de descarga: transición de calentamiento a descarga
        # Simplificación: los inicios están en t = i*T_CICLO para i=0..4
        pass

    # Usar tiempos de inicio programados
    for i in range(N_DESCARGAS):
        t_ini = i * T_CICLO
        t_fin = t_ini + T_DESCARGA
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


def graficar_ciclo(t, estados, fases):
    """Gráfica de temperatura y nivel vs tiempo."""
    T = estados[:, 0]
    m = estados[:, 1]
    nivel = m / (RHO_INICIAL * volumen_total()) * 100.0

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
        ax1.axvspan(t_ini, t_fin, color=COLOR_DESCARGA, alpha=0.15)
        ax1.text((t_ini + t_fin) / 2, 61.5, f'D{i+1}',
                 ha='center', va='bottom', fontsize=9, color=COLOR_DESCARGA,
                 fontweight='bold')

    ax1.set_ylabel('Temperatura [°C]')
    ax1.set_title('Ciclo de descargas a 12 m³/h: chaqueta 14 m², agua 75 °C')
    ax1.legend(loc='lower left', framealpha=0.95)
    ax1.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax1.set_ylim(54, 63)

    ax2 = axes[1]
    ax2.plot(t, nivel, color=COLOR_AGUA, linewidth=2.0, label='Nivel del tanque')
    for i in range(N_DESCARGAS):
        t_ini = i * T_CICLO
        t_fin = t_ini + T_DESCARGA
        ax2.axvspan(t_ini, t_fin, color=COLOR_DESCARGA, alpha=0.15)
    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('Nivel [%]')
    ax2.legend(loc='lower left', framealpha=0.95)
    ax2.grid(True, linestyle='-', alpha=0.6, color=COLOR_REJILLA)
    ax2.set_ylim(75, 85)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'ciclo_12m3h_T_vs_t.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'ciclo_12m3h_T_vs_t.pdf'))
    plt.close(fig)


def diagrama_bloques_descarga():
    """Diagrama de bloques estilizado de la fase de descarga."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Bloque del tanque
    tank = FancyBboxPatch((4.5, 2.5), 3.0, 3.0, boxstyle="round,pad=0.05,rounding_size=0.2",
                          facecolor=COLOR_BLOQUE, edgecolor=COLOR_BORDE, linewidth=2)
    ax.add_patch(tank)
    ax.text(6.0, 4.75, 'TANQUE DE\nGLUCOSA', ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_TEXTO)
    ax.text(6.0, 3.85, f'T ≈ 57–60 °C\nV ≈ {V_TANQUE_80:.1f} m³',
            ha='center', va='center', fontsize=9, color=COLOR_TEXTO)

    # Chaqueta (arriba)
    jacket = FancyBboxPatch((4.8, 6.0), 2.4, 0.9, boxstyle="round,pad=0.03,rounding_size=0.1",
                            facecolor='#FFF3E0', edgecolor=COLOR_AGUA, linewidth=2)
    ax.add_patch(jacket)
    ax.text(6.0, 6.45, 'CHAQ. MEDIA CAÑA', ha='center', va='center',
            fontsize=9, fontweight='bold', color=COLOR_AGUA)

    # Flechas agua
    ax.annotate('', xy=(5.2, 6.0), xytext=(5.2, 7.5),
                arrowprops=dict(arrowstyle='->', color=COLOR_AGUA, lw=2))
    ax.text(4.2, 7.1, 'Agua 75 °C\n2,5 m/s', ha='center', va='center',
            fontsize=9, color=COLOR_AGUA)
    ax.annotate('', xy=(6.8, 7.5), xytext=(6.8, 6.0),
                arrowprops=dict(arrowstyle='->', color=COLOR_AGUA, lw=2))
    ax.text(7.8, 7.1, 'Agua de retorno\n~74 °C', ha='center', va='center',
            fontsize=9, color=COLOR_AGUA)

    # Entrada de glucosa fría
    ax.annotate('', xy=(4.5, 3.5), xytext=(1.0, 3.5),
                arrowprops=dict(arrowstyle='->', color=COLOR_GLUCOSA, lw=2))
    ax.text(2.6, 4.2, 'Glucosa de alimentación\n55 °C, 12 m³/h',
            ha='center', va='center', fontsize=9, color=COLOR_GLUCOSA)

    # Salida hacia carrotanque
    ax.annotate('', xy=(11.0, 4.0), xytext=(7.5, 4.0),
                arrowprops=dict(arrowstyle='->', color=COLOR_DESCARGA, lw=2))
    ax.text(9.6, 4.7, 'Hacia carrotanque\n~57–60 °C, 12 m³/h',
            ha='center', va='center', fontsize=9, color=COLOR_DESCARGA)

    # Pérdidas
    ax.annotate('', xy=(6.0, 2.5), xytext=(6.0, 1.0),
                arrowprops=dict(arrowstyle='->', color=COLOR_BANDA, lw=1.5,
                                linestyle='--'))
    ax.text(6.6, 1.5, 'Pérdidas al ambiente\n~14,7 MJ/h',
            ha='left', va='center', fontsize=9, color=COLOR_BANDA)

    ax.set_title('Fase de descarga: balance de masa y energía', fontsize=14, pad=20)
    fig.savefig(os.path.join(FIGURES_DIR, 'diagrama_bloques_descarga.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'diagrama_bloques_descarga.pdf'))
    plt.close(fig)


def diagrama_bloques_calentamiento():
    """Diagrama de bloques estilizado de la fase de calentamiento."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Tanque
    tank = FancyBboxPatch((3.5, 2.5), 3.0, 3.0, boxstyle="round,pad=0.05,rounding_size=0.2",
                          facecolor=COLOR_BLOQUE, edgecolor=COLOR_BORDE, linewidth=2)
    ax.add_patch(tank)
    ax.text(5.0, 4.75, 'TANQUE DE\nGLUCOSA', ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_TEXTO)
    ax.text(5.0, 3.85, 'T < 60 °C\nSin flujo de entrada/salida',
            ha='center', va='center', fontsize=9, color=COLOR_TEXTO)

    # Chaqueta
    jacket = FancyBboxPatch((3.8, 6.0), 2.4, 0.9, boxstyle="round,pad=0.03,rounding_size=0.1",
                            facecolor='#FFF3E0', edgecolor=COLOR_AGUA, linewidth=2)
    ax.add_patch(jacket)
    ax.text(5.0, 6.45, 'CHAQ. MEDIA CAÑA', ha='center', va='center',
            fontsize=9, fontweight='bold', color=COLOR_AGUA)

    ax.annotate('', xy=(4.2, 6.0), xytext=(4.2, 7.5),
                arrowprops=dict(arrowstyle='->', color=COLOR_AGUA, lw=2))
    ax.text(3.2, 7.1, 'Agua 75 °C', ha='center', va='center',
            fontsize=9, color=COLOR_AGUA)
    ax.annotate('', xy=(5.8, 7.5), xytext=(5.8, 6.0),
                arrowprops=dict(arrowstyle='->', color=COLOR_AGUA, lw=2))
    ax.text(6.8, 7.1, 'Agua retorno', ha='center', va='center',
            fontsize=9, color=COLOR_AGUA)

    ax.annotate('', xy=(5.0, 2.5), xytext=(5.0, 1.0),
                arrowprops=dict(arrowstyle='->', color=COLOR_BANDA, lw=1.5, linestyle='--'))
    ax.text(5.6, 1.5, 'Pérdidas al ambiente', ha='left', va='center',
            fontsize=9, color=COLOR_BANDA)

    ax.set_title('Fase de calentamiento: recuperación de temperatura', fontsize=14, pad=20)
    fig.savefig(os.path.join(FIGURES_DIR, 'diagrama_bloques_calentamiento.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'diagrama_bloques_calentamiento.pdf'))
    plt.close(fig)


def grafico_barras_resultados(resumen):
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
    fig.savefig(os.path.join(FIGURES_DIR, 'ciclo_12m3h_barras_Tfin.png'))
    fig.savefig(os.path.join(FIGURES_DIR, 'ciclo_12m3h_barras_Tfin.pdf'))
    plt.close(fig)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == '__main__':
    os.makedirs(FIGURES_DIR, exist_ok=True)
    print("=" * 80)
    print("CICLO DE DESCARGAS A 12 m³/h — Chaqueta 14 m², agua 75 °C")
    print("=" * 80)
    print(f"Masa inicial:       {MASA_INICIAL/1000:.1f} ton")
    print(f"Volumen inicial:    {V_TANQUE_80:.2f} m³")
    print(f"Volumen por descarga: {VOLUMEN_DESCARGA:.2f} m³")
    print(f"Duración descarga:  {T_DESCARGA:.3f} h ({T_DESCARGA*60:.1f} min)")
    print(f"Período de ciclo:   {T_CICLO:.2f} h")
    print(f"Tiempo de calentamiento disponible: {T_CICLO - T_DESCARGA:.2f} h")
    print()

    t, estados, fases = simular_ciclo()
    resumen = resumen_ciclo(t, estados)

    print("RESULTADOS POR DESCARGA:")
    print(f"{'Desc':>5} {'t_ini[h]':>10} {'t_fin[h]':>10} {'T_ini[°C]':>12} {'T_fin[°C]':>12} {'Cumple':>8}")
    for r in resumen:
        print(f"{r['descarga']:>5} {r['t_ini_h']:>10.2f} {r['t_fin_h']:>10.2f} "
              f"{r['T_ini_C']:>12.2f} {r['T_fin_C']:>12.2f} "
              f"{'Sí' if r['cumple_min'] else 'No':>8}")

    T_final = estados[-1, 0]
    T_min_ciclo = np.min(estados[:, 0])
    print()
    print(f"Temperatura mínima alcanzada en el ciclo: {T_min_ciclo:.2f} °C")
    print(f"Temperatura final del tanque (24 h):      {T_final:.2f} °C")
    print(f"Factibilidad (T_min >= {T_MIN_DESPACHO:.0f} degC): {'SI' if T_min_ciclo >= T_MIN_DESPACHO else 'NO'}")

    print()
    print("Generando gráficas...")
    graficar_ciclo(t, estados, fases)
    diagrama_bloques_descarga()
    diagrama_bloques_calentamiento()
    grafico_barras_resultados(resumen)
    print(f"Figuras guardadas en: {FIGURES_DIR}")
