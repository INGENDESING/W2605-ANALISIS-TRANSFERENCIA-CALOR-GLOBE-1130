"""
Módulo de balance de energía - Cálculos de transferencia de calor
Integra los módulos existentes del proyecto W2605
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
        Área de contacto en m² (default: A_CONTACTO = 14.0)
    
    Returns
    -------
    dict
        Resultados del cálculo
    """
    # Parámetros
    A = area_contacto if area_contacto else A_CONTACTO
    Q_agua = flujo_agua_m3h / 3600.0  # Convertir a m³/s
    
    # Velocidad en media caña — geometría real: sección 45.5×141 mm
    A_sec_mc = 0.0455 * 0.141  # m² = 6.4155e-3 m²
    v_agua = (flujo_agua_m3h / 3600.0) / A_sec_mc  # m/s
    
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


def simular_calentamiento_y_ciclo(T_inicial, T_objetivo_inicio_descarga,
                                   T_agua, v_agua, area,
                                   volumen_inicial_m3,
                                   num_descargas, masa_por_descarga_kg,
                                   tiempo_descarga_h, periodo_ciclo_h,
                                   temp_minima_aceptable=55.0,
                                   dt_seg=30,
                                   max_descargas=5):
    """
    Simulacion completa: calentamiento inicial + ciclo de descargas.

    El numero de descargas se limita a max_descargas (5 descargas/dia por
    requerimiento operativo del proyecto W2605).
    """
    """
    Simulación completa: calentamiento inicial + ciclo de descargas.

    Fase 1: ODE desde T_inicial hasta T_objetivo (glucosa en reposo, sin descarga).
    Fase 2: ciclo de N descargas (ODE con dm/dt durante descargas).

    Retorna serie temporal unificada con etiqueta de fase por punto.
    """
    A = area
    dot_m_out = masa_por_descarga_kg / (tiempo_descarga_h * 3600.0)
    tiempo_calentamiento_entre_h = periodo_ciclo_h - tiempo_descarga_h

    rho_ini = rho_glucosa(T_inicial)
    masa_inicial = volumen_inicial_m3 * rho_ini

    serie = []   # puntos de la serie temporal unificada
    fases = []   # resumen de fases
    descargas = []

    def _ode_sin_descarga(t, y):
        T = y[0]
        if T >= T_agua - 0.1:
            return [0.0]
        m = y[1] if len(y) > 1 else None
        rho_g = rho_glucosa(T)
        Cp_g = Cp_glucosa(T)
        mass = m if m is not None else rho_g * volumen_inicial_m3
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        dT = U * A * (T_agua - T) / (mass * Cp_g)
        return [dT]

    def _ode_con_masa(t, y, descargando):
        T, m = y
        if m < 500:
            return [0.0, 0.0]
        Cp_g = Cp_glucosa(T)
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        DeltaT = T_agua - T
        dT = U * A * DeltaT / (m * Cp_g) if DeltaT > 0.01 else 0.0
        dm = -dot_m_out if descargando else 0.0
        return [dT, dm]

    t_cursor = 0.0  # segundos

    # ── FASE 1: Calentamiento inicial ─────────────────────────────────────────
    t_max_cal = min(int(tiempo_maximo_h * 3600), 36 * 3600)  # respetar límite global
    t_eval_f1 = np.arange(0, t_max_cal + 1, dt_seg)

    sol_f1 = solve_ivp(
        lambda t, y: _ode_sin_descarga(t, y),
        [0, t_max_cal],
        [T_inicial],
        t_eval=t_eval_f1,
        method='RK45', max_step=120,
        events=lambda t, y: y[0] - T_objetivo_inicio_descarga
    )
    # Cortar en el evento (temperatura objetivo alcanzada)
    t_f1 = sol_f1.t
    T_f1 = sol_f1.y[0]
    if sol_f1.t_events and len(sol_f1.t_events[0]) > 0:
        t_stop = sol_f1.t_events[0][0]
        mask = t_f1 <= t_stop
        t_f1 = t_f1[mask]
        T_f1 = T_f1[mask]

    m_f1 = np.full_like(T_f1, masa_inicial)

    for t, T, m in zip(t_f1, T_f1, m_f1):
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        Q = U * A * max(T_agua - T, 0)
        serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                      'T_glucosa': round(T, 3),
                      'm_ton': round(m / 1000, 3),
                      'U': round(U, 3),
                      'Q_kW': round(Q / 1000, 4),
                      'fase': 'calentamiento_inicial'})

    t_cal_ini_h = 0.0
    t_cal_fin_h = round(t_f1[-1] / 3600, 4)
    fases.append({'tipo': 'calentamiento_inicial',
                  't_inicio_h': t_cal_ini_h, 't_fin_h': t_cal_fin_h,
                  'T_inicio': round(T_inicial, 2),
                  'T_fin': round(T_f1[-1], 2)})

    t_cursor += t_f1[-1]
    T_actual = T_f1[-1]
    m_actual = masa_inicial

    # ── FASE 2: Ciclo de descargas ────────────────────────────────────────────
    num_descargas = min(int(num_descargas), int(max_descargas))
    for i in range(num_descargas):
        # — Descarga —
        t0 = 0.0
        t1 = tiempo_descarga_h * 3600
        t_eval_d = np.arange(t0, t1 + 1, dt_seg)
        sol_d = solve_ivp(
            lambda t, y: _ode_con_masa(t, y, True),
            [t0, t1], [T_actual, m_actual],
            t_eval=t_eval_d, method='RK45', max_step=60
        )
        T_ini_d = T_actual
        m_ini_d = m_actual
        for t, T, m in zip(sol_d.t, sol_d.y[0], sol_d.y[1]):
            U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
            Q = U * A * max(T_agua - T, 0)
            serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                          'T_glucosa': round(T, 3),
                          'm_ton': round(m / 1000, 3),
                          'U': round(U, 3),
                          'Q_kW': round(Q / 1000, 4),
                          'fase': f'descarga_{i+1}'})

        T_actual = sol_d.y[0][-1]
        m_actual = sol_d.y[1][-1]
        t_d_ini_h = round(t_cursor / 3600, 4)
        t_cursor += t1
        t_d_fin_h = round(t_cursor / 3600, 4)

        masa_desc = m_ini_d - m_actual
        T_promedio_U = (T_ini_d + T_actual) / 2
        U_prom, _, _, _ = coeficiente_U(v_agua, T_agua, T_promedio_U)
        estado = ('OK' if T_actual >= 55 else
                  'Marginal' if T_actual >= 50 else 'Fuera')
        descargas.append({'descarga': i + 1,
                          't_inicio_h': t_d_ini_h, 't_fin_h': t_d_fin_h,
                          'T_inicio': round(T_ini_d, 2),
                          'T_fin': round(T_actual, 2),
                          'm_inicio_ton': round(m_ini_d / 1000, 3),
                          'm_fin_ton': round(m_actual / 1000, 3),
                          'masa_descargada_ton': round(masa_desc / 1000, 3),
                          'U_prom': round(U_prom, 2),
                          'estado': estado})
        fases.append({'tipo': 'descarga', 'descarga_num': i + 1,
                      't_inicio_h': t_d_ini_h, 't_fin_h': t_d_fin_h,
                      'T_inicio': round(T_ini_d, 2), 'T_fin': round(T_actual, 2)})

        # — Calentamiento entre descargas —
        if i < num_descargas - 1 and tiempo_calentamiento_entre_h > 0:
            t0 = 0.0
            t1 = tiempo_calentamiento_entre_h * 3600
            t_eval_c = np.arange(t0, t1 + 1, dt_seg)
            sol_c = solve_ivp(
                lambda t, y: _ode_con_masa(t, y, False),
                [t0, t1], [T_actual, m_actual],
                t_eval=t_eval_c, method='RK45', max_step=60
            )
            T_ini_c = T_actual
            t_c_ini_h = round(t_cursor / 3600, 4)
            for t, T, m in zip(sol_c.t, sol_c.y[0], sol_c.y[1]):
                U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
                Q = U * A * max(T_agua - T, 0)
                serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                              'T_glucosa': round(T, 3),
                              'm_ton': round(m / 1000, 3),
                              'U': round(U, 3),
                              'Q_kW': round(Q / 1000, 4),
                              'fase': f'mantenimiento_{i+1}'})
            T_actual = sol_c.y[0][-1]
            m_actual = sol_c.y[1][-1]
            t_cursor += t1
            fases.append({'tipo': 'mantenimiento',
                          't_inicio_h': t_c_ini_h,
                          't_fin_h': round(t_cursor / 3600, 4),
                          'T_inicio': round(T_ini_c, 2),
                          'T_fin': round(T_actual, 2)})

    # ── Métricas de resumen ───────────────────────────────────────────────────
    T_vals = [p['T_glucosa'] for p in serie]
    masa_total_desc = sum(d['masa_descargada_ton'] for d in descargas)
    descargas_ok = sum(1 for d in descargas if d['estado'] == 'OK')

    return {
        'serie_temporal': serie,
        'fases': fases,
        'descargas': descargas,
        'metricas': {
            'tiempo_calentamiento_inicial_h': round(t_cal_fin_h, 3),
            'tiempo_total_h': round(t_cursor / 3600, 3),
            'T_final': round(T_actual, 2),
            'masa_total_descargada_ton': round(masa_total_desc, 2),
            'descargas_ok': descargas_ok,
            'descargas_totales': num_descargas,
            'T_min_ciclo': round(min(T_vals), 2),
            'T_promedio_ciclo': round(sum(T_vals) / len(T_vals), 2),
        }
    }


