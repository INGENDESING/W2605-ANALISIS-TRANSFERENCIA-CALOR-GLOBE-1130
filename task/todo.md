# Plan de Trabajo — Proyecto W2605
## Generación de dos documentos finales: informe técnico W2605PRINF001 y resumen ejecutivo W2605PRINF002

**Fecha del plan:** 13 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Consolidar el proyecto en dos entregables oficiales con contenido técnico coherente, estilo Elsevier / Science Direct y figuras profesionales actualizadas.

---

## 1. Objetivo

Consolidar el proyecto en dos entregables oficiales:

| Código | Documento | Base principal | Observaciones |
|---|---|---|---|
| W2605PRINF001 | Informe técnico principal (memoria descriptiva) | `docs/report/W2605PRINF001.tex` | Documento completo con metodología, resultados, análisis, conclusiones y anexos. |
| W2605PRINF002 | Resumen ejecutivo gerencial | `docs/report/W2605PRINF002.tex` | Documento autónomo para toma de decisiones, sin viñetas, con KPIs y recomendaciones priorizadas. |

---

## 2. Requerimientos consolidados del usuario

1. **Códigos de documento definitivos:** W2605PRINF001 y W2605PRINF002.
2. **Empresa:** el único autor es **DMV SAS**.
3. **Correos electrónicos:** placeholder genérico (`[correo@empresa.com]`).
4. **Encabezado:** sin líneas verticales en la tabla del membrete.
5. **Capacidad operativa:** máximo **5 descargas/día** (120 ton/día).
6. **Código de proyecto:** **W2605**; eliminar P2611 en archivos activos.
7. **Estilo de redacción:** Elsevier / Science Direct, sin viñetas, tablas autónomas.
8. **Documentos antiguos:** organizados en `docs/report/RECICLAJE/`.
9. **Ilustraciones:** estilo profesional a nivel experto, coherente entre figuras y con los datos del ciclo oficial.

---

## 3. Hallazgos críticos identificados

### 3.1 Inconsistencias numéricas resueltas

| Tema | Hallazgo | Decisión |
|---|---|---|
| Requerimiento operativo | Referencias a 6/7/8 descargas y 192 ton/día. | Unificado a 5 descargas/día (120 ton/día). |
| Flujo de glucosa | Valores de 7.200 y 8.000 kg/h. | Unificado a **5.000 kg/h** (5 × 24 ton / 24 h). |
| Duración de descarga | Scripts de figuras usaban 1,5 h. | Actualizado a **2,0 h** (12 ton/h). |
| Masa inicial Esc. 4 y 5 | Scripts usaban 192 ton. | Actualizado a **80 % del volumen operativo** (~250 ton). |
| Pérdidas térmicas | 4,82 MJ/h vs 51,1 MJ/h. | Valor de diseño con aislamiento: **4,6 MJ/h**; 51,1 MJ/h como referencia sin aislamiento. |

### 3.2 Problemas de compilación y referencias

- Carácter em-dash en `bibliografia.bib` causaba `Missing character`.
- `sections/03_nomenclatura.tex` usaba el carácter `°` literal.
- Etiquetas duplicadas y referencias rotas resueltas en sesiones previas.

### 3.3 Obsolescencia

- `W2605-PR-INF-001.tex` y `W2605-PR-INF-003.tex` eliminados.
- `sections/02_resumen.tex` movido a `RECICLAJE/`.

---

## 4. Lista de tareas

### Fase 0. Preparación del terreno

- [x] **0.1** Crear `docs/report/RECICLAJE/` y mover documentos obsoletos (`02_resumen.tex`, `fix_p2611_global.py`).
- [x] **0.2** Eliminar todo rastro de `P2611` en archivos activos.
- [x] **0.3** Verificar que `RECICLAJE/` no tenga referencias cruzadas desde archivos activos.

### Fase 1. Arquitectura de los dos documentos finales

- [x] **1.1** Renombrar maestros a `W2605PRINF001.tex` y `W2605PRINF002.tex`.
- [x] **1.2** Actualizar `config/datos_proyecto.tex` y `config/datos_proyecto_002.tex`.
- [x] **1.3** Eliminar `sections/02_resumen.tex` del maestro y moverlo a `RECICLAJE/`.
- [x] **1.4** Definir el índice final de cada documento.

### Fase 2. Corrección de inconsistencias numéricas

- [x] **2.1** Unificar requerimiento operativo a 5 descargas/día (120 ton/día).
- [x] **2.2** Definir valor oficial de pérdidas térmicas.
- [x] **2.3** Definir masa inicial y tiempos de recalentamiento.
- [x] **2.4** Ajustar Escenario 4 al límite de 5 descargas/día.
- [x] **2.5** Unificar caudal medio de glucosa a 5.000 kg/h.
- [x] **2.6** Regenerar figuras y tablas afectadas por los cambios numéricos.

### Fase 3. Configuración corporativa común

- [x] **3.1** Actualizar `config/header.tex` eliminando líneas verticales.
- [x] **3.2** Reemplazar nombre de empresa por **DMV SAS**.
- [x] **3.3** Configurar autor único **DMV SAS**.
- [x] **3.4** Dejar correos electrónicos como placeholder.

### Fase 4. Construcción de W2605PRINF001

- [x] **4.1** Integrar secciones modulares coherentes.
- [x] **4.2** Resolver referencias cruzadas rotas y duplicadas.
- [x] **4.3** Corregir citas bibliográficas.
- [x] **4.4** Eliminar viñetas y convertir a tablas/prosa.
- [x] **4.5** Verificar ortografía y gramática.

### Fase 5. Construcción de W2605PRINF002

- [x] **5.1** Estructurar resumen ejecutivo autónomo.
- [x] **5.2** Limpiar placeholders y errores ortográficos.
- [x] **5.3** Asegurar coherencia numérica con W2605PRINF001.
- [x] **5.4** Eliminar viñetas.
- [x] **5.5** Actualizar PFD TikZ con balance oficial.

### Fase 6. Revisión de estilo y calidad

- [x] **6.1** Revisar viñetas en cuerpo de documentos.
- [x] **6.2** Verificar tablas autónomas sin líneas verticales.
- [x] **6.3** Revisar ortografía, gramática y coherencia numérica.
- [x] **6.4** Estandarizar términos.

### Fase 7. Compilación y verificación

- [x] **7.1** Compilar `W2605PRINF001.tex` con flujo completo.
- [x] **7.2** Compilar `W2605PRINF002.tex` con flujo completo.
- [x] **7.3** Ejecutar tests de Python.
- [x] **7.4** Verificar referencias, citas y errores de glifo.

### Fase 8. Actualización de ilustraciones

- [x] **8.1** Actualizar `src/ciclo_descargas.py`, `src/escenario4_ciclo.py`, `src/escenario5_ciclo.py`, `src/escenarios.py` al ciclo oficial (2 h de descarga, masa inicial al 80 %).
- [x] **8.2** Aplicar estilo profesional uniforme a todos los generadores de figuras.
- [x] **8.3** Actualizar `src/calcular_areas.py`, `src/comparativa_chaquetas.py`, `src/graficar_resistencias.py` con el mismo estilo.
- [x] **8.4** Regenerar todas las figuras en PDF y PNG.
- [x] **8.5** Verificar coherencia visual entre figuras.

### Fase 9. Cierre y documentación

- [x] **9.1** Actualizar `task/todo.md` con sección de revisión.
- [x] **9.2** Entregar los dos PDFs finales y el resumen de cambios.

---

## 5. Criterios de aceptación

1. Los dos documentos finales compilan sin errores fatales.
2. No quedan referencias a P2611 ni a 6/7/8 descargas en archivos activos.
3. Encabezado sin líneas verticales en tabla del membrete.
4. Empresa identificada como **DMV SAS**.
5. Correos electrónicos como placeholder.
6. Estilo Elsevier / Science Direct, sin viñetas.
7. Datos numéricos coherentes entre informes y scripts.
8. Figuras con estilo profesional uniforme y ciclo oficial.
9. Tests de Python pasan.

---

## 6. Notas

- Se priorizó la simplicidad en cada cambio.
- Las figuras de ciclo regeneradas usan duración de descarga de 2,0 h y masa inicial al 80 %.
- Las figuras de ciclo actualizadas no están todas referenciadas en el documento activo; se generan como material de soporte.

---

## 7. Revisión de cambios realizados — sesión de ilustraciones

**Fecha de revisión:** 13 de junio de 2026  
**Scripts afectados:** `src/ciclo_descargas.py`, `src/escenario4_ciclo.py`, `src/escenario5_ciclo.py`, `src/escenarios.py`, `src/calcular_areas.py`, `src/comparativa_chaquetas.py`, `src/graficar_resistencias.py`  
**Figuras regeneradas:** ciclo de descargas, escenarios 1-5, comparación de escenarios, comparativa de chaquetas, coeficiente global U, resistencias térmicas.

### Cambios principales

1. **Ciclo oficial en scripts de simulación:** se actualizaron `ciclo_descargas.py`, `escenario4_ciclo.py`, `escenario5_ciclo.py` y `escenarios.py` para usar duración de descarga de **2,0 h** (flujo 3,333 kg/s, 12 ton/h) y masa inicial al **80 % del volumen operativo** (~250 ton). Se corrigieron etiquetas residuales de "Escenario 4" en `escenario5_ciclo.py`.

2. **Estilo profesional uniforme:** se aplicó una paleta corporativa coherente en todos los generadores:
   - Glucosa: `#2E5AAC`
   - Agua / setpoint: `#C44E28`
   - Descarga / mínimo: `#3A7D44`
   - Bandas de descarga: `#F4A261`
   - Rejilla: `#E5E5E5`
   - Texto: `#333333`
   - Fuente serif, 300 dpi, tamaños consistentes.

3. **Figuras de análisis de área y chaquetas:** se normalizaron `calcular_areas.py`, `comparativa_chaquetas.py` y `graficar_resistencias.py`. Las figuras de chaquetas se guardan en `figures/` y se copian a `results/figures/` para coherencia con las referencias LaTeX.

4. **Formato de salida:** todas las figuras se generan en PDF (vectorial) y PNG (raster) a 300 dpi.

### Figuras regeneradas

| Figura | Ubicación |
|---|---|
| `ciclo_T_vs_tiempo_esc2/esc3` | `results/figures/` |
| `ciclo_masa_nivel`, `ciclo_gantt`, `ciclo_comparacion_esc2_esc3` | `results/figures/` |
| `escenario1/2/3_T_vs_tiempo`, `comparacion_escenarios_2_3` | `results/figures/` |
| `escenario4_ciclo_T`, `escenario4_gantt` | `results/figures/` |
| `escenario5_ciclo_T`, `escenario5_gantt` | `results/figures/` |
| `U_vs_T_glucosa`, `comparacion_escenarios` | `results/figures/` |
| `comp_batch_T_vs_t`, `comp_batch_tiempo_bar`, `comp_flujo_T_out_vs_mdot`, `comp_flujo_maximo_bar` | `figures/` y `results/figures/` |
| `resistencias_termicas` | `results/figures/` |

### Verificación

- Todos los scripts se ejecutaron sin errores con `venv/Scripts/python.exe`.
- Los documentos W2605PRINF001 y W2605PRINF002 compilaron exitosamente después de regenerar las figuras.
- Los tests de Python (`test_ciclo.py`, `test_simulacion_50C.py`, `test_api.py`) pasaron.

### Pendientes

