import sys
sys.path.insert(0, 'webapp')
sys.path.insert(0, 'src')
from app.core.balance_energia import simular_ciclo_automatico
from geometria_tanque import volumen_total

V = volumen_total() * 0.80
# Caso pre-calentado (como el src/ciclo_descargas.py)
r = simular_ciclo_automatico(57, 57, 65, 2.5, 13.0, V, 24000, 1.5, 3.0)
m = r['metricas']
print(f"Descargas calculadas: {m['descargas_calculadas']}")
print(f"Motivo corte: {m['motivo_corte']}")
print(f"Masa total desc: {m['masa_total_descargada_ton']} ton")
print(f"T final: {m['T_final']} C")
print(f"Masa restante: {m['masa_restante_ton']} ton")
print(f"T min ciclo: {m['T_min_ciclo']} C")
print(f"Descargas OK: {m['descargas_ok']}")

print("\n--- Caso con calentamiento desde 20C (T_max_h=60h) ---")
r2 = simular_ciclo_automatico(20, 57, 65, 2.5, 13.0, V, 24000, 1.5, 3.0, tiempo_maximo_h=60)
m2 = r2['metricas']
print(f"Descargas calculadas: {m2['descargas_calculadas']}")
print(f"Tiempo calentamiento: {m2['tiempo_calentamiento_inicial_h']} h")
print(f"Motivo corte: {m2['motivo_corte']}")
print(f"Masa total desc: {m2['masa_total_descargada_ton']} ton")
print(f"T final: {m2['T_final']} C")
print(f"Descargas OK: {m2['descargas_ok']}")
