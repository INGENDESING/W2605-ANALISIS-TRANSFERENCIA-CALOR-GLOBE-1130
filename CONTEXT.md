# Contexto Proyecto P2611 — Análisis Fondo Tanque Glucosa

## 1. Información General
- **Proyecto**: P2611 — Validación diseño sistema calentamiento y fondo toriesférico
- **Cliente**: Ingredion S.A.
- **Consultor**: DML Ingenieros Consultores S.A.S.
- **Ubicación**: Planta Ingredion, Cali, Colombia
- **Equipo**: Tanque glucosa Tag 53A-90A-0056 (fondo de reemplazo en construcción)

## 2. Documentación Base
| Documento | Código | Contenido Clave |
|:----------|:-------|:----------------|
| Planos mecánicos | `REV0DMI17160102` (feb 2026) | Geometría fondo toriesférico, chaqueta media caña 13 m² |
| Memoria térmica | `GTTP-1004b Rev.1` (ene 2026) | Cálculos térmicos originales (U=825 W/m²°C, erróneos) |
| Estudio espesores | `Informe Tanque Almacenamiento de Glucosa No.4 — Anillo_V1` | Tasa corrosión 0.120 mm/año |
| Estudio espesores | `MT-ME-003 Tanque 5 Espesores` | Tasa histórica 0.0625 mm/año |

## 3. Archivos Principales

### Informe Activo: `docs/report/P2611-PR-INF-003.tex`
- **Páginas**: 11 páginas, ~1.54 MB
- **Clase**: `elsarticle` (12 pt)
- **Compilación**: `pdflatex` desde `docs/report/`

#### Estructura actual
| Sección | Contenido |
|:--------|:----------|
| 1 | Introducción |
| 2 | Descripción del Proceso |
| 3 | Metodología (CFD COMSOL + FEA ANSYS Mechanical 2025 NUBE) |
| 4–6 | Escenarios 01A, 01B, 01C |
| 7 | Escenario 02A (comparativa chaquetas) |
| 8 | Escenario 02B |
| 9 | **Observaciones y recomendaciones: revisión térmica** |
| 10 | **Revisión estructural** (FEA + Observaciones/Recomendaciones) |

## 4. Datos Técnicos Consolidados

### Dimensiones y Capacidades
| Parámetro | Valor | Nota |
|:----------|:------|:-----|
| Capacidad nominal (100 %) | 222.8 m³ | Cilindro + fondo (314 t) |
| Límite operativo seguro | 178.2 m³ (251 t) | 80 % — FS ≥ 1.3 |
| Área transferencia (media caña fondo) | 13 m² | Construido actualmente |
| Área transferencia (chaqueta dimple actual) | 28 m² | Configuración existente |
| Ratio áreas | 2.154× | `A_actual / A_reemp` |

### Resultados Térmicos Clave
- **Coeficiente global U**: ~17.9–36.2 W/m²°C (depende de temperatura glucosa)
- **Resistencia dominante**: 97.7–98.8 % del total está del lado de la glucosa (viscosidad)
- **Pérdidas térmicas**: 51.1 MJ/h (ambos escenarios)
- **Balance neto**: -38.3 MJ/h (base 65°C) / -32.2 MJ/h (optimizado 75°C)

### Capacidad Operativa (Área 13 m², Tw = 75°C)
| Condición | Flujo Máx | Descargas/día | Cumplimiento |
|:----------|:---------:|:-------------:|:------------:|
| Caso A (54→57°C, con pérdidas) | 5.1 ton/h | 5 (120 ton) | 62.5 % |
| Caso B (55→57°C, aislamiento optimizado) | 7.5 ton/h | 7 (168 ton) | 87.5 % |
| **Requerimiento** | **8.0 ton/h** | **8 (192 ton)** | **100 %** |

### Comparativa Chaquetas (Escenario 02A)
| Modo | Config. actual (28 m²) | Fondo reemplazo (13 m²) | Ratio |
|:----|:----------------------|:------------------------|:------|
| Batch 25→57°C | 170.7 h | 367.5 h | 2.15× más lento |
| Batch 55→57°C | 15.5 h | 33.2 h | 2.15× más lento |
| Continuo 55→57°C | >16 ton/h | 7.54 ton/h | 2.15× menor capacidad |

**Observación técnica**: `U` es invariante entre configuraciones; la capacidad escala directamente con el área disponible.

## 5. Análisis Estructural (FEA)

