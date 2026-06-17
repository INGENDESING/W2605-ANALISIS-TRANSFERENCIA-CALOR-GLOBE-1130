"""
API Endpoints para resultados del proyecto W2605
Expone los análisis desarrollados en el informe técnico W2605PRINF001.
"""
from flask import Blueprint, jsonify

from ..core.ciclo_12m3h import simular_ciclo_12m3h
from ..core.perdidas_aislamiento import (
    resumen_perdidas_termicas,
    tabla_espesores_aislamiento,
    sensibilidad_espesor_aislamiento,
)
from ..core.escenarios_extras import (
    calentamiento_24ton,
    capacidad_operativa_diaria,
)

api_proyecto_bp = Blueprint('api_proyecto', __name__)


@api_proyecto_bp.route('/proyecto/ciclo-12m3h', methods=['GET'])
def api_ciclo_12m3h():
    """
    Resultados del ciclo de 5 descargas diarias a 12 m³/h
    con chaqueta de 14 m² y agua a 75 °C.
    """
    try:
        resultado = simular_ciclo_12m3h()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_proyecto_bp.route('/proyecto/perdidas-termicas', methods=['GET'])
def api_perdidas_termicas():
    """
    Pérdidas térmicas con área real expuesta, con y sin aislamiento.
    """
    try:
        resultado = resumen_perdidas_termicas()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_proyecto_bp.route('/proyecto/aislamiento/espesores', methods=['GET'])
def api_aislamiento_espesores():
    """
    Tabla comparativa de espesores de aislamiento de lana mineral.
    """
    try:
        resultado = tabla_espesores_aislamiento()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_proyecto_bp.route('/proyecto/aislamiento/sensibilidad', methods=['GET'])
def api_aislamiento_sensibilidad():
    """
    Sensibilidad del espesor de aislamiento a 60 °C.
    """
    try:
        resultado = sensibilidad_espesor_aislamiento()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_proyecto_bp.route('/proyecto/calentamiento-24ton', methods=['GET'])
def api_calentamiento_24ton():
    """
    Calentamiento de 24 ton de glucosa desde 40 °C hasta 60 °C.
    """
    try:
        resultado = calentamiento_24ton()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_proyecto_bp.route('/proyecto/capacidad-operativa', methods=['GET'])
def api_capacidad_operativa():
    """
    Capacidad operativa diaria con área de 13 m² y agua a 75 °C.
    """
    try:
        resultado = capacidad_operativa_diaria()
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
