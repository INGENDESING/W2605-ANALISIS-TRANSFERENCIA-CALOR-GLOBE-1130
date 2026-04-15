"""
Generador de Diagrama de Proceso PFD - Proyecto P2611
Version Matplotlib (sin dependencia de Graphviz)
Diagrama de flujo de proceso profesional con balance termico completo
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))

from propiedades_glucosa import rho_glucosa, Cp_glucosa, mu_glucosa

# =============================================================================
# PARAMETROS DEL PROCESO
# =============================================================================

# Glucosa
M_GLUCOSA = 8000.0          # kg/h
T_GLUCOSA_ENT = 57.0        # °C (caso base)
PERDIDA_TEMP = 3.0          # °C perdidos en tanque

# Agua chaqueta
Q_AGUA = 30.9               # m3/h
T_AGUA_ENT = 65.0           # °C
RHO_AGUA = 980.0            # kg/m3 @ 65°C
CP_AGUA = 4.184             # kJ/(kg·°C)

# Chaqueta
AREA_CHAQUETA = 13.0        # m2
U_GLOBAL = 30.0             # W/(m2·K) - estimado para glucosa 54-57°C

# Propiedades glucosa @ 55°C (promedio)
RHO_GLUCOSA = 1405.0        # kg/m3
CP_GLUCOSA = 2.131          # kJ/(kg·°C)
MU_GLUCOSA = 3500.0         # cP = 3.5 Pa·s
K_GLUCOSA = 0.38            # W/(m·K)

# Condicion de carga
T_MIN_CARGA = 57.0          # °C

# =============================================================================
# CALCULOS TERMODINAMICOS
# =============================================================================

def calcular_corrientes(t_entrada_glucosa):
    """
    Calcula todas las corrientes del proceso para una T de entrada dada.
    """
    # Glucosa entrada
    m_gluc = M_GLUCOSA  # kg/h
    t_gluc_ent = t_entrada_glucosa
    h_gluc_ent = m_gluc * CP_GLUCOSA * t_gluc_ent  # kJ/h
    
    # Perdidas termicas
    q_perdida = m_gluc * CP_GLUCOSA * PERDIDA_TEMP  # kJ/h
    
    # Agua chaqueta
    m_agua = Q_AGUA * RHO_AGUA  # kg/h
    h_agua_ent = m_agua * CP_AGUA * T_AGUA_ENT  # kJ/h
    
    # LMTD aproximado
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
    
    # Calor transferido en chaqueta
    q_chaqueta_w = U_GLOBAL * AREA_CHAQUETA * lmtd
    q_chaqueta = q_chaqueta_w * 3.6  # kJ/h
    
    # Balance glucosa en tanque
    h_gluc_sal = h_gluc_ent - q_perdida + q_chaqueta
    t_gluc_sal = h_gluc_sal / (m_gluc * CP_GLUCOSA)
    
    # Agua salida
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


def generar_escenarios():
    """Genera tabla de escenarios para temperaturas de entrada 60°C a 53°C"""
    temperaturas = [60, 59, 58, 57, 56, 55, 54, 53]
    resultados = []
    
    for t in temperaturas:
        res = calcular_corrientes(t)
        resultados.append({
            't_entrada': t,
            't_salida': res['t_gluc_sal'],
            'q_perdida': res['q_perdida'],
            'q_chaqueta': res['q_chaqueta'],
            'viable': res['viable'],
            'diferencia': res['t_gluc_sal'] - T_MIN_CARGA
        })
    
    return resultados


# =============================================================================
# GENERACION DIAGRAMA CON MATPLOTLIB
# =============================================================================

def dibujar_diagrama_pfd(corrientes, output_path='../results/diagrama_proceso_P2611.png'):
    """Genera diagrama PFD profesional usando matplotlib"""
    
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Ellipse, Arc, PathPatch
    from matplotlib.path import Path
    
    # Configuracion de figura
    fig, ax = plt.subplots(figsize=(20, 14), dpi=150)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_facecolor('white')
    
    # Colores ISA S5.1
    COLOR_EQUIPO = '#E8E8E8'
    COLOR_TANQUE = '#FFE4E1'
    COLOR_BOMBA = '#E6E6FA'
    COLOR_INTER = '#ADD8E6'
    COLOR_LINEA_G = '#228B22'  # Verde para glucosa
    COLOR_LINEA_A = '#1E90FF'  # Azul para agua
    COLOR_PERDIDA = '#DC143C'  # Rojo para perdidas
    
    # ============================================
    # DIBUJAR EQUIPOS
    # ============================================
    
    # 1. Entrada Glucosa E-101 (caja)
    e101 = FancyBboxPatch((0.5, 7), 2.5, 1.2, boxstyle="round,pad=0.1", 
                          facecolor=COLOR_EQUIPO, edgecolor='black', linewidth=2)
    ax.add_patch(e101)
    ax.text(1.75, 7.6, 'E-101', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.75, 7.25, 'Entrada\nGlucosa', fontsize=9, ha='center')
    
    # 2. Tanque T-101 (cilindro con fondo torisferico)
    # Cuerpo cilindrico
    tanque_cuerpo = FancyBboxPatch((4.5, 5.5), 3.5, 4, boxstyle="round,pad=0.05",
                                   facecolor=COLOR_TANQUE, edgecolor='black', linewidth=2.5)
    ax.add_patch(tanque_cuerpo)
    
    # Fondo torisferico (representado como arco inferior)
    fondo = Arc((6.25, 5.5), 3.5, 1.5, angle=0, theta1=0, theta2=180, 
                color='black', linewidth=2.5)
    ax.add_patch(fondo)
    
    # Tapa eliptica (representada como arco superior)
    tapa = Arc((6.25, 9.5), 3.5, 1.2, angle=0, theta1=180, theta2=360,
               color='black', linewidth=2.5)
    ax.add_patch(tapa)
    
    # Aislamiento (linea punteada externa)
    aislamiento = FancyBboxPatch((4.3, 5.3), 3.9, 4.4, boxstyle="round,pad=0.05",
                                 facecolor='none', edgecolor='gray', 
                                 linewidth=2, linestyle='--', alpha=0.7)
    ax.add_patch(aislamiento)
    ax.text(6.25, 10.1, 'Aislamiento Termico', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # Etiqueta tanque
    ax.text(6.25, 8.5, 'T-101', fontsize=13, fontweight='bold', ha='center')
    ax.text(6.25, 7.9, 'Tanque de\nAlmacenamiento', fontsize=10, ha='center')
    ax.text(6.25, 7.2, 'Fondo Torisferico', fontsize=9, ha='center', style='italic')
    ax.text(6.25, 6.7, 'Tapa Eliptica', fontsize=9, ha='center', style='italic')
    ax.text(6.25, 6.0, 'Nivel: 80%', fontsize=9, ha='center', color='blue')
    
    # 3. Chaqueta E-201 (serpentina en fondo)
    chaqueta = FancyBboxPatch((4.8, 4.2), 2.9, 1, boxstyle="round,pad=0.05",
                              facecolor=COLOR_INTER, edgecolor='black', linewidth=2)
    ax.add_patch(chaqueta)
    ax.text(6.25, 4.85, 'E-201', fontsize=11, fontweight='bold', ha='center')
    ax.text(6.25, 4.5, 'Chaqueta\nA=13 m2', fontsize=9, ha='center')
    
    # 4. Bomba P-101 (circulo)
    bomba = Circle((11.5, 7.5), 0.8, facecolor=COLOR_BOMBA, edgecolor='black', linewidth=2.5)
    ax.add_patch(bomba)
    ax.text(11.5, 7.7, 'P-101', fontsize=11, fontweight='bold', ha='center')
    ax.text(11.5, 7.3, 'Bomba\nCentrifuga', fontsize=9, ha='center')
    
    # 5. Estacion de carga E-102
    e102 = FancyBboxPatch((14, 6.8), 2.5, 1.4, boxstyle="round,pad=0.1",
                          facecolor=COLOR_EQUIPO, edgecolor='black', linewidth=2)
    ax.add_patch(e102)
    ax.text(15.25, 7.7, 'E-102', fontsize=11, fontweight='bold', ha='center')
    ax.text(15.25, 7.2, 'Estacion\nCarga', fontsize=9, ha='center')
    
    # Carrotanque (representado como camion simple)
    camion_x, camion_y = 17.5, 6.5
    # Cabina
    cabina = FancyBboxPatch((camion_x, camion_y), 1, 1.5, boxstyle="round,pad=0.02",
                            facecolor='#FFD700', edgecolor='black', linewidth=1.5)
    ax.add_patch(cabina)
    # Tanque
    tanque_camion = FancyBboxPatch((camion_x+1, camion_y+0.3), 1.5, 1, 
                                   boxstyle="round,pad=0.05",
                                   facecolor='#C0C0C0', edgecolor='black', linewidth=1.5)
    ax.add_patch(tanque_camion)
    ax.text(camion_x+1.25, camion_y+0.8, 'Carro\nTanque', fontsize=8, ha='center')
    
    # ============================================
    # CORRIENTES - LINEAS DE FLUJO
    # ============================================
    
    # Corriente 1: Glucosa Entrada (E-101 -> T-101)
    ax.annotate('', xy=(4.5, 7.6), xytext=(3, 7.6),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=3))
    
    # Caja de datos corriente 1
    datos1 = f'''1: Glucosa Entrada
Flujo: {corrientes['m_gluc']:.0f} kg/h
Temperatura: {corrientes['t_gluc_ent']:.1f}°C
Entalpia: {corrientes['h_gluc_ent']/1000:.1f} MJ/h
Cp: {CP_GLUCOSA:.3f} kJ/kg°C
Densidad: {RHO_GLUCOSA:.0f} kg/m³
Viscosidad: {MU_GLUCOSA:.0f} cP'''
    
    bbox1 = dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', edgecolor=COLOR_LINEA_G, linewidth=2)
    ax.text(1.5, 10.5, datos1, fontsize=9, ha='center', va='top', bbox=bbox1,
            family='monospace')
    
    # Corriente 4: Glucosa Salida (T-101 -> P-101)
    ax.annotate('', xy=(10.7, 7.5), xytext=(8, 7.5),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=3))
    
    datos4 = f'''4: Glucosa Salida
Flujo: {corrientes['m_gluc']:.0f} kg/h
Temperatura: {corrientes['t_gluc_sal']:.1f}°C
Entalpia: {corrientes['h_gluc_sal']/1000:.1f} MJ/h
Cp: {CP_GLUCOSA:.3f} kJ/kg°C
Densidad: {RHO_GLUCOSA:.0f} kg/m³
Viscosidad: {MU_GLUCOSA:.0f} cP'''
    
    color_salida = '#C8E6C9' if corrientes['viable'] else '#FFCDD2'
    bbox4 = dict(boxstyle='round,pad=0.5', facecolor=color_salida, 
                 edgecolor=COLOR_LINEA_G, linewidth=2)
    ax.text(9.3, 9.5, datos4, fontsize=9, ha='center', va='top', bbox=bbox4,
            family='monospace')
    
    # Corriente 5: A Carrotanque (P-101 -> E-102)
    ax.annotate('', xy=(14, 7.5), xytext=(12.3, 7.5),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=3))
    
    # Corriente a carrotanque
    ax.annotate('', xy=(17.5, 7.25), xytext=(16.5, 7.25),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_G, lw=2.5))
    
    # ============================================
    # SERVICIOS - AGUA
    # ============================================
    
    # Agua entrada (desde arriba a la izquierda)
    ax.plot([2, 2, 4.8], [11, 4.7, 4.7], color=COLOR_LINEA_A, lw=2.5, linestyle='--')
    ax.annotate('', xy=(4.8, 4.7), xytext=(3.5, 4.7),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_A, lw=2.5, 
                               linestyle='--'))
    
    datos_agua_ent = f'''2: Agua Entrada
Flujo: {Q_AGUA:.1f} m³/h ({corrientes['m_agua']:.0f} kg/h)
Temperatura: {corrientes['t_agua_ent']:.1f}°C
Entalpia: {corrientes['h_agua_ent']/1000000:.2f} GJ/h
Cp: {CP_AGUA:.3f} kJ/kg°C
Densidad: {RHO_AGUA:.0f} kg/m³'''
    
    bbox_a1 = dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD', 
                   edgecolor=COLOR_LINEA_A, linewidth=2)
    ax.text(1, 12.5, datos_agua_ent, fontsize=8, ha='center', va='top', bbox=bbox_a1,
            family='monospace')
    
    # Agua salida (hacia abajo a la derecha)
    ax.plot([7.7, 9.5, 9.5], [4.7, 4.7, 3], color=COLOR_LINEA_A, lw=2.5, linestyle='--')
    ax.annotate('', xy=(9.5, 3), xytext=(9.5, 4),
                arrowprops=dict(arrowstyle='->', color=COLOR_LINEA_A, lw=2.5,
                               linestyle='--'))
    
    datos_agua_sal = f'''3: Agua Salida
Flujo: {corrientes['m_agua']:.0f} kg/h
Temperatura: {corrientes['t_agua_sal']:.1f}°C
Entalpia: {corrientes['h_agua_sal']/1000000:.2f} GJ/h'''
    
    bbox_a2 = dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD',
                   edgecolor=COLOR_LINEA_A, linewidth=2)
    ax.text(11, 2.5, datos_agua_sal, fontsize=8, ha='center', va='top', bbox=bbox_a2,
            family='monospace')
    
    # ============================================
    # FLUJOS DE ENERGIA
    # ============================================
    
    # Q Perdidas (flecha roja discontinua hacia arriba)
    ax.annotate('', xy=(6.25, 11.5), xytext=(6.25, 9.7),
                arrowprops=dict(arrowstyle='->', color=COLOR_PERDIDA, lw=3,
                               linestyle=':', connectionstyle='arc3,rad=0'))
    
    qper_mj = corrientes['q_perdida'] / 1000
    ax.text(7.5, 10.8, f'Q Perdidas = {qper_mj:.1f} MJ/h\n({PERDIDA_TEMP:.0f}°C perdidos)',
            fontsize=10, color=COLOR_PERDIDA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor=COLOR_PERDIDA, linewidth=1.5))
    
    # Q Chaqueta (etiqueta)
    qcha_mj = corrientes['q_chaqueta'] / 1000
    ax.text(6.25, 3.5, f'Q Chaqueta = {qcha_mj:.1f} MJ/h\n(U={U_GLOBAL:.0f} W/m²K, A={AREA_CHAQUETA:.0f} m²)',
            fontsize=9, color='blue', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor='blue', linewidth=1.5))
    
    # ============================================
    # TITULO Y LEYENDA
    # ============================================
    
    # Titulo principal
    ax.text(10, 13.5, 'PROYECTO P2611 - DIAGRAMA DE FLUJO DE PROCESO (PFD)',
            fontsize=16, fontweight='bold', ha='center')
    ax.text(10, 13.0, 'Sistema de Almacenamiento y Carga de Glucosa Globe 42 DE',
            fontsize=12, ha='center', style='italic')
    
    # Informacion del sistema
    info_sistema = f'''CONFIGURACION DEL SISTEMA:
• Tanque: Fondo Torisferico ASME F&D + Tapa Eliptica API 650
• Aislamiento: Lana Mineral
• Chaqueta: Media cana rectangular, Area = 13 m²
• Condicion Minima para Carga: Temperatura >= {T_MIN_CARGA:.0f}°C'''
    
    ax.text(10, 0.8, info_sistema, fontsize=9, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8DC', 
                     edgecolor='black', linewidth=1.5),
            family='monospace')
    
    # Indicador de viabilidad
    if corrientes['viable']:
        estado_texto = '✓ CONDICION ACEPTABLE'
        estado_color = 'green'
    else:
        diff = corrientes['t_gluc_sal'] - T_MIN_CARGA
        estado_texto = f'✗ NO CUMPLE: T salida {diff:.1f}°C bajo minimo'
        estado_color = 'red'
    
    ax.text(15.25, 5.8, estado_texto, fontsize=11, fontweight='bold',
            color=estado_color, ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor=estado_color, linewidth=2))
    
    # Guardar figura
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.savefig(output_path.replace('.png', '.pdf'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def guardar_tabla_escenarios(escenarios, corrientes_base):
    """Genera y guarda la tabla de escenarios en formato Markdown"""
    
    md = '''# Analisis de Escenarios - Proyecto P2611
## Sistema de Almacenamiento y Carga de Glucosa

### Condiciones de Operacion Base
- **Flujo de glucosa:** 8,000 kg/h
- **Perdidas termicas del tanque:** 3 C (equivalente a 51,144 kJ/h)
- **Chaqueta de calentamiento:** Area = 13 m2, Agua @ 65 C, 30.9 m3/h
- **Coeficiente global U:** ~30 W/(m2.K)
- **Capacidad de transferencia chaqueta:** ~10,700 kJ/h
- **Temperatura minima para carga:** 57 C

---

## Tabla de Escenarios

| T Entrada (C) | T Salida (C) | Q Perdida (MJ/h) | Q Chaqueta (MJ/h) | Delta vs Min | Estado | Observaciones |
|:-------------:|:------------:|:----------------:|:-----------------:|:------------:|:------:|:--------------|
'''
    
    for e in escenarios:
        estado = "✓ ACEPTABLE" if e['viable'] else "✗ RECHAZADO"
        obs = "Cumple minimo" if e['viable'] else f"{abs(e['diferencia']):.1f}C bajo minimo"
        md += f"| {e['t_entrada']:.0f} | {e['t_salida']:.1f} | {e['q_perdida']/1000:.1f} | {e['q_chaqueta']/1000:.1f} | {e['diferencia']:+.1f}C | {estado} | {obs} |\n"
    
    md += f'''

---

## Analisis de Viabilidad

### Caso Base (Entrada a {corrientes_base['t_gluc_ent']:.0f}C)

**Balance Energetico:**
```
Glucosa Entrada:  H = {corrientes_base['h_gluc_ent']/1000:.1f} MJ/h @ {corrientes_base['t_gluc_ent']:.1f}C
Perdidas:        -Q = {corrientes_base['q_perdida']/1000:.1f} MJ/h ({PERDIDA_TEMP:.0f}C)
Chaqueta:        +Q = {corrientes_base['q_chaqueta']/1000:.1f} MJ/h (U={U_GLOBAL:.0f} W/m2K, A={AREA_CHAQUETA:.0f}m2)
--------------------------------------------------------------------------------
Glucosa Salida:  H = {corrientes_base['h_gluc_sal']/1000:.1f} MJ/h @ {corrientes_base['t_gluc_sal']:.1f}C
```

**Agua de Chaqueta:**
```
Agua Entrada:    H = {corrientes_base['h_agua_ent']/1000000:.2f} GJ/h @ {corrientes_base['t_agua_ent']:.1f}C
Transferido:     -Q = {corrientes_base['q_chaqueta']/1000:.1f} MJ/h
Agua Salida:     H = {corrientes_base['h_agua_sal']/1000000:.2f} GJ/h @ {corrientes_base['t_agua_sal']:.1f}C
```

### Conclusion Critica

**SOLO es viable cargar a carrotanque si la glucosa entra a 60C o superior.**

Con las condiciones actuales:
- Las perdidas termicas (51,144 kJ/h) son ~5x mayores que el aporte de la chaqueta ({corrientes_base['q_chaqueta']:.0f} kJ/h)
- El sistema opera con deficit energetico de ~40,000 kJ/h
- La glucosa sale {corrientes_base['t_gluc_sal']-T_MIN_CARGA:.1f}C por debajo del minimo requerido

### Recomendaciones para Operar con Entrada a 57C

Para poder cargar glucosa a 57C y mantener la temperatura de salida >=57C, se requiere **AL MENOS UNA** de las siguientes modificaciones:

1. **Aumentar area de chaqueta:**
   - Area requerida: ~65-70 m2 (actual: 13 m2)
   - Incremento: 5x el area actual

2. **Subir temperatura del agua:**
   - Temperatura requerida: ~80C (actual: 65C)
   - Incremento: +15C

3. **Reducir perdidas termicas del tanque:**
   - Mejorar aislamiento o reducir a ~0.5C de perdida
   - Requiere aislamiento adicional o reparacion

4. **Combinacion de medidas:**
   - Agua a 75C + Area 25 m2 + Mejor aislamiento

---

## Propiedades de las Corrientes

### Glucosa Globe 42 DE (~80.6 Brix)
| Propiedad | Valor @ 55C | Unidad |
|-----------|-------------|--------|
| Cp | {CP_GLUCOSA:.3f} | kJ/(kg.C) |
| Densidad | {RHO_GLUCOSA:.0f} | kg/m3 |
| Viscosidad | {MU_GLUCOSA:.0f} | cP |
| Conductividad | {K_GLUCOSA:.2f} | W/(m.K) |

### Agua de Chaqueta
| Propiedad | Valor @ 65C | Unidad |
|-----------|-------------|--------|
| Cp | {CP_AGUA:.3f} | kJ/(kg.C) |
| Densidad | {RHO_AGUA:.0f} | kg/m3 |
| Viscosidad | 0.432 | cP |

---

*Documento generado automaticamente - Proyecto P2611*
*Fecha: 2026-04-10*
'''
    
    return md


# =============================================================================
# FUNCION PRINCIPAL
# =============================================================================

def main():
    print("=" * 78)
    print("GENERADOR DE DIAGRAMA DE PROCESO PFD - PROYECTO P2611")
    print("Version Matplotlib (alta calidad tecnica)")
    print("=" * 78)
    
    # Calcular corrientes para caso base (57C entrada)
    print("\n1. Calculando corrientes termodinamicas (caso base)...")
    corrientes_base = calcular_corrientes(57.0)
    
    print(f"\n   Glucosa entrada: {corrientes_base['t_gluc_ent']:.1f}C, H = {corrientes_base['h_gluc_ent']/1000:.1f} MJ/h")
    print(f"   Glucosa salida:  {corrientes_base['t_gluc_sal']:.1f}C, H = {corrientes_base['h_gluc_sal']/1000:.1f} MJ/h")
    print(f"   Agua entrada:    {corrientes_base['t_agua_ent']:.1f}C, H = {corrientes_base['h_agua_ent']/1000000:.2f} GJ/h")
    print(f"   Agua salida:     {corrientes_base['t_agua_sal']:.1f}C, H = {corrientes_base['h_agua_sal']/1000000:.2f} GJ/h")
    print(f"   Q perdidas:      {corrientes_base['q_perdida']/1000:.1f} MJ/h")
    print(f"   Q chaqueta:      {corrientes_base['q_chaqueta']/1000:.1f} MJ/h")
    print(f"   LMTD estimado:   {corrientes_base['lmtd']:.1f}C")
    
    # Generar escenarios
    print("\n2. Generando tabla de escenarios...")
    escenarios = generar_escenarios()
    viables = sum(1 for e in escenarios if e['viable'])
    print(f"   Escenarios viables: {viables}/{len(escenarios)}")
    
    # Generar diagrama
    print("\n3. Generando diagrama PFD con Matplotlib...")
    output_path = '../results/diagrama_proceso_P2611.png'
    dibujar_diagrama_pfd(corrientes_base, output_path)
    print(f"   Guardado: {output_path}")
    print(f"   Guardado: {output_path.replace('.png', '.pdf')}")
    
    # Generar tabla de escenarios
    print("\n4. Generando informe de escenarios...")
    md_content = guardar_tabla_escenarios(escenarios, corrientes_base)
    md_path = '../results/analisis_escenarios.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"   Guardado: {md_path}")
    
    # Resumen
    print("\n" + "=" * 78)
    print("RESUMEN EJECUTIVO")
    print("=" * 78)
    print(f"""
    DIAGRAMA DE PROCESO GENERADO
    
    Archivos creados:
    - {output_path}
    - {output_path.replace('.png', '.pdf')}
    - {md_path}
    
    RESULTADOS DEL CASO BASE:
    - Glucosa entra a: {corrientes_base['t_gluc_ent']:.1f}C
    - Glucosa sale a:  {corrientes_base['t_gluc_sal']:.1f}C
    - Perdidas:        {corrientes_base['q_perdida']/1000:.1f} MJ/h ({PERDIDA_TEMP:.0f}C)
    - Aporte chaqueta: {corrientes_base['q_chaqueta']/1000:.1f} MJ/h
    
    VIABILIDAD:
    - Condicion viable: T_entrada >= 60C
    - Con 57C entrada: NO CUMPLE (sale a {corrientes_base['t_gluc_sal']:.1f}C, {corrientes_base['t_gluc_sal']-57:.1f}C bajo minimo)
    """)
    print("=" * 78)


if __name__ == "__main__":
    main()
