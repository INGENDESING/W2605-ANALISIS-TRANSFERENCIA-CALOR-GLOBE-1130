"""
Test de simulacion con parametros oficiales del ciclo W2605.
Caso de referencia: T_inicial=50 C, T_agua=67 C (pantallazo historico).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'webapp'))

from app.core.balance_energia import simular_ciclo_automatico
from geometria_tanque import volumen_total, A_CONTACTO

vol_ini = volumen_total() * 0.80
MASA_DESCARGA = 24000.0
TIEMPO_DESCARGA = 2.0
PERIODO_CICLO = 4.8

print("=" * 60)
print("TEST: Parametros del pantallazo actualizados al ciclo oficial")
print("T_inicial=50, T_agua=67, T_objetivo=57")
print("=" * 60)

r = simular_ciclo_automatico(
    T_inicial=50,
    T_objetivo_inicio_descarga=57,
    T_agua=67,
    v_agua=2.5,
    area=A_CONTACTO,
    volumen_inicial_m3=vol_ini,
    masa_por_descarga_kg=MASA_DESCARGA,
    tiempo_descarga_h=TIEMPO_DESCARGA,
    periodo_ciclo_h=PERIODO_CICLO,
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

print("\n" + "=" * 60)
print("TEST: Ciclo oficial precalentado (T_inicial=57, T_agua=75)")
print("=" * 60)

r2 = simular_ciclo_automatico(
    T_inicial=57,
    T_objetivo_inicio_descarga=57,
    T_agua=75,
    v_agua=2.5,
    area=A_CONTACTO,
    volumen_inicial_m3=vol_ini,
    masa_por_descarga_kg=MASA_DESCARGA,
    tiempo_descarga_h=TIEMPO_DESCARGA,
    periodo_ciclo_h=PERIODO_CICLO,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)

m2 = r2['metricas']
print(f"Tiempo calentamiento inicial: {m2['tiempo_calentamiento_inicial_h']:.2f} h")
print(f"Descargas calculadas:         {m2['descargas_calculadas']}")
print(f"Descargas OK:                 {m2['descargas_ok']}")
print(f"T final:                      {m2['T_final']:.2f} C")
print(f"Motivo corte:                 {m2['motivo_corte']}")
