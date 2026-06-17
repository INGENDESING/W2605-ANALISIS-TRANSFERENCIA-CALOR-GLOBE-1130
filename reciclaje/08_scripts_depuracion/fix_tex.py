import re

with open('docs/report/W2605-PR-INF-003.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Tabla 02A-1
old1 = r"""Temperatura glucosa entrada & \circ & 60.0 & 60.0 & 60.0 \\\\ 
Temperatura glucosa salida & \circ & \textbf{58.55} & \textbf{58.13} & \textbf{57.27} \\\\ 
Temperatura agua entrada & \circ & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & \circ & 64.97 & 64.97 & 64.97 \\\\ 
\midrule
$ (chaqueta) & W/m2\cdot^\circ & 25.2 & 25.4 & 25.7 \\\\ 
{\text{ext}}$ (viento) & W/m2\cdot^\circ & 2.41 & 3.29 & 5.79 \\\\ 
\midrule
Calor transferido & MJ/h & 6.7 & 7.0 & 7.5 \\\\ 
Pérdidas térmicas & MJ/h & 31.4 & 38.9 & 54.1 \\\\ 
Balance neto & MJ/h & $-.7 & $-.9 & $-.6 \\\\ """
new1 = r"""Temperatura glucosa entrada & $^\circ$C & 60.0 & 60.0 & 60.0 \\\\ 
Temperatura glucosa salida & $^\circ$C & \textbf{58.55} & \textbf{58.13} & \textbf{57.27} \\\\ 
Temperatura agua entrada & $^\circ$C & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & $^\circ$C & 64.97 & 64.97 & 64.97 \\\\ 
\midrule
$U$ (chaqueta) & W/m$^2\cdot^\circ$C & 25.2 & 25.4 & 25.7 \\\\ 
$h_{\text{ext}}$ (viento) & W/m$^2\cdot^\circ$C & 2.41 & 3.29 & 5.79 \\\\ 
\midrule
Calor transferido & MJ/h & 6.7 & 7.0 & 7.5 \\\\ 
Pérdidas térmicas & MJ/h & 31.4 & 38.9 & 54.1 \\\\ 
Balance neto & MJ/h & $-$24.7 & $-$31.9 & $-$46.6 \\\\ """

if old1 in content:
    content = content.replace(old1, new1)
    print('Reemplazo 02A-1 OK')
else:
    print('ERROR: old1 no encontrado')

# Tabla 02A-2
old2 = r"""Temperatura glucosa entrada & \circ & 57.0 & 57.0 & 57.0 \\\\ 
Temperatura glucosa salida & \circ & \textbf{55.94} & \textbf{55.55} & \textbf{54.76} \\\\ 
Temperatura agua entrada & \circ & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & \circ & 64.92 & 64.92 & 64.91 \\\\ 
\midrule
Calor transferido & MJ/h & 10.7 & 11.0 & 11.5 \\\\ 
Pérdidas térmicas & MJ/h & 28.8 & 35.7 & 49.6 \\\\ 
Balance neto & MJ/h & $-.1 & $-.7 & $-.1 \\\\ """
new2 = r"""Temperatura glucosa entrada & $^\circ$C & 57.0 & 57.0 & 57.0 \\\\ 
Temperatura glucosa salida & $^\circ$C & \textbf{55.94} & \textbf{55.55} & \textbf{54.76} \\\\ 
Temperatura agua entrada & $^\circ$C & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & $^\circ$C & 64.92 & 64.92 & 64.91 \\\\ 
\midrule
Calor transferido & MJ/h & 10.7 & 11.0 & 11.5 \\\\ 
Pérdidas térmicas & MJ/h & 28.8 & 35.7 & 49.6 \\\\ 
Balance neto & MJ/h & $-$18.1 & $-$24.8 & $-$38.1 \\\\ """

if old2 in content:
    content = content.replace(old2, new2)
    print('Reemplazo 02A-2 OK')
else:
    print('ERROR: old2 no encontrado')

# Tabla 02A-3
old3 = r"""Temperatura glucosa entrada & \circ & 54.0 & 54.0 & 54.0 \\\\ 
Temperatura glucosa salida & \circ & \textbf{53.32} & \textbf{52.97} & \textbf{52.25} \\\\ 
Temperatura agua entrada & \circ & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & \circ & 64.89 & 64.89 & 64.88 \\\\ 
\midrule
Calor transferido & MJ/h & 14.6 & 14.9 & 15.3 \\\\ 
Pérdidas térmicas & MJ/h & 26.2 & 32.4 & 45.1 \\\\ 
Balance neto & MJ/h & $-.6 & $-.5 & $-.8 \\\\ """
new3 = r"""Temperatura glucosa entrada & $^\circ$C & 54.0 & 54.0 & 54.0 \\\\ 
Temperatura glucosa salida & $^\circ$C & \textbf{53.32} & \textbf{52.97} & \textbf{52.25} \\\\ 
Temperatura agua entrada & $^\circ$C & 65.0 & 65.0 & 65.0 \\\\ 
Temperatura agua salida & $^\circ$C & 64.89 & 64.89 & 64.88 \\\\ 
\midrule
Calor transferido & MJ/h & 14.6 & 14.9 & 15.3 \\\\ 
Pérdidas térmicas & MJ/h & 26.2 & 32.4 & 45.1 \\\\ 
Balance neto & MJ/h & $-$11.6 & $-$17.5 & $-$29.8 \\\\ """

if old3 in content:
    content = content.replace(old3, new3)
    print('Reemplazo 02A-3 OK')
else:
    print('ERROR: old3 no encontrado')

with open('docs/report/W2605-PR-INF-003.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print('Archivo actualizado')
