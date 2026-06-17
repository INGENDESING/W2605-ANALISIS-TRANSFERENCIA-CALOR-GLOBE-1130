"""
Módulo de cálculos con área fija (13 m²)
Simulación de ciclo de descargas a carrotanque
"""
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from coeficiente_U import coeficiente_U
from geometria_tanque import A_CONTACTO, volumen_total

# Constantes del sistema
A_FIJA = 13.0  # m²
V_AGUA_DEFAULT = 2.5  # m/s
MASA_POR_DESCARGA_DEFAULT = 24000.0  # kg (24 ton)
TIEMPO_DESCARGA_DEFAULT = 1.5  # horas


def calcular_flujo_maximo(temp_entrada, temp_salida, temp_agua, v_agua=V_AGUA_DEFAULT, area=None):
    """
    Calcular flujo máximo de descarga dado un rango de temperaturas
    
    Parameters
    ----------
    temp_entrada : float
        Temperatura de entrada de glucosa en °C
    temp_salida : float
        Temperatura de salida deseada en °C
    temp_agua : float
        Temperatura del agua en °C
    v_agua : float
        Velocidad del agua en m/s
    area : float, optional
        Área de transferencia (default: 13 m²)
    
    Returns
    -------
    dict
        Flujo máximo y parámetros relacionados
    """
    A = area if area else A_FIJA
    
    # Temperatura promedio
    T_prom = (temp_entrada + temp_salida) / 2
    
    # Coeficiente U
    U, _, _, _ = coeficiente_U(v_agua, temp_agua, T_prom)
    
    # LMTD
    dT1 = temp_agua - temp_entrada
    dT2 = temp_agua - temp_salida
    if abs(dT1 - dT2) < 0.01:
        LMTD = dT1
    else:
        LMTD = (dT1 - dT2) / np.log(dT1 / dT2)
    
    # Potencia disponible
    Q_disponible = U * A * LMTD
    
    # Flujo máximo (balance energía)
    Cp = Cp_glucosa(T_prom)
    delta_T = temp_salida - temp_entrada
    
    if delta_T <= 0:
        return {
            'error': 'Temperatura de salida debe ser mayor que entrada',
            'flujo_kg_s': 0,
            'flujo_ton_h': 0
        }
    
    m_dot_max = Q_disponible / (Cp * delta_T)  # kg/s
    flujo_ton_h = m_dot_max * 3.6  # Convertir a ton/h
    
    # Tiempo para descargar 24 ton
    tiempo_descarga_h = MASA_POR_DESCARGA_DEFAULT / (m_dot_max * 3600)
    
    # Descargas por día
    descargas_dia = 24 / tiempo_descarga_h if tiempo_descarga_h > 0 else 0
    
    return {
        'U': round(U, 2),
        'LMTD': round(LMTD, 2),
        'Q_disponible_W': round(Q_disponible, 2),
        'Q_disponible_kW': round(Q_disponible / 1000, 3),
        'Cp_glucosa': round(Cp, 2),
        'delta_T': round(delta_T, 2),
        'flujo_kg_s': round(m_dot_max, 4),
        'flujo_ton_h': round(flujo_ton_h, 2),
        'tiempo_descarga_24ton_h': round(tiempo_descarga_h, 2),
        'descargas_por_dia': int(descargas_dia),
        'capacidad_diaria_ton': int(descargas_dia * 24)
    }


