"""
Configuración de la aplicación Flask - Proyecto P2611
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()
SRC_DIR = BASE_DIR.parent / 'src'


class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'p2611-dev-secret-key-cambiar-en-produccion'
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Cálculos
    DEFAULT_AREA_CONTACTO = 13.0  # m²
    DEFAULT_VELOCIDAD_AGUA = 2.5  # m/s
    DEFAULT_TEMP_AGUA = 65.0  # °C
    
    # Exportación
    EXPORT_MAX_ROWS = 10000
    PDF_PAGE_SIZE = 'A4'


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    """Configuración de testing"""
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
