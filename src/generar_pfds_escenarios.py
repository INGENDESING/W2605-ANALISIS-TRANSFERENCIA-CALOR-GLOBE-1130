"""
Generador de PFDs vectoriales (SVG) para los escenarios del Proyecto P2611.
Parte del SVG base PFD_Escenario_01A.svg corregido y genera 01B, 01C y 02A.
Usa reemplazos robustos por ID para tolerar formato multilinea del SVG.
"""

import csv
import os
import re
from decimal import Decimal, ROUND_HALF_UP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, '..', 'results')


def leer_csv_escenario(codigo):
    """Lee el CSV de un subescenario y retorna la fila con v_viento=1.5 m/s."""
    path = os.path.join(RESULTS_DIR, f'escenario_{codigo}_resultados.csv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row['v_viento_m_s']) == 1.5:
                return row
    raise ValueError(f"No se encontro v=1.5 en {path}")


def fmt_half_up(valor, decimales=1):
    """Redondeo half-up usando Decimal para evitar errores de representacion binaria."""
    d = Decimal(str(valor))
    quant = Decimal('0.1') ** decimales
    return str(d.quantize(quant, rounding=ROUND_HALF_UP))


def formatear_numero(valor, decimales=1):
    """Formatea un numero con separador de miles y decimales especificados."""
    s = fmt_half_up(valor, decimales)
    if decimales > 0:
        s = s.replace('.', ',')
    # Separador de miles
    entero, *decimal = s.split(',')
    entero_fmt = '{:,}'.format(int(entero)).replace(',', '.')
    if decimal:
        return f"{entero_fmt},{decimal[0]}"
    return entero_fmt


def reemplazar_texto_por_id(svg, elem_id, nuevo_valor):
    """Reemplaza el contenido textual de un elemento <text> dado su id."""
    esc_id = re.escape(elem_id)
    pattern = '(<text\\b(?:[^>]|\n)*?\\bid="' + esc_id + '"(?:[^>]|\n)*?>)([^<]*)(</text>)'
    def replacer(m):
        return m.group(1) + nuevo_valor + m.group(3)
    nuevo_svg, count = re.subn(pattern, replacer, svg, count=1, flags=re.DOTALL)
    if count == 0:
        print(f"  ADVERTENCIA: no se encontro elemento text id={elem_id}")
    return nuevo_svg


def generar_pfds():
    template_path = os.path.join(RESULTS_DIR, 'PFD_Escenario_01A.svg')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    config_escenarios = {
        '01A': {
            'subescenarios': ['01a_1', '01a_2', '01a_3'],
            'T_agua': 65.0,
            'Q_agua': 30.9,
            'area': 13,
            'titulo': 'PFD ESCENARIO 01A',
            'titulo_tabla': 'BALANCE ENERGÉTICO — ESCENARIO 01A',
        },
        '01B': {
            'subescenarios': ['01b_1', '01b_2', '01b_3'],
            'T_agua': 65.0,
            'Q_agua': 57.7,
            'area': 13,
            'titulo': 'PFD ESCENARIO 01B',
            'titulo_tabla': 'BALANCE ENERGÉTICO — ESCENARIO 01B',
        },
        '01C': {
            'subescenarios': ['01c_1', '01c_2', '01c_3'],
            'T_agua': 75.0,
            'Q_agua': 57.7,
            'area': 13,
            'titulo': 'PFD ESCENARIO 01C',
            'titulo_tabla': 'BALANCE ENERGÉTICO — ESCENARIO 01C',
        },
        '02A': {
            'subescenarios': ['02a_1', '02a_2', '02a_3'],
            'T_agua': 75.0,
            'Q_agua': 57.7,
            'area': 28,
            'titulo': 'PFD ESCENARIO 02A',
            'titulo_tabla': 'BALANCE ENERGÉTICO — ESCENARIO 02A',
        },
    }

    for esc_key, cfg in config_escenarios.items():
        print(f"\nGenerando {esc_key}...")
        svg = template

        datos = [leer_csv_escenario(sub) for sub in cfg['subescenarios']]

        # --- Reemplazos generales ---
        svg = svg.replace('PFD ESCENARIO 01A — Sistema de Almacenamiento de Glucosa',
                          f"{cfg['titulo']} — Sistema de Almacenamiento de Glucosa")
        svg = svg.replace('BALANCE ENERGÉTICO — ESCENARIO 01A', cfg['titulo_tabla'])

        old_subtitulo = (
            "Agua caliente 65 °C  ·  Caudal agua 30,900 kg/h  ·  "
            "Área chaqueta 13 m²  ·  Viento 1.5 m/s  ·  Caudal glucosa 8,000 kg/h"
        )
        new_subtitulo = (
            f"Agua caliente {cfg['T_agua']:.0f} °C  ·  Caudal agua {cfg['Q_agua']*1000:,.0f} kg/h  ·  "
            f"Área chaqueta {cfg['area']} m²  ·  Viento 1.5 m/s  ·  Caudal glucosa 8,000 kg/h"
        ).replace(',', '.')
        svg = svg.replace(old_subtitulo, new_subtitulo)

        # Corriente 2 - Agua entrada (text115)
        svg = reemplazar_texto_por_id(
            svg, 'text115',
            f"{formatear_numero(cfg['Q_agua']*1000, 0)} kg/h  |  {fmt_half_up(cfg['T_agua'], 1).replace('.', ',')} °C"
        )

        # Corriente 2 - entalpia (text116)
        H_in_ref = float(datos[0]['H_agua_in_MJ_h'])
        svg = reemplazar_texto_por_id(
            svg, 'text116',
            f"{formatear_numero(H_in_ref, 1)} MJ/h  ·  {fmt_half_up(cfg['Q_agua'], 1).replace('.', ',')} m³/h"
        )

        # Corriente 3 - Agua salida (text120)
        T_agua_out_0 = float(datos[0]['T_agua_out_C'])
        svg = reemplazar_texto_por_id(
            svg, 'text120',
            f"{formatear_numero(cfg['Q_agua']*1000, 0)} kg/h  |  {fmt_half_up(T_agua_out_0, 1).replace('.', ',')} °C"
        )

        # Corriente 3 - entalpia salida (text121)
        H_out_ref = float(datos[0]['H_agua_out_MJ_h'])
        svg = reemplazar_texto_por_id(
            svg, 'text121',
            f"{formatear_numero(H_out_ref, 1)} MJ/h"
        )

        # Corriente 3 - Q transferido rango (text122)
        q_min = min(float(d['Q_chaqueta_MJ_h']) for d in datos)
        q_max = max(float(d['Q_chaqueta_MJ_h']) for d in datos)
        svg = reemplazar_texto_por_id(svg, 'text122', f"Q transferido: {fmt_half_up(q_min, 1).replace('.', ',')} – {fmt_half_up(q_max, 1).replace('.', ',')} MJ/h")

        # --- Tabla de balance energetico ---
        # Q Transferido (text130, 131, 132)
        svg = reemplazar_texto_por_id(svg, 'text130', fmt_half_up(datos[0]['Q_chaqueta_MJ_h'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text131', fmt_half_up(datos[1]['Q_chaqueta_MJ_h'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text132', fmt_half_up(datos[2]['Q_chaqueta_MJ_h'], 1).replace('.', ','))

        # Q Perdidas (text134, 135, 136)
        svg = reemplazar_texto_por_id(svg, 'text134', fmt_half_up(datos[0]['Q_perdidas_MJ_h'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text135', fmt_half_up(datos[1]['Q_perdidas_MJ_h'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text136', fmt_half_up(datos[2]['Q_perdidas_MJ_h'], 1).replace('.', ','))

        # Q Neto (text138, 139, 140)
        def fmt_qnet(val):
            v = float(val)
            v = float(val)
            s = fmt_half_up(v, 1).replace('.', ',')
            if v < 0:
                return f"\u2212{s.lstrip('-')}"
            else:
                return f"+{s}"

        svg = reemplazar_texto_por_id(svg, 'text138', fmt_qnet(datos[0]['Q_net_MJ_h']))
        svg = reemplazar_texto_por_id(svg, 'text139', fmt_qnet(datos[1]['Q_net_MJ_h']))
        svg = reemplazar_texto_por_id(svg, 'text140', fmt_qnet(datos[2]['Q_net_MJ_h']))

        # T salida glucosa (text142, 143, 144)
        svg = reemplazar_texto_por_id(svg, 'text142', fmt_half_up(datos[0]['T_salida_C'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text143', fmt_half_up(datos[1]['T_salida_C'], 1).replace('.', ','))
        svg = reemplazar_texto_por_id(svg, 'text144', fmt_half_up(datos[2]['T_salida_C'], 1).replace('.', ','))

        # Parametros del sistema - U chaqueta (text148 contiene tspan)
        u_vals = [float(d['U_chaqueta_W_m2K']) for d in datos]
        u_min, u_max = min(u_vals), max(u_vals)
        if abs(u_max - u_min) < 0.1:
            u_str = fmt_half_up(u_min, 1).replace('.', ',')
        else:
            u_str = f"{fmt_half_up(u_min, 1).replace('.', ',')} – {fmt_half_up(u_max, 1).replace('.', ',')}"
        svg, cnt_u = re.subn(
            r'(<text\b(?:[^>]|\n)*?\bid="text148"(?:[^>]|\n)*?>).*?(</text>)',
            lambda m: f'{m.group(1)}<tspan\n   font-weight="600"\n   fill="#BF360C"\n   id="tspan147">U chaqueta:</tspan> {u_str} W/(m\u00b2·K)  (calculado){m.group(2)}',
            svg, count=1, flags=re.DOTALL
        )
        if cnt_u == 0:
            print("  ADVERTENCIA: no se reemplazo U chaqueta")

        # Parametros del sistema - h_i y h_o (text149 contiene 2 tspans)
        h_i_vals = [float(d['h_i_W_m2K']) for d in datos]
        h_o_vals = [float(d['h_o_W_m2K']) for d in datos]
        h_i_str = f"{sum(h_i_vals)/len(h_i_vals):.0f}"
        if abs(max(h_o_vals) - min(h_o_vals)) < 0.1:
            h_o_str = fmt_half_up(min(h_o_vals), 1).replace('.', ',')
        else:
            h_o_str = f"{fmt_half_up(min(h_o_vals), 1).replace('.', ',')} – {fmt_half_up(max(h_o_vals), 1).replace('.', ',')}"
        svg, cnt_h = re.subn(
            r'(<text\b(?:[^>]|\n)*?\bid="text149"(?:[^>]|\n)*?>).*?(</text>)',
            lambda m: f'{m.group(1)}<tspan\n   font-weight="600"\n   fill="#0D47A1"\n   id="tspan148">h_i (agua):</tspan> ~{h_i_str} W/(m\u00b2·K)   |   <tspan\n   font-weight="600"\n   fill="#E65100"\n   id="tspan149">h_o (glucosa):</tspan> ~{h_o_str} W/(m\u00b2·K){m.group(2)}',
            svg, count=1, flags=re.DOTALL
        )
        if cnt_h == 0:
            print("  ADVERTENCIA: no se reemplazo h_i/h_o")

        # Guardar SVG
        out_path = os.path.join(RESULTS_DIR, f'PFD_Escenario_{esc_key}.svg')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"Generado: {out_path}")


if __name__ == "__main__":
    generar_pfds()
