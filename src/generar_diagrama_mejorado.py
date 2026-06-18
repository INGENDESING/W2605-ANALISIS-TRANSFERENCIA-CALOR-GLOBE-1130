"""
Generador de Diagrama de Proceso PFD - Proyecto W2605
Version 2.0 - Diagrama esquematico profesional con equipos realistas
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import (FancyBboxPatch, Circle, Ellipse, Arc, 
                                Polygon, Rectangle, FancyArrowPatch, PathPatch)
from matplotlib.path import Path
import sys
import os

sys.path.append(os.path.dirname(__file__))

from propiedades_glucosa import rho_glucosa, Cp_glucosa
from geometria_tanque import A_CONTACTO

# =============================================================================
# PARAMETROS DEL PROCESO - ESCENARIO 3 OPTIMIZADO
# =============================================================================
# Basado en cálculos del proyecto W2605 con agua a 75°C

M_GLUCOSA = 8000.0          # Flujo de glucosa [kg/h]
T_GLUCOSA_ENT = 57.0        # Temperatura entrada glucosa [°C]
PERDIDA_TEMP = 3.0          # Pérdida térmica estimada [°C]
Q_AGUA = 57.7               # Caudal agua optimizado [m³/h] (v=2.5 m/s)
T_AGUA_ENT = 75.0           # Temperatura agua optimizada [°C]
RHO_AGUA = 975.0            # Densidad agua a 75°C [kg/m³]
CP_AGUA = 4.192             # Cp agua [kJ/kg°C]
AREA_CHAQUETA = A_CONTACTO  # Área chaqueta [m²]
U_GLOBAL = 36.2             # Coeficiente global calculado [W/m²°C] @ 60°C
RHO_GLUCOSA = 1405.0        # Densidad glucosa [kg/m³]
CP_GLUCOSA = 2.131          # Cp glucosa [kJ/kg°C]
MU_GLUCOSA = 2870.0         # Viscosidad glucosa a 57°C [cP]
K_GLUCOSA = 0.38            # Conductividad térmica glucosa [W/m°C]
T_MIN_CARGA = 57.0          # Temperatura mínima para carga [°C]

# Colores profesionales ISA
COLOR_TANQUE = '#FFE4E1'
COLOR_TANQUE_BORDE = '#8B4513'
COLOR_CHAQUETA = '#87CEEB'
COLOR_BOMBA = '#DDA0DD'
COLOR_INTERCAMBIADOR = '#98FB98'
COLOR_LINEA_G = '#228B22'
COLOR_LINEA_A = '#1E90FF'
COLOR_PERDIDA = '#DC143C'
COLOR_TEXTO = '#2F4F4F'
COLOR_FONDO_CORRIENTE = '#F5F5F5'


def calcular_corrientes(t_entrada_glucosa):
    """Calcula todas las corrientes del proceso"""
    m_gluc = M_GLUCOSA
    t_gluc_ent = t_entrada_glucosa
    h_gluc_ent = m_gluc * CP_GLUCOSA * t_gluc_ent
    
    q_perdida = m_gluc * CP_GLUCOSA * PERDIDA_TEMP
    
    m_agua = Q_AGUA * RHO_AGUA
    h_agua_ent = m_agua * CP_AGUA * T_AGUA_ENT
    
    t_gluc_fria = t_entrada_glucosa - PERDIDA_TEMP
    dt1 = T_AGUA_ENT - t_gluc_fria
    dt2 = 5.0
    
    if dt1 <= 0:
        dt1 = 1.0
    if dt2 <= 0:
        dt2 = 0.5
    
    if abs(dt1 - dt2) < 0.1:
        lmtd = (dt1 + dt2) / 2
    else:
        lmtd = (dt1 - dt2) / np.log(dt1 / dt2)
    
    q_chaqueta_w = U_GLOBAL * AREA_CHAQUETA * lmtd
    q_chaqueta = q_chaqueta_w * 3.6
    
    h_gluc_sal = h_gluc_ent - q_perdida + q_chaqueta
    t_gluc_sal = h_gluc_sal / (m_gluc * CP_GLUCOSA)
    
    h_agua_sal = h_agua_ent - q_chaqueta
    t_agua_sal = h_agua_sal / (m_agua * CP_AGUA)
    
    return {
        't_gluc_ent': t_gluc_ent,
        't_gluc_sal': t_gluc_sal,
        'h_gluc_ent': h_gluc_ent,
        'h_gluc_sal': h_gluc_sal,
        'm_gluc': m_gluc,
        't_agua_ent': T_AGUA_ENT,
        't_agua_sal': t_agua_sal,
        'h_agua_ent': h_agua_ent,
        'h_agua_sal': h_agua_sal,
        'm_agua': m_agua,
        'q_perdida': q_perdida,
        'q_chaqueta': q_chaqueta,
        'lmtd': lmtd,
        'viable': t_gluc_sal >= T_MIN_CARGA
    }


def dibujar_tanque_realista(ax, x, y, width, height):
    """Dibuja un tanque vertical realista con fondo torisferico y tapa eliptica"""
    
    # Dimensiones
    w = width
    h_cuerpo = height * 0.70
    h_fondo = height * 0.18
    h_tapa = height * 0.12
    
    # === CUERPO CILINDRICO ===
    cuerpo = FancyBboxPatch((x, y + h_fondo), w, h_cuerpo,
                            boxstyle="round,pad=0.01",
                            facecolor=COLOR_TANQUE, 
                            edgecolor=COLOR_TANQUE_BORDE, 
                            linewidth=2.5, zorder=3)
    ax.add_patch(cuerpo)
    
    # Lineas verticales para efecto 3D
    ax.plot([x+0.02*w, x+0.02*w], [y+h_fondo, y+h_fondo+h_cuerpo], 
            'k-', linewidth=0.5, alpha=0.3, zorder=4)
    ax.plot([x+0.98*w, x+0.98*w], [y+h_fondo, y+h_fondo+h_cuerpo], 
            'k-', linewidth=0.5, alpha=0.3, zorder=4)
    
    # === FONDO TORISFERICO (curvado hacia abajo) ===
    # Crear arco inferior curvado
    theta = np.linspace(np.pi, 2*np.pi, 50)
    r_fondo = w / 2
    cx_fondo = x + w/2
    cy_fondo = y + h_fondo
    
    x_fondo = cx_fondo + r_fondo * np.cos(theta)
    y_fondo = cy_fondo + (h_fondo * 0.8) * np.sin(theta)
    
    fondo_path = np.column_stack([x_fondo, y_fondo])
    fondo_patch = Polygon(fondo_path, closed=True, facecolor=COLOR_TANQUE,
                         edgecolor=COLOR_TANQUE_BORDE, linewidth=2.5, zorder=3)
    ax.add_patch(fondo_patch)
    
    # Linea de fondo interior (curva)
    ax.plot(x_fondo, y_fondo, color=COLOR_TANQUE_BORDE, linewidth=2.5, zorder=4)
    
    # === TAPA ELIPTICA (curvada hacia arriba) ===
    theta_tapa = np.linspace(0, np.pi, 50)
    r_tapa = w / 2
    cx_tapa = x + w/2
    cy_tapa = y + h_fondo + h_cuerpo
    
    x_tapa = cx_tapa + r_tapa * np.cos(theta_tapa)
    y_tapa = cy_tapa + (h_tapa * 0.8) * np.sin(theta_tapa)
    
    tapa_path = np.column_stack([x_tapa, y_tapa])
    tapa_patch = Polygon(tapa_path, closed=True, facecolor=COLOR_TANQUE,
                        edgecolor=COLOR_TANQUE_BORDE, linewidth=2.5, zorder=3)
    ax.add_patch(tapa_patch)
    
    ax.plot(x_tapa, y_tapa, color=COLOR_TANQUE_BORDE, linewidth=2.5, zorder=4)
    
    # === AISLAMIENTO TERMICO (linea punteada exterior) ===
    offset = 0.08
    # Cuerpo
    ais_cuerpo = FancyBboxPatch((x-offset, y+h_fondo-offset), w+2*offset, h_cuerpo+2*offset,
                                boxstyle="round,pad=0.01", facecolor='none',
                                edgecolor='gray', linewidth=1.5, linestyle='--', 
                                alpha=0.6, zorder=2)
    ax.add_patch(ais_cuerpo)
    
    # Arco de fondo
    theta_ais = np.linspace(np.pi*1.05, 1.95*np.pi, 30)
    r_ais = w/2 + offset
    x_ais_f = cx_fondo + r_ais * np.cos(theta_ais)
    y_ais_f = cy_fondo + (h_fondo*0.8 + offset) * np.sin(theta_ais)
    ax.plot(x_ais_f, y_ais_f, 'gray', linewidth=1.5, linestyle='--', alpha=0.6, zorder=2)
    
    # Arco de tapa
    theta_ais_t = np.linspace(0.05*np.pi, 0.95*np.pi, 30)
    x_ais_t = cx_tapa + r_ais * np.cos(theta_ais_t)
    y_ais_t = cy_tapa + (h_tapa*0.8 + offset) * np.sin(theta_ais_t)
    ax.plot(x_ais_t, y_ais_t, 'gray', linewidth=1.5, linestyle='--', alpha=0.6, zorder=2)
    
    # Lineas verticales de aislamiento
    ax.plot([x-offset, x-offset], [y+h_fondo-offset, y+h_fondo+h_cuerpo+offset], 
            'gray', linewidth=1.5, linestyle='--', alpha=0.6, zorder=2)
    ax.plot([x+w+offset, x+w+offset], [y+h_fondo-offset, y+h_fondo+h_cuerpo+offset], 
            'gray', linewidth=1.5, linestyle='--', alpha=0.6, zorder=2)
    
    # === PATAS DE SOPORTE ===
    pata_w = w * 0.08
    pata_h = height * 0.08
    # Pata izquierda
    pata_i = Rectangle((x + w*0.15, y - pata_h), pata_w, pata_h,
                       facecolor='#696969', edgecolor='black', linewidth=1.5, zorder=1)
    ax.add_patch(pata_i)
    # Pata derecha
    pata_d = Rectangle((x + w*0.77, y - pata_h), pata_w, pata_h,
                       facecolor='#696969', edgecolor='black', linewidth=1.5, zorder=1)
    ax.add_patch(pata_d)
    
    # === INDICADOR DE NIVEL ===
    nivel_y = y + h_fondo + h_cuerpo * 0.20
    ax.plot([x, x+w], [nivel_y, nivel_y], 'b-', linewidth=2, alpha=0.7, zorder=5)
    # Linea ondulada para indicar liquido
    x_onda = np.linspace(x, x+w, 20)
    y_onda = nivel_y + 0.005 * np.sin(x_onda * 50)
    ax.plot(x_onda, y_onda, 'b-', linewidth=1.5, alpha=0.5, zorder=5)
    ax.text(x + w*1.05, nivel_y, 'Nivel: 80%', fontsize=9, color='blue', 
            va='center', fontweight='bold')
    
    # === ETIQUETAS DEL TANQUE ===
    ax.text(x + w/2, y + h_fondo + h_cuerpo*0.75, 'T-101', fontsize=14, 
            fontweight='bold', ha='center', color=COLOR_TEXTO)
    ax.text(x + w/2, y + h_fondo + h_cuerpo*0.60, 'Tanque de', fontsize=10, 
            ha='center', color=COLOR_TEXTO)
    ax.text(x + w/2, y + h_fondo + h_cuerpo*0.52, 'Almacenamiento', fontsize=10, 
            ha='center', color=COLOR_TEXTO)
    ax.text(x + w/2, y + h_fondo + h_cuerpo*0.38, 'Fondo Torisferico', fontsize=9, 
            ha='center', color=COLOR_TEXTO, style='italic')
    ax.text(x + w/2, y + h_fondo + h_cuerpo*0.28, 'Tapa Eliptica', fontsize=9, 
            ha='center', color=COLOR_TEXTO, style='italic')
    
    # Etiqueta aislamiento
    ax.text(x + w/2, y + h_fondo + h_cuerpo + h_tapa + 0.15, 
            'Aislamiento Termico', fontsize=8, ha='center', 
            color='gray', style='italic')
    
    return y + h_fondo  # Retorna posicion Y del fondo interior


def dibujar_bomba_centrifuga(ax, x, y, size):
    """Dibuja una bomba centrifuga estilo ISA"""
    # Circulo principal
    circle = Circle((x, y), size, facecolor=COLOR_BOMBA, 
                   edgecolor='black', linewidth=2, zorder=5)
    ax.add_patch(circle)
    
    # Triangulo interno (simbolo de bomba)
    triangle = Polygon([(x, y+size*0.6), (x-size*0.5, y-size*0.4), 
                       (x+size*0.5, y-size*0.4)], 
                      facecolor='white', edgecolor='black', 
                      linewidth=1.5, zorder=6)
    ax.add_patch(triangle)
    
    # Linea de eje
    ax.plot([x, x], [y-size*0.4, y-size*0.7], 'k-', linewidth=2, zorder=6)
    
    # Etiquetas
    ax.text(x, y+size*1.4, 'P-101', fontsize=11, fontweight='bold', 
            ha='center', color=COLOR_TEXTO)
    ax.text(x, y-size*1.2, 'Bomba', fontsize=9, ha='center', color=COLOR_TEXTO)
    ax.text(x, y-size*1.5, 'Centrifuga', fontsize=9, ha='center', color=COLOR_TEXTO)


def dibujar_chaqueta_serpentina(ax, x, y, width, height):
    """Dibuja una chaqueta de serpentina en el fondo del tanque"""
    # Rectangulo base
    chaqueta = FancyBboxPatch((x, y), width, height,
                              boxstyle="round,pad=0.02",
                              facecolor=COLOR_CHAQUETA,
                              edgecolor='black', linewidth=2, zorder=4)
    ax.add_patch(chaqueta)
    
    # Lineas de serpentina
    n_lineas = 5
    espaciado = height / (n_lineas + 1)
    for i in range(n_lineas):
        y_line = y + espaciado * (i + 1)
        # Linea horizontal con curvas
        if i % 2 == 0:
            # Izquierda a derecha
            ax.plot([x + width*0.1, x + width*0.9], [y_line, y_line], 
                   'b-', linewidth=1.5, alpha=0.7, zorder=5)
            if i < n_lineas - 1:
                # Curva de retorno
                theta = np.linspace(-np.pi/2, np.pi/2, 20)
                r = espaciado / 2
                cx = x + width*0.9
                cy = y_line + espaciado/2
                x_arc = cx + r * np.cos(theta)
                y_arc = cy + r * np.sin(theta)
                ax.plot(x_arc, y_arc, 'b-', linewidth=1.5, alpha=0.7, zorder=5)
        else:
            # Derecha a izquierda
            ax.plot([x + width*0.9, x + width*0.1], [y_line, y_line], 
                   'b-', linewidth=1.5, alpha=0.7, zorder=5)
            if i < n_lineas - 1:
                # Curva de retorno
                theta = np.linspace(np.pi/2, 3*np.pi/2, 20)
                r = espaciado / 2
                cx = x + width*0.1
                cy = y_line + espaciado/2
                x_arc = cx + r * np.cos(theta)
                y_arc = cy + r * np.sin(theta)
                ax.plot(x_arc, y_arc, 'b-', linewidth=1.5, alpha=0.7, zorder=5)
    
    # Etiquetas
    ax.text(x + width/2, y + height*1.3, 'E-201', fontsize=11, 
            fontweight='bold', ha='center', color=COLOR_TEXTO)
    ax.text(x + width/2, y + height*0.5, 'Chaqueta', fontsize=9, 
            ha='center', color=COLOR_TEXTO)
    ax.text(x + width/2, y + height*0.2, f'A = {AREA_CHAQUETA:.0f} m²', fontsize=9, 
            ha='center', color=COLOR_TEXTO)


def dibujar_carrotanque(ax, x, y, width, height):
    """Dibuja un carrotanque estilizado"""
    # Dimensiones
    cabina_w = width * 0.35
    tanque_w = width * 0.65
    
    # === CABINA ===
    cabina = FancyBboxPatch((x, y + height*0.3), cabina_w, height*0.6,
                            boxstyle="round,pad=0.02",
                            facecolor='#FFD700', edgecolor='black', 
                            linewidth=1.5, zorder=3)
    ax.add_patch(cabina)
    
    # Ventana
    ventana = Rectangle((x + cabina_w*0.2, y + height*0.6), 
                        cabina_w*0.5, height*0.2,
                        facecolor='#87CEEB', edgecolor='black', 
                        linewidth=1, zorder=4)
    ax.add_patch(ventana)
    
    # === TANQUE CILINDRICO ===
    tanque_x = x + cabina_w
    tanque = FancyBboxPatch((tanque_x, y), tanque_w, height,
                            boxstyle="round,pad=0.02",
                            facecolor='#C0C0C0', edgecolor='black',
                            linewidth=1.5, zorder=3)
    ax.add_patch(tanque)
    
    # Lineas del tanque (efecto cilindrico)
    for offset in [0.2, 0.5, 0.8]:
        ax.plot([tanque_x + tanque_w*offset, tanque_x + tanque_w*offset], 
               [y, y+height], 'k-', linewidth=0.5, alpha=0.3, zorder=4)
    
    # === RUEDAS ===
    r_rueda = height * 0.12
    # Rueda delantera
    rueda1 = Circle((x + cabina_w*0.5, y), r_rueda, 
                   facecolor='black', edgecolor='black', zorder=2)
    ax.add_patch(rueda1)
    # Ruedas traseras
    rueda2 = Circle((x + cabina_w + tanque_w*0.3, y), r_rueda,
                   facecolor='black', edgecolor='black', zorder=2)
    ax.add_patch(rueda2)
    rueda3 = Circle((x + cabina_w + tanque_w*0.7, y), r_rueda,
                   facecolor='black', edgecolor='black', zorder=2)
    ax.add_patch(rueda3)
    
    # Etiqueta
    ax.text(x + width/2, y + height*1.15, 'Carro Tanque', fontsize=9, 
            ha='center', fontweight='bold', color=COLOR_TEXTO)


def dibujar_intercambiador_entrada(ax, x, y, width, height):
    """Dibuja un intercambiador/entrada estilizado"""
    # Caja principal
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.05",
                         facecolor='#F0F0F0', edgecolor='black',
                         linewidth=2, zorder=3)
    ax.add_patch(box)
    
    # Simbolo de entrada
    # Flecha grande
    ax.annotate('', xy=(x + width*0.7, y + height/2), 
                xytext=(x + width*0.3, y + height/2),
                arrowprops=dict(arrowstyle='->', color='green', lw=3),
                zorder=4)
    
    # Etiquetas
    ax.text(x + width/2, y + height*0.75, 'E-101', fontsize=11,
            fontweight='bold', ha='center', color=COLOR_TEXTO)
    ax.text(x + width/2, y + height*0.4, 'Entrada', fontsize=9,
            ha='center', color=COLOR_TEXTO)
    ax.text(x + width/2, y + height*0.15, 'Glucosa', fontsize=9,
            ha='center', color=COLOR_TEXTO)


def dibujar_estacion_carga(ax, x, y, width, height):
    """Dibuja una estacion de carga"""
    # Plataforma base
    base = FancyBboxPatch((x, y), width, height*0.3,
                          boxstyle="round,pad=0.02",
                          facecolor='#D3D3D3', edgecolor='black',
                          linewidth=2, zorder=3)
    ax.add_patch(base)
    
    # Estructura vertical
    poste = Rectangle((x + width*0.45, y + height*0.3), 
                      width*0.1, height*0.5,
                      facecolor='#696969', edgecolor='black',
                      linewidth=1.5, zorder=3)
    ax.add_patch(poste)
    
    # Brazo de carga
    brazo = FancyBboxPatch((x + width*0.1, y + height*0.7),
                           width*0.8, height*0.1,
                           boxstyle="round,pad=0.02",
                           facecolor='#4682B4', edgecolor='black',
                           linewidth=1.5, zorder=4)
    ax.add_patch(brazo)
    
    # Etiquetas
    ax.text(x + width/2, y + height*1.05, 'E-102', fontsize=11,
            fontweight='bold', ha='center', color=COLOR_TEXTO)
    ax.text(x + width/2, y - height*0.1, 'Estacion de Carga', fontsize=9,
            ha='center', color=COLOR_TEXTO)


def dibujar_corriente_con_datos(ax, x1, y1, x2, y2, datos, color, 
                                offset_x=0, offset_y=0.4, es_entrada=True):
    """Dibuja una flecha de corriente con caja de datos"""
    # Flecha
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5),
                zorder=5)
    
    # Caja de datos
    bbox_props = dict(boxstyle='round,pad=0.4', facecolor=COLOR_FONDO_CORRIENTE,
                     edgecolor=color, linewidth=2, alpha=0.95)
    
    x_text = (x1 + x2) / 2 + offset_x
    y_text = (y1 + y2) / 2 + offset_y
    
    ax.text(x_text, y_text, datos, fontsize=8, ha='center', va='center',
            bbox=bbox_props, family='monospace', zorder=6)


def generar_diagrama_completo():
    """Genera el diagrama PFD completo con mejoras visuales"""
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(22, 16), dpi=200)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis('off')
    ax.set_facecolor('white')
    
    # Calcular corrientes
    corrientes = calcular_corrientes(57.0)
    
    # ============================================
    # DIBUJAR EQUIPOS
    # ============================================
    
    # 1. Entrada Glucosa E-101 (izquierda)
    dibujar_intercambiador_entrada(ax, 0.5, 7.5, 2.2, 1.5)
    
    # 2. Tanque T-101 (centro)
    tanque_x, tanque_y = 4.5, 6.0
    tanque_w, tanque_h = 3.5, 5.0
    fondo_y = dibujar_tanque_realista(ax, tanque_x, tanque_y, tanque_w, tanque_h)
    
    # 3. Chaqueta E-201 (debajo del tanque)
    chaqueta_h = 1.0
    chaqueta_y = tanque_y - chaqueta_h - 0.3
    dibujar_chaqueta_serpentina(ax, tanque_x + 0.3, chaqueta_y, 
                                tanque_w - 0.6, chaqueta_h)
    
    # 4. Bomba P-101 (derecha del tanque)
    bomba_x = tanque_x + tanque_w + 3.5
    bomba_y = tanque_y + tanque_h/2
    dibujar_bomba_centrifuga(ax, bomba_x, bomba_y, 0.7)
    
    # 5. Estacion de carga E-102
    est_x = bomba_x + 2.5
    est_y = bomba_y - 0.5
    dibujar_estacion_carga(ax, est_x, est_y, 2.0, 1.5)
    
    # 6. Carrotanque
    carro_x = est_x + 3.0
    carro_y = est_y - 0.3
    dibujar_carrotanque(ax, carro_x, carro_y, 3.0, 1.5)
    
    # ============================================
    # CORRIENTES DE GLUCOSA
    # ============================================
    
    # Corriente 1: Entrada -> Tanque
    datos1 = f"1: GLUCOSA ENTRADA\n" \
             f"├─ Flujo: {corrientes['m_gluc']:.0f} kg/h\n" \
             f"├─ Temperatura: {corrientes['t_gluc_ent']:.1f}°C\n" \
             f"├─ Entalpia: {corrientes['h_gluc_ent']/1000:.1f} MJ/h\n" \
             f"├─ Cp: {CP_GLUCOSA:.3f} kJ/kg°C\n" \
             f"├─ Densidad: {RHO_GLUCOSA:.0f} kg/m³\n" \
             f"└─ Viscosidad: {MU_GLUCOSA:.0f} cP"
    
    dibujar_corriente_con_datos(ax, 2.7, 8.25, 4.5, 8.25, datos1, 
                                COLOR_LINEA_G, offset_x=0, offset_y=1.2)
    
    # Corriente 4: Tanque -> Bomba
    datos4 = f"4: GLUCOSA SALIDA\n" \
             f"├─ Flujo: {corrientes['m_gluc']:.0f} kg/h\n" \
             f"├─ Temperatura: {corrientes['t_gluc_sal']:.1f}°C\n" \
             f"├─ Entalpia: {corrientes['h_gluc_sal']/1000:.1f} MJ/h\n" \
             f"├─ Cp: {CP_GLUCOSA:.3f} kJ/kg°C\n" \
             f"├─ Densidad: {RHO_GLUCOSA:.0f} kg/m³\n" \
             f"└─ Viscosidad: {MU_GLUCOSA:.0f} cP"
    
    color_salida = '#C8E6C9' if corrientes['viable'] else '#FFCDD2'
    dibujar_corriente_con_datos(ax, 8.0, 8.5, bomba_x-0.7, bomba_y+0.5, datos4,
                                COLOR_LINEA_G, offset_x=0.5, offset_y=1.0)
    
    # Corriente 5: Bomba -> Estacion -> Carrotanque
    ax.annotate('', xy=(est_x, est_y+0.75), xytext=(bomba_x+0.7, bomba_y),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=2.5), zorder=5)
    ax.annotate('', xy=(carro_x, carro_y+0.75), xytext=(est_x+2.0, est_y+0.75),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=2.5), zorder=5)
    
    # Flecha de continuidad
    ax.text((bomba_x+0.7+est_x)/2, bomba_y+0.3, '5: A Carrotanque', 
            fontsize=9, ha='center', color=COLOR_LINEA_G, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor=COLOR_LINEA_G, linewidth=1.5))
    
    # ============================================
    # SERVICIOS - AGUA
    # ============================================
    
    # Entrada de agua (desde arriba-izquierda)
    ax.plot([1.5, 1.5, tanque_x+0.5], [14, chaqueta_y+chaqueta_h, chaqueta_y+chaqueta_h],
            color=COLOR_LINEA_A, linewidth=2.5, linestyle='--', zorder=4)
    ax.annotate('', xy=(tanque_x+0.5, chaqueta_y+chaqueta_h), xytext=(tanque_x, chaqueta_y+chaqueta_h),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_A, lw=2.5, linestyle='--'), zorder=5)
    
    # Datos agua entrada
    datos_agua_ent = f"2: AGUA ENTRADA\n" \
                     f"├─ Flujo: {Q_AGUA:.1f} m³/h\n" \
                     f"├─ Flujo: {corrientes['m_agua']:.0f} kg/h\n" \
                     f"├─ Temperatura: {corrientes['t_agua_ent']:.1f}°C\n" \
                     f"├─ Entalpia: {corrientes['h_agua_ent']/1000000:.2f} GJ/h\n" \
                     f"├─ Cp: {CP_AGUA:.3f} kJ/kg°C\n" \
                     f"└─ Densidad: {RHO_AGUA:.0f} kg/m³"
    
    ax.text(1.5, 14.8, datos_agua_ent, fontsize=8, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD',
                     edgecolor=COLOR_LINEA_A, linewidth=2),
            family='monospace', zorder=6)
    
    # Salida de agua (hacia abajo-derecha)
    ax.plot([tanque_x+tanque_w-0.5, tanque_x+tanque_w+1.5, tanque_x+tanque_w+1.5],
            [chaqueta_y, chaqueta_y, chaqueta_y-1.5],
            color=COLOR_LINEA_A, linewidth=2.5, linestyle='--', zorder=4)
    ax.annotate('', xy=(tanque_x+tanque_w+1.5, chaqueta_y-1.5),
                xytext=(tanque_x+tanque_w+1.5, chaqueta_y-0.8),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_A, lw=2.5, linestyle='--'), zorder=5)
    
    # Datos agua salida
    datos_agua_sal = f"3: AGUA SALIDA\n" \
                     f"├─ Flujo: {corrientes['m_agua']:.0f} kg/h\n" \
                     f"├─ Temperatura: {corrientes['t_agua_sal']:.1f}°C\n" \
                     f"└─ Entalpia: {corrientes['h_agua_sal']/1000000:.2f} GJ/h"
    
    ax.text(tanque_x+tanque_w+1.5, chaqueta_y-2.2, datos_agua_sal, fontsize=8,
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD',
                     edgecolor=COLOR_LINEA_A, linewidth=2),
            family='monospace', zorder=6)
    
    # ============================================
    # FLUJOS DE ENERGIA
    # ============================================
    
    # Q Perdidas (flecha roja discontinua hacia arriba desde el tanque)
    ax.annotate('', xy=(tanque_x+tanque_w/2, 14.5), 
                xytext=(tanque_x+tanque_w/2, tanque_y+tanque_h+0.3),
                arrowprops=dict(arrowstyle='->', color=COLOR_PERDIDA, 
                               lw=3, linestyle=':', connectionstyle='arc3,rad=0.1'),
                zorder=7)
    
    qper_mj = corrientes['q_perdida'] / 1000
    ax.text(tanque_x+tanque_w/2+1.5, 13.5, 
            f'Q PERDIDAS\n{qper_mj:.1f} MJ/h\n({PERDIDA_TEMP:.0f}°C)', 
            fontsize=10, color=COLOR_PERDIDA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFEBEE', 
                     edgecolor=COLOR_PERDIDA, linewidth=2), zorder=8)
    
    # Q Chaqueta (etiqueta cerca de la chaqueta)
    qcha_mj = corrientes['q_chaqueta'] / 1000
    ax.text(tanque_x+tanque_w/2, chaqueta_y-0.6, 
            f'Q CHAQUETA: {qcha_mj:.1f} MJ/h\nU={U_GLOBAL:.0f} W/m²K, A={AREA_CHAQUETA:.0f} m²',
            fontsize=9, color='blue', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E3F2FD',
                     edgecolor='blue', linewidth=1.5), zorder=6)
    
    # ============================================
    # TITULO Y ENCABEZADO
    # ============================================
    
    # Titulo principal con fondo
    titulo_bg = FancyBboxPatch((2, 15.2), 18, 0.7,
                               boxstyle="round,pad=0.05",
                               facecolor='#1E3A5F', edgecolor='black',
                               linewidth=2, zorder=1)
    ax.add_patch(titulo_bg)
    
    ax.text(11, 15.55, 'PROYECTO W2605 - DIAGRAMA DE FLUJO DE PROCESO (PFD)', 
            fontsize=16, fontweight='bold', ha='center', color='white', zorder=2)
    ax.text(11, 15.0, 'Sistema de Almacenamiento y Carga de Glucosa Globe 1130', 
            fontsize=12, ha='center', color='#1E3A5F', style='italic', zorder=2)
    
    # ============================================
    # CAJA DE INFORMACION DEL SISTEMA
    # ============================================
    
    info_text = f'''CONFIGURACION DEL SISTEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Tanque: Fondo Torisférico ASME F&D + Tapa Elíptica API 650
• Aislamiento: Lana Mineral (especificado sin espesor)
• Chaqueta: Media cana rectangular, Área = {AREA_CHAQUETA:.0f} m²
• Condición Mínima para Carga: Temperatura ≥ {T_MIN_CARGA:.0f}°C'''
    
    ax.text(11, 0.8, info_text, fontsize=9, ha='center', va='top',
            family='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8DC', 
                     edgecolor='#8B7355', linewidth=2), zorder=6)
    
    # ============================================
    # INDICADOR DE VIABILIDAD
    # ============================================
    
    if corrientes['viable']:
        estado_texto = '✓ CONDICIÓN ACEPTABLE'
        estado_color = 'green'
        bg_color = '#E8F5E9'
    else:
        diff = corrientes['t_gluc_sal'] - T_MIN_CARGA
        estado_texto = f'✗ NO CUMPLE:\nT salida {diff:.1f}°C bajo mínimo'
        estado_color = 'red'
        bg_color = '#FFEBEE'
    
    viabilidad_box = FancyBboxPatch((est_x-0.3, est_y-1.2), 2.6, 0.8,
                                    boxstyle="round,pad=0.1",
                                    facecolor=bg_color, edgecolor=estado_color,
                                    linewidth=3, zorder=7)
    ax.add_patch(viabilidad_box)
    ax.text(est_x+1.0, est_y-0.8, estado_texto, fontsize=11, fontweight='bold',
            color=estado_color, ha='center', va='center', zorder=8)
    
    # ============================================
    # LEYENDA
    # ============================================
    
    leyenda_x = 18.5
    leyenda_y = 12
    
    ax.text(leyenda_x, leyenda_y+1.5, 'LEYENDA', fontsize=11, 
            fontweight='bold', color=COLOR_TEXTO)
    
    # Lineas de corriente
    ax.plot([leyenda_x, leyenda_x+0.5], [leyenda_y+1.0, leyenda_y+1.0], 
            color=COLOR_LINEA_G, lw=2.5)
    ax.text(leyenda_x+0.7, leyenda_y+1.0, 'Glucosa', fontsize=9, va='center')
    
    ax.plot([leyenda_x, leyenda_x+0.5], [leyenda_y+0.6, leyenda_y+0.6],
            color=COLOR_LINEA_A, lw=2, linestyle='--')
    ax.text(leyenda_x+0.7, leyenda_y+0.6, 'Agua', fontsize=9, va='center')
    
    ax.plot([leyenda_x, leyenda_x+0.5], [leyenda_y+0.2, leyenda_y+0.2],
            color=COLOR_PERDIDA, lw=2, linestyle=':')
    ax.text(leyenda_x+0.7, leyenda_y+0.2, 'Perdidas', fontsize=9, va='center')
    
    # Guardar figura
    os.makedirs('../results', exist_ok=True)
    plt.tight_layout()
    plt.savefig('../results/diagrama_proceso_W2605_v2.png', dpi=200, 
                bbox_inches='tight', facecolor='white', pad_inches=0.3)
    plt.savefig('../results/diagrama_proceso_W2605_v2.pdf', dpi=300,
                bbox_inches='tight', facecolor='white', pad_inches=0.3)
    plt.close()
    
    return '../results/diagrama_proceso_W2605_v2.png'


if __name__ == "__main__":
    print("=" * 78)
    print("GENERADOR DE DIAGRAMA PFD v2.0 - PROYECTO W2605")
    print("Diagrama esquematico con equipos realistas")
    print("=" * 78)
    
    print("\nGenerando diagrama mejorado...")
    output_path = generar_diagrama_completo()
    print(f"Guardado: {output_path}")
    print(f"Guardado: {output_path.replace('.png', '.pdf')}")
    
    print("\nCaracteristicas mejoradas:")
    print("  • Tanque con fondo torisferico y tapa eliptica realistas")
    print("  • Representacion 3D con aislamiento exterior")
    print("  • Bomba centrifuga con simbolo ISA")
    print("  • Chaqueta con serpentina visible")
    print("  • Carrotanque estilizado con cabina")
    print("  • Layout organizado y profesional")
    print("  • Tipografia monospace para datos tecnicos")
    print("=" * 78)
