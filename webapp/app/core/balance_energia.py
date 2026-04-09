"""
Módulo de balance de energía - Cálculos de transferencia de calor
Integra los módulos existentes del proyecto P2611
"""
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

# Importar módulos existentes
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from propiedades_glucosa import (
    rho_glucosa, mu_glucosa, Cp_glucosa, k_glucosa, Pr_glucosa,
    rho_agua, Cp_agua
)
from coeficiente_U import coeficiente_U
from geometria_tanque import (
    A_CONTACTO, volumen_total, caudal_desde_velocidad_media_cana
)


def calcular_transferencia_calor(flujo_agua_m3h, temp_agua_entrada, 
                                  temp_glucosa, temp_glucosa_objetivo=None,
                                  volumen_glucosa_m3=24, area_contacto=None):
    """
    Calcular parámetros de transferencia de calor
    
    Parameters
    ----------
    flujo_agua_m3h : float
        Flujo de agua en m³/h
    temp_agua_entrada : float
        Temperatura de entrada del agua en °C
    temp_glucosa : float
        Temperatura actual de la glucosa en °C
    temp_glucosa_objetivo : float, optional
        Temperatura objetivo de la glucosa en °C
    volumen_glucosa_m3 : float
        Volumen de glucosa en m³
    area_contacto : float, optional
        Área de contacto en m² (default: 13.0)
    
    Returns
    -------
    dict
        Resultados del cálculo
    """
    # Parámetros
    A = area_contacto if area_contacto else A_CONTACTO
    Q_agua = flujo_agua_m3h / 3600.0  # Convertir a m³/s
    
    # Velocidad en media caña
    v_agua = flujo_agua_m3h / 30.9 * 1.338  # Escalamiento desde caso base
    
    # Propiedades de la glucosa a temperatura actual
    rho_g = rho_glucosa(temp_glucosa)
    Cp_g = Cp_glucosa(temp_glucosa)
    mu_g = mu_glucosa(temp_glucosa)
    k_g = k_glucosa(temp_glucosa)
    Pr_g = Pr_glucosa(temp_glucosa)
    
    # Coeficiente U
    T_agua_media = temp_agua_entrada - 2  # Estimación
    U, h_i, h_o, info = coeficiente_U(v_agua, T_agua_media, temp_glucosa)
    
    # Delta T
    DeltaT = temp_agua_entrada - temp_glucosa
    
    # Potencia térmica
    Q_termica = U * A * DeltaT  # W
    
    # Temperatura salida agua (balance)
    m_dot_agua = Q_agua * rho_agua(T_agua_media)
    DeltaT_agua = Q_termica / (m_dot_agua * Cp_agua(T_agua_media))
    temp_agua_salida = temp_agua_entrada - DeltaT_agua
    
    # Tiempo para alcanzar objetivo (si se especifica)
    tiempo_calentamiento = None
    if temp_glucosa_objetivo and temp_glucosa_objetivo > temp_glucosa:
        tiempo_calentamiento = calcular_tiempo_calentamiento(
            temp_glucosa, temp_glucosa_objetivo, 
            temp_agua_entrada, v_agua, volumen_glucosa_m3
        )
    
    # Área requerida para calentamiento en tiempo específico
    # (implementar si se necesita)
    
    return {
        'coeficiente_U': round(U, 2),
        'h_i': round(h_i, 2),
        'h_o': round(h_o, 2),
        'R_total': round(info['R_total'], 6),
        'pct_R_i': round(info['pct_R_i'], 1),
        'pct_R_w': round(info['pct_R_w'], 1),
        'pct_R_o': round(info['pct_R_o'], 1),
        'potencia_termica_W': round(Q_termica, 2),
        'potencia_termica_kW': round(Q_termica / 1000, 3),
        'temp_agua_salida_c': round(temp_agua_salida, 2),
        'delta_T_agua_c': round(DeltaT_agua, 3),
        'densidad_glucosa_kg_m3': round(rho_g, 2),
        'viscosidad_glucosa_Pa_s': round(mu_g, 4),
        'viscosidad_glucosa_cP': round(mu_g * 1000, 2),
        'cp_glucosa_J_kg_C': round(Cp_g, 2),
        'k_glucosa_W_m_C': round(k_g, 4),
        'prandtl_glucosa': round(Pr_g, 1),
        'reynolds_agua': round(info['Re_agua'], 0),
        'nusselt_agua': round(info['Nu_agua'], 2),
        'tiempo_calentamiento_h': round(tiempo_calentamiento, 2) if tiempo_calentamiento else None,
        'area_contacto_m2': round(A, 2)
    }


