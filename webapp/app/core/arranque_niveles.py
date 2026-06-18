"""
Wrapper Flask para el análisis de arranque 40 °C → 60 °C — Proyecto W2605
Cubre 24 ton (sin pérdidas), 50 % y 80 % del tanque (con pérdidas).
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from calentamiento_24ton_40_60 import (
    simular_calentamiento,
    ejecutar_caso,
    tiempo_para_alcanzar,
    masa_desde_nivel,
    AREA_TRANSFERENCIA,
    V_AGUA,
    T_INICIAL,
    T_OBJETIVO,
    T_FINAL_H,
    T_AGUA_OPCIONES,
)


def _serializar_resultado(res):
    """Convierte el dict de simular_calentamiento en un dict JSON-serializable."""
    t_60 = tiempo_para_alcanzar(res['t_h'], res['T_g'], T_OBJETIVO)
    return {
        'T_agua_C': float(res['T_agua']),
        'masa_kg': float(res['masa_kg']),
        'V0_m3': float(res['V0_m3']),
        'con_perdidas': bool(res['con_perdidas']),
        'tiempo_a_60_C_h': float(t_60) if t_60 is not None else None,
        'T_final_C': float(res['T_g'][-1]),
        'Q_max_kW': float(np.max(res['Q_W']) / 1000.0),
        'U_inicial_W_m2C': float(res['U'][0]),
        'U_final_W_m2C': float(res['U'][-1]),
        'energia_chaqueta_MJ': float(res['Q_MJ'][-1]),
        'energia_perdidas_MJ': float(res['Q_perd_MJ'][-1]),
        'energia_neta_MJ': float(res['Q_neto_MJ'][-1]),
        'series': {
            't_h': [float(x) for x in res['t_h']],
            'T_g_C': [float(x) for x in res['T_g']],
            'U_W_m2C': [float(x) for x in res['U']],
            'Q_W': [float(x) for x in res['Q_W']],
            'Q_acum_MJ': [float(x) for x in res['Q_MJ']],
            'Q_perd_W': [float(x) for x in res['Q_perd_W']],
            'Q_perd_acum_MJ': [float(x) for x in res['Q_perd_MJ']],
            'Q_neto_acum_MJ': [float(x) for x in res['Q_neto_MJ']],
            'rho_kg_m3': [float(x) for x in res['rho']],
            'Cp_J_kgC': [float(x) for x in res['Cp']],
            'mu_Pa_s': [float(x) for x in res['mu']],
            'k_W_mC': [float(x) for x in res['k']],
            'Pr': [float(x) for x in res['Pr']],
        },
    }


def calentamiento_24ton():
    """Calentamiento de 24 ton sin pérdidas (caso ideal de referencia)."""
    resultados = ejecutar_caso(
        nombre='24ton',
        masa_kg=24_000.0,
        con_perdidas=False,
        t_final_h=T_FINAL_H,
    )
    return {
        'configuracion': {
            'area_m2': float(AREA_TRANSFERENCIA),
            'v_agua_m_s': float(V_AGUA),
            'T_inicial_C': float(T_INICIAL),
            'T_objetivo_C': float(T_OBJETIVO),
            'T_final_h': float(T_FINAL_H),
        },
        'escenarios': {
            etiqueta: _serializar_resultado(res)
            for etiqueta, res in resultados.items()
        },
    }


def calentamiento_arranque_niveles():
    """
    Calentamiento de 50 % y 80 % del tanque con pérdidas térmicas reales.

    Retorna
    -------
    dict
        Resultados serializables para cada nivel y temperatura de agua.
    """
    casos = {
        '50pct': masa_desde_nivel(50.0, T_INICIAL),
        '80pct': masa_desde_nivel(80.0, T_INICIAL),
    }

    salida = {
        'configuracion': {
            'area_m2': float(AREA_TRANSFERENCIA),
            'v_agua_m_s': float(V_AGUA),
            'T_inicial_C': float(T_INICIAL),
            'T_objetivo_C': float(T_OBJETIVO),
            'T_final_h': float(T_FINAL_H),
            'T_agua_opciones_C': [float(x) for x in T_AGUA_OPCIONES],
        },
        'escenarios': {},
    }

    for nombre, masa_kg in casos.items():
        resultados = ejecutar_caso(
            nombre=nombre,
            masa_kg=masa_kg,
            con_perdidas=True,
            t_final_h=T_FINAL_H,
        )
        salida['escenarios'][nombre] = {
            'masa_kg': float(masa_kg),
            'resultados': {
                etiqueta: _serializar_resultado(res)
                for etiqueta, res in resultados.items()
            },
        }

    return salida