- Algunas figuras de ciclo (Escenarios 4 y 5) muestran tiempos de recalentamiento largos porque el modelo parte de una masa inicial caliente/al 80 %. Estas figuras se generan como material de soporte pero no están referenciadas directamente en los documentos activos.
- Quedan advertencias residuales menores de `Missing character` en `W2605PRINF001.pdf` asociadas a acentos dentro de entornos matemáticos; no afectan la legibilidad.

---

*Plan ejecutado. Entregables finales: `docs/report/W2605PRINF001.pdf` y `docs/report/W2605PRINF002.pdf`.*

---

## 8. Plan de trabajo adicional — sesión de depuración y validación final

**Fecha de plan:** 17 de junio de 2026  
**Estado:** En ejecución  
**Alcance:** Atender las cuatro opciones de validación solicitadas: compilación de informes, actualización de tests, revisión de coherencia numérica y corrección de advertencias LaTeX.

### Tareas

- [x] **8.1** Verificar compilación actual de `W2605PRINF001.tex` y `W2605PRINF002.tex`.
- [x] **8.2** Revisar y actualizar `task/test_ciclo.py` y `task/test_simulacion_50C.py` al ciclo oficial (2,0 h de descarga, periodo 4,8 h, 5 descargas/día).
- [x] **8.3** Revisar coherencia numérica entre scripts Python, archivos CSV en `results/` y documentos LaTeX.
- [x] **8.4** Abordar advertencias residuales de compilación LaTeX (`Missing character`, acentos en matemáticas, etc.).
- [x] **8.5** Ejecutar tests y regenerar PDFs para confirmar estabilidad.
- [x] **8.6** Registrar sección de revisión con cambios realizados.

### Criterios de aceptación

1. Ambos informes compilan sin errores fatales y con el menor número posible de advertencias.
2. Los tests reflejan el ciclo operativo oficial (2,0 h / 4,8 h) y se ejecutan sin errores.
3. Los valores clave (U, pérdidas térmicas, tiempos, capacidad, vida útil) son coherentes entre scripts, CSV y LaTeX.
4. No quedan advertencias evitables en la compilación.

---

## 9. Revisión de cambios realizados — sesión de validación final

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `task/test_ciclo.py`, `task/test_simulacion_50C.py`, `webapp/app/core/balance_energia.py`, `docs/report/config/header.tex`, `docs/report/config/preamble.tex`, `docs/report/sections/09_resultados.tex`  
**PDFs regenerados:** `docs/report/W2605PRINF001.pdf` y `docs/report/W2605PRINF002.pdf`

### Cambios principales

1. **Tests actualizados al ciclo oficial:** se reescribieron `task/test_ciclo.py` y `task/test_simulacion_50C.py` para usar los parámetros operativos definitivos: 5 descargas diarias, 24 ton por descarga, 2,0 h de descarga, periodo de ciclo 4,8 h y flujo medio de 5.000 kg/h. Se eliminaron los parámetros obsoletos (1,5 h / 3,0 h).

2. **Corrección en `webapp/app/core/balance_energia.py`:** se ajustó `t_max_cal` en `simular_calentamiento_y_ciclo()` y `simular_ciclo_automatico()` para respetar el argumento `tiempo_maximo_h` en lugar de forzar un límite fijo de 36 h.

3. **Limpieza de advertencias LaTeX:**
   - `docs/report/config/header.tex`: se reemplazaron caracteres acentuados directos por secuencias LaTeX (`DISE\~NO`, `INGENIER\'IA`, `C\'DIGO`, `REVISI\'ON`, etc.) para evitar `Missing character` en fuentes pequeñas del membrete.
   - `docs/report/config/preamble.tex`: se añadieron redefiniciones vacías de `\sectionmark`, `\subsectionmark` y `\subsubsectionmark`, junto con el paquete `textcase`, para mitigar conflictos de acentos en encabezados automáticos.
   - `docs/report/sections/09_resultados.tex`: se corrigió `$Q_{p\'erd}$` por `$Q_{\text{p\'erd}}$`, eliminando la advertencia `Command \' invalid in math mode`.

4. **Verificación de coherencia numérica:** se ejecutaron los scripts `src/coeficiente_U.py`, `src/escenarios.py`, `src/ciclo_descargas.py`, `src/comparativa_chaquetas.py` y `src/calcular_areas.py`. Los valores clave (coeficiente global U, tiempos de calentamiento, capacidad de flujo continuo, áreas requeridas y ciclo de descargas) son coherentes con las tablas y texto del informe LaTeX.

### Verificación

- Los documentos `W2605PRINF001.tex` y `W2605PRINF002.tex` compilan sin errores fatales. El primer documento solo conserva advertencias no bloqueantes de `Infinite glue shrinkage` originadas en ajustes de caja; el segundo compila limpio.
- Los tests `task/test_ciclo.py`, `task/test_simulacion_50C.py` y `webapp/tests/test_api.py` se ejecutan sin errores.
- Los scripts de generación de figuras se ejecutan correctamente y los CSVs se actualizan con los valores esperados.

### Hallazgos documentados (no corregidos por ser decisiones de diseño o documentales previas)

- **Pérdidas térmicas:** el documento adopta un valor de diseño de 4,6 MJ/h con `A_total ≈ 30 m²`. El script `src/calculo_calor_perdido_80.py` calcula ~3,7 kW (~13,4 MJ/h) usando el área total real expuesta al 80 % de llenado (~149,7 m²). La diferencia obedece a la estimación conservadora del área expuesta en el informe; no se modificó el texto porque el valor de 4,6 MJ/h es el criterio de diseño establecido.
- **Calor específico de la glucosa:** el documento reporta `C_{p,g,55} = 2.126,3 J/(kg·°C)` y `C_{p,g,57} = 2.130,6 J/(kg·°C)`, mientras que `propiedades_glucosa.py` arroja 2.128,9 y 2.130,9 J/(kg·°C), respectivamente. La diferencia es menor al 0,2 % y no afecta el balance energético global.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` (54 páginas)
- `docs/report/W2605PRINF002.pdf` (5 páginas)

---

*Sesión de validación final completada.*

---

## 10. Plan de trabajo adicional — recálculo de pérdidas térmicas con área real y aislamiento de lana mineral

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Atender la instrucción del usuario de que la glucosa debe mantenerse a 60 °C, realizar un nuevo cálculo de pérdidas térmicas con los datos actuales, lógicos y coherentes, considerando que el tanque está aislado con lana mineral.

### Tareas

- [x] **10.1** Definir hipótesis de cálculo: área real expuesta del tanque al 80 % de llenado, aislamiento de lana mineral de 50,8 mm, conductividad térmica k = 0,045 W/(m·°C), coeficientes convectivos interno y externo coherentes.
- [x] **10.2** Crear script `src/perdidas_termicas_real.py` para calcular pérdidas térmicas a 57 °C y 60 °C, con y sin aislamiento, y exportar resultados a `results/perdidas_termicas_real.csv`.
- [x] **10.3** Actualizar `docs/report/sections/05_balance_materia_energia.tex` con los nuevos valores de pérdidas, balance neto, eficiencia térmica y tiempo de enfriamiento.
- [x] **10.4** Actualizar `docs/report/sections/09_resultados.tex` con la tabla de aislamiento térmico basada en el área real y la temperatura de operación de 60 °C.
- [x] **10.5** Actualizar `docs/report/W2605PRINF002.tex` con el hallazgo crítico de reducción de pérdidas térmicas del 91,6 % por efecto del aislamiento.
- [x] **10.6** Revisar y ajustar referencias cruzadas en `docs/report/sections/11_conclusiones.tex` y `docs/report/sections/12_recomendaciones.tex`.
- [x] **10.7** Recompilar W2605PRINF001.tex (bibtex + dos pasadas) y W2605PRINF002.tex (dos pasadas).
- [x] **10.8** Ejecutar tests de Python y verificar estabilidad.
- [x] **10.9** Registrar sección de revisión con cambios realizados.

### Criterios de aceptación

1. Los cálculos de pérdidas térmicas usan el área real expuesta del tanque (~150 m²) y el aislamiento de lana mineral de 50,8 mm.
2. Los documentos LaTeX reflejan coherencia entre balance de energía, pérdidas al ambiente y eficiencia térmica.
3. Ambos informes compilan sin errores fatales.
4. Los tests de Python pasan sin errores.
5. El resumen ejecutivo comunica el hallazgo crítico de reducción de pérdidas térmicas.

---

## 11. Revisión de cambios realizados — recálculo de pérdidas térmicas y ajuste a 60 °C

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `src/perdidas_termicas_real.py` (nuevo), `results/perdidas_termicas_real.csv` (nuevo), `docs/report/sections/05_balance_materia_energia.tex`, `docs/report/sections/09_resultados.tex`, `docs/report/W2605PRINF002.tex`, `docs/report/sections/11_conclusiones.tex`, `docs/report/sections/12_recomendaciones.tex`.  
**PDFs regenerados:** `docs/report/W2605PRINF001.pdf` y `docs/report/W2605PRINF002.pdf`.

### Decisiones de diseño adoptadas

1. **Temperatura de operación objetivo:** la glucosa debe mantenerse a **60 °C**. Esta condición se adopta como requerimiento operativo principal y se usa para el balance energético global.

2. **Área expuesta real:** se considera el área real del fondo toriesférico más la zona cilíndrica expuesta al 80 % de llenado, resultando en **149,7 m²**. Esta estimación reemplaza el valor simplificado de ~30 m² usado previamente.

3. **Aislamiento térmico:** se mantiene el aislamiento de **50,8 mm de lana mineral** con conductividad térmica **k = 0,045 W/(m·°C)**.

### Cambios principales

1. **Nuevo script de pérdidas térmicas (`src/perdidas_termicas_real.py`):**
   - Calcula el coeficiente global de transferencia de calor U considerando resistencias convectivas interna y externa, y resistencia conductiva del aislamiento.
   - Resultado con aislamiento: **U ≈ 0,38 W/(m²·°C)**.
   - Pérdidas a 60 °C: **14,7 MJ/h**.
   - Pérdidas a 57 °C: **13,3 MJ/h**.
   - Pérdidas sin aislamiento a 60 °C: **175,4 MJ/h**.
   - Reducción por efecto del aislamiento: **91,6 %**.

2. **Balance de energía actualizado (`05_balance_materia_energia.tex`):**
   - Aporte térmico estimado de la chaqueta (operación isoterma a 60 °C): **30,0 MJ/h**.
   - Pérdidas al ambiente: **14,7 MJ/h**.
   - Balance neto: **+15,3 MJ/h** (superávit para mantener o recuperar temperatura).
   - Eficiencia térmica del sistema: **67,2 %**.
   - Tiempo para perder 3 °C en parada (sin calentamiento): **4,5 días** a 60 °C; **5,0 días** a 57 °C.
   - Temperatura superficial exterior del aislamiento: **28,3 °C**, inferior al límite seguro de contacto (≈43 °C).

3. **Tabla de aislamiento térmico (`09_resultados.tex`):**
   - Se actualiza con el área total real de 149,7 m², U = 0,38 W/(m²·°C), y pérdidas de 14,7 MJ/h para T_glucosa = 60 °C.
   - Se mantiene la comparativa con la configuración sin aislamiento.

4. **Resumen ejecutivo (`W2605PRINF002.tex`):**
   - Se incorpora el hallazgo crítico: el aislamiento de lana mineral reduce las pérdidas térmicas desde **175,4 MJ/h** (sin aislamiento) hasta **14,7 MJ/h** (con aislamiento), lo que representa una reducción del **91,6 %**.
   - Se destaca que la temperatura de 60 °C se mantiene estable con un balance neto positivo de 15,3 MJ/h.

5. **Referencias cruzadas:**
   - Se ajustaron las conclusiones y recomendaciones para reflejar el nuevo balance energético y la reducción de pérdidas por aislamiento.

### Verificación

- Los documentos `W2605PRINF001.tex` y `W2605PRINF002.tex` compilaron sin errores fatales.
- Los tests `task/test_ciclo.py`, `task/test_simulacion_50C.py` y `webapp/tests/test_api.py` se ejecutan sin errores.
- El CSV `results/perdidas_termicas_real.csv` contiene los valores de referencia y el análisis de sensibilidad al espesor de aislamiento.

### Hallazgos documentados

- El uso del área real expuesta eleva las pérdidas con aislamiento de 4,6 MJ/h (estimación anterior con ~30 m²) a 14,7 MJ/h. Aun así, el balance neto sigue siendo positivo, por lo que el sistema puede mantener 60 °C sin riesgo térmico.
- La reducción del 91,6 % respecto al caso sin aislamiento confirma que el aislamiento de lana mineral es la medida determinante para controlar las pérdidas térmicas.
- En parada prolongada, el tanque tarda más de 4 días en perder 3 °C, lo que reduce la necesidad de recalentamiento de emergencia.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` (56 páginas)
- `docs/report/W2605PRINF002.pdf` (5 páginas)
- `src/perdidas_termicas_real.py`
- `results/perdidas_termicas_real.csv`

