"""
Módulo de propiedades termofísicas calculadas
Tablas y valores derivados
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from propiedades_glucosa import (
    rho_glucosa, mu_glucosa, Cp_glucosa, k_glucosa, Pr_glucosa,
    rho_agua, mu_agua, Cp_agua, k_agua, Pr_agua
)


def calcular_propiedades_completas(temperatura_c):
    """
    Calcular todas las propiedades termofísicas a una temperatura
    
    Parameters
    ----------
    temperatura_c : float
        Temperatura en °C
    
    Returns
    -------
    dict
        Propiedades de glucosa y agua
    """
    # Propiedades de glucosa
    rho_g = rho_glucosa(temperatura_c)
    mu_g = mu_glucosa(temperatura_c)
    Cp_g = Cp_glucosa(temperatura_c)
    k_g = k_glucosa(temperatura_c)
    Pr_g = Pr_glucosa(temperatura_c)
    
    # Propiedades de agua
    rho_w = rho_agua(temperatura_c)
    mu_w = mu_agua(temperatura_c)
    Cp_w = Cp_agua(temperatura_c)
    k_w = k_agua(temperatura_c)
    Pr_w = Pr_agua(temperatura_c)
    
    return {
        'temperatura_c': round(temperatura_c, 2),
        'glucosa': {
            'densidad_kg_m3': round(rho_g, 2),
            'viscosidad_Pa_s': round(mu_g, 6),
            'viscosidad_cP': round(mu_g * 1000, 3),
            'cp_J_kg_C': round(Cp_g, 2),
            'k_W_m_C': round(k_g, 5),
            'prandtl': round(Pr_g, 1)
        },
        'agua': {
            'densidad_kg_m3': round(rho_w, 2),
            'viscosidad_Pa_s': round(mu_w, 6),
            'viscosidad_cP': round(mu_w * 1000, 4),
            'cp_J_kg_C': round(Cp_w, 2),
            'k_W_m_C': round(k_w, 5),
            'prandtl': round(Pr_w, 2)
        }
    }


def generar_tabla_propiedades(temp_min=20, temp_max=80, paso=5):
    """
    Generar tabla de propiedades en rango de temperaturas
    
    Parameters
    ----------
    temp_min : float
        Temperatura mínima en °C
    temp_max : float
        Temperatura máxima en °C
    paso : float
        Paso de temperatura
    
    Returns
    -------
    list
        Lista de propiedades por temperatura
    """
    temperaturas = np.arange(temp_min, temp_max + paso, paso)
    tabla = []
    
    for T in temperaturas:
        props = calcular_propiedades_completas(T)
        tabla.append({
            'temperatura_c': round(T, 1),
            'rho_glucosa': props['glucosa']['densidad_kg_m3'],
            'mu_glucosa_Pa_s': props['glucosa']['viscosidad_Pa_s'],
            'mu_glucosa_cP': props['glucosa']['viscosidad_cP'],
            'cp_glucosa': props['glucosa']['cp_J_kg_C'],
            'k_glucosa': props['glucosa']['k_W_m_C'],
            'Pr_glucosa': props['glucosa']['prandtl'],
            'rho_agua': props['agua']['densidad_kg_m3'],
            'mu_agua_cP': props['agua']['viscosidad_cP'],
            'cp_agua': props['agua']['cp_J_kg_C'],
            'k_agua': props['agua']['k_W_m_C'],
            'Pr_agua': props['agua']['prandtl']
        })
    
    return tabla


def comparar_propiedades_escenarios():
    """
    Comparar propiedades a temperaturas típicas de operación
    
    Returns
    -------
    dict
        Comparación de escenarios
    """
    escenarios = {
        'frio': 20,
        'templado': 40,
        'operacion': 57,
        'caliente': 60
    }
    
    resultado = {}
    for nombre, temp in escenarios.items():
        resultado[nombre] = calcular_propiedades_completas(temp)
    
    return resultado