def calcular_capacidad_descarga(temp_inicial, temp_agua, 
                                num_descargas=5, 
                                masa_por_descarga_kg=MASA_POR_DESCARGA_DEFAULT,
                                tiempo_descarga_h=TIEMPO_DESCARGA_DEFAULT,
                                nivel_inicial_pct=80,
                                v_agua=V_AGUA_DEFAULT):
    """
    Calcular capacidad operativa de descarga
    
    Parameters
    ----------
    temp_inicial : float
        Temperatura inicial de glucosa en °C
    temp_agua : float
        Temperatura del agua en °C
    num_descargas : int
        Número de descargas a simular
    masa_por_descarga_kg : float
        Masa por cada descarga en kg
    tiempo_descarga_h : float
        Tiempo de cada descarga en horas
    nivel_inicial_pct : float
        Nivel inicial del tanque en porcentaje
    v_agua : float
        Velocidad del agua en m/s
    
    Returns
    -------
    dict
        Resultados de capacidad
    """
    V_total = volumen_total()
    V_inicial = V_total * (nivel_inicial_pct / 100)
    rho_inicial = rho_glucosa(temp_inicial)
    masa_inicial = V_inicial * rho_inicial
    
    # Flujo de salida
    dot_m_out = masa_por_descarga_kg / (tiempo_descarga_h * 3600)
    
    # Calcular flujo máximo promedio (para temperaturas típicas)
    T_prom_op = (temp_inicial + 60) / 2  # Asumiendo operación hacia 60°C
    flujo_info = calcular_flujo_maximo(temp_inicial, 60, temp_agua, v_agua)
    
    # Capacidad máxima teórica
    capacidad_max_ton_dia = flujo_info['capacidad_diaria_ton']
    
    # Limitación por masa disponible
    masa_total_disponible = masa_inicial
    descargas_posibles = int(masa_total_disponible / masa_por_descarga_kg)
    
    return {
        'temp_inicial': temp_inicial,
        'temp_agua': temp_agua,
        'masa_inicial_kg': round(masa_inicial, 2),
        'masa_inicial_ton': round(masa_inicial / 1000, 2),
        'volumen_inicial_m3': round(V_inicial, 2),
        'flujo_maximo_ton_h': flujo_info['flujo_ton_h'],
        'capacidad_maxima_ton_dia': capacidad_max_ton_dia,
        'num_descargas_planificadas': num_descargas,
        'descargas_posibles_masa': descargas_posibles,
        'tiempo_descarga_h': tiempo_descarga_h,
        'masa_por_descarga_ton': round(masa_por_descarga_kg / 1000, 2),
        'flujo_descarga_kg_s': round(dot_m_out, 3)
    }


