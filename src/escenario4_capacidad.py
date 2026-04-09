"""
Escenario 4: Capacidad Operativa Diaria - Proyecto P2611
=======================================================
Comparativa de capacidad con diferentes temperaturas de entrada:
  - Caso A: 54°C -> 57°C (escenario conservador)
  - Caso B: 55°C -> 57°C (mejorado)

Parametros:
  T agua:        75°C
  Area:          13 m² (media cana propuesta)
  Masa descarga: 24 ton

Resultados:
  - Caso A (54°C): 3.8 ton/h, 6.3 h/descarga, 3 descargas/dia
  - Caso B (55°C): 7.5 ton/h, 3.2 h/descarga, 7 descargas/dia
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from coeficiente_U import coeficiente_U
from geometria_tanque import A_CONTACTO

# Configuracion graficas profesionales
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# =============================================================================
# PARAMETROS COMUNES
# =============================================================================

T_AGUA = 75.0            # °C
V_AGUA = 2.5             # m/s
A = 13.0                 # m² (area propuesta)
MASA_DESCARGA = 24000.0  # kg (24 ton)

# =============================================================================
# FUNCION DE CALCULO
# =============================================================================

def calcular_capacidad(T_in, T_out, nombre_caso):
    """Calcula capacidad operativa para un caso dado"""
    
    # U promedio
    T_prom = (T_in + T_out) / 2
    U, _, _, _ = coeficiente_U(V_AGUA, T_AGUA, T_prom)
    
    # LMTD
    dT1 = T_AGUA - T_in
    dT2 = T_AGUA - T_out
    if abs(dT1 - dT2) < 0.01:
        LMTD = dT1
    else:
        LMTD = (dT1 - dT2) / np.log(dT1 / dT2)
    
    # Q disponible
    Q_disponible = U * A * LMTD
    
    # Flujo maximo
    Cp = Cp_glucosa(T_prom)
    delta_T_glucosa = T_out - T_in
    m_dot_max = Q_disponible / (Cp * delta_T_glucosa)  # kg/s
    flujo_ton_h = m_dot_max * 3.6  # ton/h
    
    # Tiempo por descarga
    tiempo_h = MASA_DESCARGA / (m_dot_max * 3600)
    
    # Descargas por dia
    descargas_dia = 24 / tiempo_h
    
    print(f"\n=== {nombre_caso} ({T_in}°C -> {T_out}°C) ===")
    print(f"  DeltaT: {delta_T_glucosa}°C")
    print(f"  U efectivo: {U:.2f} W/m²°C")
    print(f"  LMTD: {LMTD:.2f}°C")
    print(f"  Q disponible: {Q_disponible/1000:.2f} kW")
    print(f"  Flujo maximo: {flujo_ton_h:.2f} ton/h")
    print(f"  Tiempo por descarga: {tiempo_h:.2f} horas")
    print(f"  Descargas por dia: {int(descargas_dia)}")
    
    return {
        'T_in': T_in,
        'T_out': T_out,
        'delta_T': delta_T_glucosa,
        'U': U,
        'LMTD': LMTD,
        'Q': Q_disponible,
        'flujo': flujo_ton_h,
        'tiempo_descarga': tiempo_h,
        'descargas_dia': int(descargas_dia),
        'capacidad_dia': int(descargas_dia) * 24
    }

# =============================================================================
# CALCULAR AMBOS CASOS
# =============================================================================

print("=" * 70)
print("ESCENARIO 4: CAPACIDAD OPERATIVA DIARIA")
print("Comparativa 54°C vs 55°C (Area 13 m²)")
print("=" * 70)

caso_54 = calcular_capacidad(54.0, 57.0, "CASO A - CONSERVADOR")
caso_55 = calcular_capacidad(55.0, 57.0, "CASO B - MEJORADO")

# =============================================================================
# GRAFICA PROFESIONAL COMPARATIVA
# =============================================================================

fig = plt.figure(figsize=(14, 10))

# Crear grid de subplots
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.2], hspace=0.3, wspace=0.3)

# --- Subplot 1: Comparativa de flujos ---
ax1 = fig.add_subplot(gs[0, 0])
casos = ['Caso A\n54°C→57°C', 'Caso B\n55°C→57°C']
flujos = [caso_54['flujo'], caso_55['flujo']]
colores_flujo = ['#E74C3C', '#27AE60']

bars1 = ax1.bar(casos, flujos, color=colores_flujo, edgecolor='black', linewidth=1.5, alpha=0.8)
ax1.set_ylabel('Flujo Máximo (ton/h)', fontweight='bold')
ax1.set_title('Flujo Máximo Alcanzable', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Anotaciones
for i, (bar, val) in enumerate(zip(bars1, flujos)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
             f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# --- Subplot 2: Tiempo por descarga ---
ax2 = fig.add_subplot(gs[0, 1])
tiempos = [caso_54['tiempo_descarga'], caso_55['tiempo_descarga']]

bars2 = ax2.bar(casos, tiempos, color=colores_flujo, edgecolor='black', linewidth=1.5, alpha=0.8)
ax2.set_ylabel('Tiempo por Descarga (horas)', fontweight='bold')
ax2.set_title('Tiempo para Llenar 24 ton', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
ax2.axhline(y=3, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Objetivo (3h)')

for i, (bar, val) in enumerate(zip(bars2, tiempos)):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             f'{val:.1f}h', ha='center', va='bottom', fontweight='bold', fontsize=11)

# --- Subplot 3: Descargas por dia ---
ax3 = fig.add_subplot(gs[1, 0])
descargas = [caso_54['descargas_dia'], caso_55['descargas_dia']]

bars3 = ax3.bar(casos, descargas, color=colores_flujo, edgecolor='black', linewidth=1.5, alpha=0.8)
ax3.set_ylabel('Descargas por Día', fontweight='bold')
ax3.set_title('Capacidad Operativa Diaria (24h)', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
ax3.axhline(y=8, color='blue', linestyle='--', linewidth=2, alpha=0.5, label='Requerimiento (8)')
ax3.legend()

for i, (bar, val) in enumerate(zip(bars3, descargas)):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             f'{val}', ha='center', va='bottom', fontweight='bold', fontsize=14)

# --- Subplot 4: Capacidad toneladas ---
ax4 = fig.add_subplot(gs[1, 1])
capacidades = [caso_54['capacidad_dia'], caso_55['capacidad_dia']]
requerimiento = 192  # 8 descargas x 24 ton

bars4 = ax4.bar(casos, capacidades, color=colores_flujo, edgecolor='black', linewidth=1.5, alpha=0.8)
ax4.axhline(y=requerimiento, color='blue', linestyle='--', linewidth=2, alpha=0.5, label='Requerimiento (192 ton)')
ax4.set_ylabel('Capacidad (ton/día)', fontweight='bold')
ax4.set_title('Capacidad Diaria Total', fontsize=12, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
ax4.legend()

for i, (bar, val) in enumerate(zip(bars4, capacidades)):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, 
             f'{val} ton', ha='center', va='bottom', fontweight='bold', fontsize=11)

# --- Subplot 5: Diagrama de proceso (span completo abajo) ---
ax5 = fig.add_subplot(gs[2, :])
ax5.set_xlim(0, 24)
ax5.set_ylim(0, 10)
ax5.axis('off')

# Titulo del diagrama
ax5.text(12, 9.5, 'DIAGRAMA DE PROCESO: CARGA Y DESCARGA DE CARROTANQUES', 
         ha='center', fontsize=13, fontweight='bold')

# === Caso A (54°C) - Parte superior ===
y_caso_a = 6.5
ax5.text(2, y_caso_a + 1.5, 'CASO A: 54°C→57°C (3 descargas/día)', 
         fontsize=11, fontweight='bold', color='#C0392B')

# Dibujar 3 descargas
colores_a = ['#F5B7B1', '#F1948A', '#E74C3C']
for i in range(3):
    inicio = i * 8  # Cada 8 horas
    # Rectangulo de descarga
    rect = FancyBboxPatch((inicio, y_caso_a - 0.8), 6.35, 1.2, 
                           boxstyle="square,pad=0.02", 
                           facecolor=colores_a[i], edgecolor='black', linewidth=1.5)
    ax5.add_patch(rect)
    # Texto
    ax5.text(inicio + 3.175, y_caso_a - 0.2, f'D{i+1}\n(6.3h)', 
             ha='center', va='center', fontsize=9, fontweight='bold')

# Eje de tiempo
ax5.plot([0, 24], [y_caso_a - 1.5, y_caso_a - 1.5], 'k-', linewidth=2)
for h in range(0, 25, 4):
    ax5.plot([h, h], [y_caso_a - 1.6, y_caso_a - 1.4], 'k-', linewidth=1)
    ax5.text(h, y_caso_a - 2, f'{h}h', ha='center', fontsize=8)

# === Caso B (55°C) - Parte inferior ===
y_caso_b = 2.5
ax5.text(2, y_caso_b + 1.5, 'CASO B: 55°C→57°C (7 descargas/día)', 
         fontsize=11, fontweight='bold', color='#1E8449')

# Dibujar 7 descargas
colores_b = ['#A9DFBF', '#7DCEA0', '#52BE80', '#27AE60', '#229954', '#1E8449', '#196F3D']
for i in range(7):
    inicio = i * 3.4  # Cada 3.4 horas
    duracion = 3.18
    rect = FancyBboxPatch((inicio, y_caso_b - 0.8), duracion, 1.2, 
                           boxstyle="square,pad=0.02", 
                           facecolor=colores_b[i], edgecolor='black', linewidth=1.5)
    ax5.add_patch(rect)
    ax5.text(inicio + duracion/2, y_caso_b - 0.2, f'D{i+1}', 
             ha='center', va='center', fontsize=8, fontweight='bold')

# Eje de tiempo
ax5.plot([0, 24], [y_caso_b - 1.5, y_caso_b - 1.5], 'k-', linewidth=2)
for h in range(0, 25, 4):
    ax5.plot([h, h], [y_caso_b - 1.6, y_caso_b - 1.4], 'k-', linewidth=1)
    ax5.text(h, y_caso_b - 2, f'{h}h', ha='center', fontsize=8)

# Leyenda
ax5.text(12, 0.3, 'Cada rectángulo representa el llenado de un carrotanque de 24 toneladas', 
         ha='center', fontsize=9, style='italic')

plt.suptitle('Escenario 4: Análisis de Capacidad Operativa con Área 13 m²', 
             fontsize=14, fontweight='bold', y=0.98)

plt.savefig('../figures/escenario4_comparativa_capacidad.png', bbox_inches='tight')
plt.savefig('../figures/escenario4_comparativa_capacidad.pdf', bbox_inches='tight')
print("\n  Guardada: escenario4_comparativa_capacidad.png/pdf")

# =============================================================================
# RESUMEN EJECUTIVO
# =============================================================================

print("\n" + "=" * 70)
print("RESUMEN COMPARATIVO - ESCENARIO 4")
print("=" * 70)
print("""
COMPARATIVA DE CASOS (Area 13 m2, Agua 75C):

