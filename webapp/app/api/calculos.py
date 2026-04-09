"""
API Endpoints para cálculos de transferencia de calor y balance
"""
from flask import Blueprint, request, jsonify

from ..core.balance_energia import (
    calcular_transferencia_calor,
    simular_calentamiento_transitorio
)
from ..core.balance_masa import (
    calcular_masa_glucosa,
    calcular_volumen_a_nivel,
    calcular_nivel_porcentaje,
    calcular_capacidad_tanque
)
from ..core.props_calculadas import (
    calcular_propiedades_completas,
    generar_tabla_propiedades
)

api_calculos_bp = Blueprint('api_calculos', __name__)


@api_calculos_bp.route('/calcular/transferencia-calor', methods=['POST'])
def api_calcular_transferencia_calor():
    """
    Calcular transferencia de calor
    
    Request JSON:
    {
        "flujo_agua_m3h": 30.9,
        "temp_agua_entrada": 65,
        "temp_glucosa_inicial": 20,
        "temp_glucosa_objetivo": 60,
        "volumen_glucosa_m3": 24,
        "area_contacto_m2": 13.0
    }
    """
    data = request.get_json()
    
    try:
        # Parámetros requeridos
        flujo_agua = float(data.get('flujo_agua_m3h', 30.9))
        temp_agua = float(data.get('temp_agua_entrada', 65))
        temp_glucosa = float(data.get('temp_glucosa_inicial', 20))
        
        # Parámetros opcionales
        temp_objetivo = data.get('temp_glucosa_objetivo')
        if temp_objetivo is not None:
            temp_objetivo = float(temp_objetivo)
        
        volumen = float(data.get('volumen_glucosa_m3', 24))
        area = data.get('area_contacto_m2')
        if area is not None:
            area = float(area)
        
        # Validaciones
        if flujo_agua <= 0:
            return jsonify({'error': 'Flujo de agua debe ser positivo'}), 400
        if temp_agua <= temp_glucosa:
            return jsonify({'error': 'Temperatura del agua debe ser mayor que la glucosa'}), 400
        
        # Calcular
        resultado = calcular_transferencia_calor(
            flujo_agua, temp_agua, temp_glucosa,
            temp_objetivo, volumen, area
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/simular-calentamiento', methods=['POST'])
def api_simular_calentamiento():
    """
    Simular calentamiento transitorio completo
    
    Request JSON:
    {
        "temp_inicial": 20,
        "temp_agua": 65,
        "flujo_agua_m3h": 30.9,
        "volumen_glucosa_m3": 24,
        "tiempo_final_h": 24,
        "dt_min": 10
    }
    """
    data = request.get_json()
    
    try:
        temp_inicial = float(data.get('temp_inicial', 20))
        temp_agua = float(data.get('temp_agua', 65))
        flujo_agua = float(data.get('flujo_agua_m3h', 30.9))
        volumen = float(data.get('volumen_glucosa_m3', 24))
        t_final = float(data.get('tiempo_final_h', 24))
        dt = float(data.get('dt_min', 10))
        
        # Velocidad estimada
        v_agua = flujo_agua / 30.9 * 1.338
        
        resultado = simular_calentamiento_transitorio(
            temp_inicial, temp_agua, v_agua, volumen, t_final, dt
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/masa-glucosa', methods=['POST'])
def api_calcular_masa():
    """Calcular masa de glucosa"""
    data = request.get_json()
    
    try:
        volumen = float(data.get('volumen_m3', 24))
        temperatura = float(data.get('temperatura_c', 40))
        
        resultado = calcular_masa_glucosa(volumen, temperatura)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/nivel-a-volumen', methods=['POST'])
def api_nivel_a_volumen():
    """Convertir nivel a volumen"""
    data = request.get_json()
    
    try:
        nivel = float(data.get('nivel_m', 5))
        resultado = calcular_volumen_a_nivel(nivel)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/porcentaje-a-nivel', methods=['POST'])
def api_porcentaje_a_nivel():
    """Convertir porcentaje a nivel"""
    data = request.get_json()
    
    try:
        porcentaje = float(data.get('porcentaje', 80))
        resultado = calcular_nivel_porcentaje(porcentaje)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/capacidad-tanque', methods=['GET'])
def api_capacidad_tanque():
    """Obtener capacidad del tanque"""
    try:
        resultado = calcular_capacidad_tanque()
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/propiedades', methods=['POST'])
def api_calcular_propiedades():
    """Calcular propiedades termofísicas a una temperatura"""
    data = request.get_json()
    
    try:
        temperatura = float(data.get('temperatura_c', 40))
        resultado = calcular_propiedades_completas(temperatura)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_calculos_bp.route('/calcular/tabla-propiedades', methods=['GET'])
def api_tabla_propiedades():
    """Generar tabla de propiedades"""
    try:
        temp_min = float(request.args.get('temp_min', 20))
        temp_max = float(request.args.get('temp_max', 80))
        paso = float(request.args.get('paso', 5))
        
        resultado = generar_tabla_propiedades(temp_min, temp_max, paso)
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
