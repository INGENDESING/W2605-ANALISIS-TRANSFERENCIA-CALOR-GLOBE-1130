"""
API Endpoints para simulación de ciclo de descargas
"""
from flask import Blueprint, request, jsonify

from ..core.area_fija import (
    calcular_flujo_maximo,
    calcular_capacidad_descarga,
    simular_ciclo_descargas
)

api_simulacion_bp = Blueprint('api_simulacion', __name__)


@api_simulacion_bp.route('/simular/flujo-maximo', methods=['POST'])
def api_flujo_maximo():
    """
    Calcular flujo máximo de descarga
    
    Request JSON:
    {
        "temp_entrada": 57,
        "temp_salida": 60,
        "temp_agua": 65,
        "v_agua": 2.5,
        "area_m2": 13
    }
    """
    data = request.get_json()
    
    try:
        temp_entrada = float(data.get('temp_entrada', 57))
        temp_salida = float(data.get('temp_salida', 60))
        temp_agua = float(data.get('temp_agua', 65))
        v_agua = float(data.get('v_agua', 2.5))
        area = data.get('area_m2')
        if area is not None:
            area = float(area)
        
        resultado = calcular_flujo_maximo(temp_entrada, temp_salida, temp_agua, v_agua, area)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_simulacion_bp.route('/simular/capacidad', methods=['POST'])
def api_capacidad():
    """
    Calcular capacidad operativa
    
    Request JSON:
    {
        "temp_inicial": 57,
        "temp_agua": 65,
        "num_descargas": 8,
        "masa_por_descarga_ton": 24,
        "tiempo_descarga_h": 1.5,
        "nivel_inicial_pct": 80
    }
    """
    data = request.get_json()
    
    try:
        temp_inicial = float(data.get('temp_inicial', 57))
        temp_agua = float(data.get('temp_agua', 65))
        num_descargas = int(data.get('num_descargas', 8))
        masa_por_descarga = float(data.get('masa_por_descarga_ton', 24)) * 1000
        tiempo_descarga = float(data.get('tiempo_descarga_h', 1.5))
        nivel_inicial = float(data.get('nivel_inicial_pct', 80))
        v_agua = float(data.get('v_agua', 2.5))
        
        resultado = calcular_capacidad_descarga(
            temp_inicial, temp_agua, num_descargas,
            masa_por_descarga, tiempo_descarga, nivel_inicial, v_agua
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_simulacion_bp.route('/simular/ciclo-descargas', methods=['POST'])
def api_ciclo_descargas():
    """
    Simular ciclo completo de descargas
    
    Request JSON:
    {
        "temp_inicial": 57,
        "temp_agua": 65,
        "num_descargas": 8,
        "masa_por_descarga_ton": 24,
        "tiempo_descarga_h": 1.5,
        "nivel_inicial_pct": 80,
        "periodo_ciclo_h": 3.0
    }
    """
    data = request.get_json()
    
    try:
        temp_inicial = float(data.get('temp_inicial', 57))
        temp_agua = float(data.get('temp_agua', 65))
        num_descargas = int(data.get('num_descargas', 8))
        masa_por_descarga = float(data.get('masa_por_descarga_ton', 24)) * 1000
        tiempo_descarga = float(data.get('tiempo_descarga_h', 1.5))
        nivel_inicial = float(data.get('nivel_inicial_pct', 80))
        v_agua = float(data.get('v_agua', 2.5))
        periodo = float(data.get('periodo_ciclo_h', 3.0))
        
        resultado = simular_ciclo_descargas(
            temp_inicial, temp_agua, num_descargas,
            masa_por_descarga, tiempo_descarga, nivel_inicial, v_agua, periodo
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_simulacion_bp.route('/simular/comparar-escenarios', methods=['POST'])
def api_comparar_escenarios():
    """
    Comparar Escenario 2 (65°C) vs Escenario 3 (75°C)
    
    Request JSON:
    {
        "temp_inicial": 57,
        "num_descargas": 8
    }
    """
    data = request.get_json()
    
    try:
        temp_inicial = float(data.get('temp_inicial', 57))
        num_descargas = int(data.get('num_descargas', 8))
        
        # Simular escenario 2 (65°C)
        resultado_65 = simular_ciclo_descargas(
            temp_inicial, 65.0, num_descargas
        )
        
        # Simular escenario 3 (75°C)
        resultado_75 = simular_ciclo_descargas(
            temp_inicial, 75.0, num_descargas
        )
        
        return jsonify({
            'success': True,
            'data': {
                'escenario_2_65C': {
                    'temp_final': resultado_65['temp_final'],
                    'masa_final_ton': resultado_65['masa_final_ton'],
                    'temp_min': resultado_65['temp_min'],
                    'temp_max': resultado_65['temp_max'],
                    'U_promedio': resultado_65['U_promedio'],
                    'masa_total_descargada': resultado_65['masa_total_descargada_ton']
                },
                'escenario_3_75C': {
                    'temp_final': resultado_75['temp_final'],
                    'masa_final_ton': resultado_75['masa_final_ton'],
                    'temp_min': resultado_75['temp_min'],
                    'temp_max': resultado_75['temp_max'],
                    'U_promedio': resultado_75['U_promedio'],
                    'masa_total_descargada': resultado_75['masa_total_descargada_ton']
                },
                'comparacion': {
                    'mejora_temp_final': round(resultado_75['temp_final'] - resultado_65['temp_final'], 2),
                    'mejora_U_promedio': round(resultado_75['U_promedio'] - resultado_65['U_promedio'], 2)
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
