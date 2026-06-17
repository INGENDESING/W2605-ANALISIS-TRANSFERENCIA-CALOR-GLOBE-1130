"""
Wrapper Flask para pérdidas térmicas y análisis de aislamiento — W2605
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from perdidas_termicas_real import (
    calcular_area_real_expuesta,
    calcular_perdidas,
    calcular_tiempo_perdida_3C,
    analisis_sensibilidad_espesor,
    T_AMBIENTE,
    ESPESOR_AISLAMIENTO,
    K_AISLAMIENTO,
)
from aislamiento import tabla_espesores


def resumen_perdidas_termicas():
    """
    Calcula pérdidas térmicas con y sin aislamiento usando el área real
    expuesta del tanque al 80 % de llenado.

    Retorna
    -------
    dict
        Resultados serializables para temperaturas de operación 57 °C y 60 °C.
    """
    areas = calcular_area_real_expuesta()

    resultados = []
    for T_g in [57.0, 60.0]:
        con_aisl = calcular_perdidas(T_g)
        sin_aisl = calcular_perdidas(T_g, espesor_aisl=0.0)
        tiempo_3c = calcular_tiempo_perdida_3C(T_g, con_aisl['Q_W'])

        resultados.append({
            'T_glucosa_C': T_g,
            'Q_con_aislamiento_W': round(con_aisl['Q_W'], 1),
            'Q_con_aislamiento_kW': round(con_aisl['Q_kW'], 3),
            'Q_con_aislamiento_MJ_h': round(con_aisl['Q_MJ_h'], 2),
            'Q_sin_aislamiento_W': round(sin_aisl['Q_W'], 1),
            'Q_sin_aislamiento_MJ_h': round(sin_aisl['Q_MJ_h'], 2),
            'reduccion_porc': round((1.0 - con_aisl['Q_W'] / sin_aisl['Q_W']) * 100, 1),
            'U_perdidas_W_m2_C': round(con_aisl['U_perdidas'], 3),
            'R_total_m2_C_W': round(con_aisl['R_total'], 4),
            'tiempo_3C_h': round(tiempo_3c['tiempo_h'], 1),
            'tiempo_3C_d': round(tiempo_3c['tiempo_d'], 1),
        })

    return {
        'parametros': {
            'T_ambiente_C': float(T_AMBIENTE),
            'espesor_aislamiento_mm': float(ESPESOR_AISLAMIENTO * 1000),
            'k_aislamiento_W_m_C': float(K_AISLAMIENTO),
            'nivel_llenado_porc': 80.0,
        },
        'areas_m2': {
            'A_fondo': round(areas['A_fondo'], 1),
            'A_cilindro_80porc': round(areas['A_cil_80'], 1),
            'A_total': round(areas['A_total'], 1),
        },
        'resultados': resultados,
    }


def tabla_espesores_aislamiento(T_agua=75.0):
    """
    Genera tabla comparativa de espesores de aislamiento.

    Parameters
    ----------
    T_agua : float
        Temperatura del agua de calentamiento [°C].

    Retorna
    -------
    list
        Filas con espesor, pérdida, temperatura superficial y eficiencia.
    """
    return [
        {
            'espesor_mm': round(fila['espesor_mm'], 1),
            'espesor_in': round(fila['espesor_in'], 2),
            'Q_perdida_W': round(fila['Q_perdida_W'], 1),
            'Q_perdida_kW': round(fila['Q_perdida_kW'], 3),
            'T_sup_ext_C': round(fila['T_sup_ext'], 1),
            'eficiencia_porc': round(fila['eficiencia'], 1),
            'seguro_contacto': bool(fila['seguro_contacto']),
        }
        for fila in tabla_espesores(T_agua)
    ]


def sensibilidad_espesor_aislamiento():
    """
    Análisis de sensibilidad del espesor de aislamiento a 60 °C.

    Retorna
    -------
    list
        Resultados para espesores de 0 a 101,6 mm.
    """
    return [
        {
            'espesor_mm': round(fila['espesor_mm'], 1),
            'U_W_m2_C': round(fila['U'], 3),
            'Q_MJ_h': round(fila['Q_MJ_h'], 2),
            'tiempo_3C_d': round(fila['tiempo_3C_d'], 1),
        }
        for fila in analisis_sensibilidad_espesor(60.0)
    ]
