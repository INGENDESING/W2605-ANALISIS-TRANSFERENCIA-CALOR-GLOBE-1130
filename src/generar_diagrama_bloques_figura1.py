"""
Generador de Diagrama de Bloques - Figura 1 - Proyecto W2605
Version Matplotlib (sin dependencia de Graphviz)
Diagrama de bloques profesional del sistema de almacenamiento y carga de glucosa.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from geometria_tanque import A_CONTACTO

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


# =============================================================================
# COLORES CORPORATIVOS Y ESTILO
# =============================================================================
COLOR_FONDO = '#FFFFFF'
COLOR_BLOQUE_PROCESO = '#E8F5E9'      # verde claro
COLOR_BLOQUE_SERVICIO = '#E3F2FD'     # azul claro
COLOR_BLOQUE_PERDIDA = '#FFEBEE'      # rojo claro
COLOR_BORDE = '#263238'
COLOR_TEXTO = '#212121'
COLOR_FLECHA_G = '#2E7D32'            # verde oscuro (glucosa)
COLOR_FLECHA_A = '#1565C0'            # azul oscuro (agua)
COLOR_FLECHA_P = '#C62828'            # rojo (perdidas)
COLOR_FLECHA_N = '#424242'            # gris (otros)


def dibujar_bloque(ax, x, y, ancho, alto, etiqueta, subetiqueta=None,
                   color=COLOR_BLOQUE_PROCESO, fontsize=11, subfontsize=9):
    """Dibuja un bloque rectangular redondeado con etiqueta centrada."""
    bloque = FancyBboxPatch(
        (x, y), ancho, alto,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        facecolor=color, edgecolor=COLOR_BORDE, linewidth=1.8
    )
    ax.add_patch(bloque)
    ax.text(x + ancho/2, y + alto/2 + 0.15, etiqueta,
            fontsize=fontsize, fontweight='bold', ha='center', va='center',
            color=COLOR_TEXTO)
    if subetiqueta:
        ax.text(x + ancho/2, y + alto/2 - 0.35, subetiqueta,
                fontsize=subfontsize, ha='center', va='center',
                color=COLOR_TEXTO, style='italic')


def flecha(ax, x1, y1, x2, y2, color=COLOR_FLECHA_N, estilo='-', lw=2.0,
           etiqueta=None, offset_etiqueta=(0, 0.35), fontsize=9):
    """Dibuja una flecha entre dos puntos."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle=estilo,
                                connectionstyle='arc3,rad=0'))
    if etiqueta:
        ax.text((x1 + x2)/2 + offset_etiqueta[0],
                (y1 + y2)/2 + offset_etiqueta[1],
                etiqueta, fontsize=fontsize, ha='center', va='bottom',
                color=color, fontweight='bold')


