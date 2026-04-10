"""
Modulo de simulacion del ciclo de descargas a carrotanque — Proyecto P2611
==========================================================================
Simula la operacion ciclica de 8 descargas de 24 toneladas de glucosa
Globe 1130 a carrotanques en un periodo de 24 horas, para los Escenarios
2 (agua a 65 C) y 3 (agua a 75 C).

Modelo fisico:
  Durante descarga (1.5 h por carga):
    m_g(t) * Cp_g * dT_g/dt = U(T_g) * A * (T_agua - T_g)
    dm_g/dt = -dot_m_out

  Entre descargas (calentamiento puro):
    m_g * Cp_g * dT_g/dt = U(T_g) * A * (T_agua - T_g)
    dm_g/dt = 0

Donde:
  dot_m_out = 24,000 kg / (1.5 * 3600 s) = 4.444 kg/s durante descarga
  A = 13.0 m2 (area de contacto media cana con tanque)
  U = f(T_g) — coeficiente global dependiente de temperatura

La masa decreciente reduce la inercia termica, acelerando el
calentamiento entre descargas sucesivas.

Refs:
  - Kern, Process Heat Transfer, Cap. 18 (Jacketed Vessels)
  - Incropera et al., Fundamentals of Heat and Mass Transfer, 7th ed.
  - Perry's Chemical Engineers' Handbook, 8th ed., Sec. 11
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# Agregar el directorio src al path para importar modulos hermanos
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
# CONSTANTES DEL CICLO OPERATIVO
# =============================================================================

N_DESCARGAS = 8               # Numero de descargas a carrotanque en 24 h
MASA_POR_DESCARGA = 24000.0   # Masa de glucosa por descarga [kg] (24 ton)
T_DESCARGA = 1.5              # Duracion de cada descarga [h]
T_CICLO = 3.0                 # Periodo entre descargas [h]
T_TOTAL = 24.0                # Duracion total de la simulacion [h]
V_AGUA = 2.5                  # Velocidad del agua en la media cana [m/s]
A = A_CONTACTO                # Area de transferencia [m2] = 13.0

# Flujo masico de descarga [kg/s]
DOT_M_OUT = MASA_POR_DESCARGA / (T_DESCARGA * 3600.0)


# =============================================================================
# CONDICIONES INICIALES
# =============================================================================

T_GLUCOSA_INICIAL = 57.0      # Temperatura inicial de la glucosa [C]
NIVEL_INICIAL = 0.80          # 80% de la capacidad del tanque

# Masa inicial: volumen al 80% * densidad a T_GLUCOSA_INICIAL
V_80 = volumen_total() * NIVEL_INICIAL
RHO_INICIAL = rho_glucosa(T_GLUCOSA_INICIAL)
MASA_INICIAL = V_80 * RHO_INICIAL  # [kg]


# =============================================================================
# FUNCION ODE DEL SISTEMA
# =============================================================================

def ode_sistema(t, y, T_agua, descargando):
    """
    Sistema de ecuaciones diferenciales ordinarias para el tanque.

    Estado: y = [T_g, m_g]
      T_g : Temperatura de la glucosa [C]
      m_g : Masa de glucosa en el tanque [kg]

    Ecuaciones:
      dT_g/dt = U(T_g) * A * (T_agua - T_g) / (m_g * Cp_g)
      dm_g/dt = -dot_m_out (si descargando) o 0 (si no)

    Parametros
    ----------
    t           : float — Tiempo [s]
    y           : array — Estado [T_g, m_g]
    T_agua      : float — Temperatura del agua caliente [C]
    descargando : bool  — True si se esta descargando al carrotanque

    Retorna
    -------
    dydt : list — Derivadas [dT_g/dt, dm_g/dt]
    """
    T_g = y[0]
    m_g = y[1]

    # Proteccion contra masa negativa o excesivamente baja
    if m_g < 1000.0:
        return [0.0, 0.0]

    # Propiedades de la glucosa a temperatura actual
    Cp_g = Cp_glucosa(T_g)

    # Coeficiente global U dependiente de temperatura
    # Temperatura de pared estimada como promedio agua-glucosa
    U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g)

    # Balance de energia con CONTROL TERMOSTATICO MAX 60C
    DeltaT = T_agua - T_g
    if DeltaT < 0.01 or T_g >= 60.0:
        dT_dt = 0.0
    else:
        dT_dt = U_val * A * DeltaT / (m_g * Cp_g)

    # Balance de masa
    if descargando:
        dm_dt = -DOT_M_OUT
    else:
        dm_dt = 0.0

    return [dT_dt, dm_dt]


# =============================================================================
# SIMULACION DEL CICLO COMPLETO
# =============================================================================

def simular_ciclo(T_agua, T_g0=T_GLUCOSA_INICIAL, m_g0=MASA_INICIAL,
                  n_descargas=N_DESCARGAS, dt_salida_s=30.0):
    """
    Simula el ciclo completo de 8 descargas en 24 horas.

    El ciclo se divide en fases:
      - Fase de descarga (1.5 h): glucosa sale a dot_m_out, calentamiento continua
      - Fase de calentamiento (1.5 h): sin descarga, calentamiento puro
    Cada ciclo dura 3 h; 8 ciclos = 24 h.

    Parametros
    ----------
    T_agua      : float — Temperatura del agua caliente [C]
    T_g0        : float — Temperatura inicial de la glucosa [C]
    m_g0        : float — Masa inicial de glucosa [kg]
    n_descargas : int   — Numero de descargas
    dt_salida_s : float — Intervalo de salida [s]

    Retorna
    -------
    resultados : dict con claves:
        't_h'       : array — Tiempo [h]
        'T_g'       : array — Temperatura de la glucosa [C]
        'm_g'       : array — Masa de glucosa [kg]
        'U_hist'    : array — Coeficiente U [W/m2 C]
        'Q_hist'    : array — Tasa de calor [W]
        'fases'     : list  — Lista de dicts con info de cada fase
        'descargas' : list  — Lista de dicts con info de cada descarga
    """
    # Vectores de almacenamiento
    t_total = []
    T_total = []
    m_total = []
    fases_info = []
    descargas_info = []

    t_actual_s = 0.0  # Tiempo actual en segundos
    T_actual = T_g0
    m_actual = m_g0

    for i_descarga in range(n_descargas):
        t_inicio_ciclo_h = i_descarga * T_CICLO

        # =====================================================================
        # FASE 1: DESCARGA (1.5 h)
        # =====================================================================
        t_ini_desc_s = t_actual_s
        t_fin_desc_s = t_actual_s + T_DESCARGA * 3600.0
        T_inicio_desc = T_actual
        m_inicio_desc = m_actual

        t_eval_desc = np.arange(t_ini_desc_s, t_fin_desc_s + 1, dt_salida_s)
        if t_eval_desc[-1] > t_fin_desc_s:
            t_eval_desc[-1] = t_fin_desc_s

        sol_desc = solve_ivp(
            lambda t, y: ode_sistema(t, y, T_agua, True),
            [t_ini_desc_s, t_fin_desc_s],
            [T_actual, m_actual],
            t_eval=t_eval_desc,
            method='RK45',
            max_step=60.0,
            rtol=1e-8,
            atol=1e-8
        )

        t_total.extend(sol_desc.t.tolist())
        T_total.extend(sol_desc.y[0].tolist())
        m_total.extend(sol_desc.y[1].tolist())

        T_fin_desc = sol_desc.y[0][-1]
        m_fin_desc = sol_desc.y[1][-1]

        descargas_info.append({
            'descarga': i_descarga + 1,
            't_inicio_h': t_ini_desc_s / 3600,
            't_fin_h': t_fin_desc_s / 3600,
            'T_inicio': T_inicio_desc,
            'T_fin': T_fin_desc,
            'm_inicio_kg': m_inicio_desc,
            'm_fin_kg': m_fin_desc,
            'masa_descargada_kg': m_inicio_desc - m_fin_desc,
        })

        fases_info.append({
            'tipo': 'descarga',
            'descarga_num': i_descarga + 1,
            't_inicio_h': t_ini_desc_s / 3600,
            't_fin_h': t_fin_desc_s / 3600,
            'T_inicio': T_inicio_desc,
            'T_fin': T_fin_desc,
        })

        t_actual_s = t_fin_desc_s
        T_actual = T_fin_desc
        m_actual = m_fin_desc

        # =====================================================================
        # FASE 2: CALENTAMIENTO PURO (1.5 h)
        # =====================================================================
        t_ini_cal_s = t_actual_s
        t_fin_cal_s = t_actual_s + (T_CICLO - T_DESCARGA) * 3600.0
        T_inicio_cal = T_actual

        # Si es la ultima descarga y excedemos 24 h, truncar
        if t_fin_cal_s / 3600 > T_TOTAL:
            t_fin_cal_s = T_TOTAL * 3600.0

        if t_fin_cal_s > t_ini_cal_s + 1:
            t_eval_cal = np.arange(t_ini_cal_s, t_fin_cal_s + 1, dt_salida_s)
            if t_eval_cal[-1] > t_fin_cal_s:
                t_eval_cal[-1] = t_fin_cal_s
            # Evitar duplicar el punto de union
            if len(t_total) > 0 and t_eval_cal[0] == t_total[-1]:
                t_eval_cal = t_eval_cal[1:]

            if len(t_eval_cal) > 1:
                sol_cal = solve_ivp(
                    lambda t, y: ode_sistema(t, y, T_agua, False),
                    [t_ini_cal_s, t_fin_cal_s],
                    [T_actual, m_actual],
                    t_eval=t_eval_cal,
                    method='RK45',
                    max_step=60.0,
                    rtol=1e-8,
                    atol=1e-8
                )

                t_total.extend(sol_cal.t.tolist())
                T_total.extend(sol_cal.y[0].tolist())
                m_total.extend(sol_cal.y[1].tolist())

                T_actual = sol_cal.y[0][-1]
                m_actual = sol_cal.y[1][-1]

            fases_info.append({
                'tipo': 'calentamiento',
                't_inicio_h': t_ini_cal_s / 3600,
                't_fin_h': t_fin_cal_s / 3600,
                'T_inicio': T_inicio_cal,
                'T_fin': T_actual,
            })

        t_actual_s = t_fin_cal_s

    # Convertir a arrays
    t_h = np.array(t_total) / 3600.0
    T_g = np.array(T_total)
    m_g = np.array(m_total)

    # Calcular U y Q en cada punto de salida
    U_hist = np.zeros_like(T_g)
    Q_hist = np.zeros_like(T_g)
    for i in range(len(T_g)):
        if T_g[i] < T_agua - 0.1:
            U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g[i])
            U_hist[i] = U_val
            Q_hist[i] = U_val * A * (T_agua - T_g[i])
        else:
            U_hist[i] = U_hist[max(0, i - 1)]

    return {
        't_h': t_h,
        'T_g': T_g,
        'm_g': m_g,
        'U_hist': U_hist,
        'Q_hist': Q_hist,
        'fases': fases_info,
        'descargas': descargas_info,
        'T_agua': T_agua,
    }


# =============================================================================
# FUNCIONES DE GRAFICACION
# =============================================================================

def graficar_T_vs_tiempo(res, escenario_num, figures_dir):
    """
    Grafica la temperatura de la glucosa vs tiempo durante el ciclo de 24 h,
    con las descargas marcadas como bandas sombreadas.

    Parametros
    ----------
    res           : dict — Resultados de simular_ciclo()
    escenario_num : int  — Numero de escenario (2 o 3)
    figures_dir   : str  — Directorio de salida para figuras
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                    gridspec_kw={'height_ratios': [3, 1]})

    t_h = res['t_h']
    T_g = res['T_g']
    T_agua = res['T_agua']

    # --- Panel superior: Temperatura ---
    ax1.plot(t_h, T_g, 'b-', linewidth=1.8, label='T glucosa', zorder=3)
    ax1.axhline(y=T_agua, color='red', linestyle='--', alpha=0.6,
                linewidth=1.0, label=f'T agua = {T_agua:.0f} $\\degree$C')
    ax1.axhline(y=60, color='gray', linestyle=':', alpha=0.5,
                linewidth=0.8, label='T inicial = 60 $\\degree$C')

    # Sombrear descargas
    colores_desc = plt.cm.Oranges(np.linspace(0.25, 0.65, N_DESCARGAS))
    for i, desc in enumerate(res['descargas']):
        ax1.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.20, color=colores_desc[i], zorder=1)
        # Anotar numero de descarga
        t_mid = (desc['t_inicio_h'] + desc['t_fin_h']) / 2
        T_mid = (desc['T_inicio'] + desc['T_fin']) / 2
        ax1.annotate(f"D{i+1}",
                     xy=(t_mid, T_mid), fontsize=8, fontweight='bold',
                     color='darkorange', ha='center', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                               edgecolor='orange', alpha=0.8))

    ax1.set_ylabel('Temperatura [$\\degree$C]')
    ax1.set_title(f'Escenario {escenario_num}: Ciclo de {N_DESCARGAS} descargas '
                  f'de {MASA_POR_DESCARGA/1000:.0f} ton '
                  f'(T$_{{agua}}$ = {T_agua:.0f} $\\degree$C, v = {V_AGUA} m/s)')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, T_TOTAL)

    # --- Panel inferior: Coeficiente U ---
    ax2.plot(t_h, res['U_hist'], 'g-', linewidth=1.2)
    for i, desc in enumerate(res['descargas']):
        ax2.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.15, color=colores_desc[i])
    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('U [W/m$^2\\cdot\\degree$C]')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, T_TOTAL)

    plt.tight_layout()
    nombre = f'ciclo_T_vs_tiempo_esc{escenario_num}'
    plt.savefig(os.path.join(figures_dir, f'{nombre}.pdf'))
    plt.savefig(os.path.join(figures_dir, f'{nombre}.png'))
    plt.close()
    print(f"  Guardada: {nombre}.pdf/.png")


