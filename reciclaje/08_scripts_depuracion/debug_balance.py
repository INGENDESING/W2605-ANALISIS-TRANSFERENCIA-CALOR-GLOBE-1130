import sys
sys.path.insert(0, 'webapp')
sys.path.insert(0, 'src')

print('Importando...')
from app.core.balance_energia import simular_ciclo_automatico
from geometria_tanque import volumen_total

V = volumen_total() * 0.80
print('Volumen inicial:', V)

print('Ejecutando simulacion...')
r = simular_ciclo_automatico(
    T_inicial=57,
    T_objetivo_inicio_descarga=57,
    T_agua=75,
    v_agua=2.5,
    area=13.0,
    volumen_inicial_m3=V,
    masa_por_descarga_kg=24000,
    tiempo_descarga_h=2.0,
    periodo_ciclo_h=4.8,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)
print('OK')
print(r['metricas'])
