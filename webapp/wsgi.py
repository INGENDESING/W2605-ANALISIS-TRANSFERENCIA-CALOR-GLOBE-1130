"""
WSGI entry point for production deployment
Usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from app import create_app

# Create app instance for production
app = create_app('production')

if __name__ == '__main__':
    app.run()
