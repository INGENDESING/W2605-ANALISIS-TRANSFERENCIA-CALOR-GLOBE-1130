# Plan Maestro: Ejecucion del Proyecto P2611

## Objetivo
Ejecutar todas las instrucciones del `CLAUDE.md`: investigacion tecnica, calculos de transferencia de calor (Python), analisis de espesores, y redaccion del informe LaTeX completo para INGREDION SA.

## Principio
Cada fase depende de la anterior. Dentro de cada fase, las tareas son minimas y aisladas. El informe se redacta en prosa humanizada estilo Elsevier (sin vinetas). Las secciones CFD (COMSOL) y FEA (ANSYS) quedan como placeholder metodologico.

---

## Fase 0 -- Investigacion Tecnica (base de datos del proyecto)

- [x] **0.1 Investigar transferencia de calor en half-pipe jackets** (completado 2026-04-01)
  - Resultado: Ver `investigacionUtranf.txt`, Tema 1 (secciones 1.1 a 1.8)

- [x] **0.2 Investigar propiedades de glucosa Globe 1130 (Ingredion)** (completado 2026-04-01)
  - Resultado: Ver `Data/investigacion_propiedades_glucosa_y_SS316L.md`, Tema 1

- [x] **0.3 Investigar valores de U para calentamiento de glucosa/jarabes viscosos** (completado 2026-04-01)
  - Resultado: Ver `investigacionUtranf.txt`, Tema 2 (secciones 2.1 a 2.7)

- [x] **0.4 Investigar corrosion SS316L y propiedades mecanicas** (completado 2026-04-01)
  - Resultado: Ver `Data/investigacion_propiedades_glucosa_y_SS316L.md`, Tema 2

- [x] **0.5 Investigar normas sanitarias y estructurales** (completado 2026-04-01)
  - Resultado: `Data/investigacion_normas.md`

- [x] **0.6 Consolidar investigacion** (completado 2026-04-01)

---

## Fase 1 -- Actualizar secciones LaTeX del informe

- [x] **1.1 Actualizar `03_nomenclatura.tex`** (completado 2026-04-01)
  - 35 simbolos y 13 abreviaciones especificas del proyecto

- [x] **1.2 Actualizar `04_introduccion.tex`** (completado 2026-04-01)
  - Prosa Elsevier: contexto INGREDION, tanque, fondo, media cana

- [x] **1.3 Actualizar `05_objetivos.tex`** (completado 2026-04-01)
  - 5 objetivos tecnicos + 3 estrategicos

- [x] **1.4 Actualizar `06_alcance.tex`** (completado 2026-04-01)
  - Parte I y II, exclusiones, items pendientes CFD/FEA

- [x] **1.5 Actualizar `07_bases_disenio.tex`** (completado 2026-04-01)
  - Datos reales: geometria tanque, propiedades glucosa Globe 1130, 3 escenarios, SS316L, normativas

- [x] **1.6 Actualizar `08_metodologia.tex`** (completado 2026-04-01)
  - Ecuaciones: U global, Dh, Sieder-Tate, Churchill-Chu, balance transitorio, API 650, ASME VIII
  - Placeholders CFD (COMSOL) y FEA (ANSYS)

- [x] **1.7 Actualizar `01_frontmatter.tex` -- Abstract y keywords** (completado 2026-04-01)
  - Abstract real con resultados clave del proyecto

- [x] **1.8 Actualizar `02_resumen.tex` -- Resumen ejecutivo** (completado 2026-04-01)
  - Sintesis para partes interesadas no tecnicas

---

## Fase 2 -- Calculos de Transferencia de Calor (Python)

- [x] **2.1 Crear modulo de propiedades `src/propiedades_glucosa.py`** (completado 2026-04-01)
  - Funciones: rho(T), mu(T), Cp(T), k(T) para glucosa 83 Brix y agua
  - Modelo Arrhenius para viscosidad, Choi & Okos para Cp y k

- [x] **2.2 Crear modulo de geometria `src/geometria_tanque.py`** (completado 2026-04-01)
  - V_total = 222.8 m3, D_h = 68.8 mm, A_contacto = 13 m2

