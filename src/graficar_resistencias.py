import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os


# =============================================================================
# CONFIGURACIÓN DE GRÁFICAS ESTILO PUBLICACIÓN
# =============================================================================

COLOR_GLUCOSA = '#2E5AAC'
COLOR_AGUA = '#C44E28'
COLOR_DESCARGA = '#3A7D44'
COLOR_BANDA_DESCARGA = '#F4A261'
COLOR_REJILLA = '#E5E5E5'
COLOR_TEXTO = '#333333'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'axes.edgecolor': COLOR_TEXTO,
    'axes.labelcolor': COLOR_TEXTO,
    'xtick.color': COLOR_TEXTO,
    'ytick.color': COLOR_TEXTO,
    'text.color': COLOR_TEXTO,
})

def graficar_resistencias(figures_dir='../results/figures'):
    """
    Genera gráfico profesional de distribución de resistencias térmicas.
    Diseño: gráfico de dona con leyenda externa y anotaciones con líneas
    para evitar superposición de texto en sectores pequeños.
    
    Datos: Tg=40°C, Tw=75°C → U=31.1 W/m²·°C
    Ref: coeficiente_U.py, Sección 10 del informe W2605-PR-INF-001
    """
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.unicode_minus': False,
    })

    # ── Datos de resistencias térmicas ──
    # Valores consistentes con el informe (Tg=40°C, Tw=75°C)
    componentes = [
        'Glucosa — Convección natural',
        'Pared SS316L — Conducción',
        'Agua — Convección forzada',
    ]
    porcentajes = [98.0, 1.7, 0.3]
    # Valores absolutos de resistencia [m²·K/W]
    R_valores = [0.03150, 0.000563, 0.000102]

    # Paleta profesional corporativa
    colores = [COLOR_GLUCOSA, '#7F8C8D', COLOR_AGUA]
    
    # ── Crear figura con dos zonas: dona (izq) + tabla (der) ──
    fig = plt.figure(figsize=(10, 5.5))
    
    # Eje para la dona (ocupa la mitad izquierda)
    ax_pie = fig.add_axes([0.02, 0.08, 0.52, 0.82])
    
    # Dona con explode en el sector dominante
    explode = (0.03, 0.03, 0.03)
    wedges, _ = ax_pie.pie(
        porcentajes,
        explode=explode,
        colors=colores,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=2),
    )

    # ── Texto central de la dona ──
    ax_pie.text(0, 0.06, r'$U = 31.1$', fontsize=14, fontweight='bold',
                ha='center', va='center', color=COLOR_TEXTO)
    ax_pie.text(0, -0.10, r'W/m²·°C', fontsize=10,
                ha='center', va='center', color=COLOR_TEXTO)

    # ── Anotaciones con líneas de conexión (evita superposición) ──
    # Posiciones angulares medias de cada sector
    angulos = []
    ang_acum = 90  # startangle
    for p in porcentajes:
        ang_medio = ang_acum - (p / 100 * 360) / 2
        angulos.append(np.radians(ang_medio))
        ang_acum -= p / 100 * 360

    # Configuración de anotaciones: (ángulo, radio_texto, alineación)
    anotaciones_config = [
        # Glucosa (sector grande, abajo)
        {'xy_r': 0.82, 'text_r': 1.15, 'text_ang': np.radians(-90),
         'ha': 'center', 'va': 'top'},
        # Pared SS316L (sector pequeño, arriba-derecha)  
        {'xy_r': 0.82, 'text_r': 1.22, 'text_ang': np.radians(70),
         'ha': 'left', 'va': 'center'},
        # Agua (sector muy pequeño, arriba)
        {'xy_r': 0.82, 'text_r': 1.22, 'text_ang': np.radians(89.5),
         'ha': 'center', 'va': 'bottom'},
    ]

    for i, (comp, pct) in enumerate(zip(componentes, porcentajes)):
        cfg = anotaciones_config[i]
        # Punto de conexión en el borde de la dona
        xy = (cfg['xy_r'] * np.cos(angulos[i]),
              cfg['xy_r'] * np.sin(angulos[i]))
        # Punto del texto
        txt_pos = (cfg['text_r'] * np.cos(cfg['text_ang']),
                   cfg['text_r'] * np.sin(cfg['text_ang']))
        
        ax_pie.annotate(
            f'{pct:.1f} %',
            xy=xy,
            xytext=txt_pos,
            fontsize=11,
            fontweight='bold',
            color=colores[i],
            ha=cfg['ha'], va=cfg['va'],
            arrowprops=dict(
                arrowstyle='-',
                color=colores[i],
                lw=1.2,
                connectionstyle='arc3,rad=0.15',
            ),
        )

    # ── Tabla-resumen a la derecha ──
    ax_tabla = fig.add_axes([0.56, 0.12, 0.42, 0.76])
    ax_tabla.axis('off')

    # Título de la tabla
    ax_tabla.text(0.5, 0.97, 'Desglose de resistencias térmicas',
                  fontsize=11, fontweight='bold', ha='center', va='top',
                  color=COLOR_TEXTO)
    ax_tabla.text(0.5, 0.91, r'($T_g$ = 40 °C,  $T_w$ = 75 °C)',
                  fontsize=9, ha='center', va='top', color=COLOR_TEXTO)

    # Línea separadora
    ax_tabla.plot([0.05, 0.95], [0.87, 0.87], color=COLOR_REJILLA, lw=1)

    # Filas de la tabla
    y_start = 0.80
    y_step = 0.22
    for i, (comp, pct, R) in enumerate(zip(componentes, porcentajes, R_valores)):
        y = y_start - i * y_step
        
        # Indicador de color (cuadrado)
        rect = mpatches.FancyBboxPatch(
            (0.02, y - 0.02), 0.04, 0.04,
            boxstyle='round,pad=0.005',
            facecolor=colores[i], edgecolor='none',
        )
        ax_tabla.add_patch(rect)

        # Nombre del componente
        ax_tabla.text(0.10, y + 0.02, comp,
                      fontsize=9.5, fontweight='bold', va='center',
                      color=COLOR_TEXTO)
        
        # Porcentaje y valor de R
        ax_tabla.text(0.10, y - 0.06,
                      f'{pct:.1f} %  ·  R = {R:.4f} m²·K/W',
                      fontsize=8.5, va='center', color=COLOR_TEXTO,
                      style='italic')

        # Barra horizontal proporcional
        bar_width = pct / 100 * 0.85
        bar = mpatches.FancyBboxPatch(
            (0.10, y - 0.12), bar_width, 0.03,
            boxstyle='round,pad=0.003',
            facecolor=colores[i], alpha=0.25, edgecolor='none',
        )
        ax_tabla.add_patch(bar)

    # Línea separadora inferior
    ax_tabla.plot([0.05, 0.95], [0.17, 0.17], color=COLOR_REJILLA, lw=1)

    # Nota al pie
    ax_tabla.text(0.5, 0.10,
                  'La convección natural de la glucosa\n'
                  'concentra el 98 % de la resistencia total,\n'
                  'constituyendo el factor limitante del sistema.',
                  fontsize=8, ha='center', va='top', color=COLOR_TEXTO,
                  style='italic', linespacing=1.4)

    # ── Título superior global ──
    fig.suptitle('Distribución de resistencias térmicas',
                 fontsize=13, fontweight='bold', y=0.97, color=COLOR_TEXTO)

    # ── Guardar ──
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(os.path.join(figures_dir, 'resistencias_termicas.pdf'),
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(figures_dir, 'resistencias_termicas.png'),
                facecolor='white', edgecolor='none')
    plt.close()
    print("Gráfico de resistencias generado exitosamente.")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    figures_dir = os.path.join(script_dir, '..', 'results', 'figures')
    graficar_resistencias(figures_dir)
