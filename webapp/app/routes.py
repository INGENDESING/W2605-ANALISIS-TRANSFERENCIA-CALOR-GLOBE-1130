"""
Rutas principales de la aplicación
"""
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)


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
    return render_template('dashboard.html')


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


@main_bp.route('/health')
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'service': 'P2611 WebApp',
        'version': '1.0.0'
    })