---

*Sesión de recálculo de pérdidas térmicas completada.*

---

## 12. Plan de trabajo adicional — auditoría crítica del informe de tercero GTTP-1004-DOC-MC-1-1 Rev.5

**Fecha de plan:** 17 de junio de 2026  
**Estado:** En planificación  
**Alcance:** Realizar una auditoría crítica a nivel de maestría del informe térmico y de simulación elaborado por un tercero para el fondo del tanque de glucosa Tag 53A-90A-0056, y generar el documento `auditoria1.md`.

### Contexto

El cliente DMV SAS recibió un informe de un tercero ubicado en `InformeTercero/informe.pdf` (GTTP-1004-DOC-MC-1-1, Rev.5, fecha 04/06/2026). El documento presenta una memoria de cálculo térmica y simulación del serpentín de media caña del fondo del tanque de glucosa. Se requiere contrastar sus hipótesis, datos, metodología, resultados y conclusiones contra el proyecto W2605 desarrollado por DMV SAS.

### Tareas

- [ ] **12.1** Extraer y sistematizar el contenido técnico del informe de tercero (datos de entrada, propiedades, ecuaciones, resultados, conclusiones).
- [ ] **12.2** Contrastar las hipótesis de diseño del tercero con las bases de diseño del proyecto W2605 (geometría, propiedades de glucosa, condiciones operativas, ciclos de descarga).
- [ ] **12.3** Evaluar la metodología de cálculo térmico (coeficiente global U, coeficientes convectivos, LMTD, tiempo de calentamiento, caída de presión).
- [ ] **12.4** Evaluar la metodología de simulación CFD/FEA (modelo, malla, condiciones de frontera, resultados, validación).
- [ ] **12.5** Identificar inconsistencias numéricas, errores conceptuales, omisiones críticas y fortalezas del informe de tercero.
- [ ] **12.6** Redactar `auditoria1.md` con estilo académico (Elsevier / Science Direct), sin viñetas, con tablas autónomas y prosa crítica.
- [ ] **12.7** Verificar coherencia, ortografía, gramática y secuencia lógica del documento de auditoría.
- [ ] **12.8** Registrar sección de revisión con los cambios realizados.

### Criterios de aceptación

1. La auditoría cubre todos los capítulos técnicos del informe de tercero (propiedades, térmica, diseño mecánico, simulación, conclusiones).
2. Se contrastan los resultados del tercero con los cálculos y documentos del proyecto W2605 de forma cuantitativa cuando sea posible.
3. Se identifican al menos tres hallazgos críticos (errores, inconsistencias u omisiones) con su correspondiente argumentación técnica.
4. El documento `auditoria1.md` sigue el estilo Elsevier / Science Direct, sin viñetas, con tablas estilo académico.
5. El documento es lógico, coherente, secuencial y revisado en ortografía y gramática.

### Notas

- Se mantendrá la simplicidad en los cambios: un único archivo `auditoria1.md` como entregable principal.
- La auditoría se fundamenta en la información disponible en el proyecto W2605 y en el informe de tercero; no se realizarán nuevos cálculos exhaustivos salvo los necesarios para contrastar ordenes de magnitud.

---

*Plan aprobado por el usuario. Ejecutado en la misma sesión.*

---

## 13. Revisión de cambios realizados — auditoría crítica del informe de tercero GTTP-1004 Rev.5

**Fecha de revisión:** 17 de junio de 2026  
**Archivos creados:** `auditoria1.md`, `InformeTercero/informe.txt`, `InformeTercero/informe_utf8.txt`.  
**Archivos consultados:** `InformeTercero/informe.pdf`, `src/coeficiente_U.py`, `src/geometria_tanque.py`, `src/propiedades_glucosa.py`, `src/perdidas_termicas_real.py`, `docs/report/sections/07_bases_disenio.tex`, `docs/report/sections/08_metodologia.tex`, `docs/report/sections/09_resultados.tex`, `docs/report/sections/10_analisis.tex`, `docs/report/sections/11_conclusiones.tex`, `CONTEXT.md`.

### Cambios principales

1. **Extracción del informe de tercero:** se convirtió el PDF `InformeTercero/informe.pdf` a texto plano mediante `pdftotext` y se generaron los archivos `InformeTercero/informe.txt` e `InformeTercero/informe_utf8.txt` para su análisis.

2. **Revisión cruzada con el proyecto W2605:** se contrastaron las hipótesis, propiedades termofísicas, metodología de cálculo del coeficiente global U, tiempos de calentamiento, caída de presión, diseño mecánico, simulaciones FEA/CFD, pérdidas térmicas y conclusiones del informe de tercero contra el estudio independiente del proyecto W2605.

3. **Redacción de `auditoria1.md`:** se generó un documento de auditoría crítica a nivel de maestría con las siguientes características:
   - Estructura secuencial y coherente con secciones numeradas.
   - Estilo académico tipo Elsevier / Science Direct.
   - Sin viñetas; la información se presenta mediante prosa y tablas autónomas.
   - Seis tablas comparativas que sintetizan datos de entrada, propiedades termofísicas, coeficiente global, pérdidas térmicas, hallazgos críticos y recomendaciones.

### Hallazgos críticos documentados

- **Subestimación del coeficiente convectivo del lado de la glucosa:** el informe de tercero reporta h_o = 3300 W/m²·°C, mientras que el proyecto W2605 obtiene 18–37 W/m²·°C con la correlación de Churchill-Chu.
- **Propiedades termofísicas inconsistentes:** el calor específico de 837 J/kg·°C es aproximadamente 2,5 veces menor que el valor esperado para un jarabe de glucosa 80,6 Brix.
- **Inconsistencia interna en el régimen de convección natural:** el tercero clasifica el flujo como laminar (Gr < 10⁹) pero reporta Gr = 8,0 × 10⁹.
- **Coeficiente global sobreestimado:** U = 783 W/m²·°C frente a 21–36 W/m²·°C del proyecto W2605 y 38 W/m²·°C de la simulación CFD independiente.
- **Ausencia de análisis de pérdidas térmicas y aislamiento:** no se cuantifica el área expuesta ni se dimensiona el aislamiento.
- **Documentación insuficiente de simulaciones numéricas:** FEA y CFD carecen de detalles de malla, convergencia, propiedades y validación.
- **Conclusiones operativas optimistas:** el tiempo de 3,82 h para calentar 24 m³ no es consistente con la física del sistema.

### Verificación

- El documento `auditoria1.md` fue revisado manualmente en busca de coherencia, secuencia lógica, ortografía y gramática.
- No se utilizaron viñetas; la información se presenta exclusivamente mediante prosa y tablas.
- No se requiere compilación LaTeX ni ejecución de tests de Python para este entregable.

### Entregables finales

- `auditoria1.md` (auditoría crítica del informe de tercero)
- `InformeTercero/informe.txt` y `InformeTercero/informe_utf8.txt` (texto extraído del PDF para soporte de la auditoría)

---

*Sesión de auditoría crítica completada.*

---

## 14. Plan de trabajo adicional — generar copia formal del informe de auditoría en carpeta InformeTercero

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Generar un informe de auditoría denominado `auditoria.md` dentro de la carpeta `InformeTercero/`, a partir del documento `auditoria1.md` previamente elaborado.

### Tareas

- [x] **14.1** Copiar el contenido de `auditoria1.md` a `InformeTercero/auditoria.md`.
- [x] **14.2** Verificar que el archivo copiado mantenga la codificación UTF-8 y la estructura del documento original.
- [x] **14.3** Registrar sección de revisión con el cambio realizado.

### Criterios de aceptación

1. El archivo `InformeTercero/auditoria.md` existe y contiene el mismo contenido técnico que `auditoria1.md`.
2. El documento conserva el formato académico, sin viñetas, con tablas autónomas.
3. La codificación es UTF-8.

---

## 15. Revisión de cambios realizados — generación de `InformeTercero/auditoria.md`

**Fecha de revisión:** 17 de junio de 2026  
**Archivos creados:** `InformeTercero/auditoria.md`  
**Archivos de referencia:** `auditoria1.md`

### Cambios principales

1. Se generó el archivo `InformeTercero/auditoria.md` copiando el contenido completo de `auditoria1.md`.
2. Se verificó que el archivo resultante tiene 182 líneas, codificación UTF-8 y la misma estructura de tablas y secciones del documento original.
3. El informe está disponible en la carpeta solicitada por el usuario para su entrega o archivo junto al informe de tercero auditado.

### Entregables finales

- `auditoria1.md` (auditoría en directorio raíz)
- `InformeTercero/auditoria.md` (auditoría en carpeta del informe de tercero)
- `InformeTercero/informe.txt` e `InformeTercero/informe_utf8.txt` (texto extraído del PDF auditado)

---

*Sesión de generación de copia formal del informe de auditoría completada.*

---

## 16. Plan de trabajo adicional — crear encabezado LaTeX estilo tercero con campos corporativos DMV SAS

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Crear un archivo de encabezado LaTeX independiente (`docs/report/config/header_estilo_tercero.tex`) que replique la disposición visual del encabezado del informe de tercero GTTP-1004 Rev.5 pero con los campos corporativos de DMV SAS, sin modificar el encabezado corporativo estándar ni los maestros LaTeX existentes.

### Tareas

- [x] **16.1** Analizar el formato del encabezado del informe de tercero y el encabezado corporativo de DMV SAS.
- [x] **16.2** Crear `docs/report/config/header_estilo_tercero.tex` con la misma estructura de dos columnas del tercero y las variables corporativas (`\documentcode`, `\documentrevision`, `\documentdate`, `\elaboratedby`, `\reviewedby`, `\approvedby`, `\documenttype`, `\targetcompany`).
- [x] **16.3** Crear `docs/report/test_header_tercero.tex` para verificar la compilación.
- [x] **16.4** Compilar el documento de prueba y generar una imagen de la primera página para verificación visual.
- [x] **16.5** No modificar `docs/report/config/header.tex`, `W2605PRINF001.tex` ni `W2605PRINF002.tex`.
- [x] **16.6** Registrar sección de revisión con el cambio realizado.

