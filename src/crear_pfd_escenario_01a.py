#!/usr/bin/env python3
"""
Generador de PFD para Escenario 01A - Proyecto P2611
SVG nativo limpio mostrando tres temperaturas de entrada de glucosa
a velocidad de viento 1.5 m/s
"""

import os

# Datos del Escenario 01A - Tres temperaturas de entrada, v=1.5 m/s
RESULTADOS = {
    60.0: {'T_salida': 58.1, 'Q_chaq': 7.0, 'Q_perd': 38.9, 'Q_net': -31.9, 'H_in': 1024, 'H_out': 992},
    57.0: {'T_salida': 55.55, 'Q_chaq': 10.9, 'Q_perd': 35.7, 'Q_net': -24.8, 'H_in': 973, 'H_out': 948},
    54.0: {'T_salida': 52.97, 'Q_chaq': 14.9, 'Q_perd': 32.4, 'Q_net': -17.5, 'H_in': 922, 'H_out': 904},
}

# Parametros del sistema
T_ENTRADA_AGUA = 65.0
T_SALIDA_AGUA = 64.9
FLUJO_GLUC = 8000
FLUJO_AGUA = 30900
H_AGUA_IN = 8224
H_AGUA_OUT = 8218

SVG_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1400" height="1000" viewBox="0 0 1400 1000" xmlns="http://www.w3.org/2000/svg">
    <title>PFD Escenario 01A - Proyecto P2611</title>
    <desc>Diagrama de Flujo de Proceso - Escenario 01A con tres temperaturas de entrada de glucosa (v = 1.5 m/s)</desc>
    
    <!-- Fondo blanco -->
    <rect width="1400" height="1000" fill="#FAFAFA"/>
    
    <!-- ===================== TITULO ===================== -->
    <g id="titulo">
        <rect x="50" y="15" width="1300" height="50" rx="8" fill="#1565C0"/>
        <text x="700" y="48" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle">
            PFD ESCENARIO 01A - Sistema de Almacenamiento de Glucosa
        </text>
        <text x="700" y="78" font-family="Arial, sans-serif" font-size="12" fill="#424242" text-anchor="middle">
            Agua 65°C | Caudal 30,900 kg/h | Area 13 m² | Viento 1.5 m/s | Caudal glucosa 8,000 kg/h
        </text>
    </g>
    
    <!-- ===================== TANQUE T-101 ===================== -->
    <g id="tanque">
        <!-- Marco exterior -->
        <rect x="320" y="280" width="220" height="300" rx="20" fill="none" stroke="#757575" stroke-width="2" stroke-dasharray="5,4"/>
        
        <!-- Cuerpo cilindrico -->
        <rect x="330" y="320" width="200" height="200" fill="#FFF3E0" stroke="#E65100" stroke-width="3"/>
        
        <!-- Fondo torisferico -->
        <path d="M 330 520 Q 430 580 530 520" fill="#FFF3E0" stroke="#E65100" stroke-width="3"/>
        <path d="M 330 520 Q 430 560 530 520" fill="none" stroke="#E65100" stroke-width="1.5" stroke-dasharray="3,2"/>
        
        <!-- Tapa eliptica -->
        <path d="M 330 320 Q 430 260 530 320" fill="#FFF3E0" stroke="#E65100" stroke-width="3"/>
        
        <!-- Lineas de refuerzo -->
        <line x1="365" y1="270" x2="365" y2="320" stroke="#FFB74D" stroke-width="1"/>
        <line x1="495" y1="270" x2="495" y2="320" stroke="#FFB74D" stroke-width="1"/>
        
        <!-- Nivel 80% -->
        <line x1="340" y1="400" x2="520" y2="400" stroke="#2196F3" stroke-width="3"/>
        <rect x="340" y="400" width="180" height="120" fill="#E3F2FD" opacity="0.4"/>
        <text x="540" y="405" font-family="Arial" font-size="12" fill="#1565C0" font-weight="bold">80%</text>
        
        <!-- Etiquetas del tanque -->
        <text x="430" y="355" font-family="Arial" font-size="18" font-weight="bold" fill="#E65100" text-anchor="middle">T-101</text>
        <text x="430" y="375" font-family="Arial" font-size="11" fill="#424242" text-anchor="middle">Tanque de Almacenamiento</text>
        <text x="430" y="445" font-family="Arial" font-size="9" fill="#757575" text-anchor="middle" font-style="italic">Fondo Torisferico</text>
        <text x="430" y="460" font-family="Arial" font-size="9" fill="#757575" text-anchor="middle">D = 5.03 m | H = 9.67 m</text>
    </g>
    
    <!-- ===================== CHAQUETA E-201 ===================== -->
    <g id="chaqueta">
        <!-- Caja principal -->
        <rect x="355" y="560" width="150" height="70" fill="#B3E5FC" stroke="#1565C0" stroke-width="2.5" rx="5"/>
        
        <!-- Serpentina -->
        <line x1="365" y1="575" x2="495" y2="575" stroke="#1565C0" stroke-width="2"/>
        <line x1="495" y1="575" x2="495" y2="590" stroke="#1565C0" stroke-width="2"/>
        <line x1="495" y1="590" x2="365" y2="590" stroke="#1565C0" stroke-width="2"/>
        <line x1="365" y1="590" x2="365" y2="605" stroke="#1565C0" stroke-width="2"/>
        <line x1="365" y1="605" x2="495" y2="605" stroke="#1565C0" stroke-width="2"/>
        <line x1="495" y1="605" x2="495" y2="620" stroke="#1565C0" stroke-width="2"/>
        <line x1="495" y1="620" x2="365" y2="620" stroke="#1565C0" stroke-width="2"/>
        
        <!-- Conexiones -->
        <line x1="355" y1="595" x2="340" y2="595" stroke="#1565C0" stroke-width="2"/>
        <line x1="505" y1="595" x2="520" y2="595" stroke="#1565C0" stroke-width="2"/>
        
        <!-- Etiquetas -->
        <text x="430" y="550" font-family="Arial" font-size="14" font-weight="bold" fill="#0D47A1" text-anchor="middle">E-201</text>
        <text x="430" y="645" font-family="Arial" font-size="10" fill="#424242" text-anchor="middle">Chaqueta Media Caña</text>
        <text x="430" y="660" font-family="Arial" font-size="9" fill="#757575" text-anchor="middle">A = 13 m²</text>
    </g>
    
    <!-- ===================== BOMBA P-101 ===================== -->
    <g id="bomba">
        <circle cx="720" cy="400" r="35" fill="#E1BEE7" stroke="#7B1FA2" stroke-width="2.5"/>
        <path d="M 720 385 L 705 415 L 735 415 Z" fill="#FFFFFF" stroke="#7B1FA2" stroke-width="2"/>
        <circle cx="720" cy="400" r="6" fill="#FFFFFF" stroke="#7B1FA2" stroke-width="1.5"/>
        <text x="720" y="355" font-family="Arial" font-size="14" font-weight="bold" fill="#7B1FA2" text-anchor="middle">P-101</text>
        <text x="720" y="455" font-family="Arial" font-size="10" fill="#424242" text-anchor="middle">Bomba</text>
    </g>
    
    <!-- ===================== CARROTANQUE ===================== -->
    <g id="carrotanque">
        <!-- Cabina -->
        <rect x="1050" y="360" width="70" height="70" fill="#FFECB3" stroke="#FF8F00" stroke-width="2" rx="4"/>
        <rect x="1060" y="375" width="35" height="25" fill="#B3E5FC" stroke="#0288D1" stroke-width="1.5" rx="2"/>
        
        <!-- Tanque -->
        <rect x="1125" y="355" width="110" height="80" fill="#BDBDBD" stroke="#616161" stroke-width="2"/>
        <line x1="1155" y1="355" x2="1155" y2="435" stroke="#757575" stroke-width="1.5"/>
        <line x1="1190" y1="355" x2="1190" y2="435" stroke="#757575" stroke-width="1.5"/>
        <line x1="1225" y1="355" x2="1225" y2="435" stroke="#757575" stroke-width="1.5"/>
        
        <!-- Ruedas -->
        <circle cx="1075" cy="445" r="10" fill="#424242" stroke="#212121" stroke-width="1.5"/>
        <circle cx="1095" cy="445" r="10" fill="#424242" stroke="#212121" stroke-width="1.5"/>
        <circle cx="1145" cy="445" r="10" fill="#424242" stroke="#212121" stroke-width="1.5"/>
        <circle cx="1180" cy="445" r="10" fill="#424242" stroke="#212121" stroke-width="1.5"/>
        <circle cx="1220" cy="445" r="10" fill="#424242" stroke="#212121" stroke-width="1.5"/>
        
        <!-- Etiqueta -->
        <text x="1145" y="350" font-family="Arial" font-size="13" font-weight="bold" fill="#424242" text-anchor="middle">Carro Tanque</text>
        <text x="1145" y="470" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">Capacidad: 24 ton</text>
    </g>
    
    <!-- ===================== VIENTO ===================== -->
    <g id="viento">
        <text x="430" y="230" font-family="Arial" font-size="14" font-weight="bold" fill="#00ACC1" text-anchor="middle">Viento 1.5 m/s</text>
        <line x1="350" y1="245" x2="510" y2="245" stroke="#00ACC1" stroke-width="2.5" marker-end="url(#arrowhead)"/>
        <line x1="370" y1="260" x2="490" y2="260" stroke="#00ACC1" stroke-width="2" marker-end="url(#arrowhead)"/>
        <line x1="390" y1="275" x2="470" y2="275" stroke="#00ACC1" stroke-width="1.5" marker-end="url(#arrowhead)"/>
    </g>
    
    <!-- Definicion de flecha -->
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#00ACC1"/>
        </marker>
        <marker id="arrowgreen" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#2E7D32"/>
        </marker>
        <marker id="arrowred" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#C62828"/>
        </marker>
    </defs>
    
    <!-- ===================== LINEAS DE PROCESO ===================== -->
    <!-- Glucosa entrada -->
    <line x1="50" y1="260" x2="280" y2="260" stroke="#2E7D32" stroke-width="3" marker-end="url(#arrowgreen)"/>
    <line x1="280" y1="260" x2="320" y2="295" stroke="#2E7D32" stroke-width="3"/>
    
    <!-- Glucosa salida -->
    <line x1="550" y1="380" x2="620" y2="400" stroke="#2E7D32" stroke-width="3" marker-end="url(#arrowgreen)"/>
    <line x1="755" y1="400" x2="1050" y2="395" stroke="#2E7D32" stroke-width="3" marker-end="url(#arrowgreen)"/>
    
    <!-- Agua entrada -->
    <line x1="50" y1="595" x2="320" y2="595" stroke="#C62828" stroke-width="3" stroke-dasharray="8,4" marker-end="url(#arrowred)"/>
    
    <!-- Agua salida -->
    <line x1="520" y1="595" x2="600" y2="595" stroke="#C62828" stroke-width="3" stroke-dasharray="8,4" marker-end="url(#arrowred)"/>
    
    <!-- Etiquetas de corrientes -->
    <text x="180" y="250" font-family="Arial" font-size="10" fill="#2E7D32" font-weight="bold">Corriente 1</text>
    <text x="580" y="390" font-family="Arial" font-size="10" fill="#2E7D32" font-weight="bold">Corriente 4</text>
    <text x="180" y="585" font-family="Arial" font-size="10" fill="#C62828" font-weight="bold">Corriente 2</text>
    <text x="540" y="585" font-family="Arial" font-size="10" fill="#C62828" font-weight="bold">Corriente 3</text>
    
    <!-- ===================== CAJAS DE DATOS - ENTRADAS ===================== -->
    <!-- Corriente 1 - Glucosa entrada -->
    <g>
        <rect x="30" y="170" width="260" height="70" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2" rx="6"/>
        <text x="160" y="195" font-family="Arial" font-size="12" font-weight="bold" fill="#1B5E20" text-anchor="middle">
            CORRIENTE 1 - Glucosa Entrada
        </text>
        <text x="160" y="215" font-family="Arial" font-size="11" fill="#212121" text-anchor="middle">
            8,000 kg/h | 60 / 57 / 54°C
        </text>
        <text x="160" y="232" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            Cp = 2.13 kJ/kg·K
        </text>
    </g>
    
    <!-- Corriente 2 - Agua entrada -->
    <g>
        <rect x="30" y="640" width="260" height="70" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="6"/>
        <text x="160" y="665" font-family="Arial" font-size="12" font-weight="bold" fill="#B71C1C" text-anchor="middle">
            CORRIENTE 2 - Agua Entrada
        </text>
        <text x="160" y="685" font-family="Arial" font-size="11" fill="#212121" text-anchor="middle">
            30,900 kg/h | 65.0°C | 8,224 MJ/h
        </text>
        <text x="160" y="702" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            30.9 m³/h | Cp = 4.18 kJ/kg·K
        </text>
    </g>
    
    <!-- Corriente 3 - Agua salida -->
    <g>
        <rect x="620" y="640" width="260" height="70" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="6"/>
        <text x="750" y="665" font-family="Arial" font-size="12" font-weight="bold" fill="#B71C1C" text-anchor="middle">
            CORRIENTE 3 - Agua Salida
        </text>
        <text x="750" y="685" font-family="Arial" font-size="11" fill="#212121" text-anchor="middle">
            30,900 kg/h | 64.9°C | 8,218 MJ/h
        </text>
        <text x="750" y="702" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            Q transferido: 7.0-14.9 MJ/h
        </text>
    </g>
    
    <!-- ===================== CAJAS DE DATOS - SALIDAS (3 temperaturas) ===================== -->
    <!-- Corriente 4a - Entrada 60°C -->
    <g>
        <rect x="620" y="170" width="280" height="75" fill="#C8E6C9" stroke="#2E7D32" stroke-width="2.5" rx="6"/>
        <text x="760" y="195" font-family="Arial" font-size="12" font-weight="bold" fill="#1B5E20" text-anchor="middle">
            CORRIENTE 4a - Entrada 60°C
        </text>
        <text x="760" y="215" font-family="Arial" font-size="13" fill="#212121" text-anchor="middle" font-weight="bold">
            8,000 kg/h | 58.1°C | 992 MJ/h
        </text>
        <text x="760" y="235" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            h_ext = 3.29 W/m²K | U_perd = 2.22 W/m²K
        </text>
    </g>
    
    <!-- Corriente 4b - Entrada 57°C -->
    <g>
        <rect x="620" y="260" width="280" height="75" fill="#A5D6A7" stroke="#2E7D32" stroke-width="2" rx="6"/>
        <text x="760" y="285" font-family="Arial" font-size="12" font-weight="bold" fill="#1B5E20" text-anchor="middle">
            CORRIENTE 4b - Entrada 57°C
        </text>
        <text x="760" y="305" font-family="Arial" font-size="13" fill="#212121" text-anchor="middle" font-weight="bold">
            8,000 kg/h | 55.55°C | 948 MJ/h
        </text>
        <text x="760" y="325" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            h_ext = 3.29 W/m²K | U_perd = 2.22 W/m²K
        </text>
    </g>
    
    <!-- Corriente 4c - Entrada 54°C -->
    <g>
        <rect x="620" y="350" width="280" height="75" fill="#81C784" stroke="#2E7D32" stroke-width="2" rx="6"/>
        <text x="760" y="375" font-family="Arial" font-size="12" font-weight="bold" fill="#1B5E20" text-anchor="middle">
            CORRIENTE 4c - Entrada 54°C
        </text>
        <text x="760" y="395" font-family="Arial" font-size="13" fill="#212121" text-anchor="middle" font-weight="bold">
            8,000 kg/h | 52.97°C | 904 MJ/h
        </text>
        <text x="760" y="415" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle">
            h_ext = 3.29 W/m²K | U_perd = 3.12 W/m²K
        </text>
    </g>
    
    <!-- ===================== TABLA DE BALANCE ENERGETICO ===================== -->
    <g>
        <rect x="950" y="550" width="400" height="200" fill="#FFFFFF" stroke="#1565C0" stroke-width="2.5" rx="8"/>
        <rect x="950" y="550" width="400" height="35" fill="#1565C0" rx="8"/>
        <text x="1150" y="575" font-family="Arial" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">
            BALANCE ENERGÉTICO - ESCENARIO 01A
        </text>
        
        <!-- Tabla -->
        <text x="1030" y="610" font-family="Arial" font-size="11" font-weight="bold" fill="#424242" text-anchor="middle">Concepto</text>
        <text x="1130" y="610" font-family="Arial" font-size="11" font-weight="bold" fill="#424242" text-anchor="middle">60°C</text>
        <text x="1230" y="610" font-family="Arial" font-size="11" font-weight="bold" fill="#424242" text-anchor="middle">57°C</text>
        <text x="1330" y="610" font-family="Arial" font-size="11" font-weight="bold" fill="#424242" text-anchor="middle">54°C</text>
        
        <line x1="960" y1="620" x2="1340" y2="620" stroke="#BDBDBD" stroke-width="1"/>
        
        <text x="1030" y="645" font-family="Arial" font-size="10" fill="#212121" text-anchor="middle">Q Transferido (MJ/h)</text>
        <text x="1130" y="645" font-family="Arial" font-size="10" fill="#1565C0" text-anchor="middle">7.0</text>
        <text x="1230" y="645" font-family="Arial" font-size="10" fill="#1565C0" text-anchor="middle">10.9</text>
        <text x="1330" y="645" font-family="Arial" font-size="10" fill="#1565C0" text-anchor="middle">14.9</text>
        
        <text x="1030" y="670" font-family="Arial" font-size="10" fill="#212121" text-anchor="middle">Q Pérdidas (MJ/h)</text>
        <text x="1130" y="670" font-family="Arial" font-size="10" fill="#C62828" text-anchor="middle">38.9</text>
        <text x="1230" y="670" font-family="Arial" font-size="10" fill="#C62828" text-anchor="middle">35.7</text>
        <text x="1330" y="670" font-family="Arial" font-size="10" fill="#C62828" text-anchor="middle">32.4</text>
        
        <line x1="960" y1="685" x2="1340" y2="685" stroke="#BDBDBD" stroke-width="1"/>
        
        <text x="1030" y="710" font-family="Arial" font-size="11" font-weight="bold" fill="#212121" text-anchor="middle">Q Neto (MJ/h)</text>
        <text x="1130" y="710" font-family="Arial" font-size="11" font-weight="bold" fill="#D32F2F" text-anchor="middle">-31.9</text>
        <text x="1230" y="710" font-family="Arial" font-size="11" font-weight="bold" fill="#D32F2F" text-anchor="middle">-24.8</text>
        <text x="1330" y="710" font-family="Arial" font-size="11" font-weight="bold" fill="#D32F2F" text-anchor="middle">-17.5</text>
        
        <text x="1150" y="740" font-family="Arial" font-size="9" fill="#616161" text-anchor="middle" font-style="italic">
            Velocidad de viento constante: 1.5 m/s
        </text>
    </g>
    
    <!-- ===================== NOTAS ===================== -->
    <g>
        <rect x="950" y="770" width="400" height="85" fill="#FFF3E0" stroke="#FF8F00" stroke-width="1.5" rx="6"/>
        <text x="1150" y="795" font-family="Arial" font-size="11" font-weight="bold" fill="#E65100" text-anchor="middle">
            PARÁMETROS DEL SISTEMA
        </text>
        <text x="970" y="815" font-family="Arial" font-size="9" fill="#424242">
            • U chaqueta: 25.4-35.8 W/m²K (calculado)
        </text>
        <text x="970" y="832" font-family="Arial" font-size="9" fill="#424242">
            • h_i (agua): ~6,490 W/m²K | h_o (glucosa): ~25-36 W/m²K
        </text>
        <text x="970" y="849" font-family="Arial" font-size="9" fill="#424242">
            • A_superficie expuesta: 149.67 m² | T_ambiente: 26.5°C
        </text>
    </g>
    
    <!-- ===================== LEYENDA ===================== -->
    <g>
        <rect x="30" y="770" width="260" height="85" fill="#ECEFF1" stroke="#546E7A" stroke-width="1.5" rx="6"/>
        <text x="160" y="795" font-family="Arial" font-size="11" font-weight="bold" fill="#37474F" text-anchor="middle">
            EQUIPOS
        </text>
        <text x="45" y="815" font-family="Arial" font-size="9" fill="#424242">
            T-101: Tanque de almacenamiento (80% llenado)
        </text>
        <text x="45" y="832" font-family="Arial" font-size="9" fill="#424242">
            E-201: Chaqueta de media caña (A = 13 m²)
        </text>
        <text x="45" y="849" font-family="Arial" font-size="9" fill="#424242">
            P-101: Bomba de transferencia
        </text>
    </g>
    
</svg>
'''

# Guardar el archivo
output_path = '../results/PFD_Escenario_01A.svg'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(SVG_TEMPLATE)

print(f"PFD del Escenario 01A generado exitosamente:")
print(f"  Archivo: {output_path}")
print(f"  Dimensiones: 1400 x 1000 px")
print(f"  Temperaturas de entrada evaluadas: 60°C, 57°C, 54°C")
print(f"  Velocidad de viento: 1.5 m/s")
print(f"  Nota: Sin referencias a espesor de aislamiento")