def simular_ciclo_descargas(temp_inicial, temp_agua, 
                           num_descargas=5,
                           masa_por_descarga_kg=MASA_POR_DESCARGA_DEFAULT,
                           tiempo_descarga_h=TIEMPO_DESCARGA_DEFAULT,
                           nivel_inicial_pct=80,
                           v_agua=V_AGUA_DEFAULT,
                           periodo_ciclo_h=4.8):
    """
    Simular ciclo completo de descargas
    
    Parameters
    ----------
    temp_inicial : float
        Temperatura inicial en °C
    temp_agua : float
        Temperatura del agua en °C
    num_descargas : int
        Número de descargas
    masa_por_descarga_kg : float
        Masa por descarga en kg
    tiempo_descarga_h : float
        Duración de cada descarga en horas
    nivel_inicial_pct : float
        Nivel inicial en porcentaje
    v_agua : float
        Velocidad del agua en m/s
    periodo_ciclo_h : float
        Período entre inicios de descarga en horas
    
    Returns
    -------
    dict
        Serie temporal completa y métricas
    """
    A = A_FIJA
    
    # Condiciones iniciales
    V_total = volumen_total()
    V_inicial = V_total * (nivel_inicial_pct / 100)
    rho_inicial = rho_glucosa(temp_inicial)
    masa_inicial = V_inicial * rho_inicial
    
    # Flujo de salida
    dot_m_out = masa_por_descarga_kg / (tiempo_descarga_h * 3600)
    
    # Tiempo de calentamiento entre descargas
    tiempo_calentamiento_h = periodo_ciclo_h - tiempo_descarga_h
    
    # Función ODE
    def ode_sistema(t, y, descargando):
        T_g, m_g = y
        
        if m_g < 1000:
            return [0.0, 0.0]
        
        Cp_g = Cp_glucosa(T_g)
        U, _, _, _ = coeficiente_U(v_agua, temp_agua, T_g)
        
        # Control termostático máximo 60°C
        DeltaT = temp_agua - T_g
        if DeltaT < 0.01 or T_g >= 60.0:
            dT_dt = 0.0
        else:
            dT_dt = U * A * DeltaT / (m_g * Cp_g)
        
        if descargando:
            dm_dt = -dot_m_out
        else:
            dm_dt = 0.0
        
        return [dT_dt, dm_dt]
    
    # Simulación
    t_total = []
    T_total = []
    m_total = []
    fases_info = []
    descargas_info = []
    
    t_actual = 0.0
    T_actual = temp_inicial
    m_actual = masa_inicial
    
    for i_descarga in range(num_descargas):
        # Fase 1: Descarga
        t_ini_desc = t_actual
        t_fin_desc = t_actual + tiempo_descarga_h * 3600
        T_inicio_desc = T_actual
        m_inicio_desc = m_actual
        
        t_eval = np.arange(t_ini_desc, t_fin_desc + 1, 30)
        if t_eval[-1] > t_fin_desc:
            t_eval[-1] = t_fin_desc
        
        sol_desc = solve_ivp(
            lambda t, y: ode_sistema(t, y, True),
            [t_ini_desc, t_fin_desc],
            [T_actual, m_actual],
            t_eval=t_eval,
            method='RK45',
            max_step=60.0
        )
        
        t_total.extend(sol_desc.t.tolist())
        T_total.extend(sol_desc.y[0].tolist())
        m_total.extend(sol_desc.y[1].tolist())
        
        T_fin_desc = sol_desc.y[0][-1]
        m_fin_desc = sol_desc.y[1][-1]
        
        descargas_info.append({
            'descarga': i_descarga + 1,
            't_inicio_h': round(t_ini_desc / 3600, 2),
            't_fin_h': round(t_fin_desc / 3600, 2),
            'T_inicio': round(T_inicio_desc, 2),
            'T_fin': round(T_fin_desc, 2),
            'm_inicio_kg': round(m_inicio_desc, 2),
            'm_fin_kg': round(m_fin_desc, 2),
            'masa_descargada_kg': round(m_inicio_desc - m_fin_desc, 2)
        })
        
        fases_info.append({
            'tipo': 'descarga',
            'descarga_num': i_descarga + 1,
            't_inicio_h': round(t_ini_desc / 3600, 2),
            't_fin_h': round(t_fin_desc / 3600, 2)
        })
        
        t_actual = t_fin_desc
        T_actual = T_fin_desc
        m_actual = m_fin_desc
        
        # Fase 2: Calentamiento
        if i_descarga < num_descargas - 1 and tiempo_calentamiento_h > 0:
            t_ini_cal = t_actual
            t_fin_cal = t_actual + tiempo_calentamiento_h * 3600
            T_inicio_cal = T_actual
            
            t_eval_cal = np.arange(t_ini_cal, t_fin_cal + 1, 30)
            if t_eval_cal[-1] > t_fin_cal:
                t_eval_cal[-1] = t_fin_cal
            
            if len(t_eval_cal) > 1:
                sol_cal = solve_ivp(
                    lambda t, y: ode_sistema(t, y, False),
                    [t_ini_cal, t_fin_cal],
                    [T_actual, m_actual],
                    t_eval=t_eval_cal,
                    method='RK45',
                    max_step=60.0
                )
                
                t_total.extend(sol_cal.t.tolist())
                T_total.extend(sol_cal.y[0].tolist())
                m_total.extend(sol_cal.y[1].tolist())
                
                T_actual = sol_cal.y[0][-1]
                m_actual = sol_cal.y[1][-1]
            
            fases_info.append({
                'tipo': 'calentamiento',
                't_inicio_h': round(t_ini_cal / 3600, 2),
                't_fin_h': round(t_fin_cal / 3600, 2)
            })
            
            t_actual = t_fin_cal
    
    # Convertir a arrays y calcular U, Q
    t_h = np.array(t_total) / 3600.0
    T_g = np.array(T_total)
    m_g = np.array(m_total)
    
    U_hist = np.zeros_like(T_g)
    Q_hist = np.zeros_like(T_g)
    
    for i in range(len(T_g)):
        if T_g[i] < temp_agua - 0.1:
            U_val, _, _, _ = coeficiente_U(v_agua, temp_agua, T_g[i])
            U_hist[i] = U_val
            Q_hist[i] = U_val * A * (temp_agua - T_g[i])
        else:
            U_hist[i] = U_hist[max(0, i - 1)]
    
    # Serie temporal para respuesta
    serie_temporal = []
    for i in range(len(t_h)):
        serie_temporal.append({
            't_h': round(t_h[i], 3),
            'T_glucosa': round(T_g[i], 3),
            'm_kg': round(m_g[i], 2),
            'm_ton': round(m_g[i] / 1000, 3),
            'U': round(U_hist[i], 3),
            'Q_W': round(Q_hist[i], 2),
            'Q_kW': round(Q_hist[i] / 1000, 4)
        })
    
    return {
        'serie_temporal': serie_temporal,
        'descargas': descargas_info,
        'fases': fases_info,
        'temp_final': round(T_g[-1], 2),
        'masa_final_kg': round(m_g[-1], 2),
        'masa_final_ton': round(m_g[-1] / 1000, 3),
        'temp_min': round(float(np.min(T_g)), 2),
        'temp_max': round(float(np.max(T_g)), 2),
        'U_promedio': round(float(np.mean(U_hist)), 2),
        'tiempo_total_h': round(t_h[-1], 2),
        'masa_total_descargada_ton': round(sum(d['masa_descargada_kg'] for d in descargas_info) / 1000, 2)
    }
