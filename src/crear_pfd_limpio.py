#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de PFD Limpio - Proyecto P2611
SVG nativo desde cero, optimizado para visualizacion y edicion
"""

import os

# Configuracion
WIDTH = 1200
HEIGHT = 900

# Colores
C = {
    'verde_fill': '#E8F5E9',
    'verde_stroke': '#2E7D32',
    'verde_title': '#1B5E20',
    'verde_accent': '#4CAF50',
    
    'azul_fill': '#E3F2FD',
    'azul_stroke': '#1565C0',
    'azul_title': '#0D47A1',
    'azul_accent': '#2196F3',
    
    'naranja_fill': '#FFF3E0',
    'naranja_stroke': '#E65100',
    'naranja_title': '#BF360C',
    'naranja_accent': '#FF9800',
    
    'rojo_fill': '#FFEBEE',
    'rojo_stroke': '#C62828',
    'rojo_title': '#B71C1C',
    'rojo_accent': '#EF5350',
    
    'tanque_fill': '#FFF8E1',
    'tanque_stroke': '#E65100',
    'gris': '#9E9E9E',
    'texto': '#212121',
    'blanco': '#FFFFFF',
    'negro': '#000000'
}

def crear_caja(x, y, w, h, tipo, id_corriente, titulo, datos):
    """Crea una caja de balance"""
    colors = {
        'glucosa': ('verde_fill', 'verde_stroke', 'verde_title', 'verde_accent'),
        'agua': ('azul_fill', 'azul_stroke', 'azul_title', 'azul_accent'),
        'calor': ('naranja_fill', 'naranja_stroke', 'naranja_title', 'naranja_accent'),
        'perdida': ('rojo_fill', 'rojo_stroke', 'rojo_title', 'rojo_accent')
    }
    
    fill, stroke, title_col, accent = colors[tipo]
    
    svg = f'''
    <!-- Caja {id_corriente}: {titulo} -->
    <g id="caja-{id_corriente}">
        <!-- Sombra -->
        <rect x="{x+2}" y="{y+2}" width="{w}" height="{h}" rx="8" fill="{C['negro']}" opacity="0.1"/>
        <!-- Fondo -->
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{C[fill]}" stroke="{C[stroke]}" stroke-width="2"/>
        <!-- Barra superior -->
        <rect x="{x}" y="{y}" width="{w}" height="5" rx="8" fill="{C[accent]}"/>
        <rect x="{x}" y="{y+5}" width="{w}" height="3" fill="{C[accent]}" opacity="0.3"/>
        <!-- Titulo -->
        <text x="{x+10}" y="{y+22}" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="{C[title_col]}">{id_corriente}: {titulo}</text>
        <!-- Linea decorativa -->
        <line x1="{x+10}" y1="{y+28}" x2="{x+w-10}" y2="{y+28}" stroke="{C[accent]}" stroke-width="1.5" opacity="0.5"/>'''
    
    # Datos
    for i, dato in enumerate(datos):
        y_text = y + 43 + (i * 13)
        svg += f'''
        <text x="{x+10}" y="{y_text}" font-family="Consolas, monospace" font-size="9" fill="{C['texto']}">{dato}</text>'''
    
    svg += '''
    </g>'''
    return svg

def crear_indicador(x, y, num, tipo):
    """Crea un circulo indicador con numero"""
    color = C['verde_stroke'] if tipo == 'glucosa' else C['azul_stroke']
    
    return f'''
    <!-- Indicador {num} -->
    <g id="ind-{num}">
        <circle cx="{x}" cy="{y}" r="14" fill="{color}" stroke="{C['blanco']}" stroke-width="2"/>
        <text x="{x}" y="{y+4}" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="{C['blanco']}" text-anchor="middle">{num}</text>
    </g>'''

def crear_tanque():
    """Tanque T-101"""
    cx, cy = 380, 380
    w, h = 180, 240
    x = cx - w//2
    y = cy - h//2
    
    return f'''
    <!-- TANQUE T-101 -->
    <g id="tanque">
        <!-- Aislamiento -->
        <rect x="{x-6}" y="{y-6}" width="{w+12}" height="{h+12}" rx="15" fill="none" stroke="{C['gris']}" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.6"/>
        <!-- Cuerpo -->
        <rect x="{x}" y="{y+35}" width="{w}" height="{h-70}" fill="{C['tanque_fill']}" stroke="{C['tanque_stroke']}" stroke-width="2"/>
        <!-- Fondo torisferico -->
        <path d="M {x} {y+h-35} Q {cx} {y+h+15} {x+w} {y+h-35}" fill="{C['tanque_fill']}" stroke="{C['tanque_stroke']}" stroke-width="2"/>
        <!-- Tapa eliptica -->
        <path d="M {x} {y+35} Q {cx} {y-15} {x+w} {y+35}" fill="{C['tanque_fill']}" stroke="{C['tanque_stroke']}" stroke-width="2"/>
        <!-- Nivel 80% -->
        <line x1="{x+10}" y1="{y+100}" x2="{x+w-10}" y2="{y+100}" stroke="{C['azul_accent']}" stroke-width="2"/>
        <text x="{x+w+8}" y="{y+104}" font-size="9" fill="{C['azul_stroke']}" font-weight="bold">80%</text>
        <!-- Etiquetas -->
        <text x="{cx}" y="{cy-50}" font-size="14" font-weight="bold" fill="{C['tanque_stroke']}" text-anchor="middle">T-101</text>
        <text x="{cx}" y="{cy-35}" font-size="9" fill="{C['texto']}" text-anchor="middle">Tanque Almacenamiento</text>
        <text x="{cx}" y="{cy}" font-size="8" fill="{C['gris']}" text-anchor="middle" font-style="italic">Fondo Torisferico</text>
    </g>'''

def crear_bomba():
    """Bomba P-101"""
    cx, cy = 620, 380
    r = 28
    
    return f'''
    <!-- BOMBA P-101 -->
    <g id="bomba">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#E1BEE7" stroke="#7B1FA2" stroke-width="2"/>
        <path d="M {cx} {cy-12} L {cx-10} {cy+8} L {cx+10} {cy+8} Z" fill="{C['blanco']}" stroke="#7B1FA2" stroke-width="1.5"/>
        <line x1="{cx}" y1="{cy+8}" x2="{cx}" y2="{cy+20}" stroke="#7B1FA2" stroke-width="2"/>
        <text x="{cx}" y="{cy-40}" font-size="11" font-weight="bold" fill="#7B1FA2" text-anchor="middle">P-101</text>
        <text x="{cx}" y="{cy+32}" font-size="8" fill="{C['texto']}" text-anchor="middle">Bomba</text>
    </g>'''

def crear_chaqueta():
    """Chaqueta E-201"""
    x, y = 330, 520
    w, h = 100, 50
    
    serpentina = ''
    for i in range(4):
        y_line = y + 12 + i * 10
        if i % 2 == 0:
            serpentina += f'<line x1="{x+8}" y1="{y_line}" x2="{x+w-8}" y2="{y_line}" stroke="{C['azul_stroke']}" stroke-width="1.5"/>'
        else:
            serpentina += f'<line x1="{x+w-8}" y1="{y_line}" x2="{x+8}" y2="{y_line}" stroke="{C['azul_stroke']}" stroke-width="1.5"/>'
        if i < 3:
            serpentina += f'<line x1="{(x+8 if i%2 else x+w-8)}" y1="{y_line}" x2="{(x+8 if i%2 else x+w-8)}" y2="{y_line+10}" stroke="{C['azul_stroke']}" stroke-width="1.5"/>'
    
    return f'''
    <!-- CHAQUETA E-201 -->
    <g id="chaqueta">
        <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#B3E5FC" stroke="{C['azul_stroke']}" stroke-width="2" rx="4"/>
        {serpentina}
        <text x="{x+w//2}" y="{y-8}" font-size="10" font-weight="bold" fill="{C['azul_title']}" text-anchor="middle">E-201</text>
        <text x="{x+w//2}" y="{y+h+12}" font-size="8" fill="{C['texto']}" text-anchor="middle">Chaqueta</text>
    </g>'''

def crear_carrotanque():
    """Carrotanque"""
    x, y = 750, 320
    
    return f'''
    <!-- CARROTANQUE -->
    <g id="carrotanque">
        <!-- Cabina -->
        <rect x="{x}" y="{y}" width="55" height="45" fill="#FFEB3B" stroke="#FBC02D" stroke-width="2" rx="3"/>
        <rect x="{x+8}" y="{y+12}" width="28" height="18" fill="#B3E5FC" stroke="#0288D1" stroke-width="1"/>
        <!-- Tanque -->
        <rect x="{x+55}" y="{y-15}" width="95" height="60" fill="#BDBDBD" stroke="#616161" stroke-width="2" rx="3"/>
        <!-- Lineas del tanque -->
        <line x1="{x+75}" y1="{y-15}" x2="{x+75}" y2="{y+45}" stroke="#616161" stroke-width="1" opacity="0.4"/>
        <line x1="{x+102}" y1="{y-15}" x2="{x+102}" y2="{y+45}" stroke="#616161" stroke-width="1" opacity="0.4"/>
        <line x1="{x+130}" y1="{y-15}" x2="{x+130}" y2="{y+45}" stroke="#616161" stroke-width="1" opacity="0.4"/>
        <!-- Ruedas -->
        <circle cx="{x+22}" cy="{y+52}" r="7" fill="#424242"/>
        <circle cx="{x+82}" cy="{y+52}" r="7" fill="#424242"/>
        <circle cx="{x+132}" cy="{y+52}" r="7" fill="#424242"/>
        <!-- Etiqueta -->
        <text x="{x+75}" y="{y-25}" font-size="10" font-weight="bold" fill="#424242" text-anchor="middle">Carro Tanque</text>
    </g>'''

def crear_lineas():
    """Lineas de proceso con flechas"""
    return f'''
    <!-- LINEAS DE PROCESO -->
    <g id="lineas">
        <!-- Glucosa entrada -->
        <line x1="200" y1="200" x2="290" y2="280" stroke="{C['verde_accent']}" stroke-width="2.5"/>
        <polygon points="290,280 280,272 282,280 280,288" fill="{C['verde_accent']}"/>
        
        <!-- Glucosa tanque a bomba -->
        <line x1="470" y1="350" x2="592" y2="380" stroke="{C['verde_accent']}" stroke-width="2.5"/>
        
        <!-- Glucosa bomba a carrotanque -->
        <line x1="648" y1="380" x2="750" y2="350" stroke="{C['verde_accent']}" stroke-width="2.5"/>
        <polygon points="750,350 740,344 742,350 740,356" fill="{C['verde_accent']}"/>
        
        <!-- Agua entrada -->
        <line x1="180" y1="620" x2="340" y2="570" stroke="{C['azul_accent']}" stroke-width="2" stroke-dasharray="6,4"/>
        <polygon points="340,570 330,565 332,570 330,577" fill="{C['azul_accent']}"/>
        
        <!-- Agua salida -->
        <line x1="430" y1="570" x2="480" y2="670" stroke="{C['azul_accent']}" stroke-width="2" stroke-dasharray="6,4"/>
        <polygon points="480,670 472,662 475,670 472,678" fill="{C['azul_accent']}"/>
    </g>'''

def crear_titulo():
    """Titulo del diagrama"""
    return f'''
    <!-- TITULO -->
    <g id="titulo">
        <rect x="50" y="15" width="1100" height="40" rx="5" fill="#263238"/>
        <text x="600" y="42" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="{C['blanco']}" text-anchor="middle">PFD P2611 - Sistema de Almacenamiento y Carga de Glucosa</text>
        <text x="600" y="70" font-family="Arial, sans-serif" font-size="10" fill="{C['gris']}" text-anchor="middle">Balance de Materia y Energia - Escenario Optimizado (Agua 75C)</text>
    </g>'''

def generar_svg():
    """Genera el SVG completo"""
    
    # Cajas de balance
    cajas = ''
    
    # Corriente 1: Glucosa entrada
    cajas += crear_caja(20, 110, 165, 125, 'glucosa', '1', 'GLUCOSA ENTRADA', [
        'Flujo: 8,000 kg/h',
        'Temperatura: 57.0C',
        'Entalpia: 971.7 MJ/h',
        'Cp: 2.131 kJ/kgC',
        'Densidad: 1,405 kg/m3',
        'Viscosidad: 2,870 cP'
    ])
    
    # Corriente 4: Glucosa salida
    cajas += crear_caja(720, 170, 165, 125, 'glucosa', '4', 'GLUCOSA SALIDA', [
        'Flujo: 8,000 kg/h',
        'Temperatura: 55.1C',
        'Entalpia: 939.5 MJ/h',
        'Cp: 2.131 kJ/kgC',
        'Densidad: 1,405 kg/m3',
        'Viscosidad: 2,870 cP'
    ])
    
    # Corriente 2: Agua entrada
    cajas += crear_caja(20, 580, 165, 115, 'agua', '2', 'AGUA ENTRADA', [
        'Flujo: 57.7 m3/h',
        'Flujo: 56,258 kg/h',
        'Temperatura: 75.0C',
        'Entalpia: 17.69 GJ/h',
        'Cp: 4.192 kJ/kgC',
        'Densidad: 975 kg/m3'
    ])
    
    # Corriente 3: Agua salida
    cajas += crear_caja(480, 680, 165, 75, 'agua', '3', 'AGUA SALIDA', [
        'Flujo: 56,258 kg/h',
        'Temperatura: 74.9C',
        'Entalpia: 17.67 GJ/h'
    ])
    
    # Q Chaqueta
    cajas += crear_caja(250, 530, 155, 70, 'calor', 'Q', 'TRANSFERENCIA CALOR', [
        'Q = 18.9 MJ/h',
        'U = 36.2 W/m2C',
        'A = 13 m2'
    ])
    
    # Q Perdidas
    cajas += crear_caja(550, 90, 140, 55, 'perdida', 'Q', 'PERDIDAS TERMICAS', [
        'Q = 51.1 MJ/h',
        'dT = 3C'
    ])
    
    # Indicadores
    indicadores = ''
    indicadores += crear_indicador(245, 240, '1', 'glucosa')
    indicadores += crear_indicador(310, 600, '2', 'agua')
    indicadores += crear_indicador(455, 620, '3', 'agua')
    indicadores += crear_indicador(530, 280, '4', 'glucosa')
    
    # SVG completo
    svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
    <title>PFD P2611 - Balance de Materia y Energia</title>
    <desc>Diagrama de Flujo de Proceso con balance</desc>
    
    <!-- Fondo blanco -->
    <rect width="{WIDTH}" height="{HEIGHT}" fill="{C['blanco']}"/>
    
    {crear_titulo()}
    {crear_tanque()}
    {crear_bomba()}
    {crear_chaqueta()}
    {crear_carrotanque()}
    {crear_lineas()}
    {cajas}
    {indicadores}
</svg>'''
    
    # Guardar
    output_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'PFD_P2611_LIMPIO.svg')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    return output_path

if __name__ == '__main__':
    print('=' * 70)
    print('GENERADOR DE PFD LIMPIO - PROYECTO P2611')
    print('=' * 70)
    print()
    
    path = generar_svg()
    
    print(f'[OK] Archivo creado: {path}')
    print()
    print('CARACTERISTICAS:')
    print('  - SVG nativo limpio (sin codificacion draw.io)')
    print('  - Posiciones ajustadas para evitar solapamientos')
    print('  - Sin caracteres especiales problematicos')
    print('  - 4 equipos + 6 cajas de balance + 4 indicadores')
    print('  - Lineas de proceso con flechas')
    print()
    print('Abre el archivo en cualquier navegador o Inkscape')
    print('=' * 70)
