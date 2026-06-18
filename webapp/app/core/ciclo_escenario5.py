"""
Wrapper Flask para la simulación del Escenario 5 — Proyecto W2605
Caso: ciclo industrial de despacho, arranque desde 25 °C, agua a 75 °C,
      5 descargas de 24 ton en 2,0 h, control termostático a 60 °C.
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from escenario5_ciclo import (
    simular_ciclo_esc5,
    T_GLUCOSA_INICIAL,
    T_AGUA,
    V_AGUA,
    T_DESCARGA,
    MASA_POR_DESCARGA,
    T_DESCARGA_DURACION,
    N_DESCARGAS,
)
from propiedades_glucosa import rho_glucosa
from geometria_tanque import volumen_total


def _to_float_list(arr):
    return [float(x) for x in arr]


def simular_ciclo_escenario5():
    """
    Ejecuta la simulación del Escenario 5 y retorna un dict serializable
    con series temporales, resumen por fase y métricas globales.
    """
    res = simular_ciclo_esc5(dt_s=60.0)

    t_h = np.array(res['t_h'])
    T_g = np.array(res['T_g'])
    m_g = np.array(res['m_g'])

    # Nivel aproximado considerando expansión/contracción térmica y extracción
    nivel_pct = (m_g / rho_glucosa(T_g)) / volumen_total() * 100.0

    T_min = float(np.min(T_g))
    T_final = float(T_g[-1])
    t_total = float(t_h[-1])

    descargas = res['descargas']
    fases = res['fases']

    # Determinar factibilidad: todas las descargas deben partir desde >= T_DESCARGA
    descargas_ok = all(d['T_inicio'] >= T_DESCARGA - 0.05 for d in descargas)

    return {
        'configuracion': {
            'nombre': 'Escenario 5 — Ciclo industrial de despacho',
            'T_glucosa_inicial_C': float(T_GLUCOSA_INICIAL),
            'T_agua_C': float(T_AGUA),
            'v_agua_m_s': float(V_AGUA),
            'T_descarga_min_C': float(T_DESCARGA),
            'T_max_control_C': 60.0,
            'masa_por_descarga_kg': float(MASA_POR_DESCARGA),
            'n_descargas': int(N_DESCARGAS),
            'duracion_descarga_h': float(T_DESCARGA_DURACION),
            'nivel_inicial_porc': 80.0,
        },
        'series': {
            't_h': _to_float_list(t_h),
            'T_g_C': _to_float_list(T_g),
            'm_kg': _to_float_list(m_g),
            'nivel_porc': _to_float_list(nivel_pct),
        },
        'descargas': [
            {
                'descarga': int(d['descarga']),
                't_ini_h': float(d['t_inicio_h']),
                't_fin_h': float(d['t_fin_h']),
                'T_ini_C': float(d['T_inicio']),
                'T_fin_C': float(d['T_fin']),
                'm_ini_kg': float(d['m_inicio_kg']),
                'm_fin_kg': float(d['m_fin_kg']),
                'masa_descargada_kg': float(d['masa_descargada_kg']),
                'dt_recalentamiento_h': float(d['dt_recalentamiento_h']),
            }
            for d in descargas
        ],
        'fases': [
            {
                'tipo': str(f['tipo']),
                'descarga_num': int(f.get('descarga_num', 0)),
                't_inicio_h': float(f['t_inicio_h']),
                't_fin_h': float(f['t_fin_h']),
                'duracion_h': float(f['duracion_h']),
                'T_inicio_C': float(f['T_inicio']),
                'T_fin_C': float(f['T_fin']),
            }
            for f in fases
        ],
        'metricas': {
            'T_min_C': round(T_min, 2),
            'T_final_C': round(T_final, 2),
            't_total_h': round(t_total, 2),
            'masa_final_kg': round(float(m_g[-1]), 2),
            'masa_total_descargada_kg': round(
                float(sum(d['masa_descargada_kg'] for d in descargas)), 2
            ),
            'descargas_ok': int(sum(
                1 for d in descargas if d['T_inicio'] >= T_DESCARGA - 0.05
            )),
            'factible': bool(descargas_ok),
            'mensaje': (
                'El ciclo cumple el límite mínimo de descarga (57 °C).'
                if descargas_ok
                else 'El ciclo NO cumple el límite mínimo de descarga (57 °C).'
            ),
        },
    }
