"""
Wrapper Flask para casos de estudio adicionales — W2605
Incluye calentamiento de 24 ton y análisis de capacidad operativa diaria.
"""
import sys
import io
import contextlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from calentamiento_24ton_40_60 import (
    simular_calentamiento,
    tiempo_para_alcanzar,
    MASA_KG,
    T_INICIAL,
    T_OBJETIVO,
    AREA_TRANSFERENCIA as AREA_24TON,
    V_AGUA,
)
from escenario4_capacidad import calcular_capacidad


def _to_float(value, decimals=None):
    """Convierte un escalar a float Python nativo."""
    if decimals is None:
        return float(value)
    return round(float(value), decimals)


def calentamiento_24ton():
    """
    Simula el calentamiento de 24 ton de glucosa desde 40 °C hasta 60 °C
    con agua a 65 °C y 75 °C, usando el área de 14 m².

    Retorna
    -------
    dict
        Series temporales y tiempos para alcanzar 60 °C.
    """
    resultados = {}
    for T_agua in [65.0, 75.0]:
        res = simular_calentamiento(
            T_agua_in=T_agua,
            masa_kg=MASA_KG,
            T_inicial=T_INICIAL,
            T_objetivo=T_OBJETIVO,
            area_m2=AREA_24TON,
            v_agua=V_AGUA,
        )
        t_60 = tiempo_para_alcanzar(res['t_h'], res['T_g'], T_OBJETIVO)
        resultados[f'T{int(T_agua)}'] = {
            'T_agua_C': float(T_agua),
            't_h': [_to_float(x) for x in res['t_h']],
            'T_g_C': [_to_float(x) for x in res['T_g']],
            'U_W_m2_C': [_to_float(x) for x in res['U']],
            'Q_W': [_to_float(x) for x in res['Q_W']],
            'Q_MJ_h': [_to_float(x) for x in res['Q_MJ']],
            'tiempo_para_60_C_h': _to_float(t_60, 2) if t_60 else None,
        }

    return {
        'parametros': {
            'masa_kg': float(MASA_KG),
            'T_inicial_C': float(T_INICIAL),
            'T_objetivo_C': float(T_OBJETIVO),
            'area_m2': float(AREA_24TON),
            'v_agua_m_s': float(V_AGUA),
        },
        'escenarios': resultados,
    }


def capacidad_operativa_diaria():
    """
    Calcula capacidad operativa para dos temperaturas de entrada:
    54 °C → 57 °C (conservador) y 55 °C → 57 °C (mejorado).

    Retorna
    -------
    dict
        Resultados de flujo, tiempo, descargas/día y capacidad diaria.
    """
    # Suprimir salida por consola de calcular_capacidad
    with contextlib.redirect_stdout(io.StringIO()):
        caso_54 = calcular_capacidad(54.0, 57.0, 'CASO A - CONSERVADOR')
        caso_55 = calcular_capacidad(55.0, 57.0, 'CASO B - MEJORADO')

    def _formatear(caso):
        return {
            'T_in_C': _to_float(caso['T_in']),
            'T_out_C': _to_float(caso['T_out']),
            'U_W_m2_C': _to_float(caso['U'], 2),
            'LMTD_C': _to_float(caso['LMTD'], 2),
            'Q_W': _to_float(caso['Q'], 2),
            'flujo_max_ton_h': _to_float(caso['flujo'], 2),
            'tiempo_descarga_h': _to_float(caso['tiempo_descarga'], 2),
            'descargas_dia': int(caso['descargas_dia']),
            'capacidad_dia_ton': int(caso['capacidad_dia']),
        }

    return {
        'parametros': {
            'T_agua_C': 75.0,
            'area_m2': 13.0,
            'masa_descarga_kg': 24000.0,
            'requerimiento_descargas_dia': 5,
            'requerimiento_capacidad_dia_ton': 120,
        },
        'casos': {
            'conservador_T54_a_T57': _formatear(caso_54),
            'mejorado_T55_a_T57': _formatear(caso_55),
        },
    }