### Condiciones evaluadas
- **Carga hidrostática**: Nivel máximo operación normal (222.8 m³ / 314 t)
- **Carga térmica**: Fondo a 75°C, cuerpo cilíndrico a temperatura ambiente
- **Software**: ANSYS Mechanical 2025 (NUBE)

### Resultados FEA
| Zona | FS | Estado |
|:-----|:--:|:-------|
| Unión fondo-cilindro (knuckle) | **0.71** | ❌ Sobreesfuerzo local |
| Anclajes chaqueta media caña | 1.0 – 1.7 | ⚠️ Marginal |
| Fondo torisférico (promedio) | 4.9 – 6.7 | ✅ Aceptable |
| Cuerpo cilíndrico | >15 | ✅ Sobredimensionado |

### Análisis ASME VIII Div. 1
| Condición | `t_req` [mm] | `t_nom` [mm] | Estado |
|:----------|:------------:|:------------:|:------:|
| 80 % llenado | 7.85 | 9.0 | ✅ Cumple |
| 100 % llenado | 9.16 | 9.0 | ❌ No cumple |

### Vida útil proyectada
- **Escenario corrosión-fatiga** (0.120 mm/año, 75°C cíclico): **~7.5 años**
- **Escenario histórico** (0.0625 mm/año): **~14.4 años**
- Límite de retiro: 10 % = 8.1 mm

## 6. Observaciones y Recomendaciones

### Sección 9 — Revisión Térmica (Observaciones)
1. Con el diseño entregado, la salida de glucosa se mantendrá >57°C solo si la entrada está >59.5°C. A 54°C de entrada, la salida cae a ~53°C.
2. Para garantizar temperatura de salida por encima del mínimo se debe cumplir la condición del Escenario 4 (agua a 75°C, velocidad optimizada); se recomienda aumentar el área a ~30 m².
3. Se recomienda mejorar el aislamiento para disminuir pérdidas por convección.

### Sección 10.1 — Revisión Estructural (Observaciones)
1. Al nivel máximo de operación normal (222.8 m³ / 314 t), el FS en la unión fondo-cilindro desciende a ~0.71 (sobreesfuerzo local). El límite operativo seguro con FS ≥ 1.3 es 178.2 m³ (251 t).
2. Vida útil proyectada del fondo nuevo: ~7.5 años (tasa 0.120 mm/año determinada en estudios de espesores) o ~14.4 años (tasa histórica 0.0625 mm/año).

### Sección 10.1 — Revisión Estructural (Recomendaciones)
1. Incluir anclajes de chaqueta y zona de la unión fondo-cilindro en programa END (PAUT/UT) con periodicidad **bianual**.
2. Establecer programa de monitoreo de espesores durante los **primeros tres años** de operación.
3. Desarrollar un **estudio de refuerzo estructural focalizado en la unión fondo-cilindro**, evaluando: incremento localizado de espesor, anillos de rigidización perimetrales o placas de refuerzo (pads), validados con FEA actualizado.

## 7. Pipeline de Figuras
- **PFDs**: Generados vía `src/generar_pfds_escenarios.py` (regex sobre SVG base + `Decimal ROUND_HALF_UP`)
  - `results/PFD_Escenario_01A.pdf`
  - `results/PFD_Escenario_01B.pdf`
  - `results/PFD_Escenario_01C.pdf`
  - `results/PFD_Escenario_02A.pdf`
- **Figuras FEA**: `results/figures/fea1.png`, `results/figures/fea3.png`

## 8. Estado de Tareas Recientes
✅ PFDs regenerados y validados (shadow fix + datos correctos)
✅ Tabla global simplificada (solo v = 1.5 m/s)
✅ Metodología actualizada (ANSYS Mechanical 2025 NUBE)
✅ Sección 10 creada: Revisión estructural con FEA
✅ Reemplazo "nudillo" → "unión fondo-cilindro" en Sección 10
✅ Observaciones y recomendaciones separadas en subsubsecciones
✅ Referencias a estudios de espesores agregadas en Observación 2 estructural
✅ Recomendación 3 estructural: estudio de refuerzo en unión fondo-cilindro
✅ Documento compilado y estable (11 págs, 1.54 MB)

## 9. Notas para Futuras Sesiones
- **Documento activo**: `docs/report/P2611-PR-INF-003.tex`
- **Compilación**: dos pasadas de `pdflatex` desde `docs/report/`
- **Advertencias preexistentes (no bloqueantes)**: `hyperref` duplicate-page-identifier en portada; `titlesec` paragraph-format warning.
- **No hay tareas críticas pendientes** en el documento activo; el informe está en estado de redacción final.
