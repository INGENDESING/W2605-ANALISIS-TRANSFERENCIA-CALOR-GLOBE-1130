"""
Generador de tablas detalladas por tonelada — Proyecto W2605
===========================================================
Genera tablas LaTeX con detalle tonelada por tonelada (1 a 16)
para los Escenarios 2 y 3, facilitando la toma de decisiones operativas.

Las tablas muestran:
- Tonelada descargada (1 a 16)
- Tiempo acumulado [h]
- Temperatura de la glucosa [°C]
- Masa remanente en tanque [ton]
- Delta T acumulado
- Estado (descargando/calentando)
"""

import numpy as np
from scipy.integrate import solve_ivp
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from coeficiente_U import coeficiente_U
from geometria_tanque import A_CONTACTO, volumen_total

# Constantes
A = A_CONTACTO  # 14.0 m2
V_AGUA = 2.5    # m/s
T_DESCARGA = 1.5  # h por descarga de 24 ton
DOT_M_OUT = 24000.0 / (T_DESCARGA * 3600.0)  # kg/s
T_CICLO = 4.8  # h (24 h / 5 descargas)

# Condiciones iniciales
NIVEL_INICIAL = 0.80
T_GLUCOSA_INICIAL = 57.0
V_80 = volumen_total() * NIVEL_INICIAL
RHO_INICIAL = rho_glucosa(T_GLUCOSA_INICIAL)
MASA_INICIAL = V_80 * RHO_INICIAL


def ode_sistema(t, y, T_agua, descargando):
    """ODE del sistema con control termostático."""
    T_g = y[0]
    m_g = y[1]
    
    if m_g < 1000.0:
        return [0.0, 0.0]
    
    Cp_g = Cp_glucosa(T_g)
    U_val, _, _, _ = coeficiente_U(V_AGUA, T_agua, T_g)
    
    DeltaT = T_agua - T_g
    if DeltaT < 0.01 or T_g >= 60.0:
        dT_dt = 0.0
    else:
        dT_dt = U_val * A * DeltaT / (m_g * Cp_g)
    
    dm_dt = -DOT_M_OUT if descargando else 0.0
    
    return [dT_dt, dm_dt]


def simular_hasta_tonelada(T_agua, tonelada_objetivo=16, dt_salida_s=60.0):
    """
    Simula el ciclo hasta alcanzar la tonelada objetivo descargada.
    Retorna datos detallados para cada tonelada.
    
    Retorna lista de dicts con:
    - tonelada: int (1 a 16)
    - t_h: tiempo acumulado [h]
    - T_g: temperatura [°C]
    - m_rem: masa remanente [ton]
    - fase: 'descarga' o 'calentamiento'
    - descarga_num: número de descarga (1, 2, ...)
    """
    resultados = []
    tonelada_actual = 0
    
    t_actual_s = 0.0
    T_actual = T_GLUCOSA_INICIAL
    m_actual = MASA_INICIAL
    
    descarga_num = 0
    
    while tonelada_actual < tonelada_objetivo:
        descarga_num += 1
        
        # === FASE DE DESCARGA (1.5 h) ===
        t_ini_desc_s = t_actual_s
        t_fin_desc_s = t_actual_s + T_DESCARGA * 3600.0
        
        # Simular con paso fino para capturar cada tonelada
        masa_inicial_desc = m_actual
        ton_inicial = int((MASA_INICIAL - m_actual) / 1000.0)
        
        def evento_tonelada(t, y):
            """Evento: se ha descargado 1 tonelada más."""
            masa_descargada = masa_inicial_desc - y[1]
            return masa_descargada % 1000.0 - 500.0  # Cambia de signo cada 1000 kg
        
        evento_tonelada.terminal = False
        evento_tonelada.direction = 0
        
        t_eval = np.linspace(t_ini_desc_s, t_fin_desc_s, 500)
        
        sol = solve_ivp(
            lambda t, y: ode_sistema(t, y, T_agua, True),
            [t_ini_desc_s, t_fin_desc_s],
            [T_actual, m_actual],
            t_eval=t_eval,
            method='RK45',
            max_step=30.0,
            rtol=1e-8,
            atol=1e-8
        )
        
        # Extraer datos para cada tonelada durante la descarga
        for i in range(len(sol.t)):
            t_h = sol.t[i] / 3600.0
            T_g = sol.y[0][i]
            m_g = sol.y[1][i]
            tonelada_descargada = int((MASA_INICIAL - m_g) / 1000.0)
            
            # Si cruzamos una tonelada entera y no la hemos registrado
            if tonelada_descargada > tonelada_actual and tonelada_descargada <= tonelada_objetivo:
                # Interpolar para el momento exacto de la tonelada
                if i > 0:
                    m_target = MASA_INICIAL - tonelada_descargada * 1000.0
                    m_prev = sol.y[1][i-1]
                    m_curr = sol.y[1][i]
                    t_prev = sol.t[i-1]
                    t_curr = sol.t[i]
                    T_prev = sol.y[0][i-1]
                    T_curr = sol.y[0][i]
                    
                    # Fracción entre puntos
                    if m_prev != m_curr:
                        frac = (m_prev - m_target) / (m_prev - m_curr)
                        t_exact = t_prev + frac * (t_curr - t_prev)
                        T_exact = T_prev + frac * (T_curr - T_prev)
                    else:
                        t_exact = sol.t[i]
                        T_exact = T_g
                else:
                    t_exact = sol.t[i]
                    T_exact = T_g
                    m_target = m_g
                
                tonelada_actual = tonelada_descargada
                resultados.append({
                    'tonelada': tonelada_actual,
                    't_h': t_exact / 3600.0,
                    'T_g': T_exact,
                    'm_rem': (MASA_INICIAL - tonelada_actual * 1000.0) / 1000.0,
                    'fase': 'descarga',
                    'descarga_num': descarga_num,
                })
        
        T_actual = sol.y[0][-1]
        m_actual = sol.y[1][-1]
        t_actual_s = t_fin_desc_s
        
        if tonelada_actual >= tonelada_objetivo:
            break
        
        # === FASE DE CALENTAMIENTO (1.5 h) ===
        t_ini_cal_s = t_actual_s
        t_fin_cal_s = t_actual_s + (T_CICLO - T_DESCARGA) * 3600.0
        
        t_eval_cal = np.linspace(t_ini_cal_s, t_fin_cal_s, 200)
        
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
        
        T_actual = sol_cal.y[0][-1]
        m_actual = sol_cal.y[1][-1]
        t_actual_s = t_fin_cal_s
    
    return resultados


