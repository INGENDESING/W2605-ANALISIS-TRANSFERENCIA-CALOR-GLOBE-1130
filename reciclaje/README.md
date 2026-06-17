# Carpeta `reciclaje` — Proyecto W2605

Esta carpeta agrupa archivos generados, auxiliares, duplicados o desactualizados del proyecto W2605. Se organiza de forma lógica y secuente para facilitar la consulta histórica antes de la limpieza del repositorio en GitHub.

## Estructura

| Carpeta | Contenido |
|---|---|
| `01_latex_auxiliares/` | Archivos auxiliares generados por `pdflatex` y `bibtex` (`.aux`, `.bbl`, `.blg`, `.lof`, `.log`, `.lot`, `.out`, `.spl`, `.toc`). Se regeneran en cada compilación. |
| `02_logs_compilacion/` | Logs históricos de compilación (`compile_*.log`, `texput.log`). |
| `03_capturas_verificacion/` | Imágenes PNG de verificación visual de las primeras, intermedias y últimas páginas de los informes finales. |
| `04_pruebas_encabezado/` | Documento de prueba `test_header_tercero.*` y su captura, usados para validar el membrete estilo tercero. |
| `05_documentos_desactualizados/` | Documentos de contexto, estructura y auditoría reemplazados por versiones actualizadas, más el contenido previo de `docs/report/RECICLAJE/`. |
| `06_figuras_duplicadas/` | Figuras de la carpeta raíz `figures/` que están duplicadas en `results/figures/` y no son referenciadas por los informes activos. |
| `08_scripts_depuracion/` | Scripts temporales de depuración, corrección masiva y generación de PFDs placeholder; no son importados por el código activo. |
| `09_datos_duplicados/` | Archivos de datos duplicados (`Data/Memoria_Termica Glucosa.Rev.1.pdf`, `PFD.svg`) o PFDs duplicados en `docs/report/`. |
| `10_web_demo_antigua/` | Demo Flask antigua en `examples/web-demo/`, no integrada con la aplicación actual en `webapp/`. |

## Notas

- Los entregables oficiales (`docs/report/W2605PRINF001.tex/pdf` y `docs/report/W2605PRINF002.tex/pdf`) permanecen en sus rutas originales.
- Los scripts activos de `src/`, las figuras oficiales de `results/figures/` y los datos de referencia de `Data/` no se movieron.
- Los archivos de esta carpeta se conservan por trazabilidad, pero no forman parte de los entregables finales.
