"""
Test: Parametros exactos del pantallazo del usuario
T_inicial=50, T_agua=67 (segun pantallazo)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'webapp'))

from app.core.balance_energia import simular_ciclo_automatico
from geometria_tanque import volumen_total

vol_ini = volumen_total() * 0.80

print("=" * 60)
print("TEST: Parametros del pantallazo")
print("T_inicial=50, T_agua=67, T_objetivo=57")
print("=" * 60)

# Con los parametros CORRECTOS (sin saltar calentamiento)
r = simular_ciclo_automatico(
    T_inicial=50,
    T_objetivo_inicio_descarga=57,
    T_agua=67,
    v_agua=2.5,
    area=13.0,
    volumen_inicial_m3=vol_ini,
    masa_por_descarga_kg=24000,
    tiempo_descarga_h=1.5,
    periodo_ciclo_h=3.0,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)

m = r['metricas']
print(f"Tiempo calentamiento inicial: {m['tiempo_calentamiento_inicial_h']:.2f} h")
print(f"Descargas calculadas:         {m['descargas_calculadas']}")
print(f"Descargas OK:                 {m['descargas_ok']}")
print(f"T final:                      {m['T_final']:.2f} C")
print(f"Motivo corte:                 {m['motivo_corte']}")
print(f"T min ciclo:                  {m['T_min_ciclo']:.2f} C")

print("\n--- Detalle de descargas ---")
for d in r['descargas']:
    print(f"  Descarga {d['descarga']}: "
          f"T={d['T_inicio']:.1f}->{d['T_fin']:.1f}C  "
          f"Estado={d['estado']}")

# Ahora con checkbox saltar calentamiento (bug anterior: enviaba T_inicial=57)
print("\n" + "=" * 60)
print("COMPARACION: Con bug antiguo (T_inicial=57, saltando calentamiento)")
print("=" * 60)

r2 = simular_ciclo_automatico(
    T_inicial=57,
    T_objetivo_inicio_descarga=57,
    T_agua=67,
    v_agua=2.5,
    area=13.0,
    volumen_inicial_m3=vol_ini,
    masa_por_descarga_kg=24000,
    tiempo_descarga_h=1.5,
    periodo_ciclo_h=3.0,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)

m2 = r2['metricas']
print(f"Tiempo calentamiento inicial: {m2['tiempo_calentamiento_inicial_h']:.2f} h")
print(f"Descargas calculadas:         {m2['descargas_calculadas']}")
print(f"Descargas OK:                 {m2['descargas_ok']}")
print(f"T final:                      {m2['T_final']:.2f} C")
print(f"Motivo corte:                 {m2['motivo_corte']}")
