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
    parametros_iniciales,
    A_TRANSFERENCIA,
    V_AGUA,
    Q_VOL_DESCARGA,
    MASA_POR_DESCARGA,
    N_DESCARGAS,
    T_TOTAL,
    T_OBJETIVO,
    T_MIN_DESPACHO,
    T_DESCARGA,
    T_CICLO,
    VOLUMEN_DESCARGA,
)
from geometria_tanque import volumen_total


def _serializar_ciclo(t, estados, fases, T_agua, nivel_inicial, T_inicial):
    """Convierte el resultado de simular_ciclo en un dict serializable."""
    resumen = resumen_ciclo(t, estados, t_ciclo=T_TOTAL / N_DESCARGAS)

    T = estados[:, 0]
    m = estados[:, 1]
    _, MASA_INICIAL = parametros_iniciales(nivel_inicial, T_inicial)
    nivel = (m / MASA_INICIAL) * nivel_inicial * 100.0

    T_min = float(np.min(T))
    T_final = float(T[-1])

    return {
        'configuracion': {
            'area_m2': float(A_TRANSFERENCIA),
            'v_agua_m_s': float(V_AGUA),
            'T_agua_C': float(T_agua),
            'Q_vol_descarga_m3_h': float(Q_VOL_DESCARGA),
            'masa_por_descarga_kg': float(MASA_POR_DESCARGA),
            'n_descargas': int(N_DESCARGAS),
            'T_inicial_C': float(T_inicial),
            'T_objetivo_C': float(T_OBJETIVO),
            'T_min_despacho_C': float(T_MIN_DESPACHO),
            'nivel_inicial_porc': float(nivel_inicial * 100),
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
    T_agua = 75.0
    nivel_inicial = 0.80
    T_inicial = 60.0
    t, estados, fases, _ = simular_ciclo(T_agua, nivel_inicial, T_inicial)
    return _serializar_ciclo(t, estados, fases, T_agua, nivel_inicial, T_inicial)


def simular_ciclo_parametrico():
    """
    Ejecuta los cuatro escenarios paramétricos del ciclo oficial.

    Retorna
    -------
    dict
        Resultados por escenario: 80 % / 50 % con agua a 75 °C y 65 °C.
    """
    escenarios = {
        '80pct_75C': {'T_agua': 75.0, 'nivel_inicial': 0.80, 'T_inicial': 60.0},
        '80pct_65C': {'T_agua': 65.0, 'nivel_inicial': 0.80, 'T_inicial': 60.0},
        '50pct_75C': {'T_agua': 75.0, 'nivel_inicial': 0.50, 'T_inicial': 60.0},
        '50pct_65C': {'T_agua': 65.0, 'nivel_inicial': 0.50, 'T_inicial': 60.0},
    }

    resultados = {}
    for nombre, params in escenarios.items():
        t, estados, fases, _ = simular_ciclo(
            params['T_agua'], params['nivel_inicial'], params['T_inicial']
        )
        resultados[nombre] = _serializar_ciclo(
            t, estados, fases, params['T_agua'],
            params['nivel_inicial'], params['T_inicial']
        )

    return {
        'escenarios': resultados,
        'nota': 'Ciclo oficial de 5 descargas/día a 12 ton/h con área de 14 m².',
    }