- [x] **2.3 Calcular coeficiente U `src/coeficiente_U.py`** (completado 2026-04-01)
  - U = 94--171 W/m2.C, resistencia glucosa 87--94% del total

- [x] **2.4 Escenario 1: Balance de tercero** (completado 2026-04-01)
  - 24 m3, Q_agua = 30.9 m3/h, T_agua = 80 C -> alcanza 60 C en 10.0 h

- [x] **2.5 Escenario 2: Agua a 65 C, tanque al 80%** (completado 2026-04-01)
  - 178 m3, v = 2.5 m/s -> alcanza 60 C en 193.7 h (8.1 dias)

- [x] **2.6 Escenario 3: Agua a 75 C, tanque al 80%** (completado 2026-04-01)
  - 178 m3, v = 2.5 m/s -> alcanza 60 C en 93.8 h (3.9 dias)

- [x] **2.7 Generar todas las graficas en `figures/`** (completado 2026-04-01)
  - 4 graficas PDF + PNG (300 dpi): esc1, esc2, esc3, comparacion

---

## Fase 3 -- Redactar resultados de transferencia de calor en LaTeX

- [x] **3.1 Actualizar `09_resultados.tex` -- Parte I y II** (completado 2026-04-01)
  - Tablas de U, tiempos de calentamiento por escenario, figuras referenciadas
  - Espesores cuerpo y fondo, cargas viento/sismo, vida util

- [x] **3.2 Actualizar `10_analisis.tex`** (completado 2026-04-01)
  - Dominancia resistencia glucosa, efecto T_agua, limitaciones del modelo
  - Estado critico del fondo toriesferico, cargas sismicas

---

## Fase 4 -- Calculos de Espesores del Tanque (Python + LaTeX)

- [x] **4.1 Crear modulo `src/espesores_tanque.py`** (completado 2026-04-01)
  - Cuerpo: API 650 One-Foot Method, 4 virolas, todas cumplen
  - Fondo: ASME VIII UG-32(e), cumple al 90%, marginal al 100%
  - Vida util: cuerpo 46 anos, fondo 29 anos
  - Cargas: viento 120 km/h (20.3 kN), sismo NSR-10 (1102.6 kN)

- [x] **4.2 Redactar resultados Parte II en `09_resultados.tex`** (completado 2026-04-01)
  - Incluido en la seccion de resultados

- [x] **4.3 Redactar analisis Parte II en `10_analisis.tex`** (completado 2026-04-01)
  - Incluido en la seccion de analisis

---

## Fase 5 -- Secciones de Metodologia CFD y FEA (placeholder)

- [x] **5.1 Agregar seccion CFD -- COMSOL en `08_metodologia.tex`** (completado 2026-04-01)
  - Placeholder metodologico con descripcion del modelo propuesto

- [x] **5.2 Agregar seccion FEA -- ANSYS en `08_metodologia.tex`** (completado 2026-04-01)
  - Placeholder metodologico con descripcion del modelo propuesto

---

## Fase 6 -- Cierre del informe

- [x] **6.1 Redactar `11_conclusiones.tex`** (completado 2026-04-01)
  - 7 conclusiones: 4 de Parte I (transferencia calor) + 3 de Parte II (espesores)

- [x] **6.2 Redactar `12_recomendaciones.tex`** (completado 2026-04-01)
  - 4 operativas, 3 de inspeccion/mantenimiento, 2 para CFD/FEA

- [x] **6.3 Actualizar `13_anexos.tex`** (completado 2026-04-01)
  - Anexo A: tabla de modulos Python
  - Anexo B: correlaciones de propiedades de glucosa
  - Anexo C: planos de referencia

- [x] **6.4 Actualizar `references/bibliografia.bib`** (completado 2026-04-01)
  - 15 entradas BibTeX (normas, libros, articulos, informe P2543)

- [x] **6.5 Compilar documento y verificar** (completado 2026-04-01)
  - Compilado con pdflatex (3 pasadas) + bibtex
  - 36 paginas, sin errores
  - PDF: `plantillalatex/P2611-PR-INF-001 R0.pdf`

