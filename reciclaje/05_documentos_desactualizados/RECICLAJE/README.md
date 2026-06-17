# RECICLAJE — Documentos y archivos obsoletos

Esta carpeta agrupa los documentos, configuraciones y scripts que ya no forman parte de los entregables activos del proyecto W2605.

## Documentos eliminados del repositorio (histórico)

| Archivo | Motivo |
|---|---|
| `docs/report/P2611-PR-INF-001.tex` | Código de proyecto obsoleto P2611, reemplazado por W2605PRINF001. |
| `docs/report/P2611-PR-INF-002.tex` | Código de proyecto obsoleto P2611. |
| `docs/report/P2611-PR-INF-003.tex` | Código de proyecto obsoleto P2611. |
| `docs/report/ResumenEjecutivoGerencial_P2611.tex` | Resumen ejecutivo obsoleto asociado a P2611. |
| `docs/report/W2605-PR-INF-001.tex` | Borrador de resumen técnico que competía con W2605PRINF001/W2605PRINF002. |
| `docs/report/W2605-PR-INF-003.tex` | Resumen ejecutivo alternativo con datos inconsistentes. |
| `docs/report/config/datos_proyecto_001.tex` | Configuración asociada a W2605-PR-INF-001. |
| `docs/report/config/datos_proyecto_003.tex` | Configuración asociada a W2605-PR-INF-003. |
| `docs/report/sections/02_resumen.tex` | Resumen ejecutivo técnico obsoleto que competía con W2605PRINF002; removido del maestro W2605PRINF001. |

## Archivos auxiliares y temporales eliminados

- `docs/report/temp_tikz_block.txt`
- `docs/report/salida.txt`
- `docs/report/P2611-PR-INF-*.spl`
- Archivos auxiliares de compilación (`.aux`, `.log`, `.out`, `.toc`, `.lof`, `.lot`, `.spl`, `.synctex.gz`) vinculados a documentos P2611.
- Archivos de extracción de texto en raíz del proyecto: `memoria_termica_extract.txt`, `planos_mecanicos_extract.txt`, `abstract_line.txt`, `RESUMENEJECUTIVOGERENCIAL.txt`.
- Diagramas de proceso obsoletos de P2611 en `results/`.

## Archivo conservado en esta carpeta

- `fix_p2611_global.py`: script de migración utilizado para renombrar referencias de P2611 a W2605 en archivos activos. Se conserva únicamente como registro histórico del proceso de limpieza.
