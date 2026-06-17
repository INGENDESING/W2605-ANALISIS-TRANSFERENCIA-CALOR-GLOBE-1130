"""
Tests básicos para la API - Proyecto W2605
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import json
from app import create_app


class TestAPI(unittest.TestCase):
    """Tests para endpoints de la API"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test endpoint health check"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_calcular_transferencia_calor(self):
        """Test cálculo de transferencia de calor"""
        payload = {
            'flujo_agua_m3h': 30.9,
            'temp_agua_entrada': 65,
            'temp_glucosa_inicial': 20,
            'temp_glucosa_objetivo': 60,
            'volumen_glucosa_m3': 24,
            'area_contacto_m2': 13
        }
        response = self.client.post('/api/calcular/transferencia-calor',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('coeficiente_U', data['data'])
        self.assertIn('potencia_termica_kW', data['data'])
    
    def test_calcular_capacidad_tanque(self):
        """Test capacidad del tanque"""
        response = self.client.get('/api/calcular/capacidad-tanque')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('volumen_total_m3', data['data'])
    
    def test_tabla_propiedades(self):
        """Test generación de tabla de propiedades"""
        response = self.client.get('/api/calcular/tabla-propiedades?temp_min=20&temp_max=80&paso=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)


class TestSimulacion(unittest.TestCase):
    """Tests para simulación"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_simular_capacidad(self):
        """Test cálculo de capacidad"""
        payload = {
            'temp_inicial': 57,
            'temp_agua': 65,
            'num_descargas': 5,
            'masa_por_descarga_ton': 24,
            'tiempo_descarga_h': 1.5,
            'nivel_inicial_pct': 80
        }
        response = self.client.post('/api/simular/capacidad',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('flujo_maximo_ton_h', data['data'])


if __name__ == '__main__':
    unittest.main()
