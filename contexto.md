# Contexto del proyecto: W2605 — Fondo de tanque de glucosa

## Estado actual
- Última tarea completada: Confirmación del logo corporativo (`docs/report/logos/logo1.png`), actualización de `README.md` y sincronización del repositorio con GitHub.
- Próxima tarea pendiente: Ninguna crítica pendiente; proyecto listo para entrega final.
- Fecha de última actualización: 2026-06-17T13:15:00-05:00.

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
- (2026-06-17) Se corrigió la justificación de párrafos en ambos informes; la causa raíz era un `\centering` suelto en `sections/00_portada.tex` que persistía para todo el documento.

## Archivos clave y su propósito
- `docs/report/W2605PRINF001.tex` — Informe técnico principal (66 páginas).
- `docs/report/W2605PRINF002.tex` — Resumen ejecutivo gerencial (4 páginas).
- `docs/report/sections/14_calentamiento_24ton.tex` — Sección de caso de estudio: calentamiento de 24 ton con área 14 m².
- `src/calentamiento_24ton_40_60.py` — Script de simulación del caso de estudio 24 ton.
- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con logo DMV SAS.
- `src/perdidas_termicas_real.py` — Cálculo de pérdidas térmicas con área real y aislamiento.
- `src/coeficiente_U.py` — Cálculo del coeficiente global U.
- `src/ciclo_descargas.py` — Simulación del ciclo de descargas a carrotanques.
- `task/test_ciclo.py` — Test del ciclo oficial precalentado.
- `task/test_simulacion_50C.py` — Test de simulación desde 50 °C.
- `webapp/tests/test_api.py` — Tests de la API Flask.
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
- Generar figuras: ejecutar scripts en `src/` con `venv/Scripts/python.exe`.
