"""
Comparativa de Configuraciones de Chaqueta — Proyecto W2605
===========================================================
Compara la chaqueta dimple actual (A = 28 m², 3 entradas/3 salidas) con la
chaqueta de media caña rectangular en espiral propuesta (A = 13 m², paso único).

Análisis A — Batch (glucosa estática en tanque, 80% capacidad):
  dT/dt = U(T) × A × (T_agua - T_g) / (m_g × Cp_g)
  Casos: 25°C → 57°C  y  55°C → 57°C

Análisis B — Continuo (glucosa fluye a 1-16 ton/h a través de la chaqueta):
  dT/dA = U(T) × (T_agua - T) / (ṁ × Cp(T))
  Casos: T_entrada = 25°C  y  T_entrada = 55°C, objetivo 57°C

Hallazgo clave: U es idéntico para ambas chaquetas porque h_o (glucosa,
convección natural) domina el 98% de la resistencia térmica. Solo varía A.

Condiciones de agua: T = 75°C, v = 2.5 m/s
Tanque: 80% de capacidad (batch)

Referencias:
  - Incropera et al. (2011), Fundamentals of Heat and Mass Transfer, 7th ed., Sec. 11.4
  - Churchill & Chu (1975), Int. J. Heat Mass Transfer, 18(11), 1323.
  - Sieder & Tate (1936), Ind. Eng. Chem., 28, 1429.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import io
import shutil
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# Configurar salida UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(__file__))

try:
    from coeficiente_U import coeficiente_U
    from propiedades_glucosa import rho_glucosa, Cp_glucosa
    from geometria_tanque import volumen_total
    from escenarios import tiempo_para_alcanzar
except ImportError as e:
    print(f"ERROR de importacion: {e}")
    sys.exit(1)


# =============================================================================
# CONFIGURACIÓN DE GRÁFICAS ESTILO PUBLICACIÓN
# =============================================================================

COLOR_GLUCOSA = '#2E5AAC'
COLOR_AGUA = '#C44E28'
COLOR_DESCARGA = '#3A7D44'
COLOR_BANDA_DESCARGA = '#F4A261'
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
# CONSTANTES DE LAS DOS CONFIGURACIONES
# =============================================================================

A_ACTUAL   = 28.0   # Chaqueta dimple actual [m²]
A_PROPUESTA = 13.0  # Chaqueta media caña propuesta [m²]
T_AGUA     = 75.0   # Temperatura del agua caliente [°C]
V_AGUA     = 2.5    # Velocidad del agua en la chaqueta [m/s]
FRACCION_TANQUE = 0.80  # Tanque al 80% para análisis batch

CHAQUETAS = {
    'Actual (dimple, 28 m\u00b2)': A_ACTUAL,
    'Propuesta (media ca\u00f1a, 13 m\u00b2)': A_PROPUESTA,
}

FLUJOS_TON_H = list(range(1, 17))   # 1 a 16 ton/h
M_CARROTANQUE = 24.0                # Masa de un carrotanque [ton]


# =============================================================================
# ANÁLISIS A — CALENTAMIENTO BATCH
# =============================================================================

def simular_calentamiento_con_area(T_glucosa_0, T_agua_in, v_agua,
                                    volumen_glucosa, area_contacto,
                                    t_final_h=3000, dt_min=5):
    """
    Simula calentamiento de glucosa en tanque (sin descarga), con area parametrizada.

    ODE: dT_g/dt = U(T_g) × A × (T_agua - T_g) / (m_g × Cp_g)

    Parámetros
    ----------
    T_glucosa_0     : float — Temperatura inicial de la glucosa [°C]
    T_agua_in       : float — Temperatura del agua caliente [°C]
    v_agua          : float — Velocidad del agua en la chaqueta [m/s]
    volumen_glucosa : float — Volumen de glucosa en el tanque [m³]
    area_contacto   : float — Área efectiva de la chaqueta [m²]
    t_final_h       : float — Tiempo máximo de simulación [h]
    dt_min          : float — Paso de salida [min]

    Retorna
    -------
    t_h    : array — Tiempo [h]
    T_g    : array — Temperatura de la glucosa [°C]
    U_hist : array — Coeficiente U en cada paso [W/m²·°C]
    Q_hist : array — Potencia transferida en cada paso [W]
    """
    A = area_contacto

    def dTdt(t, T_g_arr):
        T_g = T_g_arr[0]
        if T_g >= T_agua_in - 0.5:
            return [0.0]
        rho_g  = rho_glucosa(T_g)
        Cp_g   = Cp_glucosa(T_g)
        m_g    = rho_g * volumen_glucosa
        U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T_g)
        dT = U_val * A * (T_agua_in - T_g) / (m_g * Cp_g)
        return [dT]

    t_span = (0, t_final_h * 3600)
    t_eval = np.arange(0, t_final_h * 3600 + 1, dt_min * 60)

    sol = solve_ivp(dTdt, t_span, [T_glucosa_0], t_eval=t_eval,
                    method='RK45', max_step=300, rtol=1e-6)

    t_h = sol.t / 3600
    T_g = sol.y[0]

    # Calcular U y Q en cada punto para postproceso
    U_hist = np.zeros_like(T_g)
    Q_hist = np.zeros_like(T_g)
    for i, T in enumerate(T_g):
        if T < T_agua_in - 0.5:
            U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T)
            U_hist[i] = U_val
            Q_hist[i] = U_val * A * (T_agua_in - T)
        else:
            U_hist[i] = U_hist[max(0, i - 1)]

    return t_h, T_g, U_hist, Q_hist


def comparacion_batch():
    """
    Ejecuta los 4 escenarios batch (2 casos × 2 chaquetas) y reporta tiempos.

    Retorna
    -------
    resultados : dict
        Estructura: {caso: {nombre_chaqueta: {'t_h', 'T_g', 'U_hist', 'Q_hist',
                                               't_objetivo_h', 'T_ini', 'T_obj', 'A'}}}
    """
    volumen = volumen_total() * FRACCION_TANQUE
    casos = [
        {'nombre': '25-57', 'T_ini': 25.0, 'T_obj': 57.0, 't_max_h': 3000},
        {'nombre': '55-57', 'T_ini': 55.0, 'T_obj': 57.0, 't_max_h': 500},
    ]

    resultados = {}
    print("\n" + "=" * 70)
    print("ANÁLISIS A — CALENTAMIENTO BATCH (tanque al 80%, agua 75°C)")
    print("=" * 70)
    print(f"Volumen glucosa: {volumen:.2f} m³")
    print()

    for caso in casos:
        nombre_caso = caso['nombre']
        resultados[nombre_caso] = {}

        print(f"Caso {nombre_caso} ({caso['T_ini']}°C → {caso['T_obj']}°C):")
        print(f"  {'Chaqueta':35s} | {'Área [m²]':9s} | {'Tiempo [h]':10s} | {'Tiempo [días]':13s}")
        print(f"  {'-'*35}-+-{'-'*9}-+-{'-'*10}-+-{'-'*13}")

        for nombre_chaqueta, area in CHAQUETAS.items():
            t_h, T_g, U_hist, Q_hist = simular_calentamiento_con_area(
                caso['T_ini'], T_AGUA, V_AGUA, volumen, area,
                t_final_h=caso['t_max_h']
            )
            t_obj = tiempo_para_alcanzar(t_h, T_g, caso['T_obj'])

            resultados[nombre_caso][nombre_chaqueta] = {
                't_h':        t_h,
                'T_g':        T_g,
                'U_hist':     U_hist,
                'Q_hist':     Q_hist,
                't_obj_h':    t_obj,
                'T_ini':      caso['T_ini'],
                'T_obj':      caso['T_obj'],
                'A':          area,
            }

            if t_obj is not None:
                dias = t_obj / 24
                print(f"  {nombre_chaqueta:35s} | {area:9.1f} | {t_obj:10.2f} | {dias:13.3f}")
            else:
                print(f"  {nombre_chaqueta:35s} | {area:9.1f} | {'NO alcanza':>10s} | {'---':>13s}")

        # Validación: ratio de tiempos debe ser ≈ A_actual/A_propuesta
        t_actual   = resultados[nombre_caso]['Actual (dimple, 28 m\u00b2)']['t_obj_h']
        t_propuesta = resultados[nombre_caso]['Propuesta (media ca\u00f1a, 13 m\u00b2)']['t_obj_h']
        if t_actual and t_propuesta:
            ratio = t_propuesta / t_actual
            esperado = A_ACTUAL / A_PROPUESTA
            print(f"  Ratio t_propuesta/t_actual = {ratio:.3f} (esperado ≈ {esperado:.3f} = A_actual/A_propuesta)")
        print()

    return resultados


# =============================================================================
# ANÁLISIS B — CALENTAMIENTO CONTINUO (ODE ESPACIAL)
# =============================================================================

def calcular_T_salida_espacial(m_dot_kg_s, T_glucosa_in, T_agua_in,
                                v_agua, area_disponible):
    """
    Calcula la temperatura de salida de la glucosa mediante ODE espacial.

    ODE: dT/dA = U(T) × (T_agua - T) / (ṁ × Cp(T))

    Integra desde A=0 (entrada) hasta A=area_disponible (salida).

    Ref: Incropera et al. (2011), Fundamentals of Heat and Mass Transfer, 7th ed.,
         Ec. 11.3b (perfil de temperatura en intercambiador con fluido a T cte).

    Parámetros
    ----------
    m_dot_kg_s     : float — Flujo másico de glucosa [kg/s]
    T_glucosa_in   : float — Temperatura entrada glucosa [°C]
    T_agua_in      : float — Temperatura del agua [°C]
    v_agua         : float — Velocidad del agua [m/s]
    area_disponible: float — Área total disponible de la chaqueta [m²]

    Retorna
    -------
    T_out   : float — Temperatura de salida de la glucosa [°C]
    A_array : array — Coordenada de área [m²]
    T_array : array — Temperatura de la glucosa a lo largo de A [°C]
    """
    def dT_dA(A_coord, T_arr):
        T = T_arr[0]
        # Límite: glucosa no puede superar T_agua - 0.1°C
        if T >= T_agua_in - 0.1:
            return [0.0]
        Cp_g = Cp_glucosa(T)
        U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T)
        dT = U_val * (T_agua_in - T) / (m_dot_kg_s * Cp_g)
        return [dT]

    n_puntos = max(50, int(area_disponible / 0.05))
    A_eval = np.linspace(0, area_disponible, n_puntos)

    sol = solve_ivp(dT_dA, [0, area_disponible], [T_glucosa_in],
                    t_eval=A_eval, method='RK45', max_step=0.1, rtol=1e-6)

    T_out = sol.y[0, -1]
    return T_out, sol.t, sol.y[0]


def flujo_maximo_alcanzable(T_in, T_objetivo, T_agua, v_agua, area):
    """
    Determina el flujo másico máximo [ton/h] que permite alcanzar T_objetivo.

    Utiliza brentq sobre la función f(m_dot) = T_out(m_dot) - T_objetivo.

    Parámetros
    ----------
    T_in      : float — Temperatura entrada glucosa [°C]
    T_objetivo: float — Temperatura salida requerida [°C]
    T_agua    : float — Temperatura agua [°C]
    v_agua    : float — Velocidad agua [m/s]
    area      : float — Área disponible [m²]

    Retorna
    -------
    m_max_ton_h : float — Flujo máximo [ton/h], o None si no converge
    """
    def f(m_dot_ton_h):
        m_dot_kg_s = m_dot_ton_h * 1000.0 / 3600.0
        T_out, _, _ = calcular_T_salida_espacial(
            m_dot_kg_s, T_in, T_agua, v_agua, area
        )
        return T_out - T_objetivo

    # Verificar si incluso 0.01 ton/h alcanza el objetivo
    if f(0.01) < 0:
        return 0.0

    # Buscar límite superior donde ya no se alcanza el objetivo
    m_upper = 0.5
    while f(m_upper) > 0 and m_upper < 200:
        m_upper *= 2

    if f(m_upper) > 0:
        return m_upper  # Alcanza para cualquier flujo hasta 200 ton/h

    try:
        m_max = brentq(f, 0.01, m_upper, xtol=0.01, rtol=1e-4)
        return m_max
    except ValueError:
        return None


def comparacion_flujo_continuo():
    """
    Para cada flujo (1-16 ton/h) y cada chaqueta, calcula T_salida y t_proceso.

    Retorna
    -------
    df_25C : DataFrame — Resultados con T_in = 25°C
    df_55C : DataFrame — Resultados con T_in = 55°C
    flujos_max : dict — Flujos máximos por chaqueta y caso
    """
    print("=" * 70)
    print("ANÁLISIS B — CALENTAMIENTO CONTINUO (agua 75°C, v=2.5 m/s)")
    print("=" * 70)

    casos_tin = [
        {'T_in': 25.0, 'T_obj': 57.0, 'nombre': '25°C'},
        {'T_in': 55.0, 'T_obj': 57.0, 'nombre': '55°C'},
    ]

    resultados_por_caso = {}
    flujos_max = {}

    for caso in casos_tin:
        T_in  = caso['T_in']
        T_obj = caso['T_obj']
        nombre = caso['nombre']

        print(f"\nCaso T_entrada = {T_in}°C → objetivo {T_obj}°C:")
        print(f"  {'Flujo':>8} | {'T_sal. actual':>13} | {'T_sal. propuesta':>16} | {'OK actual':>9} | {'OK propuesta':>12}")
        print(f"  {'-'*8}-+-{'-'*13}-+-{'-'*16}-+-{'-'*9}-+-{'-'*12}")

        filas = []
        for m_ton in FLUJOS_TON_H:
            m_dot_kg_s = m_ton * 1000.0 / 3600.0
            t_proceso_h = M_CARROTANQUE / m_ton  # horas para procesar 24 ton

            T_sal_actual, _, _ = calcular_T_salida_espacial(
                m_dot_kg_s, T_in, T_AGUA, V_AGUA, A_ACTUAL)
            T_sal_prop, _, _ = calcular_T_salida_espacial(
                m_dot_kg_s, T_in, T_AGUA, V_AGUA, A_PROPUESTA)

            ok_actual  = 'Si' if T_sal_actual  >= T_obj else 'No'
            ok_prop    = 'Si' if T_sal_prop     >= T_obj else 'No'

            filas.append({
                'Flujo_ton_h':        m_ton,
                'm_dot_kg_s':         m_dot_kg_s,
                'T_sal_actual_C':     T_sal_actual,
                'T_sal_propuesta_C':  T_sal_prop,
                'Alcanza_actual':     ok_actual,
                'Alcanza_propuesta':  ok_prop,
                't_proceso_h':        t_proceso_h,
            })
            print(f"  {m_ton:>8} | {T_sal_actual:>12.2f}° | {T_sal_prop:>15.2f}° | {ok_actual:>9} | {ok_prop:>12}")

        resultados_por_caso[nombre] = pd.DataFrame(filas)

        # Flujos máximos
        m_max_actual  = flujo_maximo_alcanzable(T_in, T_obj, T_AGUA, V_AGUA, A_ACTUAL)
        m_max_propuesta = flujo_maximo_alcanzable(T_in, T_obj, T_AGUA, V_AGUA, A_PROPUESTA)

        flujos_max[nombre] = {
            'actual':    m_max_actual,
            'propuesta': m_max_propuesta,
        }
        print(f"\n  Flujo maximo alcanzable con chaqueta actual ({A_ACTUAL} m²):    "
              f"{m_max_actual:.2f} ton/h" if m_max_actual else "  > 16 ton/h")
        print(f"  Flujo maximo alcanzable con chaqueta propuesta ({A_PROPUESTA} m²): "
              f"{m_max_propuesta:.2f} ton/h" if m_max_propuesta else "  > 16 ton/h")

    df_25C = resultados_por_caso['25°C']
    df_55C = resultados_por_caso['55°C']

    return df_25C, df_55C, flujos_max


# =============================================================================
# GRÁFICAS
# =============================================================================

def configurar_estilo():
    """Estilo publicación: serif, 300 dpi."""
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
        'lines.linewidth': 2.0,
    })


def graficar_batch(resultados, figures_dir):
    """
    Figura 1: T(t) batch — 2 paneles (25→57 y 55→57), ambas chaquetas.
    Figura 4: Barras de tiempos batch por chaqueta y caso.
    """
    configurar_estilo()

    # Colores y estilos para las dos chaquetas
    estilos = {
        'Actual (dimple, 28 m\u00b2)':         {'color': COLOR_GLUCOSA, 'ls': '-',  'marker': None},
        'Propuesta (media ca\u00f1a, 13 m\u00b2)': {'color': COLOR_AGUA, 'ls': '--', 'marker': None},
    }

    # --- Figura 1: T vs t ---
    casos_plot = [
        ('25-57', '25°C → 57°C  (calentamiento completo desde frío)'),
        ('55-57', '55°C → 57°C  (mantenimiento / ajuste térmico)'),
    ]

    fig, axes = plt.subplots(2, 1, figsize=(11, 10))

    for ax, (caso_key, titulo) in zip(axes, casos_plot):
        caso_data = resultados[caso_key]
        for nombre_chaqueta, est in estilos.items():
            d = caso_data[nombre_chaqueta]
            label_txt = (f"{nombre_chaqueta}  "
                         f"(t = {d['t_obj_h']:.1f} h)" if d['t_obj_h'] else nombre_chaqueta)
            ax.plot(d['t_h'], d['T_g'],
                    color=est['color'], linestyle=est['ls'],
                    linewidth=2.2, label=label_txt)

        ax.axhline(y=57, color=COLOR_DESCARGA, linestyle=':', linewidth=1.5,
                   label='Objetivo: 57°C')
        ax.set_xlabel('Tiempo [h]', fontsize=12)
        ax.set_ylabel('Temperatura de la glucosa [°C]', fontsize=12)
        ax.set_title(titulo, fontsize=13, fontweight='bold')
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(True, color=COLOR_REJILLA, linestyle='-', alpha=0.6)

        # Marcar los tiempos de llegada a 57°C
        for nombre_chaqueta, est in estilos.items():
            d = caso_data[nombre_chaqueta]
            if d['t_obj_h']:
                ax.axvline(x=d['t_obj_h'], color=est['color'],
                           linestyle=':', alpha=0.6, linewidth=1.2)
                ax.annotate(f"{d['t_obj_h']:.1f} h",
                            xy=(d['t_obj_h'], 57),
                            xytext=(d['t_obj_h'] + 0.5, 53),
                            fontsize=9, color=est['color'],
                            arrowprops=dict(arrowstyle='->', color=est['color'],
                                            lw=1.0))

    plt.tight_layout()
    ruta = os.path.join(figures_dir, 'comp_batch_T_vs_t')
    plt.savefig(ruta + '.png')
    plt.savefig(ruta + '.pdf')
    plt.close()
    print(f"\u2713 Figura guardada: {ruta}.png")

    # --- Figura 4: Barras de tiempos ---
    nombres_casos = ['25→57°C', '55→57°C']
    claves_casos  = ['25-57', '55-57']
    nombres_chaq  = list(CHAQUETAS.keys())

    tiempos = np.zeros((len(claves_casos), len(nombres_chaq)))
    for i, clave in enumerate(claves_casos):
        for j, nch in enumerate(nombres_chaq):
            t = resultados[clave][nch]['t_obj_h']
            tiempos[i, j] = t if t else 0

    x = np.arange(len(nombres_casos))
    width = 0.35
    colors = [COLOR_GLUCOSA, COLOR_AGUA]

    fig2, ax2 = plt.subplots(figsize=(9, 6))
    for j, (nch, col) in enumerate(zip(nombres_chaq, colors)):
        bars = ax2.bar(x + j * width - width / 2, tiempos[:, j],
                       width, label=nch, color=col, alpha=0.85, edgecolor='white')
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                         f'{h:.1f} h', ha='center', va='bottom', fontsize=9)

    ax2.set_xlabel('Caso de calentamiento', fontsize=12)
    ax2.set_ylabel('Tiempo para alcanzar 57°C [h]', fontsize=12)
    ax2.set_title('Comparativa de tiempos de calentamiento batch\n'
                  '(Tanque al 80%, agua a 75°C, v = 2.5 m/s)',
                  fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nombres_casos)
    ax2.legend(fontsize=10)
    ax2.grid(True, axis='y', color=COLOR_REJILLA, linestyle='-', alpha=0.6)

    ratio_label = f'Ratio capacidad: {A_ACTUAL}/{A_PROPUESTA} = {A_ACTUAL/A_PROPUESTA:.2f}\u00d7'
    ax2.text(0.98, 0.97, ratio_label, transform=ax2.transAxes,
             ha='right', va='top', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    ruta2 = os.path.join(figures_dir, 'comp_batch_tiempo_bar')
    plt.savefig(ruta2 + '.png')
    plt.savefig(ruta2 + '.pdf')
    plt.close()
    print(f"\u2713 Figura guardada: {ruta2}.png")


def graficar_flujo_continuo(df_25C, df_55C, flujos_max, figures_dir):
    """
    Figura 2: T_salida vs flujo — 2 paneles (T_in=25 y T_in=55), ambas chaquetas.
    Figura 3: Barras de flujo máximo alcanzable por chaqueta y caso.
    """
    configurar_estilo()

    datasets = [
        (df_25C, '25°C', flujos_max.get('25°C', {})),
        (df_55C, '55°C', flujos_max.get('55°C', {})),
    ]

    # --- Figura 2: T_salida vs flujo ---
    fig, axes = plt.subplots(2, 1, figsize=(11, 10))

    for ax, (df, T_in_label, fmax) in zip(axes, datasets):
        flujos = df['Flujo_ton_h']
        ax.plot(flujos, df['T_sal_actual_C'], color=COLOR_GLUCOSA, marker='o', linestyle='-', markersize=5,
                linewidth=2, label=f'Actual (dimple, {A_ACTUAL:.0f} m²)')
        ax.plot(flujos, df['T_sal_propuesta_C'], color=COLOR_AGUA, marker='s', linestyle='--', markersize=5,
                linewidth=2, label=f'Propuesta (media caña, {A_PROPUESTA:.0f} m²)')
        ax.axhline(y=57, color=COLOR_DESCARGA, linestyle=':', linewidth=1.5,
                   label='Objetivo: 57°C')

        # Líneas verticales en flujos máximos
        for key, col, ls in [('actual', COLOR_GLUCOSA, ':'), ('propuesta', COLOR_AGUA, ':')]:
            fm = fmax.get(key)
            if fm and fm <= 16:
                ax.axvline(x=fm, color=col, linestyle=ls, alpha=0.7,
                           linewidth=1.5)
                ax.annotate(f'{fm:.1f} t/h',
                            xy=(fm, 57),
                            xytext=(fm + 0.3, 54),
                            fontsize=9, color=col,
                            arrowprops=dict(arrowstyle='->', color=col, lw=0.8))

        ax.set_xlabel('Flujo de glucosa [ton/h]', fontsize=12)
        ax.set_ylabel('Temperatura de salida de la glucosa [°C]', fontsize=12)
        ax.set_title(f'T entrada = {T_in_label}  —  temperatura de salida alcanzable\n'
                     f'(agua 75°C, v = 2.5 m/s)',
                     fontsize=13, fontweight='bold')
        ax.legend(loc='lower left', fontsize=10)
        ax.grid(True, color=COLOR_REJILLA, linestyle='-', alpha=0.6)
        ax.set_xlim(0, 16.5)

    plt.tight_layout()
    ruta = os.path.join(figures_dir, 'comp_flujo_T_out_vs_mdot')
    plt.savefig(ruta + '.png')
    plt.savefig(ruta + '.pdf')
    plt.close()
    print(f"\u2713 Figura guardada: {ruta}.png")

    # --- Figura 3: Barras de flujo máximo ---
    nombres_casos = ['Desde 25°C', 'Desde 55°C']
    claves_fmax   = ['25°C', '55°C']
    nombres_chaq  = ['actual', 'propuesta']
    labels_chaq   = [f'Actual (dimple, {A_ACTUAL:.0f} m²)',
                     f'Propuesta (media caña, {A_PROPUESTA:.0f} m²)']
    colors = [COLOR_GLUCOSA, COLOR_AGUA]

    fmax_vals = np.zeros((len(claves_fmax), 2))
    for i, clave in enumerate(claves_fmax):
        for j, nch in enumerate(nombres_chaq):
            fm = flujos_max.get(clave, {}).get(nch)
            fmax_vals[i, j] = min(fm, 16.0) if fm else 16.0

    x = np.arange(len(nombres_casos))
    width = 0.35

    fig2, ax2 = plt.subplots(figsize=(9, 6))
    for j, (lbl, col) in enumerate(zip(labels_chaq, colors)):
        bars = ax2.bar(x + j * width - width / 2, fmax_vals[:, j],
                       width, label=lbl, color=col, alpha=0.85, edgecolor='white')
        for bar in bars:
            h = bar.get_height()
            tag = f'{h:.1f}' if h < 16 else '>16'
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                     f'{tag} t/h', ha='center', va='bottom', fontsize=9)

    ax2.set_xlabel('Caso de calentamiento', fontsize=12)
    ax2.set_ylabel('Flujo máximo alcanzable [ton/h]', fontsize=12)
    ax2.set_title('Flujo máximo continuo para alcanzar 57°C a la salida\n'
                  '(Chaqueta actual vs. propuesta)',
                  fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nombres_casos)
    ax2.legend(fontsize=10)
    ax2.grid(True, axis='y', color=COLOR_REJILLA, linestyle='-', alpha=0.6)
    ax2.set_ylim(0, 20)

    plt.tight_layout()
    ruta2 = os.path.join(figures_dir, 'comp_flujo_maximo_bar')
    plt.savefig(ruta2 + '.png')
    plt.savefig(ruta2 + '.pdf')
    plt.close()
    print(f"\u2713 Figura guardada: {ruta2}.png")


# =============================================================================
# GUARDADO DE RESULTADOS CSV
# =============================================================================

def guardar_resultados(resultados_batch, df_25C, df_55C, flujos_max, results_dir):
    """Guarda tablas de resultados en CSV."""
    os.makedirs(results_dir, exist_ok=True)

    # CSV batch
    filas_batch = []
    for caso_key, caso_data in resultados_batch.items():
        for nombre_chaqueta, d in caso_data.items():
            t = d['t_obj_h']
            filas_batch.append({
                'Caso':          f"{d['T_ini']}->57C",
                'Chaqueta':      nombre_chaqueta,
                'Area_m2':       d['A'],
                'T_inicial_C':   d['T_ini'],
                'T_final_C':     d['T_obj'],
                'Tiempo_h':      round(t, 3) if t else None,
                'Tiempo_dias':   round(t / 24, 3) if t else None,
            })
    pd.DataFrame(filas_batch).to_csv(
        os.path.join(results_dir, 'comparativa_batch.csv'), index=False, encoding='utf-8')

    # CSV flujo continuo
    df_25C.to_csv(os.path.join(results_dir, 'comparativa_flujo_25C.csv'),
                  index=False, encoding='utf-8')
    df_55C.to_csv(os.path.join(results_dir, 'comparativa_flujo_55C.csv'),
                  index=False, encoding='utf-8')

    # CSV flujos máximos
    filas_fmax = []
    for caso, vals in flujos_max.items():
        for chaqueta, fm in vals.items():
            area = A_ACTUAL if chaqueta == 'actual' else A_PROPUESTA
            filas_fmax.append({
                'Caso':           f"Tin={caso}",
                'Chaqueta':       chaqueta,
                'Area_m2':        area,
                'Flujo_max_ton_h': round(fm, 2) if fm else None,
            })
    pd.DataFrame(filas_fmax).to_csv(
        os.path.join(results_dir, 'comparativa_flujo_maximo.csv'),
        index=False, encoding='utf-8')

    print(f"\u2713 CSVs guardados en: {results_dir}")


# =============================================================================
# RESUMEN IMPRESO
# =============================================================================

def imprimir_resumen(resultados_batch, flujos_max):
    """Imprime resumen ejecutivo de los resultados."""
    print("\n" + "=" * 70)
    print("RESUMEN EJECUTIVO — COMPARATIVA DE CHAQUETAS")
    print("=" * 70)
    print(f"\n{'Chaqueta actual':30s}: Dimple,      A = {A_ACTUAL:.0f} m²,  3 entradas/3 salidas")
    print(f"{'Chaqueta propuesta':30s}: Media caña,  A = {A_PROPUESTA:.0f} m²,  1 paso en espiral")
    print(f"{'Ratio de áreas':30s}: {A_ACTUAL}/{A_PROPUESTA} = {A_ACTUAL/A_PROPUESTA:.2f}×")

    print("\nTiempos de calentamiento BATCH (tanque al 80%, agua 75°C):")
    for caso_key, caso_data in resultados_batch.items():
        t_act  = caso_data['Actual (dimple, 28 m\u00b2)']['t_obj_h']
        t_prop = caso_data['Propuesta (media ca\u00f1a, 13 m\u00b2)']['t_obj_h']
        ratio  = t_prop / t_act if (t_act and t_prop) else None
        tag    = f"{caso_key.replace('-', '→')}°C"
        print(f"  {tag:12s}: actual = {t_act:.1f} h, propuesta = {t_prop:.1f} h, "
              f"ratio = {ratio:.2f}×" if ratio else f"  {tag:12s}: resultado no disponible")

    print("\nFlujo máximo continuo para alcanzar 57°C:")
    for caso, vals in flujos_max.items():
        fa = vals.get('actual',    0)
        fp = vals.get('propuesta', 0)
        print(f"  T_entrada={caso}: actual = {fa:.1f} ton/h, propuesta = {fp:.1f} ton/h")

    print("\nHallazgo principal:")
    print(f"  La reduccion de area del {(1 - A_PROPUESTA/A_ACTUAL)*100:.0f}% (de {A_ACTUAL} a "
          f"{A_PROPUESTA} m²) reduce la capacidad de calentamiento")
    print(f"  en la misma proporcion (~{A_ACTUAL/A_PROPUESTA:.2f}×), ya que U es invariante")
    print(f"  entre configuraciones (h_o domina el 98% de la resistencia termica).")
    print("=" * 70)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("COMPARATIVA DE CONFIGURACIONES DE CHAQUETA — PROYECTO W2605")
    print(f"Chaqueta actual: Dimple, A = {A_ACTUAL} m²  (3 entradas/3 salidas)")
    print(f"Chaqueta propuesta: Media cana, A = {A_PROPUESTA} m²  (1 paso en espiral)")
    print(f"Condiciones agua: T = {T_AGUA}°C, v = {V_AGUA} m/s")
    print("=" * 70)

    # Directorios
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    results_dir = os.path.join(project_dir, 'results')
    figures_dir = os.path.join(project_dir, 'figures')
    results_figures_dir = os.path.join(results_dir, 'figures')
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(results_figures_dir, exist_ok=True)

    # Análisis A — Batch
    resultados_batch = comparacion_batch()

    # Análisis B — Flujo continuo
    df_25C, df_55C, flujos_max = comparacion_flujo_continuo()

    # Gráficas
    print("\nGenerando graficas...")
    graficar_batch(resultados_batch, figures_dir)
    graficar_flujo_continuo(df_25C, df_55C, flujos_max, figures_dir)

    # Copiar figuras a results/figures para coherencia con el documento LaTeX
    nombres_figuras = [
        'comp_batch_T_vs_t',
        'comp_batch_tiempo_bar',
        'comp_flujo_T_out_vs_mdot',
        'comp_flujo_maximo_bar',
    ]
    for nombre in nombres_figuras:
        for ext in ('.png', '.pdf'):
            src = os.path.join(figures_dir, nombre + ext)
            dst = os.path.join(results_figures_dir, nombre + ext)
            if os.path.exists(src):
                shutil.copy2(src, dst)
    print(f"\u2713 Figuras copiadas a: {results_figures_dir}")

    # Guardar CSV
    guardar_resultados(resultados_batch, df_25C, df_55C, flujos_max, results_dir)

    # Resumen
    imprimir_resumen(resultados_batch, flujos_max)

    print("\n\u2713 Analisis completado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
