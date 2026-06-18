"""Prueba rápida de endpoints nuevos de la webapp W2605."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'webapp'))

from app import create_app

app = create_app('default')
client = app.test_client()

endpoints = [
    '/api/proyecto/ciclo-12m3h',
    '/api/proyecto/ciclo-parametrico',
    '/api/proyecto/arranque-niveles',
    '/api/proyecto/calentamiento-24ton',
]

for ep in endpoints:
    print(f"\nGET {ep}")
    r = client.get(ep)
    print(f"  status: {r.status_code}")
    data = r.get_json()
    print(f"  success: {data.get('success')}")
    if not data.get('success'):
        print(f"  error: {data.get('error')}")
    else:
        print(f"  keys: {list(data.get('data', {}).keys())}")
