"""
Diagramas de bloques del ciclo oficial de calentamiento/descarga
Proyecto W2605 — Fondo de tanque de glucosa Tag 53A-90A-0056

Genera tres figuras en results/figures/:
  1. diagrama_bloques_global.{png,pdf}
  2. diagrama_bloques_descarga.{png,pdf}
  3. diagrama_bloques_calentamiento.{png,pdf}

Estilo coherente con src/generar_diagrama_bloques_figura1.py (matplotlib).
"""

import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch


# =============================================================================
# PALETA CORPORATIVA
# =============================================================================
COLOR_FONDO = "#FFFFFF"
COLOR_BORDE = "#263238"
COLOR_TEXTO = "#212121"

# Bloques
COLOR_BLOQUE_PROCESO = "#E8F5E9"      # verde claro (glucosa/proceso)
COLOR_BLOQUE_SERVICIO = "#E3F2FD"     # azul claro (agua / servicio)
COLOR_BLOQUE_PERDIDA = "#FFEBEE"      # rojo claro (pérdidas)
COLOR_BLOQUE_OTRO = "#FFF9C4"         # amarillo claro (carrotanque)
COLOR_BLOQUE_INFO = "#F5F5F5"         # gris muy claro (datos auxiliares)

# Flechas
COLOR_FLECHA_G = "#2E7D32"            # verde oscuro (glucosa)
COLOR_FLECHA_A = "#1565C0"            # azul oscuro (agua)
COLOR_FLECHA_P = "#C62828"            # rojo (pérdidas)
COLOR_FLECHA_N = "#424242"            # gris (otros)

# Constantes del proyecto (datos oficiales)
A_CHAQUETA = 14.0                     # m²
T_AGUA_IN = 75.0                      # °C
Q_AGUA = 57.7                         # m³/h
V_AGUA = 2.5                          # m/s
T_AGUA_OUT = 74.9                     # °C
Q_CHAQUETA = 27.3                     # MJ/h
Q_PERDIDAS = 14.7                     # MJ/h
FLUJO_MEDIO_G = 5000.0                # kg/h
FLUJO_DESCARGA = 12000.0              # kg/h
MASA_DESCARGA = 24000.0               # kg
T_ALIM = 55.0                         # °C (caso conservador)
T_MIN_DESPACHO = 57.0                 # °C
T_INICIAL = 60.0                      # °C
T_FINAL_CICLO = 58.56                 # °C
U_60 = 36.2                           # W/(m²·°C)
U_REP = 31.0                          # W/(m²·°C) aprox.
R_FRACCION_PRODUCTO = 0.98
CICLO_DESCARGAS = 5
DURACION_DESCARGA = 2.0               # h
PERIODO = 4.8                         # h
TIEMPO_CALENTAMIENTO = 2.8            # h
AISLAMIENTO = 50.8                    # mm


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================
def _nueva_figura():
    """Crea figura y ejes con el tamaño corporativo."""
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    ax.set_facecolor(COLOR_FONDO)
    return fig, ax


def _guardar(fig, base_path):
    """Guarda PNG (200 dpi) y PDF (300 dpi)."""
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    plt.tight_layout()
    fig.savefig(f"{base_path}.png", dpi=200, bbox_inches="tight",
                facecolor=COLOR_FONDO)
    fig.savefig(f"{base_path}.pdf", dpi=300, bbox_inches="tight",
                facecolor=COLOR_FONDO)
    plt.close(fig)


def dibujar_bloque(ax, x, y, ancho, alto, etiqueta, subetiqueta=None,
                   color=COLOR_BLOQUE_PROCESO, fontsize=11, subfontsize=9):
    """Rectángulo redondeado con etiqueta centrada."""
    bloque = FancyBboxPatch(
        (x, y), ancho, alto,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        facecolor=color, edgecolor=COLOR_BORDE, linewidth=1.8
    )
    ax.add_patch(bloque)
    ax.text(x + ancho / 2, y + alto / 2 + 0.18, etiqueta,
            fontsize=fontsize, fontweight="bold", ha="center", va="center",
            color=COLOR_TEXTO)
    if subetiqueta:
        ax.text(x + ancho / 2, y + alto / 2 - 0.35, subetiqueta,
                fontsize=subfontsize, ha="center", va="center",
                color=COLOR_TEXTO, style="italic")


