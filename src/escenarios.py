"""
Módulo de simulación de escenarios de calentamiento — Proyecto P2611
=====================================================================
Resuelve el balance de energía transitorio para los 3 escenarios.

Balance de energía (glucosa en reposo, sin descarga):
  m_g · Cp_g · dT_g/dt = U(T_g) · A · (T_w_media - T_g)

Donde T_w_media es la temperatura media del agua en la chaqueta.
Se asume que el agua experimenta un pequeño DeltaT al pasar por la chaqueta.

Ref: Incropera et al., 7th ed., Cap. 5 (Transient Conduction),
     Kern, Process Heat Transfer, Cap. 18 (Jacketed Vessels)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from propiedades_glucosa import rho_glucosa, Cp_glucosa, mu_glucosa, Cp_agua, rho_agua
from geometria_tanque import (
    volumen_total, volumen_a_nivel, nivel_a_porcentaje,
    A_CONTACTO, velocidad_en_media_cana, velocidad_en_tuberia_2in,
    caudal_desde_velocidad_media_cana, A_PIPE_8IN, ID_PIPE_8IN,
    RHO_GLUCOSA_REF
)
from coeficiente_U import coeficiente_U


# Configuración de gráficas estilo publicación
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def T_agua_salida(T_agua_in, T_glucosa, U, A, Q_agua):
    """
    Temperatura de salida del agua de la chaqueta.
    Balance: Q = U·A·LMTD = m_dot_agua · Cp_agua · (T_in - T_out)
    Simplificación: T_out ≈ T_in - U·A·(T_in - T_glucosa) / (m_dot·Cp)

    Parámetros
    ----------
    T_agua_in : float — Temperatura de entrada del agua [°C]
    T_glucosa : float — Temperatura de la glucosa [°C]
    U         : float — Coeficiente global [W/m²·°C]
    A         : float — Área de transferencia [m²]
    Q_agua    : float — Caudal volumétrico de agua [m³/s]
    """
    T_media_agua = (T_agua_in + T_glucosa) / 2  # Estimación inicial
    m_dot = rho_agua(T_media_agua) * Q_agua
    Cp = Cp_agua(T_media_agua)
    DeltaT = T_agua_in - T_glucosa
    if DeltaT < 0.1:
        return T_agua_in
    T_out = T_agua_in - U * A * DeltaT / (m_dot * Cp)
    # Limitar: T_out no puede ser menor que T_glucosa
    T_out = max(T_out, T_glucosa + 0.5)
    return T_out


def simular_calentamiento(T_glucosa_0, T_agua_in, v_agua, volumen_glucosa,
                          t_final_h=24, dt_min=10):
    """
    Simula el calentamiento de glucosa en el tanque (sin descarga).

    Parámetros
    ----------
    T_glucosa_0    : float — Temperatura inicial de la glucosa [°C]
    T_agua_in      : float — Temperatura de entrada del agua caliente [°C]
    v_agua         : float — Velocidad del agua en la media caña [m/s]
    volumen_glucosa: float — Volumen de glucosa en el tanque [m³]
    t_final_h      : float — Tiempo final de simulación [h]
    dt_min         : float — Paso de tiempo para salida [min]

    Retorna
    -------
    t_h    : array — Tiempo [h]
    T_g    : array — Temperatura de la glucosa [°C]
    U_hist : array — Coeficiente U en cada paso [W/m²·°C]
    Q_hist : array — Tasa de calor en cada paso [W]
    """
    Q_agua = caudal_desde_velocidad_media_cana(v_agua)  # m³/s
    A = A_CONTACTO  # m²

    def dTdt(t, T_g_arr):
        T_g = T_g_arr[0]
        if T_g >= T_agua_in - 0.5:
            return [0.0]

        # Propiedades a temperatura actual
        rho_g = rho_glucosa(T_g)
        Cp_g = Cp_glucosa(T_g)
        m_g = rho_g * volumen_glucosa

        # Temperatura media del agua
        T_agua_media = (T_agua_in + T_agua_in) / 2  # Simplificación: DeltaT agua pequeño

        # U dependiente de temperatura
        U_val, _, _, _ = coeficiente_U(v_agua, T_agua_media, T_g)

        # LMTD simplificada (asumiendo T_agua ≈ cte a lo largo de la chaqueta)
        DeltaT = T_agua_in - T_g

        # dT/dt
        dT = U_val * A * DeltaT / (m_g * Cp_g)
        return [dT]

    t_span = (0, t_final_h * 3600)  # Convertir a segundos
    t_eval = np.arange(0, t_final_h * 3600 + 1, dt_min * 60)

    sol = solve_ivp(dTdt, t_span, [T_glucosa_0], t_eval=t_eval,
                    method='RK45', max_step=300, rtol=1e-6)

    t_h = sol.t / 3600
    T_g = sol.y[0]

    # Calcular U y Q en cada punto
    U_hist = np.zeros_like(T_g)
    Q_hist = np.zeros_like(T_g)
    for i, T in enumerate(T_g):
        if T < T_agua_in - 0.5:
            U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T)
            U_hist[i] = U_val
            Q_hist[i] = U_val * A * (T_agua_in - T)
        else:
            U_hist[i] = U_hist[max(0, i-1)]

    return t_h, T_g, U_hist, Q_hist


def tiempo_para_alcanzar(t_h, T_g, T_objetivo):
    """Encuentra el tiempo [h] para alcanzar una temperatura objetivo."""
    idx = np.where(T_g >= T_objetivo)[0]
    if len(idx) > 0:
        return t_h[idx[0]]
    return None


# =============================================================================
# ESCENARIO 1: Balance de un tercero — 24 m³, 30.9 m³/h, 20→60°C, T_agua=65°C
# Incluye descarga de 24 ton en 1.5 h al alcanzar 60°C
# =============================================================================

def simular_descarga_esc1(T_g0, m_g0, T_agua_in, v_agua, t_descarga_h=1.5,
                          masa_descarga_kg=24000.0, dt_s=30.0):
    """
    Simula la descarga de 24 ton de glucosa en 1.5 h por boquilla de 8".
    El calentamiento continúa durante la descarga.

    Parámetros
    ----------
    T_g0            : float — Temperatura inicial de glucosa al inicio de descarga [°C]
    m_g0            : float — Masa de glucosa al inicio de descarga [kg]
    T_agua_in       : float — Temperatura de entrada del agua [°C]
    v_agua          : float — Velocidad del agua en la media caña [m/s]
    t_descarga_h    : float — Duración de la descarga [h]
    masa_descarga_kg: float — Masa total a descargar [kg]
    dt_s            : float — Paso de tiempo para salida [s]

    Retorna
    -------
    t_h     : array — Tiempo [h] (relativo al inicio de descarga)
    T_g     : array — Temperatura de la glucosa [°C]
    m_g     : array — Masa de glucosa en el tanque [kg]
    """
    dot_m_out = masa_descarga_kg / (t_descarga_h * 3600.0)  # kg/s
    A = A_CONTACTO

    def ode_desc(t, y):
        T_g = y[0]
        m_g = y[1]
        if m_g < 500.0:
            return [0.0, 0.0]
        Cp_g = Cp_glucosa(T_g)
        U_val, _, _, _ = coeficiente_U(v_agua, T_agua_in, T_g)
        DeltaT = T_agua_in - T_g
        if DeltaT < 0.01:
            dT = 0.0
        else:
            dT = U_val * A * DeltaT / (m_g * Cp_g)
        dm = -dot_m_out
        return [dT, dm]

    t_span = (0, t_descarga_h * 3600.0)
    t_eval = np.arange(0, t_descarga_h * 3600.0 + 1, dt_s)

    sol = solve_ivp(ode_desc, t_span, [T_g0, m_g0], t_eval=t_eval,
                    method='RK45', max_step=60.0, rtol=1e-8, atol=1e-8)

    return sol.t / 3600.0, sol.y[0], sol.y[1]


def escenario_1(figures_dir='../figures'):
    """Ejecuta el Escenario 1 y genera gráficas.

    T_agua = 65°C (confirmado por el usuario).
    Al alcanzar 60°C se inicia descarga de 24 ton en 1.5 h.
    """
    print("\n" + "=" * 75)
    print("ESCENARIO 1: Balance de un tercero")
    print("24 m3 de glucosa, agua a 65°C, Q = 30.9 m3/h, de 20°C a 60°C")
    print("=" * 75)

    Q_agua = 30.9 / 3600  # m³/s
    v_mc = velocidad_en_media_cana(Q_agua)
    v_2in = velocidad_en_tuberia_2in(Q_agua)
    print(f"\nVelocidad en media cana: {v_mc:.3f} m/s")
    print(f"Velocidad en tuberia 2\": {v_2in:.2f} m/s")

    # Temperatura del agua de calentamiento — CONFIRMADA por el usuario
    T_agua_in = 65.0
    print(f"Temperatura agua entrada: {T_agua_in:.0f} °C")

    # --- FASE 1: Calentamiento de 20°C a 60°C ---
    t_h, T_g, U_hist, Q_hist = simular_calentamiento(
        T_glucosa_0=20.0, T_agua_in=T_agua_in, v_agua=v_mc,
        volumen_glucosa=24.0, t_final_h=500, dt_min=5
    )

    t_60 = tiempo_para_alcanzar(t_h, T_g, 60.0)
    if t_60:
        print(f"\nTiempo para alcanzar 60°C: {t_60:.1f} h ({t_60/24:.1f} dias)")
    else:
        print("\nNo alcanza 60°C en 120 h")

    # Velocidad de descarga de glucosa por boquilla 8"
    rho_60 = rho_glucosa(60.0)
    masa_24m3 = 24.0 * rho_glucosa(20.0)
    v_descarga_8in = (24000.0 / (1.5 * 3600.0)) / (rho_60 * A_PIPE_8IN)
    print(f"\nMasa de glucosa (24 m3 a 20°C): {masa_24m3/1000:.1f} ton")
    print(f"Velocidad descarga en boquilla 8\": {v_descarga_8in:.3f} m/s")

    # --- FASE 2: Descarga de 24 ton en 1.5 h al alcanzar 60°C ---
    print("\n--- Descarga de 24 ton en 1.5 h ---")
    m_inicio_desc = masa_24m3  # toda la masa
    t_desc, T_desc, m_desc = simular_descarga_esc1(
        T_g0=60.0, m_g0=m_inicio_desc, T_agua_in=T_agua_in, v_agua=v_mc,
        t_descarga_h=1.5, masa_descarga_kg=24000.0
    )
    print(f"T glucosa al inicio de descarga: 60.0 °C")
    print(f"T glucosa al final de descarga: {T_desc[-1]:.2f} °C")
    print(f"Masa descargada: {(m_desc[0]-m_desc[-1])/1000:.1f} ton")
    print(f"Masa residual: {m_desc[-1]/1000:.1f} ton")

    # --- GRÁFICA COMBINADA: Calentamiento + Descarga ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Recortar calentamiento hasta llegar a 60°C
    if t_60:
        idx_60 = np.where(T_g >= 60.0)[0]
        if len(idx_60) > 0:
            i_cut = idx_60[0]
        else:
            i_cut = len(t_h) - 1
        t_cal = t_h[:i_cut+1]
        T_cal = T_g[:i_cut+1]
        U_cal = U_hist[:i_cut+1]
    else:
        t_cal = t_h
        T_cal = T_g
        U_cal = U_hist

    # Desplazar tiempo de descarga para que sea continuo
    t_desc_abs = t_desc + t_cal[-1]

    # Concatenar para grafica continua
    t_full = np.concatenate([t_cal, t_desc_abs])
    T_full = np.concatenate([T_cal, T_desc])

    ax1.plot(t_cal, T_cal, 'b-', linewidth=2, label='Calentamiento')
    ax1.plot(t_desc_abs, T_desc, 'r-', linewidth=2.5, label='Descarga (24 ton, 1.5 h)')
    ax1.axhline(y=60, color='gray', linestyle='--', alpha=0.5, label='T descarga = 60 °C')
    ax1.axhline(y=T_agua_in, color='orange', linestyle=':', alpha=0.5,
                label=f'T agua = {T_agua_in:.0f} °C')
    if t_60:
        ax1.axvline(x=t_60, color='gray', linestyle=':', alpha=0.4)
        ax1.annotate(f'{t_60:.1f} h', xy=(t_60, 60), fontsize=9,
                     xytext=(t_60+2, 55), arrowprops=dict(arrowstyle='->', color='gray'))
    # Sombrear zona de descarga
    ax1.axvspan(t_cal[-1], t_desc_abs[-1], alpha=0.15, color='red',
                label='Fase de descarga')
    ax1.set_ylabel('Temperatura [°C]')
    ax1.set_title('Escenario 1: Calentamiento + descarga de 24 m$^3$ de glucosa '
                  f'(Q$_{{agua}}$ = 30.9 m$^3$/h, T$_w$ = {T_agua_in:.0f} °C)')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel inferior: masa
    m_cal = np.ones_like(t_cal) * masa_24m3
    ax2.plot(t_cal, m_cal / 1000, 'b-', linewidth=2, label='Calentamiento')
    ax2.plot(t_desc_abs, m_desc / 1000, 'r-', linewidth=2.5, label='Descarga')
    ax2.axvspan(t_cal[-1], t_desc_abs[-1], alpha=0.15, color='red')
    ax2.set_xlabel('Tiempo [h]')
    ax2.set_ylabel('Masa de glucosa [ton]')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{figures_dir}/escenario1_T_vs_tiempo.pdf')
    plt.savefig(f'{figures_dir}/escenario1_T_vs_tiempo.png')
    plt.close()
    print(f"Graficas guardadas en {figures_dir}/")

    return t_h, T_g, U_hist, t_desc, T_desc, m_desc


# =============================================================================
# ESCENARIO 2: Agua a 65°C, tanque al 80%, v = 2.5 m/s
# =============================================================================

def escenario_2(figures_dir='../figures'):
    """Ejecuta el Escenario 2."""
    print("\n" + "=" * 75)
    print("ESCENARIO 2: Agua a 65°C, tanque al 80%, v = 2.5 m/s")
    print("=" * 75)

    V_80 = volumen_total() * 0.80
    print(f"Volumen al 80%: {V_80:.1f} m3")
    print(f"Masa al 80%: {V_80 * rho_glucosa(20)/1000:.0f} ton")

    Q_agua = caudal_desde_velocidad_media_cana(2.5)
    v_2in = velocidad_en_tuberia_2in(Q_agua)
    print(f"Caudal agua: {Q_agua*3600:.1f} m3/h")
    print(f"Velocidad en tuberia 2\": {v_2in:.1f} m/s")

    t_h, T_g, U_hist, Q_hist = simular_calentamiento(
        T_glucosa_0=20.0, T_agua_in=65.0, v_agua=2.5,
        volumen_glucosa=V_80, t_final_h=2000, dt_min=30
    )

    t_30 = tiempo_para_alcanzar(t_h, T_g, 30.0)
    t_40 = tiempo_para_alcanzar(t_h, T_g, 40.0)
    t_50 = tiempo_para_alcanzar(t_h, T_g, 50.0)
    t_55 = tiempo_para_alcanzar(t_h, T_g, 55.0)
    t_57 = tiempo_para_alcanzar(t_h, T_g, 57.0)
    t_60 = tiempo_para_alcanzar(t_h, T_g, 60.0)

    print(f"\nTiempos de calentamiento:")
    for T_obj, t_val in [(30, t_30), (40, t_40), (50, t_50), (55, t_55), (57, t_57), (60, t_60)]:
        if t_val:
            print(f"  Alcanza {T_obj} C en {t_val:.1f} h ({t_val/24:.1f} dias)")
        else:
            print(f"  No alcanza {T_obj} C en el tiempo simulado")
    print(f"  Temperatura final a 200 h: {T_g[-1]:.1f} C")

    # Gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_h, T_g, 'b-', linewidth=2, label='Glucosa Globe 1130')
    ax.axhline(y=60, color='r', linestyle='--', alpha=0.7, label='T descarga = 60 °C')
    ax.axhline(y=65, color='orange', linestyle=':', alpha=0.5, label='T agua = 65 °C')
    if t_60:
        ax.axvline(x=t_60, color='gray', linestyle=':', alpha=0.5)
        ax.annotate(f'{t_60:.1f} h', xy=(t_60, 60), fontsize=10,
                    xytext=(t_60+2, 55), arrowprops=dict(arrowstyle='->', color='gray'))
    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura [°C]')
    ax.set_title('Escenario 2: Tanque al 80%, agua a 65 °C, v = 2.5 m/s')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.savefig(f'{figures_dir}/escenario2_T_vs_tiempo.pdf')
    plt.savefig(f'{figures_dir}/escenario2_T_vs_tiempo.png')
    plt.close()

    return t_h, T_g, U_hist


# =============================================================================
# ESCENARIO 3: Agua a 75°C, tanque al 80%, v = 2.5 m/s
# =============================================================================

def escenario_3(figures_dir='../figures'):
    """Ejecuta el Escenario 3."""
    print("\n" + "=" * 75)
    print("ESCENARIO 3: Agua a 75°C, tanque al 80%, v = 2.5 m/s")
    print("=" * 75)

    V_80 = volumen_total() * 0.80

    t_h, T_g, U_hist, Q_hist = simular_calentamiento(
        T_glucosa_0=20.0, T_agua_in=75.0, v_agua=2.5,
        volumen_glucosa=V_80, t_final_h=2000, dt_min=30
    )

    t_30 = tiempo_para_alcanzar(t_h, T_g, 30.0)
    t_40 = tiempo_para_alcanzar(t_h, T_g, 40.0)
    t_50 = tiempo_para_alcanzar(t_h, T_g, 50.0)
    t_55 = tiempo_para_alcanzar(t_h, T_g, 55.0)
    t_57 = tiempo_para_alcanzar(t_h, T_g, 57.0)
    t_60 = tiempo_para_alcanzar(t_h, T_g, 60.0)

    print(f"\nTiempos de calentamiento:")
    for T_obj, t_val in [(30, t_30), (40, t_40), (50, t_50), (55, t_55), (57, t_57), (60, t_60)]:
        if t_val:
            print(f"  Alcanza {T_obj} C en {t_val:.1f} h ({t_val/24:.1f} dias)")
        else:
            print(f"  No alcanza {T_obj} C en el tiempo simulado")
    print(f"  Temperatura final a 200 h: {T_g[-1]:.1f} C")

    # Gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_h, T_g, 'b-', linewidth=2, label='Glucosa Globe 1130')
    ax.axhline(y=57, color='r', linestyle='--', alpha=0.7, label='T descarga = 57 °C')
    ax.axhline(y=75, color='orange', linestyle=':', alpha=0.5, label='T agua = 75 °C')
    if t_57:
        ax.axvline(x=t_57, color='gray', linestyle=':', alpha=0.5)
        ax.annotate(f'{t_57:.1f} h', xy=(t_57, 57), fontsize=10,
                    xytext=(t_57+2, 52), arrowprops=dict(arrowstyle='->', color='gray'))
    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura [°C]')
    ax.set_title('Escenario 3: Tanque al 80%, agua a 75 °C, v = 2.5 m/s')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.savefig(f'{figures_dir}/escenario3_T_vs_tiempo.pdf')
    plt.savefig(f'{figures_dir}/escenario3_T_vs_tiempo.png')
    plt.close()

    return t_h, T_g, U_hist


# =============================================================================
# GRÁFICA COMPARATIVA
# =============================================================================

def grafica_comparativa(t2, Tg2, t3, Tg3, figures_dir='../figures'):
    """Gráfica comparativa Escenario 2 vs 3."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t2, Tg2, 'b-', linewidth=2, label='Escenario 2: agua a 65 °C')
    ax.plot(t3, Tg3, 'r-', linewidth=2, label='Escenario 3: agua a 75 °C')
    ax.axhline(y=60, color='gray', linestyle='--', alpha=0.7, label='T descarga = 60 °C')
    ax.set_xlabel('Tiempo [h]')
    ax.set_ylabel('Temperatura de la glucosa [°C]')
    ax.set_title('Comparacion de escenarios de calentamiento (tanque al 80%, v = 2.5 m/s)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.savefig(f'{figures_dir}/comparacion_escenarios_2_3.pdf')
    plt.savefig(f'{figures_dir}/comparacion_escenarios_2_3.png')
    plt.close()


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    import os
    figures_dir = os.path.join(os.path.dirname(__file__), '..', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    t1, Tg1, U1, t1d, Tg1d, m1d = escenario_1(figures_dir)
    t2, Tg2, U2 = escenario_2(figures_dir)
    t3, Tg3, U3 = escenario_3(figures_dir)
    grafica_comparativa(t2, Tg2, t3, Tg3, figures_dir)

    print("\n" + "=" * 75)
    print("TODAS LAS SIMULACIONES COMPLETADAS")
    print("=" * 75)