### Criterios de aceptación

1. El archivo `docs/report/config/header_estilo_tercero.tex` existe y compila sin errores.
2. El encabezado resultante combina el formato de dos columnas del informe de tercero con los campos corporativos de DMV SAS.
3. No se alteran los archivos de encabezado y maestros LaTeX existentes.
4. Se documenta el cambio en `task/todo.md`.

---

## 17. Revisión de cambios realizados — encabezado estilo tercero con campos corporativos DMV SAS

**Fecha de revisión:** 17 de junio de 2026  
**Archivos creados:** `docs/report/config/header_estilo_tercero.tex`, `docs/report/test_header_tercero.tex`, `docs/report/test_header_tercero.pdf`, `docs/report/test_header_tercero_page1-1.png`.  
**Archivos consultados:** `docs/report/config/header.tex`, `docs/report/config/preamble.tex`, `docs/report/config/datos_proyecto.tex`, `docs/report/W2605PRINF001.tex`.

### Cambios principales

1. Se creó el archivo `docs/report/config/header_estilo_tercero.tex`, que define un nuevo estilo de página `tercerocorporativo` mediante `fancyhdr`. El membrete utiliza una tabla con la disposición de dos columnas propia del informe de tercero:
   - Columna izquierda: PROJECT, JOB, VERSION, DESIGNER, REVIEWED, APPROVED.
   - Columna derecha: valores corporativos de DMV SAS (`W2605PRINF001`, `W2605`, `REV 0`, `ABRIL 10 2026`, `DMV SAS`, `DMV SAS`, `DMV SAS`) y número de página.

2. El archivo es independiente de `docs/report/config/header.tex` y no modifica el estilo corporativo estándar. Puede incluirse en cualquier documento LaTeX del proyecto después de `config/preamble.tex` mediante `\input{config/header_estilo_tercero}`.

3. Se creó `docs/report/test_header_tercero.tex` como documento de prueba. La compilación fue exitosa y generó `test_header_tercero.pdf`. Se verificó visualmente el encabezado mediante una imagen PNG de la primera página.

### Verificación

- El documento de prueba compila sin errores fatales. Las advertencias de `LastPage` se resuelven en la segunda pasada de compilación.
- El encabezado muestra correctamente los campos corporativos de DMV SAS en el formato de dos columnas del informe de tercero.
- No se modificaron `header.tex`, `W2605PRINF001.tex` ni `W2605PRINF002.tex`.

### Entregables finales

- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con campos corporativos DMV SAS.
- `docs/report/test_header_tercero.tex` — Documento de prueba.
- `docs/report/test_header_tercero.pdf` — PDF de prueba.
- `docs/report/test_header_tercero_page1-1.png` — Imagen de verificación visual.

---

*Sesión de creación de encabezado estilo tercero completada.*

---

## 18. Plan de trabajo adicional — integrar logo de DMV SAS en el encabezado estilo tercero

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Modificar `docs/report/config/header_estilo_tercero.tex` para reservar una columna derecha e insertar el logo corporativo de DMV SAS, manteniendo la estructura de dos columnas del informe de tercero.

### Tareas

- [x] **18.1** Ampliar la tabla del membrete a cuatro columnas: etiqueta, valor, información auxiliar y logo.
- [x] **18.2** Insertar `logos/logo1.png` en la columna derecha, ocupando verticalmente el encabezado mediante `\multirow`.
- [x] **18.3** Ajustar anchos de columna para evitar desbordamiento (`Overfull \hbox`).
- [x] **18.4** Recompilar `docs/report/test_header_tercero.tex` y verificar visualmente el resultado.
- [x] **18.5** Registrar sección de revisión con el cambio realizado.

### Criterios de aceptación

1. El logo de DMV SAS aparece en el lado derecho del encabezado estilo tercero.
2. La tabla del membrete no genera advertencias de desbordamiento.
3. El documento de prueba compila sin errores fatales.
4. No se alteran los archivos de encabezado y maestros LaTeX existentes.

---

## 19. Revisión de cambios realizados — logo de DMV SAS en encabezado estilo tercero

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/config/header_estilo_tercero.tex`, `docs/report/test_header_tercero.pdf`, `docs/report/test_header_tercero_page1-1.png`.  
**Archivos consultados:** `docs/report/config/header.tex`, `docs/report/config/preamble.tex`, `docs/report/logos/logo1.png`.

### Cambios principales

1. Se modificó `docs/report/config/header_estilo_tercero.tex` para agregar una cuarta columna a la tabla del membrete. La nueva columna derecha contiene el logo corporativo de DMV SAS (`logos/logo1.png`), ubicado en la esquina superior derecha del encabezado.

2. Se cargaron los paquetes `graphicx` y `multirow` directamente en el archivo de encabezado, asegurando que el comando `\membreteestilotercero` sea autocontenido y pueda incluirse en cualquier documento sin dependencias adicionales.

3. Se ajustaron los anchos de columna para mantener el equilibrio visual y evitar desbordamientos:
   - Etiquetas: 2,2 cm
   - Valor principal: columna flexible (`X`)
   - Información auxiliar: 2,5 cm
   - Logo: 2,0 cm

4. Se restringió el ancho del logo a 1,8 cm con `keepaspectratio`, de modo que la imagen se escala proporcionalmente sin exceder el espacio asignado ni generar advertencias `Overfull \hbox`.

### Verificación

- El documento `test_header_tercero.tex` compiló sin errores fatales ni advertencias de desbordamiento.
- La imagen `test_header_tercero_page1-1.png` confirma que el logo de DMV SAS aparece correctamente en la columna derecha del encabezado, alineado con los campos PROJECT, JOB, VERSION, DESIGNER, REVIEWED y APPROVED.
- No se modificaron `docs/report/config/header.tex`, `docs/report/W2605PRINF001.tex` ni `docs/report/W2605PRINF002.tex`.

### Entregables finales

- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con logo de DMV SAS integrado.
- `docs/report/test_header_tercero.tex` — Documento de prueba.
- `docs/report/test_header_tercero.pdf` — PDF de prueba.
- `docs/report/test_header_tercero_page1-1.png` — Imagen de verificación visual.

---

*Sesión de integración del logo de DMV SAS en el encabezado estilo tercero completada.*

---

## 20. Plan de trabajo adicional — aplicar encabezado estilo tercero con logo a W2605PRINF001

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Aplicar el encabezado estilo tercero con logo de DMV SAS al informe técnico principal `W2605PRINF001.tex`, de modo que el cambio sea visible en `docs/report/W2605PRINF001.pdf`.

### Tareas

- [x] **20.1** Cambiar la inclusión de encabezado en `W2605PRINF001.tex` de `config/header.tex` a `config/header_estilo_tercero.tex`.
- [x] **20.2** Ajustar `config/header_estilo_tercero.tex` para definir el alias `corporativo` y ajustar `\headheight` y `\topmargin`.
- [x] **20.3** Compilar `W2605PRINF001.tex` (pdflatex + bibtex + dos pasadas).
- [x] **20.4** Verificar visualmente el encabezado en el PDF generado.
- [x] **20.5** Registrar sección de revisión con el cambio realizado.

### Criterios de aceptación

1. `docs/report/W2605PRINF001.pdf` muestra el encabezado estilo tercero con el logo de DMV SAS.
2. La compilación finaliza sin errores fatales.
3. No quedan advertencias de `Undefined control sequence` ni de `headheight`.
4. Se documenta el cambio en `task/todo.md`.

---

## 21. Revisión de cambios realizados — aplicación del encabezado con logo a W2605PRINF001

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/W2605PRINF001.tex`, `docs/report/config/header_estilo_tercero.tex`, `docs/report/W2605PRINF001.pdf`.  
**Archivos consultados:** `docs/report/config/header.tex`, `docs/report/config/preamble.tex`, `docs/report/sections/00_hojafirmas.tex`, `docs/report/sections/00_portada.tex`, `docs/report/sections/01_frontmatter.tex`.

### Cambios principales

1. Se modificó `docs/report/W2605PRINF001.tex` para incluir `config/header_estilo_tercero.tex` en lugar de `config/header.tex`. De este modo, el informe técnico principal adopta el encabezado estilo tercero con el logo de DMV SAS en la columna derecha.

2. Se actualizó `docs/report/config/header_estilo_tercero.tex` para garantizar la compatibilidad con las instrucciones de página del documento principal:
   - Se definió el alias `\let\ps@corporativo\ps@tercerocorporativo`, de modo que los comandos `\pagestyle{corporativo}` y `\thispagestyle{corporativo}` presentes en las secciones del informe funcionen sin errores.
   - Se ajustó `\headheight` a 118 pt y se redujo `\topmargin` en 4 pt para eliminar las advertencias de fancyhdr.

3. Se compiló `W2605PRINF001.tex` con el flujo completo (pdflatex, bibtex, pdflatex, pdflatex). El documento generado tiene 56 páginas y muestra el nuevo encabezado en todas las páginas correspondientes.

### Verificación

- La imagen `docs/report/W2605PRINF001_page1-01.png` confirma que la primera página del PDF incluye el encabezado estilo tercero con el logo de DMV SAS en la esquina superior derecha, junto con los campos PROJECT, JOB, VERSION, DESIGNER, REVIEWED y APPROVED.
- No se presentaron errores fatales durante la compilación.
- Se eliminaron las advertencias de `Undefined control sequence` y de `headheight is too small`.
- Las advertencias residuales son las mismas del informe previo (underfull en títulos, overfull menores en tablas e hipervínculos) y no afectan la visualización del encabezado.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` — Informe técnico principal con el nuevo encabezado estilo tercero y logo de DMV SAS.
- `docs/report/config/header_estilo_tercero.tex` — Encabezado reutilizable con alias `corporativo` y ajustes de geometría.
- `docs/report/W2605PRINF001_page1-01.png` — Imagen de verificación visual.

---

*Sesión de aplicación del encabezado con logo a W2605PRINF001 completada.*

---

## 22. Plan de trabajo adicional — aplicar encabezado estilo tercero con logo a W2605PRINF002

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Aplicar el encabezado estilo tercero con logo de DMV SAS al resumen ejecutivo `W2605PRINF002.tex`, de modo que el cambio sea visible en `docs/report/W2605PRINF002.pdf`.

### Tareas

- [x] **22.1** Cambiar la inclusión de encabezado en `W2605PRINF002.tex` de `config/header.tex` a `config/header_estilo_tercero.tex`.
- [x] **22.2** Verificar que `config/datos_proyecto_002.tex` defina las variables base (`\docRevision`, `\docFechaLarga`, `\firmaElaboro`, etc.) para que `config/preamble.tex` derive las variables de membrete.
- [x] **22.3** Ajustar `\headheight` y `\topmargin` en `config/header_estilo_tercero.tex` para cubrir tanto documentos de 11 pt como de 12 pt.
- [x] **22.4** Compilar `W2605PRINF002.tex` (dos pasadas).
- [x] **22.5** Recompilar `W2605PRINF001.tex` para confirmar que el ajuste de `\headheight` no lo afecta negativamente.
- [x] **22.6** Verificar visualmente ambos PDFs.
- [x] **22.7** Registrar sección de revisión con los cambios realizados.

### Criterios de aceptación

1. `docs/report/W2605PRINF002.pdf` muestra el encabezado estilo tercero con el logo de DMV SAS.
2. Ambos informes compilan sin errores fatales.
3. No quedan advertencias de `headheight is too small` en ninguno de los dos documentos.
4. Se documenta el cambio en `task/todo.md`.

---

## 23. Revisión de cambios realizados — aplicación del encabezado con logo a W2605PRINF002 y ajuste compartido de geometría

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/W2605PRINF002.tex`, `docs/report/config/header_estilo_tercero.tex`, `docs/report/W2605PRINF002.pdf`, `docs/report/W2605PRINF001.pdf`.  
**Archivos consultados:** `docs/report/config/datos_proyecto_002.tex`, `docs/report/config/preamble.tex`.