def generar_tabla_latex(datos, escenario_num, T_agua):
    """Genera código LaTeX para la tabla."""
    
    latex = []
    latex.append(r"\begin{table}[H]")
    latex.append(r"    \centering")
    latex.append(f"    \\caption{{Detalle tonelada por tonelada — Escenario {escenario_num} "
                f"($T_{{w,in}}$ = {T_agua:.0f}°C). Primeras 16 toneladas descargadas.}}")
    latex.append(f"    \\label{{tab:tonelada_esc{escenario_num}}}")
    latex.append(r"    \setcounter{itemcount}{0}")
    latex.append(r"    \begin{tabularx}{\textwidth}{@{}NcccXcccX@{}}")
    latex.append(r"        \toprule")
    latex.append(r"        \multicolumn{1}{c}{\textbf{Item}} & "
                r"\textbf{Ton} & \textbf{Desc.} & \textbf{$t$ [h]} & "
                r"\textbf{$T$ [°C]} & \textbf{$m_{rem}$ [ton]} & "
                r"\textbf{$\Delta T$ [°C]} & \textbf{Estado} & "
                r"\textbf{Obs.} \\")
    latex.append(r"        \midrule")
    
    T_inicial = T_GLUCOSA_INICIAL
    
    for i, d in enumerate(datos):
        delta_T = d['T_g'] - T_inicial
        estado = "Descarga" if d['fase'] == 'descarga' else "Calentamiento"
        
        # Observaciones especiales
        obs = "--"
        if d['tonelada'] == 24:
            obs = "Fin 1ª descarga"
        elif d['tonelada'] == 16:
            obs = "Tonelada objetivo"
        
        latex.append(f"        & {d['tonelada']} & {d['descarga_num']} & "
                    f"{d['t_h']:.3f} & {d['T_g']:.2f} & "
                    f"{d['m_rem']:.1f} & {delta_T:+.2f} & "
                    f"{estado} & {obs} \\\\")
    
    latex.append(r"        \bottomrule")
    latex.append(r"    \end{tabularx}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)


def main():
    print("=" * 80)
    print("GENERACIÓN DE TABLAS DETALLADAS POR TONELADA")
    print("=" * 80)
    
    # Escenario 2: Agua a 65°C
    print("\nSimulando Escenario 2 (T_agua = 65°C)...")
    datos_esc2 = simular_hasta_tonelada(T_agua=65.0, tonelada_objetivo=16)
    tabla_esc2 = generar_tabla_latex(datos_esc2, escenario_num=2, T_agua=65.0)
    
    print(f"  Registradas {len(datos_esc2)} toneladas")
    print("\n  Datos tonelada 1-5:")
    for d in datos_esc2[:5]:
        print(f"    Ton {d['tonelada']:2d}: t={d['t_h']:.3f}h, T={d['T_g']:.2f}°C, "
              f"m_rem={d['m_rem']:.1f}ton, {d['fase']}")
    
    # Escenario 3: Agua a 75°C
    print("\nSimulando Escenario 3 (T_agua = 75°C)...")
    datos_esc3 = simular_hasta_tonelada(T_agua=75.0, tonelada_objetivo=16)
    tabla_esc3 = generar_tabla_latex(datos_esc3, escenario_num=3, T_agua=75.0)
    
    print(f"  Registradas {len(datos_esc3)} toneladas")
    print("\n  Datos tonelada 1-5:")
    for d in datos_esc3[:5]:
        print(f"    Ton {d['tonelada']:2d}: t={d['t_h']:.3f}h, T={d['T_g']:.2f}°C, "
              f"m_rem={d['m_rem']:.1f}ton, {d['fase']}")
    
    # Guardar tablas LaTeX
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results', 'tables')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'tabla_toneladas_esc2.tex'), 'w', encoding='utf-8') as f:
        f.write(tabla_esc2)
    
    with open(os.path.join(output_dir, 'tabla_toneladas_esc3.tex'), 'w', encoding='utf-8') as f:
        f.write(tabla_esc3)
    
    print(f"\n[OK] Tablas guardadas en: {output_dir}")
    print("  - tabla_toneladas_esc2.tex")
    print("  - tabla_toneladas_esc3.tex")
    
    print("\n" + "=" * 80)
    print("GENERACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == "__main__":
    main()
