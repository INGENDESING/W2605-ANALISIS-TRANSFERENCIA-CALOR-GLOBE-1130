"""
Crear archivos PDF placeholder para los PFDs del Escenario 02B
Usando matplotlib para generar diagramas de proceso
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch
import matplotlib.patches as mpatches

# Temperature data for each scenario
scenarios = {
    1: {'name': '02B_1', 't_in_gluc': 60, 't_out': [59.64, 59.21, 58.35], 't_agua': 75},
    2: {'name': '02B_2', 't_in_gluc': 57, 't_out': [57.06, 56.67, 55.88], 't_agua': 75},
    3: {'name': '02B_3', 't_in_gluc': 54, 't_out': [54.47, 54.11, 53.39], 't_agua': 75}
}

for i, data in scenarios.items():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.5, f'Escenario {data["name"]} - PFD', fontsize=16, ha='center', weight='bold')
    ax.text(7, 7.1, f'Agua a {data["t_agua"]}C, v=2.5 m/s, Glucosa entrada {data["t_in_gluc"]}C', 
            fontsize=11, ha='center', style='italic')
    
    # Tank
    tank = FancyBboxPatch((5.5, 3), 3, 2.5, boxstyle='round,pad=0.1', 
                          facecolor='lightgray', edgecolor='black', linewidth=2)
    ax.add_patch(tank)
    ax.text(7, 4.25, 'T-101\nTanque', ha='center', va='center', fontsize=10, weight='bold')
    
    # Jacket
    jacket = Rectangle((5.3, 3.2), 0.4, 2.1, facecolor='lightblue', edgecolor='blue', linewidth=1)
    ax.add_patch(jacket)
    ax.text(5.5, 5.5, 'E-201', ha='center', fontsize=8, color='blue')
    
    # Pump
    pump = Circle((2.5, 2), 0.4, facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(pump)
    ax.text(2.5, 2, 'P-101', ha='center', va='center', fontsize=8)
    
    # Carrotanque
    carrot = FancyBboxPatch((10, 1.5), 2, 1.5, boxstyle='round,pad=0.05',
                            facecolor='wheat', edgecolor='brown', linewidth=2)
    ax.add_patch(carrot)
    ax.text(11, 2.25, 'Carro-\ntanque', ha='center', va='center', fontsize=9)
    
    # Stream 1: Glucose in
    ax.annotate('', xy=(5.5, 4.5), xytext=(1, 4.5),
               arrowprops=dict(arrowstyle='->', color='orange', lw=2))
    ax.text(3, 5, f'Corriente 1\nGlucosa\n8,000 kg/h\n{data["t_in_gluc"]}C', 
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow'))
    
    # Stream 2: Water in
    ax.annotate('', xy=(5.3, 5.5), xytext=(3, 6.5),
               arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.text(3.5, 6.8, f'Corriente 2\nAgua caliente\n57.7 m3/h\n{data["t_agua"]}C', 
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    # Stream 3: Water out
    ax.annotate('', xy=(3, 2.5), xytext=(5.3, 3.5),
               arrowprops=dict(arrowstyle='->', color='lightblue', lw=2))
    ax.text(3.5, 2.2, f'Corriente 3\nAgua salida\n~74.9C', 
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='lightcyan'))
    
    # Stream 4: Glucose out to carrotanque
    ax.annotate('', xy=(10, 2.25), xytext=(8.5, 4),
               arrowprops=dict(arrowstyle='->', color='orange', lw=2))
    
    # Output temperatures box
    output_text = f'Corriente 4 - Glucosa salida\nv=1.0 m/s: {data["t_out"][0]}C\nv=1.5 m/s: {data["t_out"][1]}C\nv=3.0 m/s: {data["t_out"][2]}C'
    ax.text(11.5, 5, output_text, ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange', lw=2))
    
    plt.tight_layout()
    plt.savefig(f'results/PFD_Escenario_{data["name"]}.pdf', format='pdf', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Created PDF: PFD_Escenario_{data["name"]}.pdf')

print('All PDFs created successfully!')
