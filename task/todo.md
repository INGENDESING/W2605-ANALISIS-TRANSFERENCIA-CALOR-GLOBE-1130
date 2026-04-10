# Plan de Reorganización y Limpieza del Proyecto P2611

## 1. ANÁLISIS DEL PROBLEMA Y ESTADO ACTUAL
Al analizar el directorio raíz y con base en el archivo `README_ESTRUCTURA.md`, se identificaron desajustes en la estructura de archivos que no obedecen al orden documentado:

- **Archivos sueltos en la raíz:** Hay varios archivos de texto y markdown referidos a auditorías e investigación (`auditoria.md`, `auditoria_final_v3.md`, `auditoriar1.txt`, `auditoriatercero.txt`, `auditoriatercero_raw.txt`, `calculoarea.txt`, `comparativaactualfuturo.txt`, `promptwebv1.txt`).
- **Archivos de administración sueltos:** `DEPURACION_RESUMEN.md`, `SESION_CHECKPOINT.md`, `INSTALACION_DEPENDENCIAS.md` están poblando la raíz.
- **Códigos huérfanos:** `debug_U.py` no se encuentra dentro del directorio `src/`.
- **Figuras duplicadas/desalineadas:** Existe un directorio `figures` en la raíz con 61 archivos, así como uno `results/figures` con 53 archivos. Según las convenciones del repositorio, las gráficas deberían residir en `results/figures/`.
- **Rutas en Python:** Los scripts guardan las imágenes en `../figures` (raíz) en lugar de `../results/figures`.
- **Rutas en LaTeX:** Los archivos del informe reportan buscar imágenes en `../../figures/` (raíz), en lugar de `../../results/figures/`.

## 2. PLAN DE TAREAS (TODO)

### FASE 1: Limpieza de la raíz (Reubicación de archivos)
- [X] **Mover archivos de auditoría:** Crear carpeta `Data/auditorias/` y mover allá `auditoria.md`, `auditoria_final_v3.md`, `auditoriar1.txt`, `auditoriatercero.txt`, `auditoriatercero_raw.txt`.
- [X] **Mover archivos de investigación y notas:** Mover `calculoarea.txt`, `comparativaactualfuturo.txt`, y `promptwebv1.txt` a la carpeta `Data/investigacion/`.
- [X] **Mover y organizar código huérfano:** Mover `debug_U.py` a dentro del directorio `src/`.
- [X] **Organizar documentación técnica/administrativa:** Crear carpeta `docs/admin/` (o `.admin/`) y reubicar archivos como `DEPURACION_RESUMEN.md`, `SESION_CHECKPOINT.md` e `INSTALACION_DEPENDENCIAS.md`.

### FASE 2: Consolidación de Directorio de Figuras
- [X] **Consolidar `figures/` y `results/figures/`:** Mover cualquier archivo único de `figures/` a `results/figures/`.
- [X] **Eliminar directorio huérfano:** Eliminar de forma segura la carpeta `figures` de la raíz una vez combinados los archivos.

### FASE 3: Corrección de Rutas
- [X] **Actualizar scripts Python:** Reemplazar todas las ocurrencias de las rutas `../figures` y `figures` sueltas, cambiándolas por las referencias adecuadas a `os.path.join(..., 'results', 'figures')` o iterando sobre `../results/figures`.
- [X] **Actualizar LaTeX:** Modificar los comandos de inclusión gráfica en `docs/report/sections/*.tex`, cambiando `../../figures/` por `../../results/figures/`. Así como en `docs/report/config/header.tex` y en `docs/report/*.tex` según aplique.
- [X] **Validar Compilación de LaTeX:** Ejecutar el comando para compilar el archivo PDF principal, comprobando que todas las imágenes y recursos enlazan adecuadamente.

---
## 3. SECCIÓN DE REVISIÓN

**Fecha:** 10 de Abril, 2026

**Resumen de los cambios realizados:**
- **Orden e Higiene del Repositorio:** El directorio base (`VERSIÓN3`) ha sido completamente purgado de archivos huérfanos. Se han creado los correspondientes subdirectorios `Data/auditorias` y `docs/admin` para categorizar la documentación de revisión de terceros y de configuración de las IAs, reduciendo así la carga visual y asegurando una estructura organizativa óptima. Se movió `debug_U.py` al núcleo de desarrollo (`src/`).
- **Arquitectura de Recursos (Figuras) Estandarizada:** Se resolvió la duplicidad originada en las carpetas de figuras. Los elementos de la carpeta raíz `/figures` han sido volcados por completo a `/results/figures` unificando un único destino formal conforme al `README_ESTRUCTURA.md`. La carpeta iterativa raíz fue eliminada.
- **Parametrización Lógica de Relatividad de Directorios:**
  1. Todos los *Python Scripts* ubicados en `src/` han sido actualizados en masa para redireccionar el resultado de `matplotlib` (`savefig`) a su equivalente en `../results/figures` en lugar de apuntar a una raíz desarticulada.
  2. Todas las invocaciones de `\includegraphics` a lo largo de los diecinueve (19) capítulos de LaTeX y los recursos del encabezado (`docs/report/*`) ahora referencian `../../results/figures/`.
- **Validación Final Exitoso:** Se corrió el compilador sintáctico `pdflatex` evaluando la estructura `P2611-PR-INF-001`. El sistema logró empaquetar de vuelta un formato PDF íntegro (de aproximadamente 10 MB) enrutando correctamente las gráficas bajo la nueva jerarquía. No se reportaron ausencias de imágenes (`No file/not found`).

**Estado Final:** 
La estructura del proyecto es ahora robusta, lógica y sumamente coherente, quedando lista y libre de ambigüedades para su actualización (`commit`) en el repositorio centralizado de Git. Cada documento tiene asignado un lugar que obedece estrictamente a la normativa de organización del proyecto Ingredion/P2611.