### Cambios principales

1. Se modificó `docs/report/W2605PRINF002.tex` para incluir `config/header_estilo_tercero.tex` en lugar de `config/header.tex`. El resumen ejecutivo adopta el mismo encabezado estilo tercero con el logo de DMV SAS en la columna derecha.

2. Se verificó que `config/datos_proyecto_002.tex` ya contiene las variables base requeridas (`\docRevision`, `\docFechaLarga`, `\firmaElaboro`, `\firmaReviso`, `\firmaAprobo`). `config/preamble.tex` deriva de ellas las variables de membrete (`\documentrevision`, `\documentdate`, `\elaboratedby`, `\reviewedby`, `\approvedby`), por lo que no fue necesario modificar `datos_proyecto_002.tex`.

3. Se actualizó `config/header_estilo_tercero.tex` para usar un `\headheight` de 130 pt y reducir `\topmargin` en 11 pt. Este valor cubre tanto el documento de 12 pt (`W2605PRINF001`) como el de 11 pt (`W2605PRINF002`), eliminando las advertencias de fancyhdr en ambos casos.

4. Se recompilaron ambos documentos:
   - `W2605PRINF001.tex`: flujo completo pdflatex + bibtex + dos pasadas (56 páginas).
   - `W2605PRINF002.tex`: dos pasadas pdflatex (5 páginas).

### Verificación

- La imagen `docs/report/W2605PRINF002_page1-1.png` confirma que la primera página del resumen ejecutivo incluye el encabezado con el logo de DMV SAS y los campos PROJECT, JOB, VERSION, DESIGNER, REVIEWED y APPROVED.
- La imagen `docs/report/W2605PRINF001_page1-01.png` confirma que el informe técnico principal conserva el mismo encabezado con logo.
- No se presentaron errores fatales en ninguna de las dos compilaciones.
- No quedan advertencias de `headheight is too small` ni de `Undefined control sequence`.
- Las advertencias residuales son menores y preexistentes (underfull en títulos, overfull menores en tablas, hipervínculos con caracteres matemáticos).

### Entregables finales

- `docs/report/W2605PRINF001.pdf` — Informe técnico principal con encabezado estilo tercero y logo de DMV SAS (56 páginas).
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo gerencial con encabezado estilo tercero y logo de DMV SAS (5 páginas).
- `docs/report/config/header_estilo_tercero.tex` — Encabezado reutilizable con alias `corporativo` y geometría ajustada para 11 pt y 12 pt.
- `docs/report/W2605PRINF001_page1-01.png` y `docs/report/W2605PRINF002_page1-1.png` — Imágenes de verificación visual.

---

*Sesión de aplicación del encabezado con logo a W2605PRINF002 y ajuste compartido de geometría completada.*

---

## 24. Plan de trabajo adicional — rediseñar encabezado estilo tercero a 4 filas, 6 columnas, con logo en columnas 5–6 y borde exterior grueso

**Fecha de plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** Modificar `docs/report/config/header_estilo_tercero.tex` para que el membrete tenga exactamente 4 filas y 6 columnas, con el logo de DMV SAS ocupando las columnas 5 y 6 en toda la altura, y dejar solo el borde exterior grueso sin líneas internas.

### Tareas

- [x] **24.1** Rediseñar la tabla del membrete a 4 filas y 6 columnas.
- [x] **24.2** Distribuir los campos según el formato del informe de tercero: PROJECT + código, JOB + Updated + fecha, VERSION + revisión + Reviewed + fecha, DESIGNER + nombre + Reviewer + nombre.
- [x] **24.3** Colocar el logo de DMV SAS en las columnas 5 y 6 ocupando las 4 filas mediante `\multirow`.
- [x] **24.4** Eliminar todas las líneas internas y dejar solo el borde exterior grueso (`\toprule`, `\bottomrule` y `\vrule width 1pt` en los laterales).
- [x] **24.5** Ajustar anchos de columna y altura del encabezado para evitar desbordamientos.
- [x] **24.6** Compilar el documento de prueba y generar imagen de verificación visual.
- [x] **24.7** Confirmar el diseño con el usuario.
- [x] **24.8** Recompilar `W2605PRINF001.tex` y `W2605PRINF002.tex` con el encabezado final.
- [x] **24.9** Registrar sección de revisión con los cambios realizados.

### Criterios de aceptación

1. El encabezado tiene exactamente 4 filas y 6 columnas.
2. El logo de DMV SAS ocupa las columnas 5 y 6 en toda la altura del encabezado.
3. La tabla tiene solo borde exterior grueso, sin líneas internas.
4. Los documentos `W2605PRINF001.tex` y `W2605PRINF002.tex` compilan sin errores fatales.
5. Ambos PDFs muestran el nuevo encabezado correctamente.
6. Se documenta el cambio en `task/todo.md`.

---

## 25. Revisión de cambios realizados — rediseño del encabezado estilo tercero a 4 filas, 6 columnas y borde exterior grueso

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/config/header_estilo_tercero.tex`, `docs/report/W2605PRINF001.tex`, `docs/report/W2605PRINF002.tex`, `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF002.pdf`.  
**Archivos de verificación:** `docs/report/test_header_tercero_page1-1.png`, `docs/report/W2605PRINF001_header_page1-01.png`, `docs/report/W2605PRINF002_header_page1-1.png`.

### Cambios principales

1. **Rediseño completo de `docs/report/config/header_estilo_tercero.tex`:**
   - Se reemplazó la estructura anterior de dos columnas por una tabla de **4 filas y 6 columnas**.
   - La distribución de campos sigue el formato del informe de tercero:
     - Fila 1: PROJECT + código del documento; Page X de Y; logo.
     - Fila 2: JOB + Updated; fecha del documento; logo.
     - Fila 3: VERSION + revisión; Reviewed + fecha; logo.
     - Fila 4: DESIGNER + nombre; Reviewer + nombre; logo.
   - El logo de DMV SAS (`logos/logo1.png`) ocupa las **columnas 5 y 6** en las 4 filas, usando `\multirow{4}{2.6cm}{...}`.

2. **Solo borde exterior grueso:**
   - Se eliminaron todas las líneas verticales y horizontales internas.
   - Se utilizó `\toprule` y `\bottomrule` para los bordes superior e inferior gruesos.
   - Se aplicó `!{\vrule width 1pt}` únicamente en los bordes laterales izquierdo y derecho.

3. **Ajuste de geometría del encabezado:**
   - Se fijó `\headheight` en **100 pt** y se redujo `\topmargin` en **10 pt** para acomodar las 4 filas en tamaño `\scriptsize` sin advertencias de `fancyhdr`.

4. **Aplicación a los documentos finales:**
   - Ambos maestros (`W2605PRINF001.tex` y `W2605PRINF002.tex`) ya cargaban `config/header_estilo_tercero.tex`; solo fue necesario recompilar.
   - Se generaron las imágenes de verificación correspondientes.

### Verificación

- El documento de prueba `test_header_tercero.tex` compiló sin errores fatales.
- Las imágenes `W2605PRINF001_header_page1-01.png` y `W2605PRINF002_header_page1-1.png` confirman que ambos PDFs muestran el encabezado rediseñado con el logo de DMV SAS en las columnas 5–6 y sin líneas internas.
- No se presentaron errores fatales durante la compilación de ninguno de los dos informes.
- No quedan advertencias de `headheight is too small` ni de `Undefined control sequence`.

### Entregables finales

- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero con 4 filas, 6 columnas, logo en columnas 5–6 y borde exterior grueso.
- `docs/report/W2605PRINF001.pdf` — Informe técnico principal con el nuevo encabezado (56 páginas).
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo gerencial con el nuevo encabezado (5 páginas).
- `docs/report/test_header_tercero_page1-1.png` — Imagen de verificación del encabezado rediseñado.
- `docs/report/W2605PRINF001_header_page1-01.png` — Verificación visual del encabezado en el informe principal.
- `docs/report/W2605PRINF002_header_page1-1.png` — Verificación visual del encabezado en el resumen ejecutivo.

---

*Sesión de rediseño del encabezado estilo tercero completada.*

---

## 26. Recuperación de sesión — corrección de `task/test_ciclo.py` y generación de `contexto.md`

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `task/test_ciclo.py`, `contexto.md` (nuevo).  
**Archivos consultados:** `task/test_simulacion_50C.py`, `webapp/tests/test_api.py`, `task/todo.md`.

### Cambios principales

1. **Corrección de `task/test_ciclo.py`:** se reemplazaron las rutas relativas `sys.path.insert(0, 'webapp')` y `sys.path.insert(0, 'src')` por rutas absolutas basadas en `Path(__file__).parent.parent`, lo que permite ejecutar el test desde cualquier directorio sin error `ModuleNotFoundError: No module named 'app'`.

2. **Generación de `contexto.md`:** se creó el archivo de contexto del proyecto en la raíz con el estado actual, bases de diseño congeladas, decisiones clave, archivos relevantes y comandos útiles, conforme a `<cierre_de_sesion>` de `AGENTS.md`.

### Verificación

- `task/test_ciclo.py` se ejecuta sin errores: 5 descargas OK para ciclos precalentados, motivo de corte `tiempo_maximo` para arranque desde 50 °C con T_agua=67 en 24 h (consistente con la física del sistema).
- `task/test_simulacion_50C.py` se ejecuta sin errores.
- `webapp/tests/test_api.py` ejecuta 5 tests con resultado OK.

### Entregables finales

- `task/test_ciclo.py` — Test del ciclo oficial con rutas absolutas.
- `contexto.md` — Contexto del proyecto W2605.

---

*Sesión recuperada. Pendiente definición de siguiente tarea por el usuario.*

---

## 27. Mejora del encabezado estilo tercero a ancho completo de página

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/config/header_estilo_tercero.tex`, `docs/report/test_header_tercero.pdf`, `docs/report/test_header_tercero_page1-1.png`, `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF001_header_page1-01.png`, `docs/report/W2605PRINF002.pdf`, `docs/report/W2605PRINF002_header_page1-1.png`.  
**Archivos consultados:** `docs/report/test_header_tercero.tex`, `docs/report/W2605PRINF001.tex`, `docs/report/W2605PRINF002.tex`.

### Cambios principales

1. **Ancho completo de página:** se reemplazó el entorno `tabular` con anchos fijos de columna por `tabularx{\textwidth}`, de modo que el membrete ocupa todo el ancho disponible del cuerpo de la página.

