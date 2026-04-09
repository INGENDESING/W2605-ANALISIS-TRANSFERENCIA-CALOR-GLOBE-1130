"""
Módulo de balance de masa - Cálculos de volumen y nivel
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from propiedades_glucosa import rho_glucosa
from geometria_tanque import (
    volumen_total, volumen_a_nivel, nivel_a_porcentaje,
    volumen_cilindro, volumen_fondo_torisferico
)


def calcular_masa_glucosa(volumen_m3, temperatura_c):
    """
    Calcular masa de glucosa dado volumen y temperatura
    
    Parameters
    ----------
    volumen_m3 : float
        Volumen en m³
    temperatura_c : float
        Temperatura en °C
    
    Returns
    -------
    dict
        Masa en kg y toneladas
    """
    rho = rho_glucosa(temperatura_c)
    masa_kg = volumen_m3 * rho
    
    return {
        'masa_kg': round(masa_kg, 2),
        'masa_ton': round(masa_kg / 1000, 3),
        'densidad_kg_m3': round(rho, 2),
        'volumen_m3': round(volumen_m3, 3)
    }


def calcular_volumen_a_nivel(nivel_m):
    """
    Calcular volumen dado el nivel de líquido
    
    Parameters
    ----------
    nivel_m : float
        Nivel desde el fondo en metros
    
    Returns
    -------
    dict
        Información de volumen y geometría
    """
    volumen = volumen_a_nivel(nivel_m)
    volumen_total_tanque = volumen_total()
    porcentaje = (volumen / volumen_total_tanque) * 100
    
    return {
        'volumen_m3': round(volumen, 2),
        'porcentaje': round(porcentaje, 1),
        'volumen_total_m3': round(volumen_total_tanque, 2),
        'nivel_m': round(nivel_m, 3)
    }


def calcular_nivel_porcentaje(porcentaje):
    """
    Calcular nivel dado un porcentaje de llenado
    
    Parameters
    ----------
    porcentaje : float
        Porcentaje de llenado (0-100)
    
    Returns
    -------
    dict
        Información de nivel y volumen
    """
    nivel = nivel_a_porcentaje(porcentaje)
    vol_info = calcular_volumen_a_nivel(nivel)
    
    return {
        'nivel_m': round(nivel, 3),
        'porcentaje': round(porcentaje, 1),
        'volumen_m3': vol_info['volumen_m3']
    }


def calcular_capacidad_tanque():
    """
    Calcular capacidad total del tanque
    
    Returns
    -------
    dict
        Capacidades a diferentes niveles
    """
    V_total = volumen_total()
    V_cil = volumen_cilindro()
    V_fondo = volumen_fondo_torisferico()
    
    # Densidad a temperatura de referencia (40°C)
    rho_ref = rho_glucosa(40)
    
    capacidades = {
        'volumen_total_m3': round(V_total, 2),
        'volumen_cilindro_m3': round(V_cil, 2),
        'volumen_fondo_m3': round(V_fondo, 2),
        'masa_total_ton': round(V_total * rho_ref / 1000, 1),
        'masa_80pct_ton': round(V_total * 0.80 * rho_ref / 1000, 1),
        'masa_90pct_ton': round(V_total * 0.90 * rho_ref / 1000, 1),
        'niveles': {
            '80%': calcular_nivel_porcentaje(80),
            '90%': calcular_nivel_porcentaje(90),
            '100%': calcular_nivel_porcentaje(100)
        }
    }
    
    return capacidades