def main():
    output_dir = 'results/figures'
    os.makedirs(output_dir, exist_ok=True)
    base_path = os.path.join(output_dir, 'diagrama_bloques_figura1')

    # Parametros representativos para anotaciones
    area_chaqueta = A_CONTACTO  # m2

    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor(COLOR_FONDO)

    # -------------------------------------------------------------------------
    # BLOQUES PRINCIPALES
    # -------------------------------------------------------------------------
    # Tanque T-101 (centro)
    dibujar_bloque(ax, 4.5, 3.2, 4.0, 2.6,
                   etiqueta='T-101',
                   subetiqueta=f'Tanque de almacenamiento\nGlobe 1130',
                   color=COLOR_BLOQUE_PROCESO)

    # Chaqueta E-201 (debajo del tanque, en fondo)
    dibujar_bloque(ax, 5.0, 1.4, 3.0, 1.2,
                   etiqueta='E-201',
                   subetiqueta=f'Chaqueta de media caña\nA = {area_chaqueta:.1f} m²',
                   color=COLOR_BLOQUE_SERVICIO)

    # Bomba P-101 (derecha del tanque)
    dibujar_bloque(ax, 10.0, 3.7, 2.2, 1.6,
                   etiqueta='P-101',
                   subetiqueta='Bomba de\ntransferencia',
                   color=COLOR_BLOQUE_PROCESO)

    # Carro tanque (salida)
    dibujar_bloque(ax, 10.0, 0.8, 2.2, 1.4,
                   etiqueta='Carro tanque',
                   subetiqueta='Despacho',
                   color='#FFF9C4')

    # Entrada de glucosa (izquierda)
    dibujar_bloque(ax, 0.8, 3.9, 2.4, 1.2,
                   etiqueta='Entrada de glucosa',
                   subetiqueta='57–60 °C',
                   color=COLOR_BLOQUE_PROCESO)

    # Agua caliente (arriba izquierda)
    dibujar_bloque(ax, 0.8, 6.8, 2.4, 1.2,
                   etiqueta='Agua caliente',
                   subetiqueta='65 / 75 °C',
                   color=COLOR_BLOQUE_SERVICIO)

    # Pérdidas térmicas (arriba derecha)
    dibujar_bloque(ax, 9.8, 7.6, 2.6, 1.2,
                   etiqueta='Pérdidas térmicas',
                   subetiqueta='~14,7 MJ/h',
                   color=COLOR_BLOQUE_PERDIDA)

    # -------------------------------------------------------------------------
    # FLUJOS DE PROCESO
    # -------------------------------------------------------------------------
    # Entrada glucosa -> Tanque
    flecha(ax, 3.2, 4.5, 4.5, 4.5, color=COLOR_FLECHA_G, etiqueta='Glucosa',
           offset_etiqueta=(0, 0.32), lw=2.5)

    # Tanque -> Bomba
    flecha(ax, 8.5, 4.5, 10.0, 4.5, color=COLOR_FLECHA_G, etiqueta='≥ 57 °C',
           offset_etiqueta=(0, 0.32), lw=2.5)

    # Bomba -> Carro tanque
    flecha(ax, 11.1, 3.7, 11.1, 2.2, color=COLOR_FLECHA_G, etiqueta='Carga',
           offset_etiqueta=(0.35, 0), lw=2.0)

    # -------------------------------------------------------------------------
    # SERVICIOS DE CALENTAMIENTO
    # -------------------------------------------------------------------------
    # Agua caliente -> Chaqueta
    flecha(ax, 3.2, 7.4, 5.0, 7.4, color=COLOR_FLECHA_A, etiqueta='Agua caliente',
           offset_etiqueta=(0, 0.32), lw=2.0)
    flecha(ax, 5.0, 7.4, 5.0, 2.6, color=COLOR_FLECHA_A, lw=2.0, estilo='--')

    # Chaqueta -> Agua fría de retorno
    flecha(ax, 8.0, 2.6, 8.0, 7.4, color=COLOR_FLECHA_A, lw=2.0, estilo='--')
    flecha(ax, 8.0, 7.4, 13.2, 7.4, color=COLOR_FLECHA_A,
           etiqueta='Agua de retorno', offset_etiqueta=(0, -0.45), lw=2.0)

    # -------------------------------------------------------------------------
    # FLUJO DE ENERGÍA
    # -------------------------------------------------------------------------
    # Q chaqueta anotación
    ax.text(6.5, 2.0, r'$\dot{Q}_{\mathrm{chaqueta}} \approx 33$ MJ/h',
            fontsize=10, ha='center', va='center', color=COLOR_FLECHA_A,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=COLOR_FLECHA_A, linewidth=1.2))

    # Pérdidas desde tanque hacia arriba
    flecha(ax, 8.5, 5.8, 10.5, 7.6, color=COLOR_FLECHA_P, lw=2.0,
           estilo=':', etiqueta='Pérdidas al ambiente',
           offset_etiqueta=(0.6, 0.0))

    # -------------------------------------------------------------------------
    # TÍTULO Y NOTAS
    # -------------------------------------------------------------------------
    ax.text(7.0, 8.75,
            'Diagrama de bloques del sistema de almacenamiento y carga de glucosa',
            fontsize=15, fontweight='bold', ha='center', va='center',
            color=COLOR_TEXTO)
    ax.text(7.0, 8.35,
            'Proyecto W2605 — Chaqueta de media caña, área de transferencia 14 m²',
            fontsize=11, ha='center', va='center', color=COLOR_TEXTO,
            style='italic')

    nota = (
        "Nota: los valores anotados corresponden al caso base con agua de chaqueta a 65 °C, "
        "glucosa de entrada 57–60 °C y aislamiento térmico de 2 pulgadas (50,8 mm)."
    )
    ax.text(7.0, 0.20, nota, fontsize=8, ha='center', va='center',
            color=COLOR_TEXTO, style='italic')

    # Leyenda simplificada
    leyenda_elementos = [
        mpatches.Patch(facecolor=COLOR_BLOQUE_PROCESO, edgecolor=COLOR_BORDE,
                       label='Proceso (glucosa)'),
        mpatches.Patch(facecolor=COLOR_BLOQUE_SERVICIO, edgecolor=COLOR_BORDE,
                       label='Servicio (agua de chaqueta)'),
        mpatches.Patch(facecolor=COLOR_BLOQUE_PERDIDA, edgecolor=COLOR_BORDE,
                       label='Pérdidas térmicas'),
    ]
    ax.legend(handles=leyenda_elementos, loc='upper left', fontsize=9,
              frameon=True, fancybox=True, shadow=False)

    plt.tight_layout()
    plt.savefig(f'{base_path}.png', dpi=200, bbox_inches='tight',
                facecolor=COLOR_FONDO)
    plt.savefig(f'{base_path}.pdf', dpi=300, bbox_inches='tight',
                facecolor=COLOR_FONDO)
    plt.close()

    print(f"Diagrama de bloques guardado en:\n  {base_path}.png\n  {base_path}.pdf")


if __name__ == "__main__":
    main()