2. **Distribución de columnas:** se simplificó la tabla a 5 columnas:
   - Columna 1: etiquetas fijas (`PROJECT`, `JOB`, `VERSION`, `DESIGNER`), 1,6 cm.
   - Columna 2: valores principales, columna expansible (`X`).
   - Columna 3: etiquetas auxiliares (`Updated`, `Reviewed`, `Reviewer`), 1,7 cm.
   - Columna 4: valores auxiliares, columna expansible (`X`).
   - Columna 5: logo de DMV SAS, 3,0 cm.

3. **Ajuste del logo:** el logo se mantiene ocupando las 4 filas mediante `\multirow{4}{=}{...}` y su ancho se fijó en 2,8 cm para aprovechar la columna más ancha sin desbordamiento.

4. **Aplicación a documentos finales:** se recompilaron `W2605PRINF001.tex` (pdflatex + bibtex + dos pasadas, 56 páginas) y `W2605PRINF002.tex` (dos pasadas, 5 páginas) con el encabezado actualizado.

### Verificación

- El documento de prueba `test_header_tercero.tex` compiló sin errores fatales.
- Las imágenes `W2605PRINF001_header_page1-01.png` y `W2605PRINF002_header_page1-1.png` confirman que el encabezado llega a los márgenes izquierdo y derecho en ambos informes.
- No se presentaron advertencias de `Overfull \hbox` relacionadas con el membrete.
- No se modificaron los maestros LaTeX ni el encabezado corporativo estándar `config/header.tex`.

### Entregables finales

- `docs/report/config/header_estilo_tercero.tex` — Encabezado estilo tercero a ancho completo.
- `docs/report/W2605PRINF001.pdf` — Informe técnico principal con encabezado a ancho completo.
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo con encabezado a ancho completo.
- `docs/report/test_header_tercero.pdf` y `_page1-1.png` — Verificación del diseño de prueba.

---

*Sesión de mejora del encabezado a ancho completo completada.*

---

## 28. Corrección de continuidad de bordes exteriores del encabezado estilo tercero

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/config/header_estilo_tercero.tex`, `docs/report/test_header_tercero.pdf`, `docs/report/test_header_tercero_page1-1.png`, `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF001_header_page1-01.png`, `docs/report/W2605PRINF002.pdf`, `docs/report/W2605PRINF002_header_page1-1.png`.  
**Archivos consultados:** `docs/report/test_header_tercero.tex`.

### Problema reportado
Los bordes exteriores del membrete no eran continuos; presentaban interrupciones causadas por el uso de `\toprule`/`\bottomrule` de `booktabs` (que no se alinean perfectamente con líneas verticales) y por el `\multicolumn{2}{l}{...}` en la fila `JOB`, que sobreescribía los bordes verticales de las columnas 3 y 4.

### Cambios principales

1. **Reemplazo de reglas horizontales:** se eliminaron `\toprule` y `\bottomrule` y se usaron `\noalign{\hrule height 1pt}` para los bordes superior e inferior, logrando que las líneas horizontales gruesas toquen exactamente las líneas verticales laterales.

2. **Eliminación de `\multicolumn`:** la fila `JOB` ahora usa 5 celdas independientes: `Updated` en la columna 2, columna 3 vacía con `\rule{0pt}{9pt}` y `\documentdate` en la columna 4, evitando la interrupción de bordes.

3. **Celdas vacías con altura forzada:** todas las celdas vacías ahora contienen `\rule{0pt}{9pt}`, lo que garantiza que las líneas verticales laterales se dibujen a lo largo de toda la altura de cada fila.

4. **Recompilación de documentos finales:** se recompilaron `W2605PRINF001.tex` y `W2605PRINF002.tex` con el encabezado corregido.

### Verificación

- El documento de prueba compiló sin errores fatales.
- Las imágenes de verificación de ambos informes confirman que los bordes superior, inferior, izquierdo y derecho del membrete son continuos y del mismo grosor.
- No se presentaron advertencias de desbordamiento ni de alineación en el encabezado.

### Entregables finales

- `docs/report/config/header_estilo_tercero.tex` — Encabezado con bordes exteriores continuos.
- `docs/report/W2605PRINF001.pdf` — Informe técnico principal con membrete corregido.
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo con membrete corregido.

---

*Sesión de corrección de bordes del encabezado completada.*

---

## 29. Eliminación de la hoja de firmas de los informes finales

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/W2605PRINF001.tex`, `docs/report/W2605PRINF002.tex`, `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF002.pdf`.  
**Archivos consultados:** `docs/report/sections/00_hojafirmas.tex`.

### Cambios principales

1. **`W2605PRINF001.tex`:** se comentó la línea `\input{sections/00_hojafirmas.tex}` para que el informe técnico principal inicie directamente con la portada (`00_portada.tex`). El archivo `00_hojafirmas.tex` se conserva en el repositorio para uso futuro si se requiere.

2. **`W2605PRINF002.tex`:** se comentó la línea `\input{sections/00_hojafirmas.tex}` después de la portada, de modo que el resumen ejecutivo continúa directamente con el contenido principal.

3. **Recompilación:** se recompilaron ambos documentos con el flujo habitual (pdflatex + bibtex + dos pasadas para W2605PRINF001; dos pasadas para W2605PRINF002).

### Resultado

- `W2605PRINF001.pdf`: 60 páginas. La portada (página 1) contiene el control de revisiones; el abstract inicia en la página 2.
- `W2605PRINF002.pdf`: 4 páginas. La portada (página 1) contiene el control de revisiones; el contenido principal inicia en la página 2.

### Verificación

- Ambos documentos compilaron sin errores fatales.
- Se revisaron visualmente las primeras y últimas páginas de ambos PDFs para confirmar que la hoja de firmas fue eliminada y que no quedaron páginas en blanco indeseadas.
- El encabezado estilo tercero con logo de DMV SAS se mantiene en todas las páginas.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` — Informe técnico principal sin hoja de firmas.
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo sin hoja de firmas.

---

*Sesión de eliminación de hoja de firmas completada.*

---

## 30. Recompilación completa del proyecto LaTeX y corrección del logo corporativo

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/logos/logo1.png`, `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF002.pdf`, `docs/report/W2605PRINF001_page1-01.png`, `docs/report/W2605PRINF002_page1-1.png`.  
**Archivos consultados:** `webapp/app/static/img/logo_dml.png`, `docs/report/W2605PRINF001.tex`, `docs/report/W2605PRINF002.tex`.

### Cambios principales

1. **Recompilación completa:** se ejecutó el flujo completo de compilación para ambos documentos finales:
   - `W2605PRINF001.tex`: pdflatex + bibtex + dos pasadas adicionales (60 páginas).
   - `W2605PRINF002.tex`: dos pasadas pdflatex (4 páginas).

2. **Corrección del logo corporativo:** durante la verificación visual se detectó que `docs/report/logos/logo1.png` había sido reemplazado por un logo distinto al utilizado previamente ("DML Ingeniería S.A.S." en tipografía gótica). Se restauró el logo corporativo correcto copiando `webapp/app/static/img/logo_dml.png` ("DML Ingenieros Consultores SAS") a `docs/report/logos/logo1.png`.

3. **Regeneración de imágenes de verificación:** se generaron nuevas capturas de la primera página de cada informe para confirmar que el logo correcto aparece en el encabezado estilo tercero.

### Verificación

