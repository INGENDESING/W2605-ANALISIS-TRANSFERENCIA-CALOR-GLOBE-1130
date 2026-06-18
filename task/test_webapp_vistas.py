"""Prueba rápida de vistas nuevas de la webapp W2605."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'webapp'))

from app import create_app

app = create_app('default')
client = app.test_client()

rutas = [
    '/ciclo-parametrico',
    '/arranque-niveles',
]

for ruta in rutas:
    print(f"\nGET {ruta}")
    r = client.get(ruta)
    print(f"  status: {r.status_code}")
    print(f"  content length: {len(r.data)}")
    if r.status_code != 200:
        print(f"  response: {r.data[:500]}")
