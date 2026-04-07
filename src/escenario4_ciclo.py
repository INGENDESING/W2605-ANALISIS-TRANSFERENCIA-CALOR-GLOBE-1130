"""
Modulo de simulacion del Escenario 4 — Proyecto P2611
======================================================
Ciclo industrial de despacho: 192 toneladas de glucosa Globe 1130
a 55°C, 8 descargas de 24 toneladas a carrotanque.

Parametros del Escenario 4:
  Masa inicial:          192,000 kg (192 ton)
  Temperatura inicial:   55°C
  Temperatura agua:      75°C
  Velocidad agua:        2.5 m/s en la media cana
  Temperatura descarga:  57°C (la glucosa debe alcanzar 57°C antes de descargar)
  Masa por descarga:     24,000 kg (24 ton)
  Duracion descarga:     1.5 h
  Numero descargas:      8 (total = 192 ton = vaciado completo)

Ciclo operativo:
  1. Calentar glucosa de T_actual hasta 57°C (recalentamiento)
  2. Descargar 24 ton en 1.5 h (calentamiento continua durante descarga)
  3. Repetir desde paso 1 con masa reducida
  4. Tras la 8va descarga, masa residual → 0 ton

Refs:
  - Kern, Process Heat Transfer, Cap. 18
  - Incropera et al., 7th ed., Cap. 5
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os
import sys

# Agregar directorio src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from propiedades_glucosa import rho_glucosa, Cp_glucosa, mu_glucosa
from coeficiente_U import coeficiente_U
from geometria_tanque import A_CONTACTO, volumen_total


# =============================================================================
# CONFIGURACION DE GRAFICAS ESTILO PUBLICACION
# =============================================================================

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


# =============================================================================
# CONSTANTES DEL ESCENARIO 4
# =============================================================================

MASA_INICIAL = 192000.0        # Masa inicial de glucosa [kg]
T_GLUCOSA_INICIAL = 55.0       # Temperatura inicial [C]
T_AGUA = 75.0                  # Temperatura del agua de calentamiento [C]
V_AGUA = 2.5                   # Velocidad del agua en media cana [m/s]
T_DESCARGA = 57.0              # Temperatura minima para descarga [C]
MASA_POR_DESCARGA = 24000.0    # Masa por carrotanque [kg]
T_DESCARGA_DURACION = 1.5      # Duracion de cada descarga [h]
N_DESCARGAS = 8                # Numero total de descargas
A = A_CONTACTO                 # Area de transferencia [m2] = 13.0

# Flujo masico durante descarga
DOT_M_OUT = MASA_POR_DESCARGA / (T_DESCARGA_DURACION * 3600.0)  # kg/s


# =============================================================================
# SISTEMA DE ECUACIONES DIFERENCIALES
# =============================================================================

def ode_tanque(t, y, T_agua, descargando):
    """
    Sistema ODE para el tanque de glucosa.

    Estado: y = [T_g, m_g]
      T_g : Temperatura de la glucosa [C]
      m_g : Masa de glucosa [kg]

    Ecuaciones:
      dT_g/dt = U(T_g) * A * (T_agua - T_g) / (m_g * Cp_g)
      dm_g/dt = -dot_m_out (si descargando) o 0

    Parametros
    ----------
    t           : float  — Tiempo [s]
    y           : array  — Estado [T_g, m_g]
    T_agua      : float  — Temperatura del agua [C]
    descargando : bool   — True si se esta descargando
    """
    T_g = y[0]
    m_g = y[1]

    if m_g < 500.0:
        return [0.0, 0.0]

    Cp_g = Cp_glucosa(T_g)
    U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g)

    # Balance termico con CONTROL TERMOSTATICO 60C MAX
    DeltaT = T_agua - T_g
    if DeltaT < 0.01 or T_g >= 60.0:
        dT_dt = 0.0
    else:
        dT_dt = U_val * A * DeltaT / (m_g * Cp_g)

    dm_dt = -DOT_M_OUT if descargando else 0.0

    return [dT_dt, dm_dt]


# =============================================================================
# SIMULACION DEL CICLO COMPLETO (ESCENARIO 4)
# =============================================================================

def simular_ciclo_esc4(dt_s=30.0):
    """
    Simula el ciclo completo del Escenario 4.

    Ciclo por descarga:
      1. Recalentar glucosa desde T_actual hasta T_DESCARGA (57°C)
      2. Descargar 24 ton en 1.5 h (calentamiento continua)

    Retorna
    -------
    resultados : dict con:
        't_h'         : array — Tiempo acumulado [h]
        'T_g'         : array — Temperatura glucosa [C]
        'm_g'         : array — Masa glucosa [kg]
        'descargas'   : list  — Info por descarga
        'fases'       : list  — Info por fase
        't_total_h'   : float — Tiempo total del ciclo [h]
    """
    t_datos = []       # Tiempo en segundos
    T_datos = []       # Temperatura
    m_datos = []       # Masa
    descargas_info = []
    fases_info = []

    t_acum_s = 0.0     # Tiempo acumulado [s]
    T_actual = T_GLUCOSA_INICIAL
    m_actual = MASA_INICIAL

    print(f"\n{'='*90}")
    print(f"ESCENARIO 4: Ciclo industrial de despacho")
    print(f"192 ton de glucosa a 55°C, agua a 75°C, 8 descargas de 24 ton a 57°C")
    print(f"{'='*90}")
    print(f"\n  Masa inicial:        {MASA_INICIAL/1000:.0f} ton")
    print(f"  T inicial:           {T_GLUCOSA_INICIAL:.0f} °C")
    print(f"  T agua:              {T_AGUA:.0f} °C")
    print(f"  T descarga:          {T_DESCARGA:.0f} °C")
    print(f"  Descargas:           {N_DESCARGAS} × {MASA_POR_DESCARGA/1000:.0f} ton")
    print(f"  Flujo descarga:      {DOT_M_OUT:.3f} kg/s")
    print(f"  Volumen tanque:      {volumen_total():.1f} m3")
    V_ini = MASA_INICIAL / rho_glucosa(T_GLUCOSA_INICIAL)
    print(f"  Volumen inicial:     {V_ini:.1f} m3 ({V_ini/volumen_total()*100:.0f}%)")

    for i_desc in range(N_DESCARGAS):

        # =================================================================
        # FASE 1: RECALENTAMIENTO (hasta T_DESCARGA = 57°C)
        # =================================================================
        if T_actual < T_DESCARGA - 0.01:
            t_ini_cal_s = t_acum_s
            T_ini_cal = T_actual

            # Integrar hasta alcanzar T_DESCARGA
            # Usamos un evento para detener la integracion a 57°C
            def evento_57(t, y):
                return y[0] - T_DESCARGA
            evento_57.terminal = True
            evento_57.direction = 1

            # Tiempo maximo de calentamiento: 48 h (seguridad)
            t_max_cal = 48.0 * 3600.0

            sol_cal = solve_ivp(
                lambda t, y: ode_tanque(t, y, T_AGUA, False),
                [0, t_max_cal],
                [T_actual, m_actual],
                events=evento_57,
                method='RK45',
                max_step=60.0,
                rtol=1e-8,
                atol=1e-8,
                dense_output=True
            )

            # Generar puntos de tiempo regulares
            t_fin_cal = sol_cal.t[-1]
            t_eval_cal = np.arange(0, t_fin_cal + 1, dt_s)
            if t_eval_cal[-1] > t_fin_cal:
                t_eval_cal[-1] = t_fin_cal

            T_cal = sol_cal.sol(t_eval_cal)[0]
            m_cal = sol_cal.sol(t_eval_cal)[1]

            t_datos.extend((t_eval_cal + t_acum_s).tolist())
            T_datos.extend(T_cal.tolist())
            m_datos.extend(m_cal.tolist())

            dt_recal_h = t_fin_cal / 3600.0
            T_actual = T_cal[-1]
            m_actual = m_cal[-1]
            t_acum_s += t_fin_cal

            fases_info.append({
                'tipo': 'recalentamiento',
                'descarga_num': i_desc + 1,
                't_inicio_h': t_ini_cal_s / 3600,
                't_fin_h': t_acum_s / 3600,
                'duracion_h': dt_recal_h,
                'T_inicio': T_ini_cal,
                'T_fin': T_actual,
            })
        else:
            dt_recal_h = 0.0

        # =================================================================
        # FASE 2: DESCARGA (1.5 h)
        # =================================================================
        t_ini_desc_s = t_acum_s
        t_fin_desc_s = t_acum_s + T_DESCARGA_DURACION * 3600.0
        T_ini_desc = T_actual
        m_ini_desc = m_actual

        t_eval_desc = np.arange(0, T_DESCARGA_DURACION * 3600.0 + 1, dt_s)
        if t_eval_desc[-1] > T_DESCARGA_DURACION * 3600.0:
            t_eval_desc[-1] = T_DESCARGA_DURACION * 3600.0

        sol_desc = solve_ivp(
            lambda t, y: ode_tanque(t, y, T_AGUA, True),
            [0, T_DESCARGA_DURACION * 3600.0],
            [T_actual, m_actual],
            t_eval=t_eval_desc,
            method='RK45',
            max_step=60.0,
            rtol=1e-8,
            atol=1e-8
        )

        # Evitar duplicar el punto de union
        if len(t_datos) > 0:
            start_idx = 1
        else:
            start_idx = 0

        t_datos.extend((sol_desc.t[start_idx:] + t_acum_s).tolist())
        T_datos.extend(sol_desc.y[0][start_idx:].tolist())
        m_datos.extend(sol_desc.y[1][start_idx:].tolist())

        T_fin_desc = sol_desc.y[0][-1]
        m_fin_desc = sol_desc.y[1][-1]
        t_acum_s = t_fin_desc_s

        T_actual = T_fin_desc
        m_actual = m_fin_desc

        descargas_info.append({
            'descarga': i_desc + 1,
            't_inicio_h': t_ini_desc_s / 3600,
            't_fin_h': t_fin_desc_s / 3600,
            'T_inicio': T_ini_desc,
            'T_fin': T_fin_desc,
            'm_inicio_kg': m_ini_desc,
            'm_fin_kg': m_fin_desc,
            'masa_descargada_kg': m_ini_desc - m_fin_desc,
            'dt_recalentamiento_h': dt_recal_h,
        })

        fases_info.append({
            'tipo': 'descarga',
            'descarga_num': i_desc + 1,
            't_inicio_h': t_ini_desc_s / 3600,
            't_fin_h': t_fin_desc_s / 3600,
            'duracion_h': T_DESCARGA_DURACION,
            'T_inicio': T_ini_desc,
            'T_fin': T_fin_desc,
        })

    # Convertir a arrays
    t_h = np.array(t_datos) / 3600.0
    T_g = np.array(T_datos)
    m_g = np.array(m_datos)

    t_total_h = t_acum_s / 3600.0

    return {
        't_h': t_h,
        'T_g': T_g,
        'm_g': m_g,
        'descargas': descargas_info,
        'fases': fases_info,
        't_total_h': t_total_h,
    }


# =============================================================================
# FUNCIONES DE IMPRESION
# =============================================================================

def imprimir_resumen(res):
    """Imprime tabla resumen del ciclo del Escenario 4."""
    print(f"\n{'='*105}")
    print(f"RESUMEN CICLO ESCENARIO 4 — T_agua = {T_AGUA:.0f} °C, "
          f"T_descarga = {T_DESCARGA:.0f} °C, v = {V_AGUA} m/s")
    print(f"{'='*105}")

    print(f"\n  {'Desc':>4} | {'dt_recal [h]':>12} | {'t_ini [h]':>9} | {'t_fin [h]':>9} | "
          f"{'T_ini [C]':>10} | {'T_fin [C]':>10} | "
          f"{'m_ini [ton]':>11} | {'m_fin [ton]':>11}")
    print(f"  {'-'*4}-+-{'-'*12}-+-{'-'*9}-+-{'-'*9}-+-{'-'*10}-+-{'-'*10}-+-"
          f"{'-'*11}-+-{'-'*11}")

    for desc in res['descargas']:
        print(f"  {desc['descarga']:>4d} | {desc['dt_recalentamiento_h']:>12.3f} | "
              f"{desc['t_inicio_h']:>9.2f} | {desc['t_fin_h']:>9.2f} | "
              f"{desc['T_inicio']:>10.2f} | {desc['T_fin']:>10.2f} | "
              f"{desc['m_inicio_kg']/1000:>11.1f} | {desc['m_fin_kg']/1000:>11.1f}")

    print(f"\n  Tiempo total del ciclo: {res['t_total_h']:.2f} h")
    print(f"  Masa final en tanque:  {res['m_g'][-1]/1000:.1f} ton")
    print(f"  T final:               {res['T_g'][-1]:.2f} °C")

    # Resumen de tiempos de recalentamiento
    print(f"\n  Tiempos de recalentamiento:")
    for desc in res['descargas']:
        print(f"    Descarga {desc['descarga']}: "
              f"dt = {desc['dt_recalentamiento_h']*60:.1f} min "
              f"({desc['dt_recalentamiento_h']:.3f} h)")

    t_recal_total = sum(d['dt_recalentamiento_h'] for d in res['descargas'])
    t_desc_total = N_DESCARGAS * T_DESCARGA_DURACION
    print(f"\n  Tiempo total recalentamiento: {t_recal_total:.2f} h")
    print(f"  Tiempo total descargas:       {t_desc_total:.1f} h")
    print(f"  Tiempo total ciclo:           {res['t_total_h']:.2f} h")


# =============================================================================
# FUNCIONES DE GRAFICACION
# =============================================================================

def graficar_T_vs_tiempo(res, figures_dir):
    """Grafica T vs tiempo del Escenario 4 con bandas de descarga."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                    gridspec_kw={'height_ratios': [3, 1]})

    t_h = res['t_h']
    T_g = res['T_g']

    # Panel superior: Temperatura
    ax1.plot(t_h, T_g, 'b-', linewidth=1.8, label='T glucosa', zorder=3)
    ax1.axhline(y=T_AGUA, color='red', linestyle='--', alpha=0.5, linewidth=0.8,
                label=f'T agua = {T_AGUA:.0f} °C')
    ax1.axhline(y=T_DESCARGA, color='green', linestyle=':', alpha=0.6, linewidth=1.0,
                label=f'T descarga = {T_DESCARGA:.0f} °C')

    colores = plt.cm.Oranges(np.linspace(0.25, 0.65, N_DESCARGAS))
    for i, desc in enumerate(res['descargas']):
        ax1.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.20, color=colores[i], zorder=1)
        t_mid = (desc['t_inicio_h'] + desc['t_fin_h']) / 2
        ax1.annotate(f"D{i+1}", xy=(t_mid, desc['T_inicio']), fontsize=7,
                     fontweight='bold', color='darkorange', ha='center', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                               edgecolor='orange', alpha=0.8))

    ax1.set_ylabel('Temperatura [°C]')
    ax1.set_title(f'Escenario 4: Ciclo de {N_DESCARGAS} descargas de '
                  f'{MASA_POR_DESCARGA/1000:.0f} ton '
                  f'(T$_{{agua}}$ = {T_AGUA:.0f} °C, T$_{{desc}}$ = {T_DESCARGA:.0f} °C)')
    ax1.legend(loc='upper left', framealpha=0.9, fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel inferior: Masa
    ax2.plot(t_h, res['m_g'] / 1000, 'b-', linewidth=1.8)
    for i, desc in enumerate(res['descargas']):
        ax2.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.15, color=colores[i])
    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('Masa [ton]')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'escenario4_ciclo_T.pdf'))
    plt.savefig(os.path.join(figures_dir, 'escenario4_ciclo_T.png'))
    plt.close()
    print("  Guardada: escenario4_ciclo_T.pdf/.png")


