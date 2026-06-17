"""
Wrapper Flask para la simulación del ciclo a 12 m³/h — Proyecto W2605
Caso: chaqueta de 14 m², agua a 75 °C, doble entrada, 5 descargas/día.
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from ciclo_descargas_14m2_75C_12m3h import (
    simular_ciclo,
    resumen_ciclo,
    A_TRANSFERENCIA,
    V_AGUA,
    T_AGUA,
    Q_VOL_DESCARGA,
    MASA_POR_DESCARGA,
    N_DESCARGAS,
    T_TOTAL,
    NIVEL_INICIAL,
    T_INICIAL,
    T_OBJETIVO,
    T_MIN_DESPACHO,
    T_DESCARGA,
    T_CICLO,
    MASA_INICIAL,
    VOLUMEN_DESCARGA,
)
from geometria_tanque import volumen_total


def simular_ciclo_12m3h():
    """
    Ejecuta la simulación del ciclo de 5 descargas diarias a 12 m³/h
    con el área de transferencia de 14 m².

    Retorna
    -------
    dict
        Datos serializables con series temporales, resumen por descarga
        y métricas globales del ciclo.
    """
    t, estados, fases = simular_ciclo()
    resumen = resumen_ciclo(t, estados)

    T = estados[:, 0]
    m = estados[:, 1]
    rho_inicial = m[0] / (volumen_total() * NIVEL_INICIAL)
    nivel = (m / (volumen_total() * rho_inicial)) * 100.0

    T_min = float(np.min(T))
    T_final = float(T[-1])

    return {
        'configuracion': {
            'area_m2': float(A_TRANSFERENCIA),
            'v_agua_m_s': float(V_AGUA),
            'T_agua_C': float(T_AGUA),
            'Q_vol_descarga_m3_h': float(Q_VOL_DESCARGA),
            'masa_por_descarga_kg': float(MASA_POR_DESCARGA),
            'n_descargas': int(N_DESCARGAS),
            'T_inicial_C': float(T_INICIAL),
            'T_objetivo_C': float(T_OBJETIVO),
            'T_min_despacho_C': float(T_MIN_DESPACHO),
            'nivel_inicial_porc': float(NIVEL_INICIAL * 100),
            'T_descarga_h': float(T_DESCARGA),
            'T_ciclo_h': float(T_CICLO),
            'T_calentamiento_disponible_h': float(T_CICLO - T_DESCARGA),
            'masa_inicial_kg': float(MASA_INICIAL),
            'volumen_descarga_m3': float(VOLUMEN_DESCARGA),
        },
        'series': {
            't_h': [float(x) for x in t],
            'T_g_C': [float(x) for x in T],
            'm_kg': [float(x) for x in m],
            'nivel_porc': [float(x) for x in nivel],
            'fases': [str(x) for x in fases],
        },
        'resumen_descargas': [
            {
                'descarga': int(r['descarga']),
                't_ini_h': float(r['t_ini_h']),
                't_fin_h': float(r['t_fin_h']),
                'T_ini_C': float(r['T_ini_C']),
                'T_fin_C': float(r['T_fin_C']),
                'delta_T_C': float(r['delta_T_C']),
                'cumple_min': bool(r['cumple_min']),
            }
            for r in resumen
        ],
        'metricas': {
            'T_min_C': round(T_min, 2),
            'T_final_C': round(T_final, 2),
            'factible': bool(T_min >= T_MIN_DESPACHO),
            'mensaje': (
                'El ciclo cumple el límite mínimo de despacho (57 °C).'
                if T_min >= T_MIN_DESPACHO
                else 'El ciclo NO cumple el límite mínimo de despacho (57 °C).'
            ),
        },
    }