---

## Fase 7 -- Revision

- [x] **7.1 Seccion de revision** (completado 2026-04-01)

---

## Seccion de Revision

### Resumen de Cambios Realizados (2026-04-01)

**Archivos creados:**
- `src/propiedades_glucosa.py` — Propiedades termofisicas glucosa Globe 1130 y agua
- `src/geometria_tanque.py` — Geometria del tanque y media cana
- `src/coeficiente_U.py` — Calculo del coeficiente global U
- `src/escenarios.py` — Simulacion transitoria de 3 escenarios de calentamiento
- `src/espesores_tanque.py` — Verificacion de espesores API 650 / ASME VIII
- `figures/escenario1_T_vs_tiempo.pdf/.png` — Grafica Escenario 1
- `figures/escenario2_T_vs_tiempo.pdf/.png` — Grafica Escenario 2
- `figures/escenario3_T_vs_tiempo.pdf/.png` — Grafica Escenario 3
- `figures/comparacion_escenarios_2_3.pdf/.png` — Comparacion Esc. 2 vs 3
- `investigacionUtranf.txt` — Investigacion transferencia calor en half-pipe jackets
- `Data/investigacion_propiedades_glucosa_y_SS316L.md` — Propiedades glucosa y SS316L
- `Data/investigacion_normas.md` — Normativas aplicables

**Archivos modificados (LaTeX):**
- `plantillalatex/P2611-PR-INF-001 R0.tex` — Documento principal (renombrado, nocite, bibliographystyle)
- `plantillalatex/config/datos_proyecto.tex` — Metadatos reales del proyecto
- `plantillalatex/sections/01_frontmatter.tex` — Abstract y autores reales
- `plantillalatex/sections/02_resumen.tex` — Resumen ejecutivo completo
- `plantillalatex/sections/03_nomenclatura.tex` — Nomenclatura del proyecto
- `plantillalatex/sections/04_introduccion.tex` — Introduccion en prosa Elsevier
- `plantillalatex/sections/05_objetivos.tex` — Objetivos tecnicos y estrategicos
- `plantillalatex/sections/06_alcance.tex` — Alcance detallado
- `plantillalatex/sections/07_bases_disenio.tex` — Bases de diseno con datos reales
- `plantillalatex/sections/08_metodologia.tex` — Metodologia completa con ecuaciones
- `plantillalatex/sections/09_resultados.tex` — Resultados Parte I y II
- `plantillalatex/sections/10_analisis.tex` — Analisis de resultados
- `plantillalatex/sections/11_conclusiones.tex` — 7 conclusiones
- `plantillalatex/sections/12_recomendaciones.tex` — 9 recomendaciones
- `plantillalatex/sections/13_anexos.tex` — 3 anexos
- `plantillalatex/references/bibliografia.bib` — 15 referencias BibTeX

### Hallazgos Clave

1. **Transferencia de calor:** La resistencia del lado de la glucosa domina (87-94%). U = 94-171 W/m2.C.
2. **Tiempos de calentamiento:** Tanque completo (80%): 3.9 dias (agua 75 C) a 8.1 dias (agua 65 C).
3. **Fondo toriesferico:** Cumple ASME VIII al 90% fill (margen 0.55 mm), marginal al 100%.
4. **Cuerpo cilindrico:** Cumple API 650 con margen de 1.02 mm en virola inferior.
5. **Cargas sismicas:** Dominan sobre viento (NSR-10, Cali zona intermedia).
6. **Vida util:** Cuerpo 46 anos, fondo 29 anos (tasa corrosion 0.0625 mm/ano).

### Pendiente (por parte del usuario)

- Simulacion CFD en COMSOL Multiphysics (secciones placeholder ya escritas)
- Analisis FEA en ANSYS (secciones placeholder ya escritas)
- Revision final del documento por parte de W. Camelo (revisor)
- Aprobacion por parte de H. Rosero (Gerente de Ingenieria)
