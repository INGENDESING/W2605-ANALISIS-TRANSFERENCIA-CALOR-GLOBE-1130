"""
Script maestro de calculo termico para todos los subescenarios del Proyecto W2605.
Genera archivos CSV con resultados para v_viento = [1.0, 1.5, 3.0] m/s.
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))

from propiedades_glucosa import rho_glucosa, Cp_glucosa, Cp_agua, rho_agua
from geometria_tanque import volumen_total, OD_SHELL, t_HEAD, A_CONTACTO
from coeficiente_U import coeficiente_U
from calculo_calor_perdido_80 import (
    h_conveccion_viento, area_fondo_torisferico, area_cilindrica_al_80porciento,
    T_AMBIENTE, K_AISLAMIENTO
)

# Constantes fisicas
K_SS316L = 16.3
h_int_glucosa = 28.0
ESPESOR_AISLAMIENTO = 0.005


def calcular_escenario(config):
    """
    Calcula los resultados termicos para una configuracion dada.
    """
    T_AGUA_IN = config['T_agua']
    Q_AGUA_M3H = config['Q_agua']
    A_CHAQUETA = config['A_chaqueta']
    T_GLUCOSA_IN = config['T_gluc']
    V_AGUA_MC = config['V_agua']
    M_GLUCOSA_KGH = 8000.0
    
    def calcular_U_chaqueta(T_glucosa, T_agua):
        U_val, h_i, h_o, info = coeficiente_U(V_AGUA_MC, T_agua, T_glucosa)
        return U_val, h_i, h_o, info
    
    def calcular_Q_chaqueta_real(T_glucosa_in, T_glucosa_out, T_agua_in):
        T_glucosa_prom = (T_glucosa_in + T_glucosa_out) / 2
        U_real, h_i, h_o, info = calcular_U_chaqueta(T_glucosa_prom, T_agua_in)
        T_agua_out = T_agua_in - 1.0
        
        for _ in range(10):
            T_agua_prom = (T_agua_in + T_agua_out) / 2
            rho_w = rho_agua(T_agua_prom)
            Cp_w = Cp_agua(T_agua_prom)
            m_dot_agua = Q_AGUA_M3H * rho_w / 3600.0
            
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
        T_pelicula = (T_glucosa_prom + T_AMBIENTE) / 2
        D_ext = OD_SHELL
        h_ext, Re, Nu = h_conveccion_viento(v_viento, T_pelicula, D_ext)
        
        R_conv_int = 1.0 / h_int_glucosa
        R_pared = t_HEAD / K_SS316L
        R_aislamiento = ESPESOR_AISLAMIENTO / K_AISLAMIENTO
        R_conv_ext = 1.0 / h_ext
        
        R_total = R_conv_int + R_pared + R_aislamiento + R_conv_ext
        U_global = 1.0 / R_total
        
        A_fondo = area_fondo_torisferico()
        A_cil_80, _, _ = area_cilindrica_al_80porciento()
        A_total = A_fondo + A_cil_80
        
        Delta_T = T_glucosa_prom - T_AMBIENTE
        Q_perdidas = U_global * A_total * Delta_T
        
        return Q_perdidas, h_ext, U_global, A_total, R_total, R_aislamiento
    
    def calcular_T_salida(v_viento):
        T_salida = T_GLUCOSA_IN - 1.0
        
        for iteration in range(30):
            T_prom = (T_GLUCOSA_IN + T_salida) / 2
            if np.isnan(T_prom) or T_prom < 0 or T_prom > 200:
                break
            
            Cp_g = Cp_glucosa(T_prom)
            if np.isnan(Cp_g) or Cp_g <= 0:
                break
            
            Q_chaq, T_agua_out, U_real, h_i, h_o = calcular_Q_chaqueta_real(T_GLUCOSA_IN, T_salida, T_AGUA_IN)
            if np.isnan(Q_chaq):
                break
            
            Q_perd, h_ext, U_perd, A_total, R_total, R_aisl = calcular_Q_perdidas(v_viento, T_prom)
            if np.isnan(Q_perd) or np.isnan(h_ext):
                break
            
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
        
        T_prom_final = (T_GLUCOSA_IN + T_salida) / 2
        Cp_g_final = Cp_glucosa(T_prom_final)
        
        Q_chaq_final, T_agua_out_final, U_real_final, h_i_final, h_o_final = calcular_Q_chaqueta_real(T_GLUCOSA_IN, T_salida, T_AGUA_IN)
        Q_perd_final, h_ext_final, U_perd_final, A_total, R_total, R_aisl_final = calcular_Q_perdidas(v_viento, T_prom_final)
        
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
    
    resultados = []
    for v in [1.0, 1.5, 3.0]:
        res = calcular_T_salida(v)
        resultados.append(res)
    
    return resultados


def main():
    ESCENARIOS = [
        # 01A
        {'codigo': '01a_1', 'T_agua': 65.0, 'Q_agua': 30.9, 'A_chaqueta': 13.0, 'T_gluc': 60.0, 'V_agua': 1.338},
        {'codigo': '01a_2', 'T_agua': 65.0, 'Q_agua': 30.9, 'A_chaqueta': 13.0, 'T_gluc': 57.0, 'V_agua': 1.338},
        {'codigo': '01a_3', 'T_agua': 65.0, 'Q_agua': 30.9, 'A_chaqueta': 13.0, 'T_gluc': 54.0, 'V_agua': 1.338},
        # 01B
        {'codigo': '01b_1', 'T_agua': 65.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 60.0, 'V_agua': 2.5},
        {'codigo': '01b_2', 'T_agua': 65.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 57.0, 'V_agua': 2.5},
        {'codigo': '01b_3', 'T_agua': 65.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 54.0, 'V_agua': 2.5},
        # 01C
        {'codigo': '01c_1', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 60.0, 'V_agua': 2.5},
        {'codigo': '01c_2', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 57.0, 'V_agua': 2.5},
        {'codigo': '01c_3', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 13.0, 'T_gluc': 54.0, 'V_agua': 2.5},
        # 02A
        {'codigo': '02a_1', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 28.0, 'T_gluc': 60.0, 'V_agua': 2.5},
        {'codigo': '02a_2', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 28.0, 'T_gluc': 57.0, 'V_agua': 2.5},
        {'codigo': '02a_3', 'T_agua': 75.0, 'Q_agua': 57.7, 'A_chaqueta': 28.0, 'T_gluc': 54.0, 'V_agua': 2.5},
    ]
    
    for esc in ESCENARIOS:
        print(f"Calculando {esc['codigo']}...")
        resultados = calcular_escenario(esc)
        csv_path = f"../results/escenario_{esc['codigo']}_resultados.csv"
        with open(csv_path, 'w') as f:
            f.write("v_viento_m_s,T_salida_C,T_agua_out_C,U_chaqueta_W_m2K,h_i_W_m2K,h_o_W_m2K,h_ext_W_m2K,U_perdidas_W_m2K,Q_chaqueta_MJ_h,Q_perdidas_MJ_h,Q_net_MJ_h,H_agua_in_MJ_h,H_agua_out_MJ_h,H_gluc_in_MJ_h,H_gluc_out_MJ_h\n")
            for res in resultados:
                f.write(f"{res['v_viento']:.1f},{res['T_salida']:.2f},{res['T_agua_out']:.2f},{res['U_chaqueta']:.2f},")
                f.write(f"{res['h_i']:.1f},{res['h_o']:.2f},{res['h_ext']:.2f},{res['U_perdidas']:.4f},")
                f.write(f"{res['Q_chaqueta_MJ_h']:.2f},{res['Q_perdidas_MJ_h']:.2f},{res['Q_net_MJ_h']:.2f},")
                f.write(f"{res['H_agua_in']:.1f},{res['H_agua_out']:.1f},{res['H_gluc_in']:.1f},{res['H_gluc_out']:.1f}\n")
        print(f"  Exportado: {csv_path}")
        # Mostrar resumen v=1.5
        res_15 = [r for r in resultados if abs(r['v_viento'] - 1.5) < 0.01][0]
        print(f"  v=1.5 m/s -> T_sal={res_15['T_salida']:.2f}C, U={res_15['U_chaqueta']:.2f}, Q_net={res_15['Q_net_MJ_h']:.2f} MJ/h")


if __name__ == "__main__":
    main()
