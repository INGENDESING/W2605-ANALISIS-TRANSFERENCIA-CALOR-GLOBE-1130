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


class TestProyecto(unittest.TestCase):
    """Tests para endpoints de resultados del proyecto"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_ciclo_12m3h(self):
        """Test endpoint del ciclo a 12 m³/h"""
        response = self.client.get('/api/proyecto/ciclo-12m3h')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['metricas']['factible'])
        self.assertGreaterEqual(data['data']['metricas']['T_min_C'], 57.0)
        self.assertEqual(len(data['data']['resumen_descargas']), 5)

    def test_perdidas_termicas(self):
        """Test endpoint de pérdidas térmicas"""
        response = self.client.get('/api/proyecto/perdidas-termicas')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('areas_m2', data['data'])
        self.assertAlmostEqual(data['data']['areas_m2']['A_total'], 149.7, places=0)

    def test_aislamiento_espesores(self):
        """Test endpoint de tabla de espesores"""
        response = self.client.get('/api/proyecto/aislamiento/espesores')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)

    def test_calentamiento_24ton(self):
        """Test endpoint de calentamiento de 24 ton"""
        response = self.client.get('/api/proyecto/calentamiento-24ton')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('T75', data['data']['escenarios'])

    def test_capacidad_operativa(self):
        """Test endpoint de capacidad operativa diaria"""
        response = self.client.get('/api/proyecto/capacidad-operativa')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('mejorado_T55_a_T57', data['data']['casos'])


class TestVistas(unittest.TestCase):
    """Tests de renderizado de vistas HTML"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_vista_factibilidad(self):
        """Test renderizado de /factibilidad"""
        response = self.client.get('/factibilidad')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Factibilidad', response.data)

    def test_vista_perdidas_aislamiento(self):
        """Test renderizado de /perdidas-aislamiento"""
        response = self.client.get('/perdidas-aislamiento')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pérdidas'.encode('utf-8'), response.data)

    def test_vista_escenarios(self):
        """Test renderizado de /escenarios"""
        response = self.client.get('/escenarios')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Escenarios', response.data)

    def test_serve_figure(self):
        """Test servicio de figuras estáticas"""
        response = self.client.get('/figures/ciclo_12m3h_T_vs_t.png')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')


if __name__ == '__main__':
    unittest.main()
