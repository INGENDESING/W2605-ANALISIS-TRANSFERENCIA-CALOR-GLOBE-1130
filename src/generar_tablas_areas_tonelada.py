"""
Generador de tablas de áreas tonelada por tonelada — Proyecto W2605
====================================================================
Genera tablas LaTeX 24 y 25 con detalle de flujo de 1 a 16 ton/h,
tonelada por tonelada, para toma de decisiones.
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calcular_areas import calcular_area_necesaria


def generar_tabla_25_57():
    """Tabla 24: Calentamiento de 25°C a 57°C."""
    T_in = 25.0
    T_out = 57.0
    T_agua = 75.0
    v_agua = 2.5
    
    latex = []
    latex.append(r"\begin{table}[H]")
    latex.append(r"    \centering")
    latex.append(r"    \caption{Area de transferencia requerida para calentamiento continuo de glucosa Globe~1130 de 25\,°C a 57\,°C ($T_w = 75$\,°C, $v = 2.5$\,m/s).}")
    latex.append(r"    \label{tab:areas_25_57}")
    latex.append(r"    \setcounter{itemcount}{0}")
    latex.append(r"    \small")
    latex.append(r"    \begin{tabularx}{\textwidth}{@{}Ncccccc@{}}")
    latex.append(r"        \toprule")
    latex.append(r"        \multicolumn{1}{c}{\textbf{It.}} & $\dot{m}$ [ton/h] & $\dot{m}$ [kg/s] & $\dot{Q}$ [kW] & $\Delta T_{lm}$ [°C] & $A_{req}$ [m\textsuperscript{2}] & $L_{eq}$ [m] \\")
    latex.append(r"        \midrule")
    
    for ton_h in range(1, 17):
        mdot_kg_s = ton_h * 1000.0 / 3600.0
        
        # Calcular área usando la función existente
        area, params = calcular_area_necesaria(ton_h, v_agua, T_agua, T_in, T_out)
        
        Q_kW = params['Q_dot_kW']
        LMTD = params['LMTD_C']
        L_eq = params['L_req_m']
        
        latex.append(f"        & {ton_h:2d} & {mdot_kg_s:.3f} & {Q_kW:6.2f} & "
                    f"{LMTD:.2f} & {area:6.2f} & {L_eq:4.0f} \\\\")
    
    latex.append(r"        \bottomrule")
    latex.append(r"    \end{tabularx}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)


def generar_tabla_54_57():
    """Tabla 25: Calentamiento de 54°C a 57°C (ESCENARIO CONSERVADOR)."""
    T_in = 54.0  # Cambiado de 55.0 a 54.0 (mas conservador)
    T_out = 57.0
    T_agua = 75.0
    v_agua = 2.5
    A_propuesta = 13.0  # m2
    
    latex = []
    latex.append(r"\begin{table}[H]")
    latex.append(r"    \centering")
    latex.append(r"    \caption{Area de transferencia requerida para calentamiento de mantenimiento de glucosa Globe~1130 de 54\,°C a 57\,°C ($T_w = 75$\,°C, $v = 2.5$\,m/s).}")
    latex.append(r"    \label{tab:areas_55_57}")
    latex.append(r"    \setcounter{itemcount}{0}")
    latex.append(r"    \small")
    latex.append(r"    \begin{tabularx}{\textwidth}{@{}Ncccccc@{}}")
    latex.append(r"        \toprule")
    latex.append(r"        \multicolumn{1}{c}{\textbf{It.}} & $\dot{m}$ [ton/h] & $\dot{m}$ [kg/s] & $\dot{Q}$ [kW] & $\Delta T_{lm}$ [°C] & $A_{req}$ [m\textsuperscript{2}] & Cumple ($A_{prop}=13$\,m\textsuperscript{2}) \\")
    latex.append(r"        \midrule")
    
    for ton_h in range(1, 17):
        mdot_kg_s = ton_h * 1000.0 / 3600.0
        
        area, params = calcular_area_necesaria(ton_h, v_agua, T_agua, T_in, T_out)
        
        Q_kW = params['Q_dot_kW']
        LMTD = params['LMTD_C']
        
        cumple_str = "Si" if area <= A_propuesta else "No"
        if abs(area - A_propuesta) < 0.3:
            cumple_str = "Limite"
        
        latex.append(f"        & {ton_h:2d} & {mdot_kg_s:.3f} & {Q_kW:6.2f} & "
                    f"{LMTD:.2f} & {area:6.2f} & {cumple_str} \\\\")
    
    latex.append(r"        \bottomrule")
    latex.append(r"    \end{tabularx}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)


def main():
    print("=" * 80)
    print("GENERACION DE TABLAS 24 Y 25 - DETALLE TONELADA POR TONELADA")
    print("=" * 80)
    
    # Generar Tabla 24 (25°C a 57°C)
    print("\nGenerando Tabla 24: Area de transferencia (25°C -> 57°C)...")
    tabla_24 = generar_tabla_25_57()
    print("  16 filas generadas (1 a 16 ton/h)")
    
    # Generar Tabla 25 (54°C a 57°C) - ESCENARIO CONSERVADOR
    print("\nGenerando Tabla 25: Area de transferencia (54°C -> 57°C) - CONSERVADOR...")
    tabla_25 = generar_tabla_54_57()
    print("  16 filas generadas (1 a 16 ton/h)")
    
    # Guardar
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results', 'tables')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'tabla_24_areas_25_57.tex'), 'w', encoding='utf-8') as f:
        f.write(tabla_24)
    
    with open(os.path.join(output_dir, 'tabla_25_areas_55_57.tex'), 'w', encoding='utf-8') as f:
        f.write(tabla_25)
    
    print(f"\n[OK] Tablas guardadas en: {output_dir}")
    print("  - tabla_24_areas_25_57.tex")
    print("  - tabla_25_areas_55_57.tex")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
