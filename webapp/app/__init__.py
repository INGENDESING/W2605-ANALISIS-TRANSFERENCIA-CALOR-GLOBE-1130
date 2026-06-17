"""
Inicialización de la aplicación Flask - Proyecto W2605
"""
from flask import Flask
from flask_cors import CORS
from config import config


def create_app(config_name='default'):
    """Factory de aplicación Flask"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Habilitar CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    
    # Registrar blueprints
    from .routes import main_bp
    from .api.calculos import api_calculos_bp
    from .api.simulacion import api_simulacion_bp
    from .api.exportar import api_exportar_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_calculos_bp, url_prefix='/api')
    app.register_blueprint(api_simulacion_bp, url_prefix='/api')
    app.register_blueprint(api_exportar_bp, url_prefix='/api')
    
    # Filtros Jinja personalizados
    @app.template_filter('format_number')
    def format_number(value, decimals=2):
        """Formatear número con decimales"""
        if value is None:
            return '-'
        try:
            return f"{float(value):,.{decimals}f}"
        except (ValueError, TypeError):
            return str(value)
    
    @app.template_filter('format_scientific')
    def format_scientific(value, decimals=2):
        """Formatear número en notación científica"""
        if value is None:
            return '-'
        try:
            return f"{float(value):.{decimals}e}"
        except (ValueError, TypeError):
            return str(value)
    
    return app
