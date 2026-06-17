# Contexto del proyecto: W2605 — Análisis térmico del fondo del tanque de glucosa

## Estado actual
- **Última tarea completada:** Validación final de compilación LaTeX, tests Python y coherencia numérica (17 de junio de 2026).
- **Próxima tarea pendiente:** Ninguna crítica pendiente; proyecto en estado de entrega final.
- **Fecha de última actualización:** 17 de junio de 2026.

## Bases de diseño congeladas
- **Cliente:** Ingredion S.A., Planta Cali, Colombia.
- **Equipo:** Tanque de almacenamiento de glucosa Tag 53A-90A-0056, fondo toriesférico de reemplazo en construcción.
- **Fluido:** Glucosa Globe 42 DE (80,6 °Brix aprox.).
- **Material:** Acero inoxidable SS316L.
- **Geometría:** Diámetro interior 5,264 m; altura cilíndrica 9,670 m; fondo toriesférico con espesor 9 mm.
- **Chaqueta:** Media caña rectangular en espiral, área de contacto 13 m², perfil interno 141 mm × 45,5 mm.
- **Ciclo operativo oficial:** 5 descargas/día de 24 ton, 2,0 h de descarga, intervalo entre inicios 4,8 h, flujo medio 5.000 kg/h.
- **Condiciones de servicio:** agua de calentamiento 75 °C, velocidad en media caña 2,5 m/s, aislamiento 50,8 mm de lana mineral.
- **Normas de referencia:** API 650, ASME VIII Div. 1, ASME B31.1, ASME B31.3.
- **Propiedades termofísicas:** correlaciones ajustadas a ficha técnica Ingredion 011420 (viscosidad VFT, Cp Choi-Okos, densidad lineal).

## Decisiones de diseño clave
- **Correlación lado agua:** Sieder-Tate para flujo turbulento en conducto rectangular (Incropera et al., 7ª ed.).
- **Correlación lado glucosa:** Churchill-Chu para convección natural (Incropera et al., 7ª ed.).
- **Modelo de pérdidas térmicas:** resistencias en serie con aislamiento de lana mineral 50,8 mm (k = 0,045 W/(m·°C)); valor actualizado 14,7 MJ/h con área real expuesta A_total ≈ 150 m² a 60 °C (17 de junio de 2026). El caso sin aislamiento arroja 175,4 MJ/h, lo que representa una reducción del 91,6 %.
- **Temperatura de operación adoptada:** 60 °C, con balance neto positivo de +15,3 MJ/h y eficiencia térmica del 67,2 %.
- **Tiempo de enfriamiento en parada:** 4,5 días para perder 3 °C desde 60 °C.
- **Límite operativo seguro:** 80 % de capacidad (178,2 m³ / 251 t) por FS ≥ 1,3 en unión fondo-cilindro.
- **Vida útil proyectada:** 7,5 años (tasa corrosión 0,120 mm/año) o 14,4 años (tasa histórica 0,0625 mm/año).

## Archivos clave y su propósito
- `docs/report/W2605PRINF001.tex` — Informe técnico principal (memoria descriptiva, 54 páginas).
- `docs/report/W2605PRINF002.tex` — Resumen ejecutivo gerencial (5 páginas).
- `src/coeficiente_U.py` — Cálculo del coeficiente global de transferencia de calor.
- `src/escenarios.py` — Simulación transitoria de calentamiento batch (Escenarios 1, 2, 3).
- `src/ciclo_descargas.py` — Simulación del ciclo de 5 descargas diarias.
- `src/comparativa_chaquetas.py` — Comparativa dimple vs. media caña.
- `src/calcular_areas.py` — Área requerida para calentamiento continuo.
- `src/aislamiento.py` — Dimensionamiento de aislamiento térmico.
- `src/perdidas_termicas_real.py` — Pérdidas térmicas con área real expuesta y aislamiento de lana mineral.
- `webapp/app/core/balance_energia.py` — Motor de simulación cíclica usado por tests y webapp.
- `task/test_ciclo.py` / `task/test_simulacion_50C.py` — Tests del ciclo oficial.

## Preguntas abiertas / bloqueos
- [ ] Confirmación del cliente sobre el valor de diseño de pérdidas térmicas (4,6 MJ/h vs. cálculo detallado con área total real).
- [ ] Definición del programa de instalación del aislamiento y puesta en marcha del lazo de control de temperatura.

## Comandos / workflows útiles
```bash
# Compilar informes (desde docs/report/)
pdflatex -interaction=nonstopmode W2605PRINF001.tex
bibtex W2605PRINF001
pdflatex -interaction=nonstopmode W2605PRINF001.tex
pdflatex -interaction=nonstopmode W2605PRINF001.tex

pdflatex -interaction=nonstopmode W2605PRINF002.tex
pdflatex -interaction=nonstopmode W2605PRINF002.tex

# Ejecutar tests
./venv/Scripts/python.exe -u task/test_ciclo.py
./venv/Scripts/python.exe -u task/test_simulacion_50C.py
cd webapp && ../venv/Scripts/python.exe -u tests/test_api.py

# Regenerar figuras principales
cd src
../venv/Scripts/python.exe coeficiente_U.py
../venv/Scripts/python.exe escenarios.py
../venv/Scripts/python.exe ciclo_descargas.py
../venv/Scripts/python.exe comparativa_chaquetas.py
../venv/Scripts/python.exe calcular_areas.py
```
