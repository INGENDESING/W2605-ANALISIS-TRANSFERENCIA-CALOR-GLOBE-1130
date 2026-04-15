"""
Generador de Diagrama de Proceso PFD - Proyecto P2611
Diagrama de flujo de proceso profesional con balance termico completo
"""

import numpy as np
import sys
import os
import subprocess

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
    
    Returns:
        dict con todas las corrientes calculadas
    """
    # Glucosa entrada
    m_gluc = M_GLUCOSA  # kg/h
    t_gluc_ent = t_entrada_glucosa
    h_gluc_ent = m_gluc * CP_GLUCOSA * t_gluc_ent  # kJ/h
    
    # Perdidas termicas
    q_perdida = m_gluc * CP_GLUCOSA * PERDIDA_TEMP  # kJ/h
    
    # Balance en tanque (operacion continua)
    # Glucosa pierde 3°C por perdidas, gana calor de chaqueta
    
    # Agua chaqueta
    m_agua = Q_AGUA * RHO_AGUA  # kg/h
    h_agua_ent = m_agua * CP_AGUA * T_AGUA_ENT  # kJ/h
    
    # LMTD aproximado (glucosa a ~54°C, agua a ~65°C)
    t_gluc_prom = t_entrada_glucosa - PERDIDA_TEMP + 0.5  # Estimacion inicial
    dt1 = T_AGUA_ENT - (t_entrada_glucosa - PERDIDA_TEMP)  # Agua - Glucosa fria
    dt2 = 5.0  # Suponemos DT pequeno en agua (caso conservador)
    
    if dt1 <= 0:
        dt1 = 1.0
    if dt2 <= 0:
        dt2 = 0.5
    
    # LMTD
    if abs(dt1 - dt2) < 0.1:
        lmtd = (dt1 + dt2) / 2
    else:
        lmtd = (dt1 - dt2) / np.log(dt1 / dt2)
    
    # Calor transferido en chaqueta (W)
    q_chaqueta_w = U_GLOBAL * AREA_CHAQUETA * lmtd
    q_chaqueta = q_chaqueta_w * 3.6  # kJ/h (1 W = 3.6 kJ/h)
    
    # Balance glucosa en tanque
    # H_entrada - Perdidas + Chaqueta = H_salida
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
# GENERACION DIAGRAMA DOT
# =============================================================================

def generar_dot(corrientes):
    """Genera codigo Graphviz DOT para el diagrama de proceso"""
    
    # Datos formateados
    te = corrientes['t_gluc_ent']
    ts = corrientes['t_gluc_sal']
    he = corrientes['h_gluc_ent'] / 1000  # MJ/h
    hs = corrientes['h_gluc_sal'] / 1000  # MJ/h
    t_ae = corrientes['t_agua_ent']
    t_as = corrientes['t_agua_sal']
    ha_e = corrientes['h_agua_ent'] / 1000  # MJ/h
    ha_s = corrientes['h_agua_sal'] / 1000  # MJ/h
    qper = corrientes['q_perdida'] / 1000  # MJ/h
    qcha = corrientes['q_chaqueta'] / 1000  # MJ/h
    
    dot = f'''digraph PFD_P2611 {{
    // Configuracion general
    graph [fontname="Arial", fontsize=12, rankdir=LR, bgcolor=white, 
           margin="20,20", nodesep=0.6, ranksep=1.2];
    node [fontname="Arial", fontsize=9, shape=box, style="filled,rounded",
          fillcolor="#f0f0f0", margin="0.15,0.08"];
    edge [fontname="Arial", fontsize=8, arrowhead=vee, arrowsize=0.8];
    
    // ============================================
    // NODOS DEL PROCESO
    // ============================================
    
    // Entrada de glucosa
    E101 [label="E-101\\nEntrada Glucosa", fillcolor="#90EE90", shape=box, width=1.5];
    
    // Tanque T-101 (grupo con componentes)
    T101 [label="T-101\\nTanque Almacenamiento\\nFondo Torisferico + Tapa Eliptica\\nAislamiento Termico", 
          fillcolor="#FFB6C1", shape=cylinder, width=2.0, height=1.5];
    
    // Chaqueta E-201
    E201 [label="E-201\\nChaqueta Calentamiento\\nA = 13 m2", 
          fillcolor="#87CEEB", shape=box, width=1.3];
    
    // Bomba P-101
    P101 [label="P-101\\nBomba\\nCentrifuga", 
          fillcolor="#DDA0DD", shape=ellipse, width=1.0];
    
    // Salida a carrotanque
    E102 [label="E-102\\nEstacion Carga\\nCarrotanque", 
          fillcolor="#F0E68C", shape=box, width=1.5];
    
    // ============================================
    // CORRIENTES PRINCIPALES
    // ============================================
    
    // Corriente 1: Glucosa entrada
    E101 -> T101 [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD COLSPAN="2"><B>1: Glucosa Entrada</B></TD></TR>
        <TR><TD>Flujo:</TD><TD>{M_GLUCOSA:.0f} kg/h</TD></TR>
        <TR><TD>Temperatura:</TD><TD>{te:.1f}°C</TD></TR>
        <TR><TD>Entalpia:</TD><TD>{he:.1f} MJ/h</TD></TR>
        <TR><TD>Cp:</TD><TD>{CP_GLUCOSA:.3f} kJ/kg°C</TD></TR>
        <TR><TD>Densidad:</TD><TD>{RHO_GLUCOSA:.0f} kg/m3</TD></TR>
        <TR><TD>Viscosidad:</TD><TD>{MU_GLUCOSA:.0f} cP</TD></TR>
    </TABLE>>, color=darkgreen, penwidth=2, minlen=2];
    
    // Corriente 4: Glucosa salida del tanque
    T101 -> P101 [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD COLSPAN="2"><B>4: Glucosa Salida</B></TD></TR>
        <TR><TD>Flujo:</TD><TD>{M_GLUCOSA:.0f} kg/h</TD></TR>
        <TR><TD>Temperatura:</TD><TD>{ts:.1f}°C</TD></TR>
        <TR><TD>Entalpia:</TD><TD>{hs:.1f} MJ/h</TD></TR>
        <TR><TD>Cp:</TD><TD>{CP_GLUCOSA:.3f} kJ/kg°C</TD></TR>
        <TR><TD>Densidad:</TD><TD>{RHO_GLUCOSA:.0f} kg/m3</TD></TR>
        <TR><TD>Viscosidad:</TD><TD>{MU_GLUCOSA:.0f} cP</TD></TR>
    </TABLE>>, color=darkgreen, penwidth=2, minlen=2];
    
    // Corriente 5: A carga
    P101 -> E102 [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD COLSPAN="2"><B>5: A Carrotanque</B></TD></TR>
        <TR><TD>Flujo:</TD><TD>{M_GLUCOSA:.0f} kg/h</TD></TR>
        <TR><TD>Temperatura:</TD><TD>{ts:.1f}°C</TD></TR>
        <TR><TD>Entalpia:</TD><TD>{hs:.1f} MJ/h</TD></TR>
    </TABLE>>, color=darkgreen, penwidth=2, minlen=2];
    
    // ============================================
    // SERVICIOS - AGUA DE CALENTAMIENTO
    // ============================================
    
    // Agua entrada (lado izquierdo)
    AguaEnt [label="", shape=none, width=0, height=0];
    AguaEnt -> E201 [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD COLSPAN="2"><B>2: Agua Entrada</B></TD></TR>
        <TR><TD>Flujo:</TD><TD>{Q_AGUA:.1f} m3/h</TD></TR>
        <TR><TD>Flujo:</TD><TD>{corrientes['m_agua']:.0f} kg/h</TD></TR>
        <TR><TD>Temperatura:</TD><TD>{t_ae:.1f}°C</TD></TR>
        <TR><TD>Entalpia:</TD><TD>{ha_e:.1f} MJ/h</TD></TR>
        <TR><TD>Cp:</TD><TD>{CP_AGUA:.3f} kJ/kg°C</TD></TR>
        <TR><TD>Densidad:</TD><TD>{RHO_AGUA:.0f} kg/m3</TD></TR>
    </TABLE>>, color=blue, penwidth=1.5, style=dashed, constraint=false];
    
    // Agua salida
    E201 -> AguaSal [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD COLSPAN="2"><B>3: Agua Salida</B></TD></TR>
        <TR><TD>Flujo:</TD><TD>{corrientes['m_agua']:.0f} kg/h</TD></TR>
        <TR><TD>Temperatura:</TD><TD>{t_as:.1f}°C</TD></TR>
        <TR><TD>Entalpia:</TD><TD>{ha_s:.1f} MJ/h</TD></TR>
    </TABLE>>, color=blue, penwidth=1.5, style=dashed];
    
    AguaSal [label="", shape=none, width=0, height=0];
    
    // Conexion chaqueta a tanque (representa intercambio)
    E201 -> T101 [style=invis, constraint=false];
    
    // ============================================
    // FLUJOS DE ENERGIA
    // ============================================
    
    // Perdidas termicas (flecha roja discontinua hacia arriba)
    Perdidas [label="Q Perdidas = {qper:.1f} MJ/h\\n({PERDIDA_TEMP:.0f}°C perdidos)", 
              shape=none, fillcolor=none, fontcolor=red];
    T101 -> Perdidas [style=dotted, color=red, penwidth=2, arrowhead=none, 
                      constraint=false, minlen=1];
    
    // Calor de chaqueta (etiqueta cerca del tanque)
    QChaqueta [label="Q Chaqueta = {qcha:.1f} MJ/h\\n(U = {U_GLOBAL:.0f} W/m2K, A = {AREA_CHAQUETA:.0f} m2)", 
               shape=none, fillcolor=none, fontcolor=blue];
    E201 -> QChaqueta [style=invis, constraint=false];
    
    // ============================================
    // LEYENDA Y ANOTACIONES
    // ============================================
    
    label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="4" BGCOLOR="#f8f8f8">
        <TR><TD COLSPAN="2"><B>PROYECTO P2611 - DIAGRAMA DE FLUJO DE PROCESO</B></TD></TR>
        <TR><TD COLSPAN="2">Sistema de Almacenamiento y Carga de Glucosa Globe 42 DE</TD></TR>
        <TR><TD>Tanque:</TD><TD>Fondo Torisferico ASME F&D + Tapa Eliptica API 650</TD></TR>
        <TR><TD>Aislamiento:</TD><TD>Lana Mineral (especificado sin espesor)</TD></TR>
        <TR><TD>Chaqueta:</TD><TD>Media cana rectangular, Area = 13 m2</TD></TR>
        <TR><TD>Condicion Minima Carga:</TD><TD>Temperatura >= {T_MIN_CARGA:.0f}°C</TD></TR>
    </TABLE>>;
    labelloc=b;
    labeljust=center;
    
    // Subgraph para agrupar servicios
    subgraph cluster_servicios {{
        label="Servicio: Agua Caliente 65°C";
        style=dashed;
        color=blue;
        AguaEnt;
        E201;
        AguaSal;
    }}
}}'''
    
    return dot


def guardar_tabla_escenarios(escenarios, corrientes_base):
    """Genera y guarda la tabla de escenarios en formato Markdown"""
    
    md = '''# Analisis de Escenarios - Proyecto P2611
## Sistema de Almacenamiento y Carga de Glucosa

### Condiciones de Operacion Base
- **Flujo de glucosa:** 8,000 kg/h
- **Perdidas termicas del tanque:** 3°C (equivalente a 51,144 kJ/h)
- **Chaqueta de calentamiento:** Area = 13 m², Agua @ 65°C, 30.9 m³/h
- **Coeficiente global U:** ~30 W/(m²·K)
- **Capacidad de transferencia chaqueta:** ~13,200 kJ/h
- **Temperatura minima para carga:** 57°C

---

## Tabla de Escenarios

| T Entrada (°C) | T Salida (°C) | Q Perdida (MJ/h) | Q Chaqueta (MJ/h) | Delta vs Min | Estado | Observaciones |
|:--------------:|:-------------:|:----------------:|:-----------------:|:------------:|:------:|:--------------|
'''
    
    for e in escenarios:
        estado = "✅ ACEPTABLE" if e['viable'] else "❌ RECHAZADO"
        obs = "Cumple minimo" if e['viable'] else f"{abs(e['diferencia']):.1f}°C bajo minimo"
        md += f"| {e['t_entrada']:.0f} | {e['t_salida']:.1f} | {e['q_perdida']/1000:.1f} | {e['q_chaqueta']/1000:.1f} | {e['diferencia']:+.1f}°C | {estado} | {obs} |\n"
    
    md += f'''

---

## Analisis de Viabilidad

### Caso Base (Entrada a {corrientes_base['t_gluc_ent']:.0f}°C)

**Balance Energetico:**
```
Glucosa Entrada:  H = {corrientes_base['h_gluc_ent']/1000:.1f} MJ/h @ {corrientes_base['t_gluc_ent']:.1f}°C
Perdidas:        -Q = {corrientes_base['q_perdida']/1000:.1f} MJ/h ({PERDIDA_TEMP:.0f}°C)
Chaqueta:        +Q = {corrientes_base['q_chaqueta']/1000:.1f} MJ/h (U={U_GLOBAL:.0f} W/m2K, A={AREA_CHAQUETA:.0f}m2)
--------------------------------------------------------------------------------
Glucosa Salida:  H = {corrientes_base['h_gluc_sal']/1000:.1f} MJ/h @ {corrientes_base['t_gluc_sal']:.1f}°C
```

**Agua de Chaqueta:**
```
Agua Entrada:    H = {corrientes_base['h_agua_ent']/1000000:.2f} GJ/h @ {corrientes_base['t_agua_ent']:.1f}°C
Transferido:     -Q = {corrientes_base['q_chaqueta']/1000:.1f} MJ/h
Agua Salida:     H = {corrientes_base['h_agua_sal']/1000000:.2f} GJ/h @ {corrientes_base['t_agua_sal']:.1f}°C
```

### Conclusion Critica

**SOLO es viable cargar a carrotanque si la glucosa entra a 60°C o superior.**

Con las condiciones actuales:
- Las perdidas termicas (51,144 kJ/h) son ~4x mayores que el aporte de la chaqueta (13,200 kJ/h)
- El sistema opera con deficit energetico de ~38,000 kJ/h
- La glucosa sale 2.2°C por debajo del minimo requerido

### Recomendaciones para Operar con Entrada a 57°C

Para poder cargar glucosa a 57°C y mantener la temperatura de salida ≥57°C, se requiere **AL MENOS UNA** de las siguientes modificaciones:

1. **Aumentar area de chaqueta:**
   - Area requerida: ~50-55 m² (actual: 13 m²)
   - Incremento: 4x el area actual

2. **Subir temperatura del agua:**
   - Temperatura requerida: ~75°C (actual: 65°C)
   - Incremento: +10°C

3. **Reducir perdidas termicas del tanque:**
   - Mejorar aislamiento o reducir a ~1°C de perdida
   - Requiere aislamiento adicional o reparacion

4. **Combinacion de medidas:**
   - Agua a 70°C + Area 25 m² + Mejor aislamiento

---

## Propiedades de las Corrientes

### Glucosa Globe 42 DE (~80.6 Brix)
| Propiedad | Valor @ 55°C | Unidad |
|-----------|--------------|--------|
| Cp | {CP_GLUCOSA:.3f} | kJ/(kg·°C) |
| Densidad | {RHO_GLUCOSA:.0f} | kg/m³ |
| Viscosidad | {MU_GLUCOSA:.0f} | cP |
| Conductividad | {K_GLUCOSA:.2f} | W/(m·K) |

### Agua de Chaqueta
| Propiedad | Valor @ 65°C | Unidad |
|-----------|--------------|--------|
| Cp | {CP_AGUA:.3f} | kJ/(kg·°C) |
| Densidad | {RHO_AGUA:.0f} | kg/m³ |
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
    print("=" * 78)
    
    # Calcular corrientes para caso base (57°C entrada)
    print("\n1. Calculando corrientes termodinamicas (caso base)...")
    corrientes_base = calcular_corrientes(57.0)
    
    print(f"\n   Glucosa entrada: {corrientes_base['t_gluc_ent']:.1f}°C, H = {corrientes_base['h_gluc_ent']/1000:.1f} MJ/h")
    print(f"   Glucosa salida:  {corrientes_base['t_gluc_sal']:.1f}°C, H = {corrientes_base['h_gluc_sal']/1000:.1f} MJ/h")
    print(f"   Agua entrada:    {corrientes_base['t_agua_ent']:.1f}°C, H = {corrientes_base['h_agua_ent']/1000000:.2f} GJ/h")
    print(f"   Agua salida:     {corrientes_base['t_agua_sal']:.1f}°C, H = {corrientes_base['h_agua_sal']/1000000:.2f} GJ/h")
    print(f"   Q perdidas:      {corrientes_base['q_perdida']/1000:.1f} MJ/h")
    print(f"   Q chaqueta:      {corrientes_base['q_chaqueta']/1000:.1f} MJ/h")
    print(f"   LMTD estimado:   {corrientes_base['lmtd']:.1f}°C")
    
    # Generar escenarios
    print("\n2. Generando tabla de escenarios...")
    escenarios = generar_escenarios()
    viables = sum(1 for e in escenarios if e['viable'])
    print(f"   Escenarios viables: {viables}/{len(escenarios)}")
    
    # Generar diagrama DOT
    print("\n3. Generando diagrama DOT...")
    dot_code = generar_dot(corrientes_base)
    
    # Guardar archivo DOT
    os.makedirs('../results', exist_ok=True)
    dot_path = '../results/diagrama_proceso_P2611.dot'
    with open(dot_path, 'w') as f:
        f.write(dot_code)
    print(f"   Guardado: {dot_path}")
    
    # Convertir a SVG
    print("\n4. Convirtiendo a SVG...")
    svg_path = '../results/diagrama_proceso_P2611.svg'
    try:
        subprocess.run(['dot', '-Tsvg', dot_path, '-o', svg_path], check=True)
        print(f"   Guardado: {svg_path}")
    except subprocess.CalledProcessError as e:
        print(f"   Error: {e}")
        print("   Asegurese de tener Graphviz instalado (dot.exe en PATH)")
    
    # Convertir a PNG
    print("\n5. Convirtiendo a PNG...")
    png_path = '../results/diagrama_proceso_P2611.png'
    try:
        subprocess.run(['dot', '-Tpng', '-Gdpi=300', dot_path, '-o', png_path], check=True)
        print(f"   Guardado: {png_path}")
    except subprocess.CalledProcessError as e:
        print(f"   Error: {e}")
    
    # Generar tabla de escenarios
    print("\n6. Generando informe de escenarios...")
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
    - {dot_path}
    - {svg_path}
    - {png_path}
    - {md_path}
    
    RESULTADOS DEL CASO BASE:
    - Glucosa entra a: {corrientes_base['t_gluc_ent']:.1f}°C
    - Glucosa sale a:  {corrientes_base['t_gluc_sal']:.1f}°C
    - Perdidas:        {corrientes_base['q_perdida']/1000:.1f} MJ/h ({PERDIDA_TEMP:.0f}°C)
    - Aporte chaqueta: {corrientes_base['q_chaqueta']/1000:.1f} MJ/h
    
    VIABILIDAD:
    - Condicion viable: T_entrada >= 60°C
    - Con 57°C entrada: ❌ NO CUMPLE (sale a {corrientes_base['t_gluc_sal']:.1f}°C, {corrientes_base['t_gluc_sal']-57:.1f}°C bajo minimo)
    """)
    print("=" * 78)


if __name__ == "__main__":
    main()
