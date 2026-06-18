# Contexto del proyecto: W2605 — Fondo de tanque de glucosa

## Estado actual
- Última tarea completada: Unificación de las vistas Simulador y Calculadora al estilo de tarjetas Power BI oscuro neón; adición de clases CSS para controles, tablas y spinners oscuros.
- Próxima tarea pendiente: Revisión final por parte del usuario y, si se solicita, actualizar W2605PRINF002 con los hallazgos paramétricos y la configuración hidráulica actualizada, o unificar las vistas restantes (factibilidad, pérdidas, escenarios, etc.) al estilo Power BI.
- Fecha de última actualización: 2026-06-18T13:52:30-05:00.

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
- (2026-06-18) Se actualizó la descripción de la chaqueta de media caña en el informe técnico a la configuración de doble entrada de agua caliente y doble salida de agua de retorno, de acuerdo con los planos mecánicos actualizados (`Data/planos/fondo.png` y `Data/planos/espiral.png`). Se modificaron las Figuras 3 y 4, sus leyendas y la tabla de geometría de la media caña en `docs/report/sections/07_bases_disenio.tex`.
- (2026-06-18) Se profundizó la metodología CFD en `docs/report/sections/08_metodologia.tex` con las ecuaciones diferenciales gobernantes: conservación de masa, Navier-Stokes, conservación de energía en fluidos, conducción en el sólido, convección natural con acoplamiento Boussinesq, condiciones de contorno y criterios de malla.
- (2026-06-18) Se eliminó la Figura 11 (`cfd1.png`) de la Sección 9 por corresponder al modelo anterior de una sola rama. Se redactó una comparación cualitativa entre la configuración de doble entrada/doble salida y el caso de una sola rama, explicando que la doble entrada mejora la uniformidad térmica y reduce gradientes azimutales sin alterar el orden de magnitud del coeficiente global $U$.
- (2026-06-18) Se integraron las seis figuras CFD de COMSOL Multiphysics 6.4 en la Sección 9 del informe técnico, validando el coeficiente global $U$ obtenido con Python. La simulación CFD reporta $U_{\text{CFD}} = 38$~W/(m²·°C), con una diferencia del 5 % respecto al valor analítico de 36~W/(m²·°C) para $T_g \approx 60$ °C, lo cual es aceptable para ingeniería de proceso.
- (2026-06-18) Se completó el análisis paramétrico de arranque y operación cíclica. Se confirmó que el arranque del tanque completo (50 % o 80 %) desde 40 °C con chaqueta de 14 m² no alcanza 60 °C en 96 h; el caso más favorable (50 %, agua 75 °C) llega a 51,50 °C. Se documentó explícitamente en el informe técnico para no contradecir el caso idealizado de 24 ton.
- (2026-06-18) Se verificó que el ciclo oficial de 5 descargas/día es factible térmicamente para niveles iniciales de 80 % y 50 % con agua a 65 °C y 75 °C, aunque el caso 50 % / 65 °C termina con margen de solo 0,11 °C respecto a 57 °C.
- (2026-06-18) Se refactorizó `src/ciclo_descargas_14m2_75C_12m3h.py` para aceptar parámetros flexibles (`T_agua`, `nivel_inicial`, `T_inicial`) y se calcularon las ganancias térmicas netas en tiempos muertos (chaqueta − pérdidas).
- (2026-06-18) Se rediseñó el dashboard de la webapp para consumir el endpoint `/api/proyecto/ciclo-escenario5` y mostrar únicamente el Escenario 5 (ciclo industrial de despacho desde 25 °C). Se agregaron gráficas por fase separada (descargas con flujo y recalentamientos sin flujo) con tiempo normalizado desde el inicio de cada fase, y una sección de alternativas de diseño y medidas operativas.
- (2026-06-18) Se estilizaron las tablas de la portada de W2605PRINF001 en `docs/report/sections/00_portada.tex`: sin color de fondo, líneas superior e inferior gruesas (`\toprule[1.5pt]`, `\bottomrule[1.5pt]`) y mayor espaciado interno (`\arraystretch=1.3`). Se mantuvo `\midrule` estándar para separar encabezado del cuerpo en la tabla de control de revisiones.
- (2026-06-18) Se eliminó la sangría de párrafos en W2605PRINF001 removiendo el paquete `ragged2e` y sus llamadas a `\justifying` (LaTeX justifica por defecto; `ragged2e` restauraba `\parindent`). Se conservó `parskip` con `\parindent=0pt` y `\parskip=6pt` para separación entre párrafos. El archivo afectado es `docs/report/config/preamble.tex`.
- (2026-06-18) Se unificó el área de transferencia de la chaqueta de media caña a 14 m² en todo el proyecto (definida en `src/geometria_tanque.py` como `A_CONTACTO = 14.0`), sustituyendo el valor histórico de 13 m² en scripts activos, API, webapp, tests, documentación LaTeX (incluyendo `01_frontmatter.tex` y `04_introduccion.tex`), README y auditoría de tercero. El valor anterior se conserva solo en `reciclaje/` para trazabilidad histórica.
- (2026-06-18) Se consolidó el ciclo operativo oficial en los documentos y scripts: 5 descargas/día de 24~ton, flujo másico de descarga 12~ton/h, duración 2,0~h, período 4,8~h, calentamiento entre descargas 2,8~h. Se eliminó la referencia obsoleta a 12~m³/h como flujo nominal.
- (2026-06-18) Se corrigió el abstract y el resumen ejecutivo: caudal de agua de diseño 57,7~m³/h a 75~°C, temperatura mínima del ciclo 58,56~°C, cumplimiento del límite inferior de 57~°C con glucosa de alimentación a 55~°C como caso conservador.
- (2026-06-18) Se estandarizó la notación de temperatura a `\textdegree C` en todo el informe técnico y el resumen ejecutivo, eliminando notaciones mixtas (`$^\circ$C`, `\degC`, carácter `°`).
- (2026-06-18) Se rediseñaron los diagramas de bloques del ciclo oficial (`src/diagramas_bloques_ciclo.py`): figuras global, descarga y calentamiento, con estilo corporativo unificado, sin superposiciones y valores coherentes con el balance energético (`Q_chaqueta = 27,3 MJ/h`, `Q_pérdidas = 14,7 MJ/h`).
- (2026-06-18) Se actualizó el balance energético a 60~°C: `Q_chaqueta = 27,3 MJ/h`, pérdidas `14,7 MJ/h`, balance neto `12,6 MJ/h`, eficiencia `65,0 %`, temperatura de salida del agua `74,9~°C`.
- (2026-06-18) Se confirmó que el logo oficial de DMV SAS es el archivo `docs/report/logos/logo1.png` (tipografía gótica verde "DML Ingeniería S.A.S."); se recompilaron W2605PRINF001 y W2605PRINF002 para aplicarlo en el membrete estilo tercero.
- (2026-06-17) Se adoptó el encabezado estilo tercero con logo de DMV SAS para W2605PRINF001 y W2605PRINF002, manteniendo el encabezado corporativo estándar disponible en `config/header.tex`.
- (2026-06-17) Se recalculó pérdidas térmicas usando el área real expuesta (149,7 m²) en lugar de la estimación simplificada (~30 m²), elevando el valor de diseño de 4,6 MJ/h a 14,7 MJ/h.
- (2026-06-17) Se eliminó del alcance activo la comparativa con la chaqueta dimple de 28 m²; el material obsoleto se archivó en `reciclaje/09_comparativa_dimple_obsoleta/` para conservar trazabilidad histórica sin mantenerlo en entregables activos.
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
- (2026-06-17) Se rediseñó la webapp con tema oscuro cyberpunk: nueva paleta en `webapp/app/static/css/main.css`, `base.html` con `data-bs-theme="dark"`, y actualización de `index.html`, `dashboard.html`, `factibilidad.html`, `perdidas_aislamiento.html`, `escenarios.html` y `about.html`.
- (2026-06-17) Se adaptaron los scripts de gráficos (`dashboard.js`, `calculadora.js`, `simulador.js`, `propiedades.js`, `sensibilidad.js`) a fondo oscuro con colores neón.
- (2026-06-17) Se añadió la ruta `/informes/<filename>` en `webapp/app/routes.py` para descargar los informes PDF desde `docs/report/`.
- (2026-06-17) Se actualizó `render.yaml` con nombre de servicio `w2605-webapp`, health check `/health` y configuración de despliegue Gunicorn.
- (2026-06-18) Se actualizó la webapp a organización tipo dashboard Power BI: se reorganizó la navegación en `webapp/app/templates/base.html`, se creó `webapp/app/templates/documentos.html` con tabla de transmittal y filtro por categoría, y se añadieron estilos DataTables dark en `main.css`.
- (2026-06-18) Se implementaron los endpoints `/codigo/<path:filename>` y `/descargar-codigo-fuente` en `webapp/app/routes.py` para descargar scripts Python individuales y un ZIP del código fuente, respectivamente, con validación de extensión `.py` y protección contra path traversal.
- (2026-06-18) Se unificaron las vistas `webapp/app/templates/calculadora.html` y `webapp/app/templates/simulador.html` al sistema de tarjetas Power BI, usando `.pb-page-header`, `.pb-card`, `.pb-kpi-row`, `.pb-kpi-card`, `.pb-control-group`, `.pb-input`, `.pb-table-dark` y `.pb-spinner-overlay`; se conservaron todos los IDs para no afectar la lógica JavaScript.
- (2026-06-18) Se añadieron clases CSS para controles de formulario, tablas oscuras, badges, modales y spinners en `webapp/app/static/css/main.css`.
- (2026-06-18) Se amplió `webapp/tests/test_api.py` a 22 tests, incluyendo validación de `/documentos`, descargas de código fuente y seguridad de rutas.
- (2026-06-18) Se actualizó el health check de la webapp a versión `2.2.0` y el sidebar/footer a `v2.2 power-bi`.
- (2026-06-17) Se amplió `webapp/tests/test_api.py` a 16 tests (incluye descarga de informes).

