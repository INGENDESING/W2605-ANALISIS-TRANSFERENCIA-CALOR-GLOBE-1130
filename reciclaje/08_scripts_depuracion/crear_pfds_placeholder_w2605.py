# -*- coding: utf-8 -*-
"""
Genera PDFs placeholder para los PFDs de los escenarios usados en los informes W2605.
Evita referencias al codigo de proyecto anterior en los PDFs incrustados.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
ESCENARIOS = {
    '01A': 'Agua 65°C | Caudal 30,900 kg/h | Área 13 m² | Glucosa 60°C',
    '01B': 'Agua 65°C | Caudal 57,700 kg/h (v=2.5 m/s) | Área 13 m²',
    '01C': 'Agua 75°C | Caudal 57,700 kg/h (v=2.5 m/s) | Área 13 m²',
    '02A': 'Agua 75°C | Caudal 57,700 kg/h (v=2.5 m/s) | Área 28 m²',
}


def crear_placeholder(codigo, subtitulo):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Caja de titulo
    title_box = FancyBboxPatch((0.5, 6.5), 11, 1.2, boxstyle="round,pad=0.1",
                               facecolor='#1565C0', edgecolor='#0D47A1', linewidth=2)
    ax.add_patch(title_box)
    ax.text(6, 7.3, f'PFD ESCENARIO {codigo} - PROYECTO W2605',
            fontsize=18, fontweight='bold', color='white', ha='center', va='center')
    ax.text(6, 6.8, subtitulo,
            fontsize=11, color='#E3F2FD', ha='center', va='center')

    # Caja informativa
    info_box = FancyBboxPatch((1.5, 2.5), 9, 3, boxstyle="round,pad=0.1",
                              facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2)
    ax.add_patch(info_box)
    ax.text(6, 4.8, 'Diagrama de Flujo de Proceso (PFD)',
            fontsize=14, fontweight='bold', color='#E65100', ha='center', va='center')
    ax.text(6, 4.0, 'Este placeholder reemplaza al PFD anterior que contenía',
            fontsize=11, color='#424242', ha='center', va='center')
    ax.text(6, 3.5, 'referencias al codigo de proyecto anterior.',
            fontsize=11, color='#424242', ha='center', va='center')
    ax.text(6, 2.9, 'El diagrama detallado debe regenerarse con los scripts del proyecto W2605.',
            fontsize=10, color='#616161', ha='center', va='center')

    # Pie
    ax.text(6, 0.5, 'DMV Ingenieros Consultores S.A.S. | Ingredion S.A.',
            fontsize=9, color='#757575', ha='center', va='center')

    output_path = os.path.join(OUTPUT_DIR, f'PFD_Escenario_{codigo}.pdf')
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f'Generado: {output_path}')


def main():
    for codigo, subtitulo in ESCENARIOS.items():
        crear_placeholder(codigo, subtitulo)


if __name__ == '__main__':
    main()
