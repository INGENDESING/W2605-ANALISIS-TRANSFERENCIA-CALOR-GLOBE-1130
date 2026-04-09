"""
Punto de entrada de la aplicación Flask
"""
import sys
from pathlib import Path

# Agregar directorio src al path para importar módulos existentes
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
