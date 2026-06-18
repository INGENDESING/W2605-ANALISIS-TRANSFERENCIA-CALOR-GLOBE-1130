import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometria_tanque import A_CONTACTO

base_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'PFD_Escenario_01A.svg')
with open(base_path, 'r', encoding='utf-8') as f:
    base = f.read()

escenarios = [
    {
        'suffix': '02B_1',
        'title_num': '02B-1',
        'glucosa_in_c': '60',
        'glucosa_in_mj': '1,022',
        'agua_out_c': '74.9',
        'agua_out_mj': '17,796',
        'q_range': '25.7-26.8',
        't4a': '59.64', 'h4a': '1,016',
        't4b': '59.21', 'h4b': '1,009',
        't4c': '58.35', 'h4c': '994',
        'q_trans': ['25.7','26.0','26.8'],
        'q_perd': ['31.9','39.5','54.9'],
        'q_net': ['-6.2','-13.5','-28.2'],
        'msg': 'Pérdidas exceden 1.2-2.1 veces el calor transferido',
        'u_val': '36.3',
        'h_o_val': '36.3',
    },
    {
        'suffix': '02B_2',
        'title_num': '02B-2',
        'glucosa_in_c': '57',
        'glucosa_in_mj': '971',
        'agua_out_c': '74.87',
        'agua_out_mj': '17,781',
        'q_range': '30.4-31.3',
        't4a': '57.06', 'h4a': '972',
        't4b': '56.67', 'h4b': '965',
        't4c': '55.88', 'h4c': '952',
        'q_trans': ['30.4','30.7','31.3'],
        'q_perd': ['29.3','36.3','50.5'],
        'q_net': ['+1.1','-5.6','-19.2'],
        'msg': 'Balance energético marginal: pérdidas equivalentes al 96-161% del calor transferido',
        'u_val': '36.2',
        'h_o_val': '36.2',
    },
    {
        'suffix': '02B_3',
        'title_num': '02B-3',
        'glucosa_in_c': '54',
        'glucosa_in_mj': '920',
        'agua_out_c': '74.85',
        'agua_out_mj': '17,766',
        'q_range': '34.7-35.6',
        't4a': '54.47', 'h4a': '928',
        't4b': '54.11', 'h4b': '922',
        't4c': '53.39', 'h4c': '910',
        'q_trans': ['34.7','35.0','35.6'],
        'q_perd': ['26.7','33.1','46.0'],
        'q_net': ['+8.0','+1.9','-10.4'],
        'msg': 'Balance energético positivo en condiciones de viento bajo',
        'u_val': '35.8',
        'h_o_val': '35.8',
    },
]

for esc in escenarios:
    svg = base
    tn = esc['title_num']
    sfx = esc['suffix']
    
    svg = svg.replace('PFD Escenario 01A - Proyecto W2605', f'PFD Escenario {tn} - Proyecto W2605')
    svg = svg.replace('Diagrama de Flujo de Proceso - Escenario 01A con tres velocidades de viento',
                      f'Diagrama de Flujo de Proceso - Escenario {tn} con tres velocidades de viento')
    svg = svg.replace('PFD_Escenario_01A.svg', f'PFD_Escenario_{sfx}.svg')
    svg = svg.replace('PFD_Escenario_01A.pdf', f'PFD_Escenario_{sfx}.pdf')
    svg = svg.replace('PFD ESCENARIO 01A - Sistema de Almacenamiento de Glucosa',
                      f'PFD ESCENARIO {tn} - Sistema de Almacenamiento de Glucosa')
    
    old_sub = f'Agua 65°C | Caudal 30,900 kg/h | Area {A_CONTACTO:.0f} m² | Glucosa 60°C | Caudal 8,000 kg/h'
    new_sub = f'Agua 75°C | Caudal 57,700 kg/h | Area {A_CONTACTO:.0f} m² | Glucosa {esc["glucosa_in_c"]}°C | Caudal 8,000 kg/h'
    svg = svg.replace(old_sub, new_sub)
    
    old_c1 = '8,000 kg/h | 60.0°C | 1,024 MJ/h'
    new_c1 = f'8,000 kg/h | {esc["glucosa_in_c"]}.0°C | {esc["glucosa_in_mj"]} MJ/h'
    svg = svg.replace(old_c1, new_c1)
    
    old_c2 = '30,900 kg/h | 65.0°C | 8,224 MJ/h'
    new_c2 = '57,700 kg/h | 75.0°C | 17,822 MJ/h'
    svg = svg.replace(old_c2, new_c2)
    
    svg = svg.replace('30.9 m³/h | Cp = 4.18 kJ/kg·K', '57.7 m³/h | Cp = 4.18 kJ/kg·K')
    
    old_c3 = '30,900 kg/h | 64.9°C | 8,218 MJ/h'
    new_c3 = f'57,700 kg/h | {esc["agua_out_c"]}°C | {esc["agua_out_mj"]} MJ/h'
    svg = svg.replace(old_c3, new_c3)
    
    svg = svg.replace('Q transferido: 6.7-7.5 MJ/h', f'Q transferido: {esc["q_range"]} MJ/h')
    
    old_4a = '8,000 kg/h | 58.55°C | 999 MJ/h'
    new_4a = f'8,000 kg/h | {esc["t4a"]}°C | {esc["h4a"]} MJ/h'
    svg = svg.replace(old_4a, new_4a)
    
    old_4b = '8,000 kg/h | 58.13°C | 992 MJ/h'
    new_4b = f'8,000 kg/h | {esc["t4b"]}°C | {esc["h4b"]} MJ/h'
    svg = svg.replace(old_4b, new_4b)
    
    old_4c = '8,000 kg/h | 57.27°C | 977 MJ/h'
    new_4c = f'8,000 kg/h | {esc["t4c"]}°C | {esc["h4c"]} MJ/h'
    svg = svg.replace(old_4c, new_4c)
    
    svg = svg.replace('BALANCE ENERGÉTICO - ESCENARIO 01A', f'BALANCE ENERGÉTICO - ESCENARIO {tn}')
    
    svg = svg.replace('>6.7<', f'>{esc["q_trans"][0]}<')
    svg = svg.replace('>7.0<', f'>{esc["q_trans"][1]}<')
    svg = svg.replace('>7.5<', f'>{esc["q_trans"][2]}<')
    svg = svg.replace('>31.4<', f'>{esc["q_perd"][0]}<')
    svg = svg.replace('>38.9<', f'>{esc["q_perd"][1]}<')
    svg = svg.replace('>54.1<', f'>{esc["q_perd"][2]}<')
    svg = svg.replace('>-24.7<', f'>{esc["q_net"][0]}<')
    svg = svg.replace('>-31.9<', f'>{esc["q_net"][1]}<')
    svg = svg.replace('>-46.6<', f'>{esc["q_net"][2]}<')
    
    svg = svg.replace('Pérdidas exceden 4.7-7.2 veces el calor transferido', esc['msg'])
    svg = svg.replace('U chaqueta: 25.2-25.7 W/m²K (calculado)', f'U chaqueta: {esc["u_val"]} W/m²K (calculado)')
    svg = svg.replace('h_i (agua): ~6,490 W/m²K | h_o (glucosa): ~25-26 W/m²K',
                      f'h_i (agua): ~11,300 W/m²K | h_o (glucosa): ~{esc["h_o_val"]} W/m²K')
    
    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', f'PFD_Escenario_{sfx}.svg')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Escrito {out_path}')