def simular_ciclo_automatico(T_inicial, T_objetivo_inicio_descarga,
                              T_agua, v_agua, area,
                              volumen_inicial_m3,
                              masa_por_descarga_kg,
                              tiempo_descarga_h, periodo_ciclo_h,
                              temp_minima_aceptable=55.0,
                              tiempo_maximo_h=24.0,
                              dt_seg=30,
                              max_descargas=5):
    """
    Simulación automática: calentamiento inicial + ciclo de descargas
    hasta que se violen restricciones.

    A diferencia de simular_calentamiento_y_ciclo(), aquí el número de
    descargas NO es un parámetro de entrada sino un RESULTADO calculado.

    Restricciones de corte (cualquiera detiene el ciclo):
      1. T glucosa < temp_minima_aceptable después de una descarga
      2. Masa restante < masa_por_descarga_kg
      3. Tiempo acumulado > tiempo_maximo_h (24 h)
    """
    A = area
    dot_m_out = masa_por_descarga_kg / (tiempo_descarga_h * 3600.0)
    tiempo_calentamiento_entre_h = periodo_ciclo_h - tiempo_descarga_h

    rho_ini = rho_glucosa(T_inicial)
    masa_inicial = volumen_inicial_m3 * rho_ini

    serie = []
    fases = []
    descargas = []

    def _ode_con_masa(t, y, descargando):
        T, m = y
        if m < 500:
            return [0.0, 0.0]
        Cp_g = Cp_glucosa(T)
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        DeltaT = T_agua - T
        dT = U * A * DeltaT / (m * Cp_g) if DeltaT > 0.01 else 0.0
        dm = -dot_m_out if descargando else 0.0
        return [dT, dm]

    t_cursor = 0.0

    # ── FASE 1: Calentamiento inicial ─────────────────────────────────────────
    t_max_cal = min(int(tiempo_maximo_h * 3600), 36 * 3600)  # respetar límite global
    t_eval_f1 = np.arange(0, t_max_cal + 1, dt_seg)

    def _ode_sin_descarga(t, y):
        T = y[0]
        if T >= T_agua - 0.1:
            return [0.0]
        rho_g = rho_glucosa(T)
        Cp_g = Cp_glucosa(T)
        mass = rho_g * volumen_inicial_m3
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        dT = U * A * (T_agua - T) / (mass * Cp_g)
        return [dT]

    sol_f1 = solve_ivp(
        lambda t, y: _ode_sin_descarga(t, y),
        [0, t_max_cal], [T_inicial],
        t_eval=t_eval_f1, method='RK45', max_step=120,
        events=lambda t, y: y[0] - T_objetivo_inicio_descarga
    )

    t_f1 = sol_f1.t
    T_f1 = sol_f1.y[0]
    if sol_f1.t_events and len(sol_f1.t_events[0]) > 0:
        t_stop = sol_f1.t_events[0][0]
        mask = t_f1 <= t_stop
        t_f1 = t_f1[mask]
        T_f1 = T_f1[mask]

    m_f1 = np.full_like(T_f1, masa_inicial)

    for t, T, m in zip(t_f1, T_f1, m_f1):
        U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
        Q = U * A * max(T_agua - T, 0)
        serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                      'T_glucosa': round(T, 3),
                      'm_ton': round(m / 1000, 3),
                      'U': round(U, 3),
                      'Q_kW': round(Q / 1000, 4),
                      'fase': 'calentamiento_inicial'})

    t_cal_fin_h = round(t_f1[-1] / 3600, 4)
    fases.append({'tipo': 'calentamiento_inicial',
                  't_inicio_h': 0.0, 't_fin_h': t_cal_fin_h,
                  'T_inicio': round(T_inicial, 2),
                  'T_fin': round(T_f1[-1], 2)})

    t_cursor += t_f1[-1]
    T_actual = T_f1[-1]
    m_actual = masa_inicial

    # ── FASE 2: Ciclo automático de descargas ─────────────────────────────────
    i_descarga = 0
    motivo_corte = 'completado'

    while True:
        # Verificar limite maximo de descargas (5 descargas/dia)
        if i_descarga >= max_descargas:
            motivo_corte = 'maximo_descargas'
            break

        # Verificar restricción de tiempo
        if t_cursor / 3600 >= tiempo_maximo_h:
            motivo_corte = 'tiempo_maximo'
            break

        # Verificar restricción de masa
        if m_actual < masa_por_descarga_kg:
            motivo_corte = 'masa_insuficiente'
            break

        # Verificar restricción de temperatura (aplica a todas las descargas)
        if T_actual < temp_minima_aceptable:
            motivo_corte = 'temperatura_baja'
            break

        # — Descarga —
        t0 = 0.0
        t1 = tiempo_descarga_h * 3600
        # No exceder tiempo máximo
        t_restante = (tiempo_maximo_h * 3600) - t_cursor
        if t1 > t_restante:
            t1 = t_restante
        if t1 < 60:
            motivo_corte = 'tiempo_maximo'
            break

        t_eval_d = np.arange(t0, t1 + 1, dt_seg)
        sol_d = solve_ivp(
            lambda t, y: _ode_con_masa(t, y, True),
            [t0, t1], [T_actual, m_actual],
            t_eval=t_eval_d, method='RK45', max_step=60
        )
        T_ini_d = T_actual
        m_ini_d = m_actual
        for t, T, m in zip(sol_d.t, sol_d.y[0], sol_d.y[1]):
            U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
            Q = U * A * max(T_agua - T, 0)
            serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                          'T_glucosa': round(T, 3),
                          'm_ton': round(m / 1000, 3),
                          'U': round(U, 3),
                          'Q_kW': round(Q / 1000, 4),
                          'fase': f'descarga_{i_descarga+1}'})

        T_actual = sol_d.y[0][-1]
        m_actual = sol_d.y[1][-1]
        t_d_ini_h = round(t_cursor / 3600, 4)
        t_cursor += t1
        t_d_fin_h = round(t_cursor / 3600, 4)

        masa_desc = m_ini_d - m_actual
        estado = ('OK' if T_actual >= temp_minima_aceptable else
                  'Marginal' if T_actual >= temp_minima_aceptable - 5 else 'Fuera')
        descargas.append({'descarga': i_descarga + 1,
                          't_inicio_h': t_d_ini_h, 't_fin_h': t_d_fin_h,
                          'T_inicio': round(T_ini_d, 2),
                          'T_fin': round(T_actual, 2),
                          'm_inicio_ton': round(m_ini_d / 1000, 3),
                          'm_fin_ton': round(m_actual / 1000, 3),
                          'masa_descargada_ton': round(masa_desc / 1000, 3),
                          'U_prom': round(coeficiente_U(v_agua, T_agua, (T_ini_d + T_actual) / 2)[0], 2),
                          'estado': estado})
        fases.append({'tipo': 'descarga', 'descarga_num': i_descarga + 1,
                      't_inicio_h': t_d_ini_h, 't_fin_h': t_d_fin_h,
                      'T_inicio': round(T_ini_d, 2), 'T_fin': round(T_actual, 2)})

        i_descarga += 1

        # Si T cayó por debajo del mínimo, no hacemos más descargas
        if T_actual < temp_minima_aceptable:
            motivo_corte = 'temperatura_baja'
            break

        # — Calentamiento entre descargas —
        if tiempo_calentamiento_entre_h > 0 and t_cursor / 3600 < tiempo_maximo_h:
            t0 = 0.0
            t1 = tiempo_calentamiento_entre_h * 3600
            t_restante = (tiempo_maximo_h * 3600) - t_cursor
            if t1 > t_restante:
                t1 = t_restante
            if t1 > 60:
                t_eval_c = np.arange(t0, t1 + 1, dt_seg)
                sol_c = solve_ivp(
                    lambda t, y: _ode_con_masa(t, y, False),
                    [t0, t1], [T_actual, m_actual],
                    t_eval=t_eval_c, method='RK45', max_step=60
                )
                T_ini_c = T_actual
                t_c_ini_h = round(t_cursor / 3600, 4)
                for t, T, m in zip(sol_c.t, sol_c.y[0], sol_c.y[1]):
                    U, _, _, _ = coeficiente_U(v_agua, T_agua, T)
                    Q = U * A * max(T_agua - T, 0)
                    serie.append({'t_h': round((t_cursor + t) / 3600, 4),
                                  'T_glucosa': round(T, 3),
                                  'm_ton': round(m / 1000, 3),
                                  'U': round(U, 3),
                                  'Q_kW': round(Q / 1000, 4),
                                  'fase': f'mantenimiento_{i_descarga}'})
                T_actual = sol_c.y[0][-1]
                m_actual = sol_c.y[1][-1]
                t_cursor += t1
                fases.append({'tipo': 'mantenimiento',
                              't_inicio_h': t_c_ini_h,
                              't_fin_h': round(t_cursor / 3600, 4),
                              'T_inicio': round(T_ini_c, 2),
                              'T_fin': round(T_actual, 2)})

    # ── Métricas de resumen ───────────────────────────────────────────────────
    T_vals = [p['T_glucosa'] for p in serie]
    masa_total_desc = sum(d['masa_descargada_ton'] for d in descargas)
    descargas_ok = sum(1 for d in descargas if d['estado'] == 'OK')

    return {
        'serie_temporal': serie,
        'fases': fases,
        'descargas': descargas,
        'metricas': {
            'tiempo_calentamiento_inicial_h': round(t_cal_fin_h, 3),
            'tiempo_total_h': round(t_cursor / 3600, 3),
            'T_final': round(T_actual, 2),
            'masa_total_descargada_ton': round(masa_total_desc, 2),
            'descargas_ok': descargas_ok,
            'descargas_calculadas': i_descarga,
            'motivo_corte': motivo_corte,
            'T_min_ciclo': round(min(T_vals), 2),
            'T_promedio_ciclo': round(sum(T_vals) / len(T_vals), 2),
            'masa_restante_ton': round(m_actual / 1000, 2),
        }
    }

