# Contexto del proyecto: W2605 — Fondo de tanque de glucosa

## Estado actual
- Última tarea completada: Actualización de la aplicación web (`webapp/`): integración de los nuevos análisis del proyecto (ciclo a 12 m³/h con 14 m², pérdidas térmicas con área real, calentamiento de 24 ton, capacidad operativa), refactor import-safe de los scripts de `src/`, servicio estático de figuras desde `results/figures/`, ampliación de tests a 14 casos (OK), actualización de documentación y sincronización con GitHub.
- Próxima tarea pendiente: Ninguna crítica pendiente; proyecto listo para entrega final.
- Fecha de última actualización: 2026-06-17T16:45:00-05:00.

## Bases de diseño congeladas
- Capacidad operativa: máximo 5 descargas/día, 24 ton/descarga, 120 ton/día.
- Caudal medio de glucosa: 5.000 kg/h.
- Duración de descarga: 2,0 h; periodo de ciclo: 4,8 h.
- Temperatura de operación objetivo de la glucosa: 60 °C.
- Masa inicial en simulaciones de ciclo: 80 % del volumen operativo (~250 ton).
- Aislamiento térmico: lana mineral 50,8 mm, k = 0,045 W/(m·°C).
- Área expuesta real del tanque al 80 % de llenado: 149,7 m².
- Coeficiente global con aislamiento: U ≈ 0,38 W/(m²·°C).
- Pérdidas térmicas con aislamiento a 60 °C: 14,7 MJ/h.
- Pérdidas térmicas sin aislamiento a 60 °C: 175,4 MJ/h.
- Reducción de pérdidas por aislamiento: 91,6 %.
- Código de proyecto: W2605 (P2611 eliminado de archivos activos).
- Empresa: DMV SAS.
- Normas: API 650, ASME VIII, ASME B31.3, RETIE, NSR-10.

## Decisiones de diseño clave
- (2026-06-17) Se adoptó el encabezado estilo tercero con logo de DMV SAS para W2605PRINF001 y W2605PRINF002, manteniendo el encabezado corporativo estándar disponible en `config/header.tex`.
- (2026-06-17) Se recalculó pérdidas térmicas usando el área real expuesta (149,7 m²) en lugar de la estimación simplificada (~30 m²), elevando el valor de diseño de 4,6 MJ/h a 14,7 MJ/h.
- (2026-06-17) Se aplicó la correlación de Churchill-Chu para convección natural del lado de la glucosa, con h_o en el rango 18–37 W/(m²·°C).
- (2026-06-17) Se unificó el ciclo operativo oficial: 5 descargas/día, 2 h de descarga, periodo 4,8 h.
- (2026-06-17) Se completó auditoría crítica del informe de tercero GTTP-1004 Rev.5 en `auditoria1.md` y `InformeTercero/auditoria.md`.
- (2026-06-17) Se añadió la sección 9 al informe técnico con el caso de estudio de calentamiento de 24 ton de glucosa desde 40 °C hasta 60 °C con área de 14 m², para agua de calentamiento a 65 °C y 75 °C.
- (2026-06-17) Se añadió la sección 15 al informe técnico con el análisis de factibilidad térmica del ciclo de 5 descargas diarias a 12 m³/h con chaqueta de 14 m² y agua a 75 °C; resultado: T_min = 58,55 °C (cumple ≥ 57 °C).
- (2026-06-17) Se añadió al resumen ejecutivo W2605PRINF002 una sección de factibilidad térmica del ciclo a 12 m³/h con tabla resumen y referencia a la Sección 15 del informe técnico.
- (2026-06-17) Se corrigió la justificación de párrafos en ambos informes; la causa raíz era un `\centering` suelto en `sections/00_portada.tex` que persistía para todo el documento.
- (2026-06-17) Se refactorizaron `src/ciclo_descargas_14m2_75C_12m3h.py`, `src/calentamiento_24ton_40_60.py` y `src/escenario4_capacidad.py` para que sean import-safe desde Flask (directorios y `os.makedirs` dentro de `main()` o como parámetros).
- (2026-06-17) Se crearon los wrappers `webapp/app/core/ciclo_12m3h.py`, `perdidas_aislamiento.py` y `escenarios_extras.py` para exponer los análisis del proyecto a la API y a las vistas HTML.
- (2026-06-17) Se añadió el blueprint `webapp/app/api/proyecto.py` con endpoints JSON para ciclo 12 m³/h, pérdidas térmicas, espesores de aislamiento, calentamiento 24 ton y capacidad operativa.
- (2026-06-17) Se implementó el servicio estático `/figures/<path:filename>` en `webapp/app/routes.py` para servir las gráficas generadas en `results/figures/`.
- (2026-06-17) Se añadieron las páginas HTML `/factibilidad`, `/perdidas-aislamiento` y `/escenarios`, y se actualizaron `base.html`, `index.html`, `dashboard.html` y `about.html`.
- (2026-06-17) Se amplió `webapp/tests/test_api.py` a 14 tests; todos pasan exitosamente.