def calcular_tiempo_calentamiento(T_inicial, T_objetivo, T_agua, v_agua, volumen_glucosa):
    """
    Calcular tiempo necesario para alcanzar temperatura objetivo
    
    Parameters
    ----------
    T_inicial : float
        Temperatura inicial de glucosa en °C
    T_objetivo : float
        Temperatura objetivo en °C
    T_agua : float
        Temperatura del agua en °C
    v_agua : float
        Velocidad del agua en m/s
    volumen_glucosa : float
        Volumen de glucosa en m³
    
    Returns
    -------
    float
        Tiempo en horas
    """
    A = A_CONTACTO
    
    def dTdt(t, T):
        if T[0] >= T_agua - 0.5 or T[0] >= T_objetivo:
            return [0.0]
        
        rho_g = rho_glucosa(T[0])
        Cp_g = Cp_glucosa(T[0])
        m_g = rho_g * volumen_glucosa
        
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T[0])
        DeltaT = T_agua - T[0]
        
        dT = U * A * DeltaT / (m_g * Cp_g)
        return [dT]
    
    # Resolver ODE
    sol = solve_ivp(dTdt, [0, 86400], [T_inicial],  # Máximo 24 horas
                    method='RK45', max_step=300, rtol=1e-6,
                    dense_output=True)
    
    # Encontrar cuando alcanza T_objetivo
    t_vals = np.linspace(0, sol.t[-1], 1000)
    T_vals = sol.sol(t_vals)[0]
    
    idx = np.where(T_vals >= T_objetivo)[0]
    if len(idx) > 0:
        return t_vals[idx[0]] / 3600.0  # Convertir a horas
    
    return None


def calcular_area_requerida(Q_termica, U, T_agua, T_glucosa):
    """
    Calcular área requerida para una potencia térmica dada
    
    Parameters
    ----------
    Q_termica : float
        Potencia térmica en W
    U : float
        Coeficiente global en W/m²·°C
    T_agua : float
        Temperatura del agua en °C
    T_glucosa : float
        Temperatura de la glucosa en °C
    
    Returns
    -------
    float
        Área requerida en m²
    """
    DeltaT = T_agua - T_glucosa
    if DeltaT <= 0:
        return float('inf')
    return Q_termica / (U * DeltaT)


def simular_calentamiento_transitorio(T_inicial, T_agua, v_agua, volumen_glucosa, 
                                       t_final_h=24, dt_min=10):
    """
    Simular calentamiento transitorio completo
    
    Returns
    -------
    dict con serie temporal
    """
    A = A_CONTACTO
    
    def dTdt(t, T):
        if T[0] >= T_agua - 0.5:
            return [0.0]
        
        rho_g = rho_glucosa(T[0])
        Cp_g = Cp_glucosa(T[0])
        m_g = rho_g * volumen_glucosa
        
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T[0])
        DeltaT = T_agua - T[0]
        
        dT = U * A * DeltaT / (m_g * Cp_g)
        return [dT]
    
    t_span = (0, t_final_h * 3600)
    t_eval = np.arange(0, t_final_h * 3600 + 1, dt_min * 60)
    
    sol = solve_ivp(dTdt, t_span, [T_inicial], t_eval=t_eval,
                    method='RK45', max_step=300, rtol=1e-6)
    
    # Calcular U y Q en cada punto
    serie = []
    for i, (t, T) in enumerate(zip(sol.t, sol.y[0])):
        if T < T_agua - 0.5:
            U, _, _, info = coeficiente_U(v_agua, T_agua, T)
            Q = U * A * (T_agua - T)
        else:
            U = serie[-1]['U'] if serie else 0
            Q = 0
        
        serie.append({
            't_h': round(t / 3600, 3),
            'T_glucosa': round(T, 3),
            'U': round(U, 3),
            'Q_W': round(Q, 2),
            'Q_kW': round(Q / 1000, 4),
            'rho_glucosa': round(rho_glucosa(T), 2),
            'mu_glucosa_cP': round(mu_glucosa(T) * 1000, 2)
        })
    
    return {
        'serie_temporal': serie,
        'tiempo_total_h': round(sol.t[-1] / 3600, 2),
        'temp_final': round(sol.y[0][-1], 2)
    }
