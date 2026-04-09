# ESTRUCTURA DEL PROYECTO P2611

Organización profesional del proyecto de análisis térmico y estructural del tanque de glucosa Ingredion.

## 📁 Estructura de Carpetas

```
Proyecto-P2611/
│
├── 📂 Data/                          # Datos de referencia y documentación
│   ├── datasheets/                   # Fichas técnicas (PDF)
│   │   ├── glucosa 40de globe 1130.pdf
│   │   ├── Memoria_Termica Glucosa.Rev.1.pdf  # Diseño del tercero
│   │   └── P2543-PR-INF-002 REV0.pdf # Estudio de corrosión anterior
│   │
│   ├── investigacion/                # Documentos de investigación técnica
│   │   ├── investigacionUtranf.txt
│   │   ├── investigacion_normas.md
│   │   └── investigacion_propiedades_glucosa_y_SS316L.md
│   │
│   ├── normas/                       # Referencias normativas (vacío - por llenar)
│   │
│   └── planos/                       # Planos de referencia (imágenes)
│       ├── fondo.png
│       ├── espiral.png
│       └── membrete.pdf
│
├── 📂 docs/                          # Documentación del proyecto
│   └── report/                       # Informe principal LaTeX
│       ├── config/                   # Configuración LaTeX
│       │   ├── datos_proyecto.tex
│       │   ├── header.tex
│       │   └── preamble.tex
│       │
│       ├── sections/                 # Secciones del informe (19 archivos .tex)
│       │   ├── 00_portada.tex
│       │   ├── 01_frontmatter.tex    # Abstract
│       │   ├── 02_resumen.tex        # Resumen ejecutivo
│       │   ├── 03_nomenclatura.tex
│       │   ├── 04_introduccion.tex
│       │   ├── 05_objetivos.tex
│       │   ├── 06_alcance.tex
│       │   ├── 07_bases_disenio.tex
│       │   ├── 08_metodologia.tex
│       │   ├── 09_resultados.tex     # Resultados principales
│       │   ├── 10_analisis.tex
│       │   ├── 11_conclusiones.tex
│       │   ├── 12_recomendaciones.tex
│       │   └── 13_anexos.tex
│       │
│       ├── P2611-PR-INF-001 R0.tex   # Documento maestro
│       └── P2611-PR-INF-001 R0.pdf   # PDF generado
│
├── 📂 examples/                      # Ejemplos y demos (web)
│   └── web-demo/                     # Demo Flask interactiva
│
├── 📂 results/                       # Resultados y análisis
│   ├── figures/                      # 📊 TODAS las figuras del proyecto (53 archivos)
│   │   ├── *.png                     # Gráficas generadas por Python
│   │   ├── *.pdf                     # Versiones vectoriales
│   │   ├── cfd1.png                  # Simulación CFD (COMSOL)
│   │   ├── fea*.png                  # Simulaciones FEA (ANSYS)
│   │   └── IsoT1.png                 # Vista isométrica
│   │
│   └── *.csv                         # Datos tabulados (7 archivos)
│       ├── areas_calentamiento.csv
│       ├── areas_escenario_55_57.csv
│       ├── comparativa_batch.csv
│       ├── comparativa_flujo_*.csv
│       └── ...
│
├── 📂 src/                           # Código fuente Python (12 módulos)
│   ├── coeficiente_U.py              # Cálculo del coeficiente global U
│   ├── escenarios.py                 # Simulación de escenarios 1, 2, 3
│   ├── escenario4_ciclo.py           # Simulación escenario 4 (ciclo)
│   ├── ciclo_descargas.py            # Ciclos de descarga a carrotanque
│   ├── comparativa_chaquetas.py      # Comparativa dimple vs media caña
│   ├── calcular_areas.py             # Cálculo de áreas de transferencia
│   ├── propiedades_glucosa.py        # Propiedades termofísicas de glucosa
│   ├── geometria_tanque.py           # Parámetros geométricos
│   ├── espesores_tanque.py           # Cálculos API 650 / ASME VIII
│   ├── aislamiento.py                # Cálculo de aislamiento térmico
│   ├── ciclo_vida.py                 # Análisis de vida útil por corrosión
│   └── graficar_resistencias.py      # Visualización de resistencias térmicas
│
├── 📂 .vscode/                       # Configuración VS Code
│
└── 📄 Archivos de configuración y documentación
    ├── README.md                     # Descripción general del proyecto
    ├── AGENTS.md                     # Guía para agentes de IA
    ├── CLAUDE.md                     # Documentación maestra
    ├── requirements.txt              # Dependencias Python
    ├── auditoriar1.txt               # Auditoría técnica del proyecto
    └── auditoriatercero.txt          # Auditoría del diseñador tercero
```

## 🔧 Convenciones de Organización

### Código Fuente (`src/`)
- **12 módulos Python** especializados por función
- Nomenclatura: `snake_case.py`
- Cada módulo tiene docstring con descripción y referencias bibliográficas
- Sin `__pycache__` ni archivos compilados (ignorados en `.gitignore`)

### Figuras (`results/figures/`)
- **53 archivos**: versiones PNG (ráster) y PDF (vectorial)
- Generadas automáticamente por scripts Python
- Las figuras CFD/FEA provienen de simulaciones externas (COMSOL/ANSYS)
- Formato: `{tema}_{descripcion}.{ext}`

### Datos (`Data/`)
- **`datasheets/`**: Documentación técnica de fabricantes
- **`investigacion/`**: Documentos de investigación técnica
- **`planos/`**: Imágenes de referencia (fondo, espiral)
- **`normas/`**: (Reservado para normas aplicables)

### Documentación (`docs/report/`)
- **Documento maestro**: `P2611-PR-INF-001 R0.tex`
- **19 secciones modulares** importadas con `\input{}`
- Configuración separada en `config/`
- PDF generado en la raíz del proyecto

### Resultados (`results/`)
- **`figures/`**: Todas las gráficas (PNG + PDF)
- **Archivos CSV**: Datos tabulados para análisis
- Separado del código fuente para mantener orden

## 📝 Notas Importantes

1. **Figuras**: LaTeX accede vía `../../../results/figures/` desde `docs/report/sections/`

2. **Planos**: Referenciados en LaTeX como `../../Data/planos/`

3. **PDF Final**: Se genera en `docs/report/` y se copia a raíz del proyecto

4. **No hay archivos temporales**: Carpetas `.temp_venv`, `figures/` (raíz) eliminadas

## 🔄 Flujo de Trabajo

1. **Ejecutar scripts Python** en `src/` → Generan figuras en `results/figures/`
2. **Compilar LaTeX** → `docs/report/P2611-PR-INF-001 R0.tex`
3. **PDF resultante** → Copiado a raíz del proyecto

## 📊 Estadísticas del Proyecto

- **Código Python**: ~2,500 líneas (12 módulos)
- **Documento LaTeX**: ~85 páginas, 19 secciones
- **Figuras**: 53 archivos (PNG + PDF)
- **Datos CSV**: 7 archivos de resultados tabulados
- **Total archivos**: ~120 (sin contar .git)

---

*Estructura organizada el 8 de abril de 2026*
*Sistema de control de versiones: Git*
