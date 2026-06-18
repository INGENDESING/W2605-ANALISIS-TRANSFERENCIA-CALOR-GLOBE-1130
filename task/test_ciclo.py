import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'webapp'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from app.core.balance_energia import simular_ciclo_automatico
from geometria_tanque import volumen_total, A_CONTACTO

V = volumen_total() * 0.80
MASA_DESCARGA = 24000.0
TIEMPO_DESCARGA = 2.0
PERIODO_CICLO = 4.8

print("=" * 70)
print("TEST: Ciclo oficial precalentado (Escenario 3 - agua 75 C)")
print("T_inicial=57, T_objetivo=57, T_agua=75, 5 descargas de 24 ton")
print("=" * 70)
r = simular_ciclo_automatico(
    T_inicial=57,
    T_objetivo_inicio_descarga=57,
    T_agua=75,
    v_agua=2.5,
    area=A_CONTACTO,
    volumen_inicial_m3=V,
    masa_por_descarga_kg=MASA_DESCARGA,
    tiempo_descarga_h=TIEMPO_DESCARGA,
    periodo_ciclo_h=PERIODO_CICLO,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)
m = r['metricas']
print(f"Descargas calculadas: {m['descargas_calculadas']}")
print(f"Motivo corte: {m['motivo_corte']}")
print(f"Masa total desc: {m['masa_total_descargada_ton']} ton")
print(f"T final: {m['T_final']} C")
print(f"Masa restante: {m['masa_restante_ton']} ton")
print(f"T min ciclo: {m['T_min_ciclo']} C")
print(f"Descargas OK: {m['descargas_ok']}")

print("\n" + "=" * 70)
print("TEST: Ciclo oficial precalentado (Escenario 2 - agua 65 C)")
print("=" * 70)
r2 = simular_ciclo_automatico(
    T_inicial=57,
    T_objetivo_inicio_descarga=57,
    T_agua=65,
    v_agua=2.5,
    area=A_CONTACTO,
    volumen_inicial_m3=V,
    masa_por_descarga_kg=MASA_DESCARGA,
    tiempo_descarga_h=TIEMPO_DESCARGA,
    periodo_ciclo_h=PERIODO_CICLO,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)
m2 = r2['metricas']
print(f"Descargas calculadas: {m2['descargas_calculadas']}")
print(f"Motivo corte: {m2['motivo_corte']}")
print(f"Masa total desc: {m2['masa_total_descargada_ton']} ton")
print(f"T final: {m2['T_final']} C")
print(f"Descargas OK: {m2['descargas_ok']}")

print("\n" + "=" * 70)
print("TEST: Calentamiento desde 50 C con T_agua=67 (24 h)")
print("=" * 70)
r3 = simular_ciclo_automatico(
    T_inicial=50,
    T_objetivo_inicio_descarga=57,
    T_agua=67,
    v_agua=2.5,
    area=A_CONTACTO,
    volumen_inicial_m3=V,
    masa_por_descarga_kg=MASA_DESCARGA,
    tiempo_descarga_h=TIEMPO_DESCARGA,
    periodo_ciclo_h=PERIODO_CICLO,
    temp_minima_aceptable=55,
    tiempo_maximo_h=24
)
m3 = r3['metricas']
print(f"Tiempo calentamiento inicial: {m3['tiempo_calentamiento_inicial_h']:.2f} h")
print(f"Descargas calculadas: {m3['descargas_calculadas']}")
print(f"Descargas OK: {m3['descargas_ok']}")
print(f"T final: {m3['T_final']:.2f} C")
print(f"Motivo corte: {m3['motivo_corte']}")
print(f"T min ciclo: {m3['T_min_ciclo']:.2f} C")
