#!/usr/bin/env python3
import sys

# Read file
with open('../docs/report/W2605-PR-INF-003.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start and end lines of the figure
start_line = None
end_line = None

for i, line in enumerate(lines):
    if 'FIGURA: PFD ESCENARIO 01A (MEJORADA)' in line:
        start_line = i
    if start_line is not None and '\\end{figure}' in line and end_line is None:
        end_line = i
        break

if start_line is not None and end_line is not None:
    new_figure = '''% -------------------- FIGURA: PFD ESCENARIO 01A (PDF) --------------------
\\begin{figure}[H]
\\centering
\\includegraphics[width=\\textwidth]{../results/PFD_Escenario_01A.pdf}
\\caption{Diagrama de flujo de proceso (PFD) detallado --- Escenario 01A: agua de servicio a 65$^\\circ$C, caudal 30,900~kg/h, área de transferencia 13~m$^2$, glucosa entrando a 60$^\\circ$C. Comparativa de temperatura de salida para velocidades de viento 1.0~m/s, 1.5~m/s y 3.0~m/s.}
\\label{fig:pfd_escenario_01a}
\\end{figure}
'''
    new_lines = lines[:start_line] + [new_figure] + lines[end_line+1:]
    
    with open('../docs/report/W2605-PR-INF-003.tex', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f'Figure replaced successfully (lines {start_line+1} to {end_line+1})')
    sys.exit(0)
else:
    print('Could not find figure boundaries')
    sys.exit(1)
