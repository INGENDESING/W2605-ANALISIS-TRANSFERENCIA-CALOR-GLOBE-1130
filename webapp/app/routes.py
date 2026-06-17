"""
Rutas principales de la aplicación
"""
from pathlib import Path
from flask import Blueprint, render_template, jsonify, send_from_directory

from .core.ciclo_12m3h import simular_ciclo_12m3h
from .core.perdidas_aislamiento import (
    resumen_perdidas_termicas,
    tabla_espesores_aislamiento,
    sensibilidad_espesor_aislamiento,
)
from .core.escenarios_extras import capacidad_operativa_diaria

main_bp = Blueprint('main', __name__)

# Directorio de figuras generadas por los scripts de análisis
FIGURES_DIR = (Path(__file__).resolve().parent.parent.parent
               / 'results' / 'figures')


@main_bp.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')


@main_bp.route('/calculadora')
def calculadora():
    """Módulo calculadora de transferencia de calor"""
    return render_template('calculadora.html')


@main_bp.route('/simulador')
def simulador():
    """Módulo simulador de ciclo de descargas"""
    return render_template('simulador.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard de KPIs"""
    ciclo = simular_ciclo_12m3h()
    perdidas = resumen_perdidas_termicas()
    capacidad = capacidad_operativa_diaria()
    return render_template(
        'dashboard.html',
        ciclo=ciclo,
        perdidas=perdidas,
        capacidad=capacidad,
    )


@main_bp.route('/about')
def about():
    """Información del proyecto"""
    return render_template('about.html')


@main_bp.route('/sensibilidad')
def sensibilidad():
    """Módulo de análisis de sensibilidad"""
    return render_template('sensibilidad.html')


@main_bp.route('/propiedades')
def propiedades():
    """Propiedades termofísicas de la glucosa"""
    return render_template('propiedades.html')


@main_bp.route('/factibilidad')
def factibilidad():
    """Factibilidad térmica de cinco descargas diarias a 12 m³/h"""
    ciclo = simular_ciclo_12m3h()
    perdidas = resumen_perdidas_termicas()
    capacidad = capacidad_operativa_diaria()
    return render_template(
        'factibilidad.html',
        ciclo=ciclo,
        perdidas=perdidas,
        capacidad=capacidad
    )


@main_bp.route('/perdidas-aislamiento')
def perdidas_aislamiento():
    """Pérdidas térmicas y análisis de aislamiento"""
    return render_template(
        'perdidas_aislamiento.html',
        perdidas=resumen_perdidas_termicas(),
        espesores=tabla_espesores_aislamiento(),
        sensibilidad=sensibilidad_espesor_aislamiento(),
    )


@main_bp.route('/escenarios')
def escenarios():
    """Resumen de escenarios del proyecto"""
    return render_template('escenarios.html')


@main_bp.route('/figures/<path:filename>')
def serve_figure(filename):
    """Servir figuras generadas en results/figures/"""
    return send_from_directory(str(FIGURES_DIR), filename)


@main_bp.route('/health')
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'service': 'W2605 WebApp',
        'version': '1.0.0'
    })