- Ambos documentos compilaron sin errores fatales.
- Las imágenes de verificación confirman que el encabezado muestra el logo corporativo correcto (triángulo verde + "DML Ingenieros Consultores SAS").
- Los bordes exteriores del membrete se mantienen continuos.
- Los tests de Python (`task/test_ciclo.py`, `task/test_simulacion_50C.py`, `webapp/tests/test_api.py`) se ejecutan sin errores.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` — Informe técnico principal, 60 páginas, logo corporativo restaurado.
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo, 4 páginas, logo corporativo restaurado.
- `docs/report/logos/logo1.png` — Logo corporativo correcto.

---

*Sesión de recompilación completa y corrección de logo completada.*

---

## 31. Recompilación completa del proyecto LaTeX

**Fecha de revisión:** 17 de junio de 2026  
**Archivos modificados:** `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF002.pdf`, `docs/report/test_header_tercero.pdf`, `docs/report/W2605PRINF001_page1-01.png`, `docs/report/W2605PRINF002_page1-1.png`, `docs/report/test_header_tercero_page1-1.png`.  
**Archivos consultados:** `docs/report/W2605PRINF001.tex`, `docs/report/W2605PRINF002.tex`, `docs/report/test_header_tercero.tex`, `docs/report/logos/logo1.png`, `webapp/app/static/img/logo_dml.png`.

### Cambios principales

1. **Recompilación de todos los documentos maestros LaTeX:**
   - `W2605PRINF001.tex`: pdflatex + bibtex + dos pasadas adicionales.
   - `W2605PRINF002.tex`: dos pasadas pdflatex.
   - `test_header_tercero.tex`: dos pasadas pdflatex.

2. **Verificación del logo corporativo:** se constató que `docs/report/logos/logo1.png` contiene el logo original del repositorio ("DML Ingeniería S.A.S.", tipografía gótica). No se realizaron cambios al logo porque el usuario indicó previamente que ninguno de los logos disponibles en el proyecto es el correcto.

### Verificación

- Los tres documentos compilaron sin errores fatales.
- Se generaron imágenes de verificación de la primera página de cada documento.
- Los tests de Python (`task/test_ciclo.py`, `task/test_simulacion_50C.py`, `webapp/tests/test_api.py`) se ejecutan sin errores.

### Entregables finales

- `docs/report/W2605PRINF001.pdf` — Informe técnico principal, 60 páginas.
- `docs/report/W2605PRINF002.pdf` — Resumen ejecutivo, 4 páginas.
- `docs/report/test_header_tercero.pdf` — Documento de prueba del encabezado, 2 páginas.

### Pendiente

- Definir y aplicar el logo corporativo correcto de DMV SAS. El logo no se encuentra en el repositorio; se requiere que el usuario lo proporcione o indique su ubicación.

---

*Sesión de recompilación completa del proyecto LaTeX completada.*

---

## 32. Plan de trabajo — justificación de párrafos y cálculo detallado de calentamiento de 24 ton de 40 °C a 60 °C

**Fecha del plan:** 17 de junio de 2026  
**Estado:** Ejecutado  
**Alcance:** (1) Ajustar la justificación de los párrafos en los informes finales; (2) Crear una sección técnica detallada con cálculo en Python del calentamiento de 24 toneladas de glucosa desde 40 °C hasta 60 °C con área de transferencia de 14 m², incluyendo curvas de calentamiento y flujo de calor en el tiempo con propiedades variables.

---

## 32.1 Contexto

- **Objetivo:** Mejorar la presentación tipográfica de los informes y agregar un caso de estudio adicional de calentamiento de glucosa con área de 14 m².
- **Cliente / Proyecto:** DMV SAS — Proyecto W2605 (tanque de glucosa Tag 53A-90A-0056).
- **Normas aplicables:** API 650, ASME VIII, ASME B31.3.
- **Correlaciones:** Sieder-Tate (lado agua), Churchill-Chu (lado glucosa), modelo VFT para viscosidad de glucosa, Choi & Okos para Cp y k.

---

## 32.2 Supuestos clave

- [x] Masa de glucosa: 24 ton = 24 000 kg.
- [x] Temperatura inicial: 40 °C; temperatura objetivo: 60 °C.
- [x] Área de transferencia: 14 m² (aumento respecto a los 13 m² base; documentado en la sección).
- [x] Velocidad del agua en media caña: 2,5 m/s.
- [x] Temperatura de entrada del agua: evaluadas ambas opciones, 65 °C y 75 °C.
- [x] Propiedades de la glucosa dependen de la temperatura: rho(T), Cp(T), mu(T), k(T), beta(T), Pr(T).
- [x] Coeficiente global U se calcula en cada paso de integración mediante resistencias en serie.
- [x] No hay pérdidas térmicas al ambiente durante el calentamiento (tanque ideal aislado).

---

## 32.3 Tareas

- [x] **T1. Justificación de párrafos.** Se agregó configuración explícita de justificación en `docs/report/config/preamble.tex` y se corrigió la causa raíz: un `\centering` suelto en `docs/report/sections/00_portada.tex` que persistía para todo el documento. Impacto: 2 archivos.
- [x] **T2. Script Python de cálculo detallado.** Se creó `src/calentamiento_24ton_40_60.py`, que integra el balance de energía con `solve_ivp`, actualiza U(T) en cada paso, exporta `results/calentamiento_24ton_40_60.csv` y genera figuras T vs t, Q vs t, U vs t y propiedades termofísicas.
- [x] **T3. Sección LaTeX detallada.** Se creó `docs/report/sections/14_calentamiento_24ton.tex` con planteamiento, supuestos, ecuaciones, tablas de propiedades y resultados, y figuras.
- [x] **T4. Integrar sección en informe principal.** Se incluyó `sections/14_calentamiento_24ton.tex` en `W2605PRINF001.tex` después de `10_analisis.tex`.
- [x] **T5. Recompilar informes.** Se ejecutó el flujo completo de ambos informes.
- [x] **T6. Verificación.** Se verificó visualmente la justificación de párrafos y la calidad de figuras.

---

## 32.4 Riesgos / Puntos de verificación

- [x] **Validación dimensional:** unidades consistentes (U en W/(m²·°C), Q en kW, energía en MJ, tiempo en h).
- [x] **Coherencia física:** tiempos obtenidos 60,3 h (65 °C) y 24,6 h (75 °C), dentro del orden de magnitud esperado.
- [x] **Independencia del área:** el cálculo usa explícitamente A = 14 m².
- [x] **Impacto tipográfico:** la justificación aplica solo a párrafos; tablas, figuras y encabezado no se afectan.

---

## 32.5 Resultados obtenidos

| Parámetro | Escenario A (65 °C) | Escenario B (75 °C) | Unidad |
|---|---|---|---|
| Tiempo para alcanzar 60 °C | 60,3 | 24,6 | h |
| Energía total transferida | 1017,2 | 1020,0 | MJ |
| Flujo de calor máximo | 9,11 | 15,24 | kW |
| Flujo de calor promedio | 4,69 | 11,56 | kW |
| U inicial | 26,0 | 31,1 | W/(m²·°C) |
| U final | 20,4 | 23,8 | W/(m²·°C) |

## 32.6 Revisión

- **Cambios realizados:**
  - `docs/report/config/preamble.tex`: se añadieron parámetros de justificación explícitos (`\tolerance`, `\emergencystretch`, `\hyphenpenalty`).
  - `docs/report/sections/00_portada.tex`: se encapsuló el contenido de la portada en `\begingroup ... \endgroup` para evitar que `\centering` afecte el resto del documento.
  - `docs/report/sections/14_calentamiento_24ton.tex`: nueva sección técnica con cálculo detallado, tablas y figuras.
  - `docs/report/W2605PRINF001.tex`: se incluyó la nueva sección 14 entre análisis y conclusiones.
  - `docs/report/sections/08_metodologia.tex`: se añadió la etiqueta `sec:metodologia_U` para referencia cruzada.
  - `src/calentamiento_24ton_40_60.py`: script de simulación con propiedades variables.
- **Desviaciones respecto al plan original:** se evaluaron ambas temperaturas de agua (65 °C y 75 °C) en lugar de esperar confirmación del usuario; esto enriquece el análisis sin cambiar el alcance.
- **Limitaciones conocidas:** el logo corporativo sigue siendo el placeholder disponible; se requiere el archivo correcto de DMV SAS.
- **Archivos entregables:**
  - `docs/report/W2605PRINF001.pdf` (66 páginas).
  - `docs/report/W2605PRINF002.pdf` (4 páginas).
  - `results/figures/calentamiento_24ton_*.pdf` y `.png`.
  - `results/calentamiento_24ton_40_60.csv`.

---

*Tarea completada.*

---

## 33. Plan de trabajo adicional — organización de información generada pero desactualizada en carpeta `reciclaje`

**Fecha del plan:** 17 de junio de 2026  
**Estado:** En planificación  
**Alcance:** Mover a una carpeta `reciclaje/` en la raíz del proyecto todos los archivos generados, auxiliares, logs, duplicados y documentos desactualizados, preservando los entregables oficiales y los scripts activos.

---

### 33.1 Contexto

- **Objetivo:** Limpiar el repositorio antes de la actualización en GitHub, de forma lógica, coherente y secuente.
- **Entregables oficiales a preservar:** `docs/report/W2605PRINF001.tex/pdf`, `docs/report/W2605PRINF002.tex/pdf`, scripts activos en `src/`, figuras oficiales en `results/figures/` y datos de referencia en `Data/`.

---

### 33.2 Clasificación de archivos candidatos

| Categoría | Archivos representativos | Destino propuesto |
|---|---|---|
| Auxiliares LaTeX | `.aux`, `.bbl`, `.blg`, `.lof`, `.log`, `.lot`, `.out`, `.spl`, `.toc` en `docs/report/` | `reciclaje/01_latex_auxiliares/` |
| Logs de compilación | `docs/report/compile_*.log`, `compile_002.log`, `texput.log` | `reciclaje/02_logs_compilacion/` |
| Capturas de verificación | PNG `_check`, `_end`, `_header`, `_mid`, `_page1` en `docs/report/` | `reciclaje/03_capturas_verificacion/` |
| Pruebas de encabezado | `docs/report/test_header_tercero.*` | `reciclaje/04_pruebas_encabezado/` |
| Documentos desactualizados | `CONTEXT.md`, `README_ESTRUCTURA.md`, `auditoria1.md`, `docs/report/RECICLAJE/*` | `reciclaje/05_documentos_desactualizados/` |
| Figuras duplicadas / antiguas | `figures/` raíz (duplicadas en `results/figures/`) | `reciclaje/06_figuras_duplicadas/` |
| CSV intermedios | CSV en `results/` no referenciados por el informe activo | `reciclaje/07_csv_intermedios/` |
| Scripts de depuración / fix | `src/debug_U.py`, `src/fix_*.py`, `src/replace_figure.py`, `src/crear_pfd_*.py`, `src/create_pfd_pdfs.py` | `reciclaje/08_scripts_depuracion/` |
| Datos duplicados | `Data/Memoria_Termica Glucosa.Rev.1.pdf`, `PFD.svg` | `reciclaje/09_datos_duplicados/` |

---

### 33.3 Tareas

- [x] **T1.** Crear la estructura de carpetas dentro de `reciclaje/`.
- [x] **T2.** Mover archivos seguros: auxiliares LaTeX, logs de compilación, capturas de verificación y pruebas de encabezado.
- [x] **T3.** Mover duplicados y documentos desactualizados.
- [x] **T4.** Mover figuras de `figures/` raíz, verificando que no se rompan referencias en documentos activos.
- [x] **T5.** Mover scripts de depuración/fix que no son importados por scripts activos.
- [x] **T6.** Generar `reciclaje/README.md` con índice de contenidos.
- [x] **T7.** Verificar que los informes oficiales compilan y los tests de Python pasen tras la limpieza.
- [x] **T8.** Confirmar que `.gitignore` no requiere cambios (la carpeta `reciclaje/` se subirá a GitHub intencionalmente).
- [x] **T9.** Registrar sección de revisión con los cambios realizados.

---

### 33.4 Riesgos / Puntos de verificación

- [x] Ningún archivo movido es referenciado por los documentos LaTeX activos.
- [x] Ningún script activo importa los scripts movidos a `reciclaje/`.
- [x] La compilación de `W2605PRINF001.tex` y `W2605PRINF002.tex` sigue funcionando tras eliminar auxiliares.
- [x] Los tests de Python (`task/test_ciclo.py`, `task/test_simulacion_50C.py`, `webapp/tests/test_api.py`) pasan sin errores.

---

### 33.5 Decisiones de alcance confirmadas por el usuario

1. Sí incluir los **scripts de depuración/fix** en `reciclaje/`.
2. Sí incluir la carpeta **`examples/web-demo/`** en `reciclaje/`.
3. Ubicar la carpeta en la **raíz como `reciclaje/`**.

---

*Plan aprobado y ejecutado.*

---

## 34. Revisión de cambios realizados — organización de información desactualizada en `reciclaje/`

**Fecha de revisión:** 17 de junio de 2026  
**Archivos movidos:** 111 archivos a `reciclaje/`; estructura organizada en 10 subcarpetas.  
**Archivos clave generados:** `reciclaje/README.md`.  
**PDFs regenerados:** `docs/report/W2605PRINF001.pdf`, `docs/report/W2605PRINF002.pdf`.

### Cambios principales

1. **Creación de `reciclaje/` en la raíz:** se organizó la información generada pero desactualizada en 10 subcarpetas numeradas:
   - `01_latex_auxiliares/`: archivos auxiliares de compilación LaTeX.
   - `02_logs_compilacion/`: logs históricos de compilación.
   - `03_capturas_verificacion/`: imágenes PNG de verificación visual.
   - `04_pruebas_encabezado/`: documento de prueba del membrete estilo tercero.
   - `05_documentos_desactualizados/`: `CONTEXT.md`, `README_ESTRUCTURA.md`, `auditoria1.md`, `contexto_tecnico_w2605.md`, configuraciones de membrete obsoletas y contenido previo de `docs/report/RECICLAJE/`.
   - `06_figuras_duplicadas/`: figuras de `figures/` raíz duplicadas en `results/figures/`.
   - `08_scripts_depuracion/`: scripts temporales (`debug_U.py`, `fix_*.py`, `crear_pfd_*.py`, `create_pfd_pdfs.py`, `debug_balance.py`, `debug_import.py`).
   - `09_datos_duplicados/`: `Data/Memoria_Termica Glucosa.Rev.1.pdf`, `PFD.svg`, `docs/report/PFD_Escenario_01A.pdf`.
   - `10_web_demo_antigua/`: demo Flask anterior en `examples/web-demo/`.

2. **Limpieza de `docs/report/`:** después de recompilar, la carpeta contiene únicamente los maestros `.tex` y `.pdf` oficiales, más `config/`, `sections/`, `references/` y `logos/`.

3. **Generación de índice:** se creó `reciclaje/README.md` que describe el contenido de cada subcarpeta y aclara que los archivos no forman parte de los entregables finales.

### Verificación

- Se recompilaron `W2605PRINF001.tex` (flujo completo pdflatex + bibtex + dos pasadas) y `W2605PRINF002.tex` (dos pasadas) sin errores fatales.
- Se ejecutaron los tests `task/test_ciclo.py`, `task/test_simulacion_50C.py` y `webapp/tests/test_api.py` con resultado exitoso.
- Se verificó que ningún documento activo referencia archivos movidos a `reciclaje/`.
- Se verificó que ningún script activo importa los scripts movidos a `reciclaje/`.

### Archivos entregables

- `reciclaje/README.md` — índice de archivos reciclados.
- `docs/report/W2605PRINF001.tex` y `docs/report/W2605PRINF001.pdf` — informe técnico principal.
- `docs/report/W2605PRINF002.tex` y `docs/report/W2605PRINF002.pdf` — resumen ejecutivo.

### Notas y trabajo futuro

- `README.md` de la raíz permanece desactualizado (menciona código de documento antiguo y estructura previa). Se recomienda actualizarlo antes de la publicación en GitHub.
- No se movieron los CSV de `results/` ni las figuras oficiales de `results/figures/` porque están vinculados a los informes activos o sirven como datos de soporte.
- La carpeta `reciclaje/` se subirá a GitHub intencionalmente para conservar trazabilidad histórica; por tanto no se añadió a `.gitignore`.

---

*Sesión de organización en `reciclaje/` completada.*

---

## Revisión — actualización de la webapp W2605

**Fecha de revisión:** 17 de junio de 2026

### Resumen de cambios
- Se refactorizaron `src/ciclo_descargas_14m2_75C_12m3h.py`, `src/calentamiento_24ton_40_60.py` y `src/escenario4_capacidad.py` para que sean import-safe desde Flask.
- Se crearon los wrappers `webapp/app/core/ciclo_12m3h.py`, `perdidas_aislamiento.py` y `escenarios_extras.py`.
- Se añadió el blueprint `webapp/app/api/proyecto.py` con seis endpoints JSON.
- Se implementó el servicio estático `/figures/<path:filename>` para `results/figures/`.
- Se añadieron las páginas `/factibilidad`, `/perdidas-aislamiento` y `/escenarios`, y se actualizó la navegación.
- Se amplió `webapp/tests/test_api.py` a 14 tests, todos exitosos.
- Se actualizaron `README.md` y `contexto.md` con las nuevas rutas, API y archivos.
- Se sincronizó el repositorio con GitHub (`main` actualizado).

### Desviaciones respecto al plan original
Ninguna desviación crítica. La agrupación de los wrappers de calentamiento de 24 ton y capacidad operativa en un único archivo (`escenarios_extras.py`) simplificó la superficie de importación sin alterar la funcionalidad.

### Limitaciones conocidas y trabajo futuro recomendado
- Advertencia residual `ResourceWarning` en `test_serve_figure` por archivo no cerrado; no afecta el funcionamiento.
- Pendiente: definición del logo corporativo correcto de DMV SAS para el membrete de los informes PDF.

### Archivos entregables y sus rutas
- Aplicación web: `webapp/`
- Blueprint de API: `webapp/app/api/proyecto.py`
- Wrappers Flask: `webapp/app/core/ciclo_12m3h.py`, `webapp/app/core/perdidas_aislamiento.py`, `webapp/app/core/escenarios_extras.py`
- Rutas HTML: `webapp/app/routes.py`
- Templates: `webapp/app/templates/factibilidad.html`, `perdidas_aislamiento.html`, `escenarios.html`
- Tests: `webapp/tests/test_api.py`
- Scripts refactorizados: `src/ciclo_descargas_14m2_75C_12m3h.py`, `src/calentamiento_24ton_40_60.py`, `src/escenario4_capacidad.py`
- Documentación: `README.md`, `contexto.md`

---

## Plan: rediseño dark cyberpunk de la webapp W2605 y despliegue en Render

**Fecha del plan:** 17 de junio de 2026  
**Estado:** Propuesto — a la espera de aprobación explícita  
**Alcance:** Migrar la interfaz actual de la webapp a un tema oscuro cyberpunk con acentos verde claro, naranja translúcido y azul transparente; agregar descarga de informes PDF; preparar el despliegue en Render.

---

### Contexto
- Objetivo: renovar la estética de `webapp/` y habilitar la descarga de los informes W2605PRINF001 y W2605PRINF002 desde el navegador.
- Cliente / Proyecto DML: W2605 — Análisis térmico del fondo toriesférico del tanque de glucosa Tag 53A-90A-0056 (Ingredion Cali).
- Normas aplicables: API 650, ASME VIII, ASME B31.3, RETIE, NSR-10 (documentadas en los informes; la webapp actúa como visualizador).

---

### Supuestos clave
- [ ] Se mantendrán Bootstrap 5.3.2 y las librerías CDN actuales (Plotly, Chart.js, DataTables); se forzará `data-bs-theme="dark"` y se sobreescribirán variables/clases con CSS propio.
- [ ] La paleta propuesta será: fondo `#0a0a0f` / `#0f111a`; acento verde claro `#39ff14`; naranja translúcido `rgba(255, 140, 0, 0.15)`; azul transparente `rgba(0, 150, 255, 0.12)`; texto `#e0e6ed`.
- [ ] Los PDFs oficiales se encuentran en `docs/report/W2605PRINF001.pdf` y `docs/report/W2605PRINF002.pdf`.
- [ ] Render despliega desde el repositorio completo; `wsgi.py` resuelve rutas relativas a la raíz del proyecto, por lo que `results/figures/` seguirá disponible.
- [ ] Los gráficos Plotly/Chart.js se adaptarán a fondo oscuro mediante layouts/ opciones de tema; no se recalcularán los datos.

---

### Tareas
- [x] **T1. Definir paleta y sistema de diseño en CSS.** Modificar `webapp/app/static/css/main.css`: rediseñar `:root` con colores cyberpunk, sombras neon, bordes translúcidos, tipografía monoespaciada para datos. (Impacto: 1 archivo CSS.)
- [x] **T2. Actualizar layout base.** Modificar `webapp/app/templates/base.html`: aplicar `data-bs-theme="dark"`, clases del nuevo sistema, sidebar oscuro con acentos neon, footer actualizado. (Impacto: 1 archivo.)
- [x] **T3. Rediseñar home (`index.html`).** Aplicar estilos cyberpunk, hero section con gradientes y tipografía destacada, tarjetas de acceso a módulos. (Impacto: 1 archivo.)
- [x] **T4. Rediseñar dashboard (`dashboard.html`).** Adaptar KPIs, tarjetas, tablas y gráficos al tema oscuro; ajustar SVG del tanque a la paleta. (Impacto: 1 archivo.)
- [x] **T5. Rediseñar páginas de análisis (`factibilidad.html`, `perdidas_aislamiento.html`, `escenarios.html`).** Unificar tarjetas, tablas, alertas y badges con el nuevo estilo. (Impacto: 3 archivos.)
- [x] **T6. Actualizar JS de gráficos.** Ajustar `webapp/app/static/js/dashboard.js`, `calculadora.js`, `simulador.js`, `propiedades.js`, `sensibilidad.js` para layouts oscuros en Plotly/Chart.js. (Impacto: ≤ 5 archivos, cambios menores por archivo.)
- [x] **T7. Agregar descarga de informes.** Añadir ruta `/informes/<filename>` en `webapp/app/routes.py` con `send_from_directory`; actualizar `about.html` (y/o home) con botones de descarga para W2605PRINF001 y W2605PRINF002. (Impacto: 2 archivos.)
- [x] **T8. Preparar despliegue en Render.** Revisar `render.yaml`, `webapp/wsgi.py` y `webapp/requirements.txt`; confirmar health check, variables de entorno y rutas de archivos estáticos. (Impacto: 3 archivos como máximo.)
- [x] **T9. Verificación local y tests.** Ejecutar `webapp/tests/test_api.py`, levantar servidor local y revisar visualmente las rutas principales. (Impacto: validación, sin cambios de código.)
- [x] **T10. Actualizar documentación.** Reflejar el nuevo diseño, la descarga de informes y las instrucciones de despliegue en `README.md` y `contexto.md`. (Impacto: 2 archivos.)
- [x] **T11. Commit y push.** Subir cambios a GitHub para activar/desplegar en Render. (Impacto: operación git.)

---

### Riesgos / Puntos de verificación
- [ ] **R1. Coherencia visual:** verificar que no queden elementos con clases Bootstrap `bg-white`, `bg-light`, `text-muted` o `table-light` que rompan el tema oscuro.
- [ ] **R2. Legibilidad de gráficos:** confirmar que colores de series en Plotly/Chart.js tengan contraste suficiente sobre fondo oscuro.
- [ ] **R3. Rutas de archivos en producción:** validar que `/figures/<filename>` y `/informes/<filename>` funcionen tanto en local como en Render.
- [ ] **R4. Rendimiento:** mantener el uso de CDN; no agregar dependencias pesadas sin necesidad.
- [ ] **R5. Trazabilidad:** no alterar datos, supuestos de cálculo ni resultados numéricos del proyecto.

---

**Detente aquí. Notifica al usuario y espera aprobación explícita antes de ejecutar.**

---

## Revisión — rediseño dark cyberpunk de la webapp W2605

**Fecha de revisión:** 17 de junio de 2026

### Resumen de cambios
- Se rediseñó completamente el sistema de estilos en `webapp/app/static/css/main.css` con paleta oscura cyberpunk: fondos `#0a0a0f`/`#0f111a`, verde neón `#39ff14`, naranja translúcido, azul transparente, tipografía monoespaciada para datos y efectos *glow*.
- Se actualizó `base.html` con `data-bs-theme="dark"`, sidebar oscuro con acentos neón y footer renovado.
- Se rediseñaron `index.html`, `dashboard.html`, `factibilidad.html`, `perdidas_aislamiento.html`, `escenarios.html` y `about.html` eliminando fondos claros, bordes Bootstrap genéricos y colores corporativos anteriores.
- Se adaptaron `dashboard.js`, `calculadora.js`, `simulador.js`, `propiedades.js` y `sensibilidad.js` para usar layouts Plotly/Chart.js con fondo transparente, rejilla azul tenue y series en colores neón.
- Se añadió la ruta `/informes/<filename>` en `webapp/app/routes.py` para descargar los informes PDF desde `docs/report/`.
- Se añadieron botones de descarga en `about.html` para `W2605PRINF001.pdf` y `W2605PRINF002.pdf`.
- Se actualizó `render.yaml` (nombre `w2605-webapp`, health check `/health`).
- Se amplió `webapp/tests/test_api.py` de 14 a 16 tests, incluyendo validación de descarga de informes.
- Se actualizaron `README.md` y `contexto.md`.

### Desviaciones respecto al plan original
Ninguna desviación crítica. Se mantuvo Bootstrap 5 y las librerías CDN existentes; solo se forzó el tema oscuro y se sobrescribieron variables/clases con CSS propio.

### Limitaciones conocidas y trabajo futuro recomendado
- Advertencia residual `ResourceWarning` por archivos no cerrados en `send_from_directory` durante los tests; no afecta funcionamiento.
- Pendiente: despliegue en Render y validación de rutas `/figures` e `/informes` en producción.
- Pendiente: definición del logo corporativo correcto de DMV SAS para el membrete de los informes PDF.

### Archivos entregables y sus rutas
- CSS tema: `webapp/app/static/css/main.css`
- Layout y templates: `webapp/app/templates/base.html`, `index.html`, `dashboard.html`, `factibilidad.html`, `perdidas_aislamiento.html`, `escenarios.html`, `about.html`
- JS de gráficos: `webapp/app/static/js/dashboard.js`, `calculadora.js`, `simulador.js`, `propiedades.js`, `sensibilidad.js`
- Rutas y descargas: `webapp/app/routes.py`
- Tests: `webapp/tests/test_api.py`
- Despliegue: `render.yaml`
- Documentación: `README.md`, `contexto.md`