## Archivos clave y su propósito
- `docs/report/W2605PRINF001.tex` — Informe técnico principal (78 páginas tras actualización de configuración hidráulica y metodología CFD).
- `docs/report/W2605PRINF002.tex` — Resumen ejecutivo gerencial (5 páginas).
- `docs/report/sections/09_resultados.tex` — Sección de resultados con subsección de validación CFD ampliada (seis figuras).
- `docs/report/sections/14_calentamiento_24ton.tex` — Sección de caso de estudio: calentamiento de 24 ton con área 14 m².
- `docs/report/sections/15_analisis_ciclo_12m3h.tex` — Sección de análisis del ciclo oficial de 5 descargas/día con flujo 12~ton/h, chaqueta 14 m² y agua 75 °C.
- `src/calentamiento_24ton_40_60.py` — Script de simulación del caso de estudio 24 ton.
- `src/ciclo_descargas_14m2_75C_12m3h.py` — Script de simulación del ciclo oficial de descargas a 12~ton/h y generación de figuras.
- `src/diagramas_bloques_ciclo.py` — Generador unificado de los diagramas de bloques del ciclo oficial.
- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con logo DMV SAS.
- `src/perdidas_termicas_real.py` — Cálculo de pérdidas térmicas con área real y aislamiento.
- `src/coeficiente_U.py` — Cálculo del coeficiente global U.
- `src/ciclo_descargas.py` — Simulación del ciclo de descargas a carrotanques.
- `reciclaje/09_comparativa_dimple_obsoleta/src/comparativa_chaquetas.py` — Script archivado de comparativa chaqueta dimple 28 m² vs. media caña 13 m² (no activo).
- `task/test_ciclo.py` — Test del ciclo oficial precalentado.
- `task/test_simulacion_50C.py` — Test de simulación desde 50 °C.
- `webapp/tests/test_api.py` — Tests de la API Flask (22 casos).
- `webapp/app/static/css/main.css` — Sistema de diseño dark cyberpunk / Power BI, incluyendo estilos DataTables dark.
- `webapp/app/routes.py` — Rutas HTML, servicio de figuras, descarga de informes PDF, descarga de códigos Python y ZIP de código fuente.
- `webapp/app/templates/documentos.html` — Tabla de transmittal con informe técnico y códigos Python descargables.
- `webapp/app/static/js/documentos.js` — Inicialización de DataTables y filtro por categoría.
- `webapp/app/api/proyecto.py` — Endpoints JSON de los análisis del proyecto.
- `webapp/app/core/ciclo_12m3h.py` — Wrapper Flask del ciclo a 12 m³/h con 14 m².
- `webapp/app/core/perdidas_aislamiento.py` — Wrapper Flask de pérdidas térmicas y espesores.
- `webapp/app/core/escenarios_extras.py` — Wrapper Flask del calentamiento de 24 ton y de la capacidad operativa diaria.
- `webapp/app/core/ciclo_escenario5.py` — Wrapper Flask del Escenario 5 (ciclo industrial de despacho desde 25 °C).
- `webapp/app/core/arranque_niveles.py` — Wrapper Flask del arranque del 50 % y 80 % del tanque con pérdidas.
- `webapp/app/core/ciclo_12m3h.py` — Wrapper Flask del ciclo oficial y del análisis paramétrico (4 escenarios).
- `webapp/app/templates/ciclo_parametrico.html` — Vista del análisis paramétrico del ciclo.
- `webapp/app/templates/arranque_niveles.html` — Vista del arranque por niveles con pérdidas.
- `src/ciclo_descargas_14m2_75C_12m3h.py` — Simulación del ciclo a 12 m³/h y generación de figuras.
- `src/calentamiento_24ton_40_60.py` — Simulación del calentamiento de 24 ton.
- `src/escenario4_capacidad.py` — Cálculo de capacidad operativa diaria.
- `auditoria1.md` — Auditoría crítica del informe de tercero.
- `src/diagramas_bloques_ciclo.py` — Generador de los diagramas de bloques del ciclo oficial (global, descarga, calentamiento).
- `task/todo.md` — Plan de trabajo y registro de revisiones.