def flecha(ax, x1, y1, x2, y2, color=COLOR_FLECHA_N, estilo="-", lw=2.0,
           etiqueta=None, offset_etiqueta=(0, 0.35), fontsize=9,
           flecha_style="->"):
    """Flecha con etiqueta opcional."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=flecha_style, color=color, lw=lw,
                        linestyle=estilo, connectionstyle="arc3,rad=0")
    )
    if etiqueta:
        ax.text((x1 + x2) / 2 + offset_etiqueta[0],
                (y1 + y2) / 2 + offset_etiqueta[1],
                etiqueta, fontsize=fontsize, ha="center", va="bottom",
                color=color, fontweight="bold")


def _leyenda(ax, loc="lower left", bbox_to_anchor=(0.02, 0.04), ncol=2):
    """Leyenda corporativa de flujos."""
    elementos = [
        mpatches.Patch(facecolor=COLOR_BLOQUE_PROCESO, edgecolor=COLOR_BORDE,
                       label="Proceso (glucosa)"),
        mpatches.Patch(facecolor=COLOR_BLOQUE_SERVICIO, edgecolor=COLOR_BORDE,
                       label="Servicio (agua de chaqueta)"),
        mpatches.Patch(facecolor=COLOR_BLOQUE_PERDIDA, edgecolor=COLOR_BORDE,
                       label="Pérdidas térmicas"),
        mpatches.Patch(facecolor=COLOR_BLOQUE_OTRO, edgecolor=COLOR_BORDE,
                       label="Despacho"),
    ]
    ax.legend(handles=elementos, loc=loc, bbox_to_anchor=bbox_to_anchor,
              ncol=ncol, fontsize=9, frameon=True, fancybox=True, shadow=False)


# =============================================================================
# 1. DIAGRAMA GLOBAL DEL SISTEMA
# =============================================================================
def generar_diagrama_global(output_dir="results/figures"):
    """Figura 1: vista global del sistema de almacenamiento y carga."""
    base_path = os.path.join(output_dir, "diagrama_bloques_global")
    fig, ax = _nueva_figura()

    # -------------------------------------------------------------------------
    # Bloques
    # -------------------------------------------------------------------------
    # Entrada de glucosa (izquierda, centro)
    dibujar_bloque(ax, 0.5, 4.8, 2.6, 1.4,
                   etiqueta="Entrada de glucosa",
                   subetiqueta=f"{FLUJO_MEDIO_G:,.0f} kg/h\n{T_ALIM:.0f} °C (caso conservador)",
                   color=COLOR_BLOQUE_PROCESO)

    # Tanque (centro)
    dibujar_bloque(ax, 4.6, 3.6, 4.8, 2.8,
                   etiqueta="Tag 53A-90A-0056",
                   subetiqueta=("Tanque de almacenamiento\n"
                                "Globe 1130, 80,6 °Brix\n"
                                "Fondo toriesférico"),
                   color=COLOR_BLOQUE_PROCESO, fontsize=12)

    # Chaqueta (debajo del tanque)
    dibujar_bloque(ax, 5.5, 1.7, 3.0, 1.3,
                   etiqueta="Chaqueta E-201",
                   subetiqueta=f"Media caña rectangular\nA = {A_CHAQUETA:.0f} m²",
                   color=COLOR_BLOQUE_SERVICIO)

    # Bomba (derecha)
    dibujar_bloque(ax, 11.0, 4.7, 2.2, 1.5,
                   etiqueta="Bomba P-101",
                   subetiqueta="Transferencia a\ncarrotanque",
                   color=COLOR_BLOQUE_PROCESO)

    # Carrotanque (abajo derecha)
    dibujar_bloque(ax, 11.0, 1.0, 2.2, 1.5,
                   etiqueta="Carro tanque",
                   subetiqueta=f"{MASA_DESCARGA/1000:.0f} ton × {CICLO_DESCARGAS} / día",
                   color=COLOR_BLOQUE_OTRO)

    # Agua caliente (arriba izquierda)
    dibujar_bloque(ax, 0.5, 6.6, 2.6, 1.3,
                   etiqueta="Agua caliente",
                   subetiqueta=f"{Q_AGUA:.1f} m³/h | {V_AGUA:.1f} m/s\n{T_AGUA_IN:.0f} °C",
                   color=COLOR_BLOQUE_SERVICIO)

    # Pérdidas térmicas (arriba derecha, desplazado para no cruzar flechas)
    dibujar_bloque(ax, 9.8, 6.5, 3.4, 1.2,
                   etiqueta="Pérdidas térmicas",
                   subetiqueta=f"{Q_PERDIDAS:.1f} MJ/h\n{AISLAMIENTO:.1f} mm lana mineral",
                   color=COLOR_BLOQUE_PERDIDA)

    # Datos de ciclo (abajo izquierda)
    dibujar_bloque(ax, 0.5, 1.0, 3.8, 1.6,
                   etiqueta="Ciclo oficial",
                   subetiqueta=(f"{CICLO_DESCARGAS} descargas/día de {MASA_DESCARGA/1000:.0f} ton\n"
                                f"{FLUJO_DESCARGA/1000:.0f} ton/h durante {DURACION_DESCARGA:.1f} h\n"
                                f"Período {PERIODO:.1f} h | Calentamiento {TIEMPO_CALENTAMIENTO:.1f} h"),
                   color=COLOR_BLOQUE_INFO, fontsize=10)

    # -------------------------------------------------------------------------
    # Flechas de proceso
    # -------------------------------------------------------------------------
    flecha(ax, 3.1, 5.5, 4.6, 5.0, color=COLOR_FLECHA_G, lw=2.5,
           etiqueta="Glucosa", offset_etiqueta=(0, 0.32))

    flecha(ax, 9.4, 5.0, 11.0, 5.45, color=COLOR_FLECHA_G, lw=2.5,
           etiqueta=f"≥ {T_MIN_DESPACHO:.0f} °C", offset_etiqueta=(0, 0.32))

    flecha(ax, 12.1, 4.7, 12.1, 2.5, color=COLOR_FLECHA_G, lw=2.0,
           etiqueta="Carga", offset_etiqueta=(0.35, 0))

    # -------------------------------------------------------------------------
    # Flechas de servicio
    # -------------------------------------------------------------------------
    flecha(ax, 3.1, 8.0, 5.5, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta="Agua caliente", offset_etiqueta=(0, 0.15))
    flecha(ax, 5.5, 8.0, 5.5, 3.0, color=COLOR_FLECHA_A, lw=2.0, estilo="--")

    flecha(ax, 8.4, 3.0, 8.4, 8.0, color=COLOR_FLECHA_A, lw=2.0, estilo="--")
    flecha(ax, 8.4, 8.0, 13.5, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta=f"Retorno ~{T_AGUA_OUT:.1f} °C", offset_etiqueta=(0, 0.15))

    # -------------------------------------------------------------------------
    # Energía y pérdidas
    # -------------------------------------------------------------------------
    ax.text(7.0, 1.05,
            r"$\dot{Q}_{\mathrm{chaqueta}} \approx$ "
            f"{Q_CHAQUETA:.1f} MJ/h  |  "
            r"$\dot{Q}_{\mathrm{pérdidas}} \approx$ "
            f"{Q_PERDIDAS:.1f} MJ/h",
            fontsize=10, ha="center", va="center", color=COLOR_TEXTO,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=COLOR_BORDE, linewidth=1.2))

    flecha(ax, 8.8, 6.4, 10.0, 6.6, color=COLOR_FLECHA_P, lw=2.0,
           estilo=":")
    ax.text(8.2, 6.9, "Pérdidas al ambiente", fontsize=9,
            ha="left", va="center", color=COLOR_FLECHA_P, fontweight="bold")

    # -------------------------------------------------------------------------
    # Título y notas
    # -------------------------------------------------------------------------
    ax.text(7.0, 9.2,
            "Diagrama de bloques del sistema de almacenamiento y carga de glucosa",
            fontsize=15, fontweight="bold", ha="center", va="center",
            color=COLOR_TEXTO)
    ax.text(7.0, 8.7,
            f"Proyecto W2605 — Tag 53A-90A-0056 | Chaqueta de {A_CHAQUETA:.0f} m² | "
            f"U ≈ {U_60:.0f} W/(m²·°C) a 60 °C",
            fontsize=11, ha="center", va="center", color=COLOR_TEXTO,
            style="italic")

    nota = (
        "Nota: valores para ciclo oficial con agua a 75 °C, glucosa de alimentación a 55 °C, "
        f"aislamiento de 50,8 mm, U ≈ {U_REP:.0f} W/(m²·°C) en condiciones representativas "
        "y resistencia térmica del lado del producto ≈ 98 %."
    )
    ax.text(7.0, 0.25, nota, fontsize=8, ha="center", va="center",
            color=COLOR_TEXTO, style="italic")

    _leyenda(ax, loc="lower left", bbox_to_anchor=(0.02, 0.05), ncol=2)
    _guardar(fig, base_path)
    print(f"[OK] Diagrama global guardado en:\n  {base_path}.png\n  {base_path}.pdf")


# =============================================================================
# 2. DIAGRAMA DE LA FASE DE DESCARGA
# =============================================================================
def generar_diagrama_descarga(output_dir="results/figures"):
    """Balance de masa y energía durante la descarga."""
    base_path = os.path.join(output_dir, "diagrama_bloques_descarga")
    fig, ax = _nueva_figura()

    # -------------------------------------------------------------------------
    # Bloques
    # -------------------------------------------------------------------------
    # Entrada de glucosa fría
    dibujar_bloque(ax, 0.6, 4.9, 2.8, 1.4,
                   etiqueta="Entrada de glucosa",
                   subetiqueta=f"{FLUJO_DESCARGA/1000:.0f} ton/h\n{T_ALIM:.0f} °C",
                   color=COLOR_BLOQUE_PROCESO)

    # Tanque
    dibujar_bloque(ax, 4.8, 3.5, 4.4, 2.8,
                   etiqueta="Tag 53A-90A-0056",
                   subetiqueta=("Glucosa Globe 1130\n"
                                f"T inicial {T_INICIAL:.0f} °C → final {T_FINAL_CICLO:.2f} °C"),
                   color=COLOR_BLOQUE_PROCESO, fontsize=12)

    # Chaqueta
    dibujar_bloque(ax, 5.5, 1.3, 3.0, 1.3,
                   etiqueta="Chaqueta E-201",
                   subetiqueta=f"A = {A_CHAQUETA:.0f} m² | Agua {T_AGUA_IN:.0f} °C",
                   color=COLOR_BLOQUE_SERVICIO)

    # Salida hacia carrotanque
    dibujar_bloque(ax, 10.8, 4.9, 2.8, 1.4,
                   etiqueta="Salida a carro tanque",
                   subetiqueta=f"{FLUJO_DESCARGA/1000:.0f} ton/h\n≥ {T_MIN_DESPACHO:.0f} °C",
                   color=COLOR_BLOQUE_OTRO)

    # Pérdidas
    dibujar_bloque(ax, 5.1, 6.5, 3.8, 1.2,
                   etiqueta="Pérdidas térmicas",
                   subetiqueta=f"{Q_PERDIDAS:.1f} MJ/h",
                   color=COLOR_BLOQUE_PERDIDA)

    # Balance energético (abajo)
    dibujar_bloque(ax, 9.5, 0.9, 4.0, 1.5,
                   etiqueta="Balance energético",
                   subetiqueta=(f"Aporte chaqueta: {Q_CHAQUETA:.1f} MJ/h\n"
                                f"Pérdidas:        {Q_PERDIDAS:.1f} MJ/h\n"
                                f"Neto disponible: {Q_CHAQUETA - Q_PERDIDAS:.1f} MJ/h"),
                   color=COLOR_BLOQUE_INFO, fontsize=10)

    # -------------------------------------------------------------------------
    # Flechas de proceso
    # -------------------------------------------------------------------------
    flecha(ax, 3.4, 5.6, 4.8, 5.2, color=COLOR_FLECHA_G, lw=2.5,
           etiqueta="Glucosa fría", offset_etiqueta=(0, 0.32))

    flecha(ax, 9.2, 5.2, 10.8, 5.6, color=COLOR_FLECHA_G, lw=2.5,
           etiqueta="Glucosa caliente", offset_etiqueta=(0, 0.32))

    # -------------------------------------------------------------------------
    # Servicio
    # -------------------------------------------------------------------------
    flecha(ax, 1.5, 8.0, 5.5, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta="Agua 75 °C", offset_etiqueta=(0, 0.15))
    flecha(ax, 5.5, 8.0, 5.5, 2.6, color=COLOR_FLECHA_A, lw=2.0, estilo="--")

    flecha(ax, 8.2, 2.6, 8.2, 8.0, color=COLOR_FLECHA_A, lw=2.0, estilo="--")
    flecha(ax, 8.2, 8.0, 12.5, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta=f"Retorno ~{T_AGUA_OUT:.1f} °C", offset_etiqueta=(0, 0.15))

    # -------------------------------------------------------------------------
    # Pérdidas desde tanque
    # -------------------------------------------------------------------------
    flecha(ax, 7.0, 6.3, 7.0, 6.6, color=COLOR_FLECHA_P, lw=2.0,
           estilo=":")
    ax.text(4.0, 6.9, "Pérdidas al ambiente", fontsize=9,
            ha="left", va="center", color=COLOR_FLECHA_P, fontweight="bold")

    # -------------------------------------------------------------------------
    # Título y notas
    # -------------------------------------------------------------------------
    ax.text(7.0, 9.2,
            "Diagrama de bloques — Fase de descarga",
            fontsize=15, fontweight="bold", ha="center", va="center",
            color=COLOR_TEXTO)
    ax.text(7.0, 8.7,
            f"Ciclo oficial: {FLUJO_DESCARGA/1000:.0f} ton/h durante {DURACION_DESCARGA:.1f} h | "
            f"descarga de {MASA_DESCARGA/1000:.0f} ton",
            fontsize=11, ha="center", va="center", color=COLOR_TEXTO,
            style="italic")

    nota = (
        "Nota: durante la descarga ingresa glucosa fría (55 °C) al mismo flujo con que se retira "
        "producto hacia el carro tanque. El calor neto de la chaqueta compensa pérdidas y limita "
        "la caída de temperatura del inventario."
    )
    ax.text(7.0, 0.20, nota, fontsize=8, ha="center", va="center",
            color=COLOR_TEXTO, style="italic")

    _leyenda(ax, loc="lower left", bbox_to_anchor=(0.02, 0.05), ncol=2)
    _guardar(fig, base_path)
    print(f"[OK] Diagrama de descarga guardado en:\n  {base_path}.png\n  {base_path}.pdf")


# =============================================================================
# 3. DIAGRAMA DE LA FASE DE CALENTAMIENTO
# =============================================================================
def generar_diagrama_calentamiento(output_dir="results/figures"):
    """Recuperación térmica entre descargas."""
    base_path = os.path.join(output_dir, "diagrama_bloques_calentamiento")
    fig, ax = _nueva_figura()

    # -------------------------------------------------------------------------
    # Bloques
    # -------------------------------------------------------------------------
    # Tanque central
    dibujar_bloque(ax, 4.8, 3.4, 4.4, 2.8,
                   etiqueta="Tag 53A-90A-0056",
                   subetiqueta=("Inventario de glucosa\n"
                                "Globe 1130, 80,6 °Brix\n"
                                "Sin entrada ni salida"),
                   color=COLOR_BLOQUE_PROCESO, fontsize=12)

    # Chaqueta debajo
    dibujar_bloque(ax, 5.5, 1.2, 3.0, 1.3,
                   etiqueta="Chaqueta E-201",
                   subetiqueta=f"A = {A_CHAQUETA:.0f} m² | Agua {T_AGUA_IN:.0f} °C",
                   color=COLOR_BLOQUE_SERVICIO)

    # Pérdidas arriba
    dibujar_bloque(ax, 5.1, 6.5, 3.8, 1.2,
                   etiqueta="Pérdidas térmicas",
                   subetiqueta=f"{Q_PERDIDAS:.1f} MJ/h",
                   color=COLOR_BLOQUE_PERDIDA)

    # Agua caliente arriba izquierda
    dibujar_bloque(ax, 0.6, 6.6, 2.8, 1.3,
                   etiqueta="Agua caliente",
                   subetiqueta=f"{Q_AGUA:.1f} m³/h\n{T_AGUA_IN:.0f} °C",
                   color=COLOR_BLOQUE_SERVICIO)

    # Agua retorno arriba derecha
    dibujar_bloque(ax, 10.6, 6.6, 2.8, 1.3,
                   etiqueta="Agua de retorno",
                   subetiqueta=f"{Q_AGUA:.1f} m³/h\n~{T_AGUA_OUT:.1f} °C",
                   color=COLOR_BLOQUE_SERVICIO)

    # Balance energético (derecha)
    dibujar_bloque(ax, 10.4, 2.0, 3.2, 2.2,
                   etiqueta="Recuperación térmica",
                   subetiqueta=(f"Tiempo: {TIEMPO_CALENTAMIENTO:.1f} h\n"
                                f"Aporte: {Q_CHAQUETA:.1f} MJ/h\n"
                                f"Pérdidas: {Q_PERDIDAS:.1f} MJ/h\n"
                                f"Neto al inventario: {Q_CHAQUETA - Q_PERDIDAS:.1f} MJ/h"),
                   color=COLOR_BLOQUE_INFO, fontsize=10)

    # -------------------------------------------------------------------------
    # Servicio
    # -------------------------------------------------------------------------
    flecha(ax, 3.4, 8.0, 5.5, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta="Agua caliente", offset_etiqueta=(0, 0.15))
    flecha(ax, 5.5, 8.0, 5.5, 2.5, color=COLOR_FLECHA_A, lw=2.0, estilo="--")

    flecha(ax, 8.2, 2.5, 8.2, 8.0, color=COLOR_FLECHA_A, lw=2.0, estilo="--")
    flecha(ax, 8.2, 8.0, 10.6, 8.0, color=COLOR_FLECHA_A, lw=2.0,
           etiqueta=f"Retorno ~{T_AGUA_OUT:.1f} °C", offset_etiqueta=(0, 0.15))

    # -------------------------------------------------------------------------
    # Pérdidas y recuperación
    # -------------------------------------------------------------------------
    flecha(ax, 7.0, 6.2, 7.0, 6.6, color=COLOR_FLECHA_P, lw=2.0,
           estilo=":")
    ax.text(4.0, 6.9, "Pérdidas al ambiente", fontsize=9,
            ha="left", va="center", color=COLOR_FLECHA_P, fontweight="bold")

    flecha(ax, 9.2, 4.5, 10.4, 4.2, color=COLOR_FLECHA_N, lw=2.0,
           etiqueta="Calor neto", offset_etiqueta=(0, 0.32))

    # -------------------------------------------------------------------------
    # Título y notas
    # -------------------------------------------------------------------------
    ax.text(7.0, 9.2,
            "Diagrama de bloques — Fase de calentamiento entre descargas",
            fontsize=15, fontweight="bold", ha="center", va="center",
            color=COLOR_TEXTO)
    ax.text(7.0, 8.7,
            f"Recuperación térmica durante {TIEMPO_CALENTAMIENTO:.1f} h | "
            f"ciclo {CICLO_DESCARGAS} descargas/día",
            fontsize=11, ha="center", va="center", color=COLOR_TEXTO,
            style="italic")

    nota = (
        "Nota: entre descargas no hay flujo de entrada ni salida de glucosa. "
        "La chaqueta aporta calor neto al inventario, compensando las pérdidas térmicas "
        "y recuperando parcialmente la temperatura antes del siguiente evento de despacho."
    )
    ax.text(7.0, 0.25, nota, fontsize=8, ha="center", va="center",
            color=COLOR_TEXTO, style="italic")

    _leyenda(ax, loc="lower left", bbox_to_anchor=(0.02, 0.05), ncol=2)
    _guardar(fig, base_path)
    print(f"[OK] Diagrama de calentamiento guardado en:\n  {base_path}.png\n  {base_path}.pdf")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
def main():
    output_dir = "results/figures"
    generar_diagrama_global(output_dir)
    generar_diagrama_descarga(output_dir)
    generar_diagrama_calentamiento(output_dir)


if __name__ == "__main__":
    main()
