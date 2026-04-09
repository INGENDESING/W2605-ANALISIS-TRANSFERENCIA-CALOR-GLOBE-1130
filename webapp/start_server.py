#!/usr/bin/env python
"""
Script para iniciar el servidor Flask de forma persistente
"""
import sys
from pathlib import Path

# Agregar directorio src al path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    # Ejecutar sin debug y sin reloader para evitar problemas
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