## Preguntas abiertas / bloqueos
- [ ] Revisar si el usuario requiere actualizar W2605PRINF002 con los hallazgos de arranque y ciclo paramétrico.
- [ ] Evaluar si se desea suprimir la salida por consola de `ejecutar_caso` al consumir `/api/proyecto/arranque-niveles`.

## Repositorio remoto
- URL: `https://github.com/INGENDESING/W2605-ANALISIS-TRANSFERENCIA-CALOR-GLOBE-1130.git`
- Rama: `main`

## Comandos / workflows útiles
- Compilar informe principal: `cd docs/report && pdflatex W2605PRINF001.tex && bibtex W2605PRINF001 && pdflatex W2605PRINF001.tex && pdflatex W2605PRINF001.tex`
- Compilar resumen ejecutivo: `cd docs/report && pdflatex W2605PRINF002.tex && pdflatex W2605PRINF002.tex`
- Ejecutar tests: `cd task && ../venv/Scripts/python.exe test_ciclo.py && ../venv/Scripts/python.exe test_simulacion_50C.py && cd ../webapp && ../venv/Scripts/python.exe tests/test_api.py`
- Ejecutar tests webapp con pytest: `cd webapp && ../venv/Scripts/python.exe -m pytest tests/test_api.py -v`
- Levantar servidor web: `cd webapp && ../venv/Scripts/python.exe run.py`
- Desplegar en Render: push a `main`; `render.yaml` configura el servicio `w2605-webapp` automáticamente.
- Generar figuras: ejecutar scripts en `src/` con `venv/Scripts/python.exe`.