+---------------------+------------------+------------------+----------+
| Parametro           | Caso A (54->57C) | Caso B (55->57C) | Mejora   |
+---------------------+------------------+------------------+----------+
| DeltaT              | 3C               | 2C               | -        |
| Flujo maximo        | %.1f ton/h       | %.1f ton/h       | +%d%%     |
| Tiempo/descarga     | %.1f h           | %.1f h           | -%d%%     |
| Descargas/dia       | %d               | %d               | +%d      |
| Capacidad diaria    | %d ton           | %d ton           | +%d     |
| vs. Requerimiento   | 37.5%%            | 87.5%%            | +50%%     |
+---------------------+------------------+------------------+----------+

RECOMENDACION:
  - Caso A (54C): Conservador, %d descargas/dia (deficit %d%%)
  - Caso B (55C): Optimizado, %d descargas/dia (deficit %d%%)
  
Se recomienda operar manteniendo la glucosa almacenada a minimo 55C
para maximizar la capacidad del sistema (7 descargas/dia).
""" % (
    caso_54['flujo'], caso_55['flujo'], int((caso_55['flujo']/caso_54['flujo']-1)*100),
    caso_54['tiempo_descarga'], caso_55['tiempo_descarga'], int((1-caso_55['tiempo_descarga']/caso_54['tiempo_descarga'])*100),
    caso_54['descargas_dia'], caso_55['descargas_dia'], caso_55['descargas_dia']-caso_54['descargas_dia'],
    caso_54['capacidad_dia'], caso_55['capacidad_dia'], caso_55['capacidad_dia']-caso_54['capacidad_dia'],
    caso_54['descargas_dia'], int((1-caso_54['capacidad_dia']/192)*100),
    caso_55['descargas_dia'], int((1-caso_55['capacidad_dia']/192)*100)
))

print("=" * 70)
