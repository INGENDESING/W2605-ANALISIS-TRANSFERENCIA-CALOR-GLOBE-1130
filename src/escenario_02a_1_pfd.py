"""
Escenario 02A-1 - Calculo de temperatura de salida de glucosa
Velocidad de agua aumentada a 2.5 m/s (vs 1.338 m/s del 01A)
Proyecto W2605 - Analisis Termico del Tanque de Glucosa

Este script calcula la temperatura de salida de glucosa considerando:
- Balance de energia en estado estacionario
- Calor ganado desde la chaqueta (usando U real calculado)
- Calor perdido al ambiente con aislamiento 5mm (dependiente de viento)

Parametros del Escenario 01A:
- Agua de servicio: 65°C
- Caudal de agua: 30,900 kg/h (30.9 m3/h)
- Area de transferencia: 14 m2
- Glucosa entrando: 60°C
- Caudal glucosa: 8,000 kg/h
- Aislamiento: 5 mm (NO 50.8 mm)
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))

from propiedades_glucosa import rho_glucosa, Cp_glucosa, Cp_agua, rho_agua
from geometria_tanque import (
    volumen_total, OD_SHELL, t_HEAD, A_CONTACTO
)
from coeficiente_U import coeficiente_U
from calculo_calor_perdido_80 import (
    h_conveccion_viento, area_fondo_torisferico, area_cilindrica_al_80porciento,
    T_AMBIENTE, K_AISLAMIENTO
)

# =============================================================================
# PARAMETROS DEL ESCENARIO 01A
# =============================================================================

T_AGUA_IN = 65.0           # Temperatura de entrada del agua [°C]
Q_AGUA_M3H = 57.7          # Caudal de agua [m3/h] - aumentado para v=2.5 m/s
A_CHAQUETA = A_CONTACTO    # Area de transferencia de la chaqueta [m2]
T_GLUCOSA_IN = 60.0        # Temperatura de entrada de glucosa [°C] (igual al 01A)
M_GLUCOSA_KGH = 8000.0     # Caudal masico de glucosa [kg/h]
ESPESOR_AISLAMIENTO = 0.005  # 5 mm [m] - CORREGIDO: era 50.8mm

# Constantes
K_SS316L = 16.3            # Conductividad termica acero [W/(m·K)]
h_int_glucosa = 28.0       # Coef. conveccion interna glucosa [W/m2K]
V_AGUA_MC = 2.5            # Velocidad en media caña [m/s] - AUMENTADA


def calcular_U_chaqueta(T_glucosa, T_agua):
    """
    Calcula el coeficiente U real de la chaqueta usando el modelo de resistencias.
    
    Retorna
    -------
    U : float - Coeficiente global [W/m2K]
    h_i : float - Coeficiente interno [W/m2K]
    h_o : float - Coeficiente externo [W/m2K]
    """
    U_val, h_i, h_o, info = coeficiente_U(V_AGUA_MC, T_agua, T_glucosa)
    return U_val, h_i, h_o, info


def calcular_Q_chaqueta_real(T_glucosa_in, T_glucosa_out, T_agua_in):
    """
    Calcula el calor transferido desde la chaqueta a la glucosa usando U real.
    
    Parametros
    ----------
    T_glucosa_in : float - Temperatura de entrada de glucosa [°C]
    T_glucosa_out : float - Temperatura de salida de glucosa [°C] (estimada)
    T_agua_in : float - Temperatura de entrada del agua [°C]
    
    Retorna
    -------
    Q_chaqueta : float - Calor transferido [W]
    T_agua_out : float - Temperatura de salida del agua [°C]
    U_real : float - Coeficiente U calculado [W/m2K]
    """
    # Temperatura promedio de la glucosa en el tanque
    T_glucosa_prom = (T_glucosa_in + T_glucosa_out) / 2
    
    # Calcular U real
    U_real, h_i, h_o, info = calcular_U_chaqueta(T_glucosa_prom, T_agua_in)
    
    # Iteracion simple para encontrar T_agua_out
    T_agua_out = T_agua_in - 1.0
    
    for _ in range(10):
        T_agua_prom = (T_agua_in + T_agua_out) / 2
        rho_w = rho_agua(T_agua_prom)
        Cp_w = Cp_agua(T_agua_prom)
        m_dot_agua = Q_AGUA_M3H * rho_w / 3600.0
        
        # LMTD
        DeltaT1 = T_agua_in - T_glucosa_out
        DeltaT2 = T_agua_out - T_glucosa_in
        
        DeltaT1 = max(DeltaT1, 0.1)
        DeltaT2 = max(DeltaT2, 0.1)
        
        if abs(DeltaT1 - DeltaT2) < 0.01:
            LMTD = DeltaT1
        else:
            ratio = DeltaT1 / DeltaT2
            if ratio <= 0:
                LMTD = (DeltaT1 + DeltaT2) / 2
            else:
                LMTD = (DeltaT1 - DeltaT2) / np.log(ratio)
        
        Q = U_real * A_CHAQUETA * LMTD
        T_agua_out_new = T_agua_in - Q / (m_dot_agua * Cp_w)
        
        if abs(T_agua_out_new - T_agua_out) < 0.01:
            break
        T_agua_out = T_agua_out_new
    
    return Q, T_agua_out, U_real, h_i, h_o


def calcular_Q_perdidas(v_viento, T_glucosa_prom):
    """
    Calcula las perdidas termicas al ambiente con aislamiento 5mm.
    
    Parametros
    ----------
    v_viento : float - Velocidad del viento [m/s]
    T_glucosa_prom : float - Temperatura promedio de la glucosa [°C]
    
    Retorna
    -------
    Q_perdidas : float - Perdidas termicas [W]
    h_ext : float - Coeficiente convectivo externo [W/m2K]
    U_global : float - Coeficiente global de perdidas [W/m2K]
    A_total : float - Area de transferencia [m2]
    """
    T_pelicula = (T_glucosa_prom + T_AMBIENTE) / 2
    
    D_ext = OD_SHELL
    h_ext, Re, Nu = h_conveccion_viento(v_viento, T_pelicula, D_ext)
    
    # Resistencias termicas
    R_conv_int = 1.0 / h_int_glucosa
    R_pared = t_HEAD / K_SS316L
    R_aislamiento = ESPESOR_AISLAMIENTO / K_AISLAMIENTO
    R_conv_ext = 1.0 / h_ext
    
    R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext
    U_global = 1.0 / R_total
    
    # Areas
    A_fondo = area_fondo_torisferico()
    A_cil_80, _, _ = area_cilindrica_al_80porciento()
    A_total = A_fondo + A_cil_80
    
    Delta_T = T_glucosa_prom - T_AMBIENTE
    Q_perdidas = U_global * A_total * Delta_T
    
    return Q_perdidas, h_ext, U_global, A_total, R_total, R_aislamiento


def calcular_T_salida(v_viento):
    """
    Calcula la temperatura de salida de glucosa para una velocidad de viento dada.
    
    Parametros
    ----------
    v_viento : float - Velocidad del viento [m/s]
    
    Retorna
    -------
    dict : Resultados del calculo
    """
    T_salida = T_GLUCOSA_IN - 1.0
    
    for iteration in range(30):
        T_prom = (T_GLUCOSA_IN + T_salida) / 2
        
        if np.isnan(T_prom) or T_prom < 0 or T_prom > 200:
            break
        
        Cp_g = Cp_glucosa(T_prom)
        rho_g = rho_glucosa(T_prom)
        
        if np.isnan(Cp_g) or Cp_g <= 0:
            break
        
        # Calor desde chaqueta (con U real)
        Q_chaq, T_agua_out, U_real, h_i, h_o = calcular_Q_chaqueta_real(T_GLUCOSA_IN, T_salida, T_AGUA_IN)
        
        if np.isnan(Q_chaq):
            break
        
        # Perdidas al ambiente
        Q_perd, h_ext, U_perd, A_total, R_total, R_aisl = calcular_Q_perdidas(v_viento, T_prom)
        
        if np.isnan(Q_perd) or np.isnan(h_ext):
            break
        
        # Balance de energia
        m_dot_gluc = M_GLUCOSA_KGH / 3600.0
        Q_net = Q_chaq - Q_perd
        delta_T = Q_net / (m_dot_gluc * Cp_g)
        T_salida_new = T_GLUCOSA_IN + delta_T
        
        if np.isnan(T_salida_new) or T_salida_new < 0 or T_salida_new > 200:
            break
        
        if abs(T_salida_new - T_salida) < 0.001:
            T_salida = T_salida_new
            break
        
        T_salida = T_salida_new
    
    # Resultados finales
    T_prom_final = (T_GLUCOSA_IN + T_salida) / 2
    Cp_g_final = Cp_glucosa(T_prom_final)
    
    Q_chaq_final, T_agua_out_final, U_real_final, h_i_final, h_o_final = calcular_Q_chaqueta_real(T_GLUCOSA_IN, T_salida, T_AGUA_IN)
    Q_perd_final, h_ext_final, U_perd_final, A_total, R_total, R_aisl_final = calcular_Q_perdidas(v_viento, T_prom_final)
    
    # Entalpias
    H_gluc_in = M_GLUCOSA_KGH * Cp_g_final * T_GLUCOSA_IN / 1e6
    H_gluc_out = M_GLUCOSA_KGH * Cp_g_final * T_salida / 1e6
    
    rho_w_ref = rho_agua(60)
    Cp_w_ref = Cp_agua(60)
    H_agua_in = Q_AGUA_M3H * rho_w_ref * Cp_w_ref * T_AGUA_IN / 1e6
    H_agua_out = Q_AGUA_M3H * rho_w_ref * Cp_w_ref * T_agua_out_final / 1e6
    
    return {
        'v_viento': v_viento,
        'T_salida': T_salida,
        'T_glucosa_in': T_GLUCOSA_IN,
        'T_agua_in': T_AGUA_IN,
        'T_agua_out': T_agua_out_final,
        'Q_chaqueta_MJ_h': Q_chaq_final * 0.0036,
        'Q_perdidas_MJ_h': Q_perd_final * 0.0036,
        'Q_net_MJ_h': (Q_chaq_final - Q_perd_final) * 0.0036,
        'U_chaqueta': U_real_final,
        'h_i': h_i_final,
        'h_o': h_o_final,
        'h_ext': h_ext_final,
        'U_perdidas': U_perd_final,
        'R_aislamiento': R_aisl_final,
        'A_superficie': A_total,
        'H_gluc_in': H_gluc_in,
        'H_gluc_out': H_gluc_out,
        'H_agua_in': H_agua_in,
        'H_agua_out': H_agua_out,
    }


def main():
    print("=" * 78)
    print("ESCENARIO 01A - Calculo de temperatura de salida de glucosa")
    print("Proyecto W2605 - Analisis Termico del Tanque de Glucosa")
    print("=" * 78)
    print()
    print("Parametros del escenario:")
    print(f"  - Agua de servicio: {T_AGUA_IN}°C")
    print(f"  - Caudal de agua: {Q_AGUA_M3H} m3/h")
    print(f"  - Area de transferencia: {A_CHAQUETA} m2")
    print(f"  - Glucosa entrando: {T_GLUCOSA_IN}°C")
    print(f"  - Caudal glucosa: {M_GLUCOSA_KGH} kg/h")
    print(f"  - Aislamiento: {ESPESOR_AISLAMIENTO*1000:.1f} mm (CORREGIDO)")
    print(f"  - Velocidad agua media caña: {V_AGUA_MC:.3f} m/s")
    print()
    
    velocidades = [1.0, 1.5, 3.0]
    resultados = []
    
    print("-" * 78)
    print("RESULTADOS:")
    print("-" * 78)
    
    for v in velocidades:
        res = calcular_T_salida(v)
        resultados.append(res)
        
        print()
        print(f"Velocidad del viento: {v:.1f} m/s")
        print(f"  COEFICIENTES CHAQUETA:")
        print(f"    U_real: {res['U_chaqueta']:.2f} W/m2K")
        print(f"    h_i (agua): {res['h_i']:.1f} W/m2K")
        print(f"    h_o (glucosa): {res['h_o']:.2f} W/m2K")
        print()
        print(f"  PERDIDAS AL AMBIENTE:")
        print(f"    h_ext (viento): {res['h_ext']:.2f} W/m2K")
        print(f"    U_perdidas: {res['U_perdidas']:.3f} W/m2K")
        print(f"    R_aislamiento (5mm): {res['R_aislamiento']:.4f} m2K/W")
        print(f"    A_superficie: {res['A_superficie']:.2f} m2")
        print()
        print(f"  TEMPERATURA DE SALIDA DE GLUCOSA: {res['T_salida']:.2f}°C")
        print()
        print(f"  BALANCE ENERGETICO:")
        print(f"    Q_chaqueta (ganado):  {res['Q_chaqueta_MJ_h']:.1f} MJ/h")
        print(f"    Q_perdidas (perdido): {res['Q_perdidas_MJ_h']:.1f} MJ/h")
        print(f"    Q_net:                {res['Q_net_MJ_h']:.1f} MJ/h")
        print()
        print(f"  CORRIENTES:")
        print(f"    Glucosa entrada: {M_GLUCOSA_KGH:.0f} kg/h | {res['T_glucosa_in']:.1f}°C | {res['H_gluc_in']:.1f} MJ/h")
        print(f"    Glucosa salida:  {M_GLUCOSA_KGH:.0f} kg/h | {res['T_salida']:.2f}°C | {res['H_gluc_out']:.1f} MJ/h")
        print(f"    Agua entrada:    {Q_AGUA_M3H*1000:.0f} kg/h | {res['T_agua_in']:.1f}°C | {res['H_agua_in']:.1f} MJ/h")
        print(f"    Agua salida:     {Q_AGUA_M3H*1000:.0f} kg/h | {res['T_agua_out']:.2f}°C | {res['H_agua_out']:.1f} MJ/h")
        print()
    
    # Exportar a CSV
    csv_path = '../results/escenario_02a_1_resultados.csv'
    with open(csv_path, 'w') as f:
        f.write("v_viento_m_s,T_salida_C,U_chaqueta_W_m2K,Q_chaqueta_MJ_h,Q_perdidas_MJ_h,Q_net_MJ_h\n")
        for res in resultados:
            f.write(f"{res['v_viento']:.1f},{res['T_salida']:.2f},{res['U_chaqueta']:.2f},")
            f.write(f"{res['Q_chaqueta_MJ_h']:.2f},{res['Q_perdidas_MJ_h']:.2f},{res['Q_net_MJ_h']:.2f}\n")
    
    print(f"Resultados exportados a: {csv_path}")
    
    return resultados


if __name__ == "__main__":
    main()