def graficar_gantt(res, figures_dir):
    """Diagrama de Gantt del Escenario 4."""
    fig, ax = plt.subplots(figsize=(14, 4))

    bar_height = 0.5
    y_pos = 0.0
    color_cal = '#2E6EAB'
    color_desc = '#E8833A'

    for fase in res['fases']:
        t_ini = fase['t_inicio_h']
        duracion = fase['duracion_h']

        if fase['tipo'] == 'recalentamiento':
            color = color_cal
            hatch = ''
            ec = 'navy'
        else:
            color = color_desc
            hatch = '///'
            ec = 'darkorange'

        ax.barh(y_pos, duracion, left=t_ini, height=bar_height,
                color=color, edgecolor=ec, linewidth=0.5,
                hatch=hatch, alpha=0.85)

    # Anotar temperaturas en las descargas
    for desc in res['descargas']:
        t_mid = (desc['t_inicio_h'] + desc['t_fin_h']) / 2
        ax.text(t_mid, y_pos + bar_height / 2 + 0.05,
                f"{desc['T_inicio']:.1f}→{desc['T_fin']:.1f} °C\n"
                f"Δt_recal={desc['dt_recalentamiento_h']*60:.0f} min",
                ha='center', va='bottom', fontsize=6, color='black',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                          edgecolor='gray', alpha=0.85))

    ax.set_yticks([y_pos])
    ax.set_yticklabels([f'Esc. 4 ({T_AGUA:.0f} °C)'], fontsize=11)
    ax.set_xlabel('Tiempo [h]')
    ax.set_title(f'Diagrama de Gantt — Escenario 4: {N_DESCARGAS} descargas de '
                 f'{MASA_POR_DESCARGA/1000:.0f} ton (T$_{{desc}}$ = {T_DESCARGA:.0f} °C)')
    ax.set_ylim(-0.5, 1.2)
    ax.grid(True, axis='x', alpha=0.3)

    leyenda = [
        Patch(facecolor=color_cal, edgecolor='navy', label='Recalentamiento'),
        Patch(facecolor=color_desc, edgecolor='darkorange', hatch='///',
              label='Descarga a carrotanque'),
    ]
    ax.legend(handles=leyenda, loc='upper right', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'escenario4_gantt.pdf'))
    plt.savefig(os.path.join(figures_dir, 'escenario4_gantt.png'))
    plt.close()
    print("  Guardada: escenario4_gantt.pdf/.png")


# =============================================================================
# EJECUCION PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    figures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    # Simular ciclo
    res = simular_ciclo_esc4()
    imprimir_resumen(res)

    # Generar graficas
    print("\nGenerando graficas...")
    graficar_T_vs_tiempo(res, figures_dir)
    graficar_gantt(res, figures_dir)

    print(f"\n{'='*90}")
    print("SIMULACION ESCENARIO 4 COMPLETADA")
    print(f"{'='*90}")