## Archivos clave y su propósito
- `docs/report/W2605PRINF001.tex` — Informe técnico principal (71 páginas).
- `docs/report/W2605PRINF002.tex` — Resumen ejecutivo gerencial (5 páginas).
- `docs/report/sections/14_calentamiento_24ton.tex` — Sección de caso de estudio: calentamiento de 24 ton con área 14 m².
- `docs/report/sections/15_analisis_ciclo_12m3h.tex` — Sección de análisis del ciclo de descargas a 12 m³/h con chaqueta 14 m² y agua 75 °C.
- `src/calentamiento_24ton_40_60.py` — Script de simulación del caso de estudio 24 ton.
- `src/ciclo_descargas_14m2_75C_12m3h.py` — Script de simulación del ciclo de descargas a 12 m³/h y generación de figuras.
- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con logo DMV SAS.
- `src/perdidas_termicas_real.py` — Cálculo de pérdidas térmicas con área real y aislamiento.
- `src/coeficiente_U.py` — Cálculo del coeficiente global U.
- `src/ciclo_descargas.py` — Simulación del ciclo de descargas a carrotanques.
- `task/test_ciclo.py` — Test del ciclo oficial precalentado.
- `task/test_simulacion_50C.py` — Test de simulación desde 50 °C.
- `webapp/tests/test_api.py` — Tests de la API Flask (14 casos).
- `webapp/app/routes.py` — Rutas HTML y servicio de figuras.
- `webapp/app/api/proyecto.py` — Endpoints JSON de los análisis del proyecto.
- `webapp/app/core/ciclo_12m3h.py` — Wrapper Flask del ciclo a 12 m³/h con 14 m².
- `webapp/app/core/perdidas_aislamiento.py` — Wrapper Flask de pérdidas térmicas y espesores.
- `webapp/app/core/escenarios_extras.py` — Wrapper Flask del calentamiento de 24 ton y de la capacidad operativa diaria.
- `src/ciclo_descargas_14m2_75C_12m3h.py` — Simulación del ciclo a 12 m³/h y generación de figuras.
- `src/calentamiento_24ton_40_60.py` — Simulación del calentamiento de 24 ton.
- `src/escenario4_capacidad.py` — Cálculo de capacidad operativa diaria.
- `auditoria1.md` — Auditoría crítica del informe de tercero.
- `task/todo.md` — Plan de trabajo y registro de revisiones.

## Preguntas abiertas / bloqueos
Ninguna crítica pendiente.

## Repositorio remoto
- URL: `https://github.com/INGENDESING/W2605-ANALISIS-TRANSFERENCIA-CALOR-GLOBE-1130.git`
- Rama: `main`

## Comandos / workflows útiles
- Compilar informe principal: `cd docs/report && pdflatex W2605PRINF001.tex && bibtex W2605PRINF001 && pdflatex W2605PRINF001.tex && pdflatex W2605PRINF001.tex`
- Compilar resumen ejecutivo: `cd docs/report && pdflatex W2605PRINF002.tex && pdflatex W2605PRINF002.tex`
- Ejecutar tests: `cd task && ../venv/Scripts/python.exe test_ciclo.py && ../venv/Scripts/python.exe test_simulacion_50C.py && cd ../webapp && ../venv/Scripts/python.exe tests/test_api.py`
- Levantar servidor web: `cd webapp && ../venv/Scripts/python.exe run.py`
- Generar figuras: ejecutar scripts en `src/` con `venv/Scripts/python.exe`.