def graficar_masa_nivel(res2, res3, figures_dir):
    """
    Grafica la masa y nivel de la glucosa vs tiempo para ambos escenarios
    (la masa es identica en ambos escenarios, la temperatura difiere).

    Parametros
    ----------
    res2, res3  : dict — Resultados de simular_ciclo() para cada escenario
    figures_dir : str  — Directorio de salida
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    # --- Panel 1: Masa ---
    ax1.plot(res2['t_h'], res2['m_g'] / 1000, 'b-', linewidth=1.8,
             label=f'Esc. 2 (T$_{{agua}}$ = {res2["T_agua"]:.0f} $\\degree$C)')
    ax1.plot(res3['t_h'], res3['m_g'] / 1000, 'r-', linewidth=1.8,
             label=f'Esc. 3 (T$_{{agua}}$ = {res3["T_agua"]:.0f} $\\degree$C)')

    # Marcar descargas con bandas
    for desc in res2['descargas']:
        ax1.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.10, color='orange')

    ax1.set_ylabel('Masa de glucosa [ton]')
    ax1.set_title(f'Masa y nivel del tanque durante ciclo de {N_DESCARGAS} '
                  f'descargas de {MASA_POR_DESCARGA/1000:.0f} ton')
    ax1.legend(loc='upper right', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, T_TOTAL)

    # --- Panel 2: Nivel (porcentaje) ---
    # Calcular nivel como porcentaje: V = m / rho(T), % = V / V_total * 100
    V_tot = volumen_total()
    nivel_2 = (res2['m_g'] / rho_glucosa(res2['T_g'])) / V_tot * 100
    nivel_3 = (res3['m_g'] / rho_glucosa(res3['T_g'])) / V_tot * 100

    ax2.plot(res2['t_h'], nivel_2, 'b-', linewidth=1.8,
             label=f'Esc. 2 (T$_{{agua}}$ = {res2["T_agua"]:.0f} $\\degree$C)')
    ax2.plot(res3['t_h'], nivel_3, 'r-', linewidth=1.8,
             label=f'Esc. 3 (T$_{{agua}}$ = {res3["T_agua"]:.0f} $\\degree$C)')

    for desc in res2['descargas']:
        ax2.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                    alpha=0.10, color='orange')

    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('Nivel del tanque [%]')
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, T_TOTAL)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'ciclo_masa_nivel.pdf'))
    plt.savefig(os.path.join(figures_dir, 'ciclo_masa_nivel.png'))
    plt.close()
    print("  Guardada: ciclo_masa_nivel.pdf/.png")


def graficar_gantt(res2, res3, figures_dir):
    """
    Diagrama de Gantt del ciclo operativo mostrando las fases de
    calentamiento y descarga para ambos escenarios, con anotaciones
    de temperatura.

    Parametros
    ----------
    res2, res3  : dict — Resultados de simular_ciclo() para cada escenario
    figures_dir : str  — Directorio de salida
    """
    fig, ax = plt.subplots(figsize=(14, 5))

    y_positions = {'Esc. 3 (75 $\\degree$C)': 1.0, 'Esc. 2 (65 $\\degree$C)': 0.0}
    bar_height = 0.35

    for label, y_pos, res, color_cal, color_desc in [
        ('Esc. 2 (65 $\\degree$C)', 0.0, res2, '#4A90D9', '#E8833A'),
        ('Esc. 3 (75 $\\degree$C)', 1.0, res3, '#2E6EAB', '#C96A2B'),
    ]:
        for fase in res['fases']:
            t_ini = fase['t_inicio_h']
            duracion = fase['t_fin_h'] - fase['t_inicio_h']

            if fase['tipo'] == 'descarga':
                color = color_desc
                hatch = '///'
                edgecolor = 'darkorange'
            else:
                color = color_cal
                hatch = ''
                edgecolor = 'navy'

            ax.barh(y_pos, duracion, left=t_ini, height=bar_height,
                    color=color, edgecolor=edgecolor, linewidth=0.5,
                    hatch=hatch, alpha=0.85)

        # Anotar temperaturas en las descargas
        for desc in res['descargas']:
            t_mid = (desc['t_inicio_h'] + desc['t_fin_h']) / 2
            ax.text(t_mid, y_pos + bar_height / 2 + 0.02,
                    f"{desc['T_inicio']:.1f}$\\rightarrow${desc['T_fin']:.1f} $\\degree$C",
                    ha='center', va='bottom', fontsize=6.5, color='black',
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                              edgecolor='gray', alpha=0.85))

    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()), fontsize=11)
    ax.set_xlabel('Tiempo [h]')
    ax.set_title(f'Diagrama de Gantt: Ciclo de {N_DESCARGAS} descargas '
                 f'de {MASA_POR_DESCARGA/1000:.0f} ton en {T_TOTAL:.0f} h')
    ax.set_xlim(0, T_TOTAL)
    ax.set_ylim(-0.5, 1.8)
    ax.grid(True, axis='x', alpha=0.3)

    # Leyenda manual
    from matplotlib.patches import Patch
    leyenda = [
        Patch(facecolor='#4A90D9', edgecolor='navy', label='Calentamiento'),
        Patch(facecolor='#E8833A', edgecolor='darkorange', hatch='///',
              label='Descarga a carrotanque'),
    ]
    ax.legend(handles=leyenda, loc='upper right', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'ciclo_gantt.pdf'))
    plt.savefig(os.path.join(figures_dir, 'ciclo_gantt.png'))
    plt.close()
    print("  Guardada: ciclo_gantt.pdf/.png")


# =============================================================================
# TABLA RESUMEN
# =============================================================================

def imprimir_resumen(res, escenario_num):
    """
    Imprime tabla resumen del ciclo de descargas.

    Parametros
    ----------
    res           : dict — Resultados de simular_ciclo()
    escenario_num : int  — Numero de escenario
    """
    T_agua = res['T_agua']
    print(f"\n{'='*90}")
    print(f"RESUMEN CICLO DE DESCARGAS — ESCENARIO {escenario_num} "
          f"(T_agua = {T_agua:.0f} C, v = {V_AGUA} m/s)")
    print(f"{'='*90}")

    print(f"\n  Masa inicial:  {MASA_INICIAL/1000:.1f} ton  "
          f"({V_80:.1f} m3 al 80%)")
    print(f"  T inicial:     {T_GLUCOSA_INICIAL:.0f} C")
    print(f"  T agua:        {T_agua:.0f} C")
    print(f"  Area contacto: {A:.1f} m2")
    print(f"  Flujo descarga: {DOT_M_OUT:.3f} kg/s "
          f"({MASA_POR_DESCARGA/1000:.0f} ton en {T_DESCARGA:.1f} h)")

    print(f"\n  {'Desc':>4} | {'t_ini [h]':>9} | {'t_fin [h]':>9} | "
          f"{'T_ini [C]':>9} | {'T_fin [C]':>9} | "
          f"{'m_ini [ton]':>11} | {'m_fin [ton]':>11} | {'Desc [ton]':>10}")
    print(f"  {'-'*4}-+-{'-'*9}-+-{'-'*9}-+-{'-'*9}-+-{'-'*9}-+-"
          f"{'-'*11}-+-{'-'*11}-+-{'-'*10}")

    masa_total_desc = 0.0
    for desc in res['descargas']:
        masa_desc = desc['masa_descargada_kg']
        masa_total_desc += masa_desc
        print(f"  {desc['descarga']:>4d} | {desc['t_inicio_h']:>9.2f} | "
              f"{desc['t_fin_h']:>9.2f} | {desc['T_inicio']:>9.2f} | "
              f"{desc['T_fin']:>9.2f} | {desc['m_inicio_kg']/1000:>11.1f} | "
              f"{desc['m_fin_kg']/1000:>11.1f} | {masa_desc/1000:>10.1f}")

    # Temperatura y masa final (al final de la ultima fase de calentamiento)
    T_final = res['T_g'][-1]
    m_final = res['m_g'][-1]
    V_final = m_final / rho_glucosa(T_final)
    nivel_final = V_final / volumen_total() * 100

    print(f"\n  Total glucosa descargada: {masa_total_desc/1000:.1f} ton "
          f"({N_DESCARGAS} carrotanques)")
    print(f"  Masa final en tanque:    {m_final/1000:.1f} ton")
    print(f"  Volumen final:           {V_final:.1f} m3")
    print(f"  Nivel final:             {nivel_final:.1f}%")
    print(f"  Temperatura final:       {T_final:.2f} C")
    print(f"  Rango de T durante ciclo: "
          f"{min(res['T_g']):.2f} - {max(res['T_g']):.2f} C")
    print(f"  U promedio:              {np.mean(res['U_hist']):.2f} W/(m2 C)")


# =============================================================================
# EJECUCION PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 90)
    print("SIMULACION DEL CICLO DE DESCARGAS A CARROTANQUE — Proyecto P2611")
    print("=" * 90)
    print(f"\nParametros del ciclo:")
    print(f"  Descargas:       {N_DESCARGAS} carrotanques de "
          f"{MASA_POR_DESCARGA/1000:.0f} ton")
    print(f"  Duracion desc:   {T_DESCARGA:.1f} h cada una")
    print(f"  Periodo ciclo:   {T_CICLO:.1f} h (descarga + calentamiento)")
    print(f"  Tiempo total:    {T_TOTAL:.0f} h")
    print(f"  Flujo descarga:  {DOT_M_OUT:.3f} kg/s")
    print(f"\nCondiciones iniciales:")
    print(f"  Volumen total tanque:  {volumen_total():.1f} m3")
    print(f"  Volumen al 80%:        {V_80:.1f} m3")
    print(f"  Densidad a {T_GLUCOSA_INICIAL:.0f} C:     {RHO_INICIAL:.0f} kg/m3")
    print(f"  Masa inicial:          {MASA_INICIAL/1000:.1f} ton")
    print(f"  Temperatura inicial:   {T_GLUCOSA_INICIAL:.0f} C")

    # Directorio de figuras
    figures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'results', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    # --- Escenario 2: Agua a 65 C ---
    print("\n\nSimulando Escenario 2 (T_agua = 65 C)...")
    res2 = simular_ciclo(T_agua=65.0)
    imprimir_resumen(res2, escenario_num=2)

    # --- Escenario 3: Agua a 75 C ---
    print("\n\nSimulando Escenario 3 (T_agua = 75 C)...")
    res3 = simular_ciclo(T_agua=75.0)
    imprimir_resumen(res3, escenario_num=3)

    # --- Generar graficas ---
    print("\n\nGenerando graficas...")
    graficar_T_vs_tiempo(res2, escenario_num=2, figures_dir=figures_dir)
    graficar_T_vs_tiempo(res3, escenario_num=3, figures_dir=figures_dir)
    graficar_masa_nivel(res2, res3, figures_dir=figures_dir)
    graficar_gantt(res2, res3, figures_dir=figures_dir)

    # --- Comparativa ---
    print("\n\nGenerando grafica comparativa...")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(res2['t_h'], res2['T_g'], 'b-', linewidth=1.8,
            label=f'Escenario 2: T$_{{agua}}$ = 65 $\\degree$C')
    ax.plot(res3['t_h'], res3['T_g'], 'r-', linewidth=1.8,
            label=f'Escenario 3: T$_{{agua}}$ = 75 $\\degree$C')
    ax.axhline(y=60, color='gray', linestyle=':', alpha=0.5,
               label='T inicial = 60 $\\degree$C')

    for desc in res2['descargas']:
        ax.axvspan(desc['t_inicio_h'], desc['t_fin_h'],
                   alpha=0.10, color='orange')

    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura de la glucosa [$\\degree$C]')
    ax.set_title(f'Comparación de escenarios: Ciclo de {N_DESCARGAS} '
                 f'descargas de {MASA_POR_DESCARGA/1000:.0f} ton en {T_TOTAL:.0f} h')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, T_TOTAL)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'ciclo_comparacion_esc2_esc3.pdf'))
    plt.savefig(os.path.join(figures_dir, 'ciclo_comparacion_esc2_esc3.png'))
    plt.close()
    print("  Guardada: ciclo_comparacion_esc2_esc3.pdf/.png")

    print("\n" + "=" * 90)
    print("SIMULACION DEL CICLO DE DESCARGAS COMPLETADA")
    print("=" * 90)
