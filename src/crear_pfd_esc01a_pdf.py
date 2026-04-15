#!/usr/bin/env python3
"""
Generador de PFD para Escenario 01A en formato PDF - Proyecto P2611
Usando matplotlib para máxima calidad y compatibilidad
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arc, PathPatch
from matplotlib.path import Path
import numpy as np

# Configuración de estilo
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.linewidth'] = 1.2

# Crear figura
fig, ax = plt.subplots(1, 1, figsize=(16, 11), dpi=150)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 1100)
ax.axis('off')

# ===================== TITULO =====================
title_box = FancyBboxPatch((50, 1030), 1500, 50, boxstyle="round,pad=5", 
                            facecolor='#1565C0', edgecolor='#0D47A1', linewidth=2)
ax.add_patch(title_box)
ax.text(800, 1060, 'PFD ESCENARIO 01A - Sistema de Almacenamiento de Glucosa', 
        fontsize=16, fontweight='bold', color='white', ha='center', va='center')
ax.text(800, 1020, 'Agua 65°C | Caudal 30,900 kg/h | Área 13 m² | Glucosa 60°C | Caudal 8,000 kg/h', 
        fontsize=10, color='#424242', ha='center', va='center')

# ===================== TANQUE T-101 =====================
# Marco exterior (aislamiento)
ax.add_patch(FancyBboxPatch((320, 350), 220, 300, boxstyle="round,pad=10", 
                            facecolor='none', edgecolor='#9E9E9E', linewidth=2, linestyle='--'))

# Cuerpo cilindrico
ax.add_patch(Rectangle((330, 400), 200, 200, facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2.5))

# Fondo torisferico
arc_bottom = Arc((430, 400), 200, 80, angle=0, theta1=180, theta2=360, 
                 facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2.5)
ax.add_patch(arc_bottom)
ax.add_patch(Arc((430, 400), 200, 80, angle=0, theta1=180, theta2=360, 
                 edgecolor='#E65100', linewidth=1.5, linestyle='--'))

# Tapa eliptica
ax.add_patch(Arc((430, 600), 200, 80, angle=0, theta1=0, theta2=180, 
                 facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2.5))
ax.plot([330, 530], [600, 600], color='#E65100', linewidth=2.5)

# Lineas de refuerzo
ax.plot([365, 365], [360, 400], color='#FFB74D', linewidth=1)
ax.plot([495, 495], [360, 400], color='#FFB74D', linewidth=1)

# Nivel 80%
ax.plot([340, 520], [480, 480], color='#2196F3', linewidth=3)
ax.add_patch(Rectangle((340, 400), 180, 80, facecolor='#E3F2FD', alpha=0.4))
ax.text(540, 485, '80%', fontsize=10, color='#1565C0', fontweight='bold')

# Etiquetas del tanque
ax.text(430, 550, 'T-101', fontsize=16, fontweight='bold', color='#E65100', ha='center')
ax.text(430, 530, 'Tanque de Almacenamiento', fontsize=10, color='#424242', ha='center')
ax.text(430, 470, 'Fondo Torisferico', fontsize=8, color='#757575', ha='center', style='italic')
ax.text(430, 455, 'D = 5.03 m | H = 9.67 m', fontsize=8, color='#757575', ha='center')

# ===================== CHAQUETA E-201 =====================
# Caja principal
ax.add_patch(FancyBboxPatch((355, 250), 150, 70, boxstyle="round,pad=3", 
                            facecolor='#B3E5FC', edgecolor='#1565C0', linewidth=2))

# Serpentina
for y in [265, 285, 305]:
    ax.plot([365, 495], [y, y], color='#1565C0', linewidth=2)
ax.plot([495, 495], [265, 305], color='#1565C0', linewidth=2)
ax.plot([365, 365], [285, 305], color='#1565C0', linewidth=2)

# Conexiones
ax.plot([355, 340], [285, 285], color='#1565C0', linewidth=2)
ax.plot([505, 520], [285, 285], color='#1565C0', linewidth=2)

# Etiquetas
ax.text(430, 235, 'E-201', fontsize=12, fontweight='bold', color='#0D47A1', ha='center')
ax.text(430, 330, 'Chaqueta Media Caña', fontsize=9, color='#424242', ha='center')
ax.text(430, 345, 'A = 13 m²', fontsize=8, color='#757575', ha='center')

# ===================== BOMBA P-101 =====================
bomba_x, bomba_y = 720, 480
ax.add_patch(Circle((bomba_x, bomba_y), 35, facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=2))
triangle = Polygon([(bomba_x, bomba_y-15), (bomba_x-15, bomba_y+10), (bomba_x+15, bomba_y+10)], 
                   facecolor='white', edgecolor='#7B1FA2', linewidth=2)
ax.add_patch(triangle)
ax.add_patch(Circle((bomba_x, bomba_y), 6, facecolor='white', edgecolor='#7B1FA2', linewidth=1.5))
ax.text(bomba_x, 530, 'P-101', fontsize=11, fontweight='bold', color='#7B1FA2', ha='center')
ax.text(bomba_x, 435, 'Bomba', fontsize=9, color='#424242', ha='center')

# ===================== CARROTANQUE =====================
# Cabina
ax.add_patch(FancyBboxPatch((1050, 440), 70, 70, boxstyle="round,pad=3", 
                            facecolor='#FFECB3', edgecolor='#FF8F00', linewidth=2))
ax.add_patch(FancyBboxPatch((1060, 460), 35, 25, boxstyle="round,pad=2", 
                            facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=1.5))
ax.plot([1120, 1120], [440, 510], color='#FF8F00', linewidth=2)

# Tanque
ax.add_patch(Rectangle((1125, 435), 110, 80, facecolor='#BDBDBD', edgecolor='#616161', linewidth=2))
for x in [1155, 1190, 1225]:
    ax.plot([x, x], [435, 515], color='#757575', linewidth=1.5)

# Ruedas
for cx in [1075, 1095, 1145, 1180, 1220]:
    ax.add_patch(Circle((cx, 425), 10, facecolor='#424242', edgecolor='#212121', linewidth=1.5))

ax.text(1145, 430, 'Carro Tanque', fontsize=11, fontweight='bold', color='#424242', ha='center')
ax.text(1145, 405, 'Capacidad: 24 ton', fontsize=8, color='#616161', ha='center')

# ===================== VIENTO =====================
ax.text(430, 740, 'Viento', fontsize=12, fontweight='bold', color='#00ACC1', ha='center')
ax.annotate('', xy=(510, 720), xytext=(350, 720), arrowprops=dict(arrowstyle='->', color='#00ACC1', lw=2.5))
ax.annotate('', xy=(490, 700), xytext=(370, 700), arrowprops=dict(arrowstyle='->', color='#00ACC1', lw=2))
ax.annotate('', xy=(470, 680), xytext=(390, 680), arrowprops=dict(arrowstyle='->', color='#00ACC1', lw=1.5))

# ===================== LINEAS DE PROCESO =====================
# Glucosa entrada
ax.annotate('', xy=(320, 520), xytext=(50, 520), 
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=3))
ax.plot([280, 320], [520, 570], color='#2E7D32', linewidth=3)
ax.text(180, 535, 'Corriente 1', fontsize=9, color='#2E7D32', fontweight='bold')

# Glucosa salida
ax.annotate('', xy=(620, 480), xytext=(550, 530), 
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=3))
ax.plot([620, 720], [480, 480], color='#2E7D32', linewidth=3)
ax.annotate('', xy=(1050, 480), xytext=(755, 480), 
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=3))
ax.text(850, 495, 'Corriente 4', fontsize=9, color='#2E7D32', fontweight='bold')

# Agua entrada
ax.annotate('', xy=(340, 285), xytext=(50, 285), 
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=3, linestyle='dashed'))
ax.text(180, 270, 'Corriente 2', fontsize=9, color='#C62828', fontweight='bold')

# Agua salida
ax.annotate('', xy=(600, 285), xytext=(505, 285), 
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=3, linestyle='dashed'))
ax.text(550, 270, 'Corriente 3', fontsize=9, color='#C62828', fontweight='bold')

# ===================== CAJAS DE DATOS - ENTRADAS =====================
# Corriente 1 - Glucosa entrada
ax.add_patch(FancyBboxPatch((30, 630), 260, 70, boxstyle="round,pad=5", 
                            facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2))
ax.text(160, 665, 'CORRIENTE 1 - Glucosa Entrada', fontsize=10, fontweight='bold', 
        color='#1B5E20', ha='center')
ax.text(160, 690, '8,000 kg/h | 60.0°C | 1,024 MJ/h', fontsize=10, color='#212121', ha='center')

# Corriente 2 - Agua entrada
ax.add_patch(FancyBboxPatch((30, 150), 260, 70, boxstyle="round,pad=5", 
                            facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2))
ax.text(160, 185, 'CORRIENTE 2 - Agua Entrada', fontsize=10, fontweight='bold', 
        color='#B71C1C', ha='center')
ax.text(160, 210, '30,900 kg/h | 65.0°C | 8,224 MJ/h', fontsize=10, color='#212121', ha='center')

# Corriente 3 - Agua salida
ax.add_patch(FancyBboxPatch((620, 150), 260, 70, boxstyle="round,pad=5", 
                            facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2))
ax.text(750, 185, 'CORRIENTE 3 - Agua Salida', fontsize=10, fontweight='bold', 
        color='#B71C1C', ha='center')
ax.text(750, 210, '30,900 kg/h | 64.9°C | 8,218 MJ/h', fontsize=10, color='#212121', ha='center')

# ===================== CAJAS DE DATOS - SALIDAS (3 velocidades) =====================
# Corriente 4a - v=1.0 m/s
ax.add_patch(FancyBboxPatch((620, 630), 280, 80, boxstyle="round,pad=5", 
                            facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2.5))
ax.text(760, 660, 'CORRIENTE 4a - v = 1.0 m/s', fontsize=10, fontweight='bold', 
        color='#1B5E20', ha='center')
ax.text(760, 685, '8,000 kg/h | 58.6°C | 999 MJ/h', fontsize=11, color='#212121', 
        ha='center', fontweight='bold')
ax.text(760, 705, 'h_ext = 2.41 W/m²K | U_perd = 1.78 W/m²K', fontsize=8, 
        color='#616161', ha='center')

# Corriente 4b - v=1.5 m/s
ax.add_patch(FancyBboxPatch((620, 530), 280, 80, boxstyle="round,pad=5", 
                            facecolor='#A5D6A7', edgecolor='#2E7D32', linewidth=2))
ax.text(760, 560, 'CORRIENTE 4b - v = 1.5 m/s', fontsize=10, fontweight='bold', 
        color='#1B5E20', ha='center')
ax.text(760, 585, '8,000 kg/h | 58.1°C | 992 MJ/h', fontsize=11, color='#212121', 
        ha='center', fontweight='bold')
ax.text(760, 605, 'h_ext = 3.29 W/m²K | U_perd = 2.22 W/m²K', fontsize=8, 
        color='#616161', ha='center')

# Corriente 4c - v=3.0 m/s
ax.add_patch(FancyBboxPatch((620, 430), 280, 80, boxstyle="round,pad=5", 
                            facecolor='#81C784', edgecolor='#2E7D32', linewidth=2))
ax.text(760, 460, 'CORRIENTE 4c - v = 3.0 m/s', fontsize=10, fontweight='bold', 
        color='#1B5E20', ha='center')
ax.text(760, 485, '8,000 kg/h | 57.3°C | 977 MJ/h', fontsize=11, color='#212121', 
        ha='center', fontweight='bold')
ax.text(760, 505, 'h_ext = 5.79 W/m²K | U_perd = 3.12 W/m²K', fontsize=8, 
        color='#616161', ha='center')

# ===================== TABLA DE BALANCE ENERGETICO =====================
ax.add_patch(FancyBboxPatch((950, 150), 400, 200, boxstyle="round,pad=8", 
                            facecolor='white', edgecolor='#1565C0', linewidth=2.5))
ax.add_patch(FancyBboxPatch((950, 320), 400, 35, boxstyle="round,pad=5", 
                            facecolor='#1565C0', edgecolor='#0D47A1', linewidth=2))
ax.text(1150, 342, 'BALANCE ENERGÉTICO - ESCENARIO 01A', fontsize=11, 
        fontweight='bold', color='white', ha='center')

# Tabla
ax.text(1030, 305, 'Concepto', fontsize=9, fontweight='bold', color='#424242', ha='center')
ax.text(1130, 305, '1.0 m/s', fontsize=9, fontweight='bold', color='#424242', ha='center')
ax.text(1230, 305, '1.5 m/s', fontsize=9, fontweight='bold', color='#424242', ha='center')
ax.text(1330, 305, '3.0 m/s', fontsize=9, fontweight='bold', color='#424242', ha='center')

ax.plot([960, 1340], [295, 295], color='#BDBDBD', linewidth=1)

ax.text(1030, 275, 'Q Transferido (MJ/h)', fontsize=8, color='#212121', ha='center')
ax.text(1130, 275, '6.7', fontsize=8, color='#1565C0', ha='center')
ax.text(1230, 275, '7.0', fontsize=8, color='#1565C0', ha='center')
ax.text(1330, 275, '7.5', fontsize=8, color='#1565C0', ha='center')

ax.text(1030, 255, 'Q Pérdidas (MJ/h)', fontsize=8, color='#212121', ha='center')
ax.text(1130, 255, '31.4', fontsize=8, color='#C62828', ha='center')
ax.text(1230, 255, '38.9', fontsize=8, color='#C62828', ha='center')
ax.text(1330, 255, '54.1', fontsize=8, color='#C62828', ha='center')

ax.plot([960, 1340], [240, 240], color='#BDBDBD', linewidth=1)

ax.text(1030, 220, 'Q Neto (MJ/h)', fontsize=9, fontweight='bold', color='#212121', ha='center')
ax.text(1130, 220, '-24.7', fontsize=9, fontweight='bold', color='#D32F2F', ha='center')
ax.text(1230, 220, '-31.9', fontsize=9, fontweight='bold', color='#D32F2F', ha='center')
ax.text(1330, 220, '-46.6', fontsize=9, fontweight='bold', color='#D32F2F', ha='center')

ax.text(1150, 185, 'Pérdidas exceden 4.7-7.2 veces el calor transferido', 
        fontsize=8, color='#616161', ha='center', style='italic')

# ===================== NOTAS =====================
ax.add_patch(FancyBboxPatch((950, 30), 400, 85, boxstyle="round,pad=5", 
                            facecolor='#FFF3E0', edgecolor='#FF8F00', linewidth=1.5))
ax.text(1150, 100, 'PARÁMETROS DEL SISTEMA', fontsize=10, fontweight='bold', 
        color='#E65100', ha='center')
ax.text(970, 80, '• U chaqueta: 25.2-25.7 W/m²K (calculado)', fontsize=8, color='#424242')
ax.text(970, 65, '• h_i (agua): ~6,490 W/m²K | h_o (glucosa): ~25-26 W/m²K', fontsize=8, color='#424242')
ax.text(970, 50, '• A_superficie expuesta: 149.67 m² | T_ambiente: 26.5°C', fontsize=8, color='#424242')

# ===================== LEYENDA =====================
ax.add_patch(FancyBboxPatch((30, 30), 260, 85, boxstyle="round,pad=5", 
                            facecolor='#ECEFF1', edgecolor='#546E7A', linewidth=1.5))
ax.text(160, 100, 'EQUIPOS', fontsize=10, fontweight='bold', color='#37474F', ha='center')
ax.text(45, 80, 'T-101: Tanque de almacenamiento (80% llenado)', fontsize=8, color='#424242')
ax.text(45, 65, 'E-201: Chaqueta de media caña (A = 13 m²)', fontsize=8, color='#424242')
ax.text(45, 50, 'P-101: Bomba de transferencia', fontsize=8, color='#424242')

# Guardar
plt.tight_layout(pad=0)
output_path = '../results/PFD_Escenario_01A.pdf'
plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.close()

print(f"PFD del Escenario 01A generado exitosamente:")
print(f"  Archivo: {output_path}")
print(f"  Formato: PDF vectorial de alta calidad")
print(f"  Dimensiones: 16 x 11 pulgadas (2400 x 1650 px a 150 DPI)")
print(f"  Velocidades de viento: 1.0, 1.5, 3.0 m/s")
print(f"  Nota: Sin referencias a espesor de aislamiento")
