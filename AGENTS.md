# AGENTS.md — Guía del Proyecto P2611

## Descripción General del Proyecto

**Proyecto P2611**: Estudio de transferencia de calor y análisis estructural del fondo toriesférico de un tanque de almacenamiento de glucosa para INGREDION S.A. (Planta Cali, Colombia).

**Código del documento principal**: `P2611-PR-INF-001 R0`

**Alcance técnico**:
- Parte I: Transferencia de calor en chaqueta de media caña (espiral rectangular) sobre fondo toriesférico, cálculo del coeficiente global U, perfiles de temperatura, y análisis de ciclo de descargas a carrotanques
- Parte II: Validación de espesores del tanque bajo normas API 650 y ASME VIII, considerando cargas hidrostáticas, viento (120 km/h), sismo (NSR-10 zona intermedia), y corrosión en SS316L

**Metodología**: Cálculos analíticos en Python + validación numérica (CFD COMSOL / FEA ANSYS, simulaciones realizadas por el usuario)

---

## Stack Tecnológico

### Herramientas Principales
- **Python 3.12**: Cálculos científicos y numéricos
- **MiKTeX**: Distribución LaTeX para generación de informes
- **VS Code**: Editor principal con LaTeX Workshop extension
- **Git**: Control de versiones (recomendado pero no obligatorio)

### Bibliotecas Python
- `numpy`, `scipy`: Cálculo numérico y optimización
- `matplotlib`, `plotly`: Generación de gráficas técnicas
- `thermo`, `CoolProp`: Propiedades termofísicas
- `pandas`: Procesamiento de datos tabulares

### Stack LaTeX
- **Clase**: `elsarticle.cls` (Elsevier)
- **Paquetes clave**: `siunitx`, `mhchem`, `graphicx`, `booktabs`, `fancyhdr`, `tikz`
- **Tipografía**: TeX Gyre Termes
- **Compilador**: `pdflatex` (requerido, no XeLaTeX/LuaLaTeX)
- **Nota importante**: No usar FerroTeX (causa errores), usar LaTeX Workshop o `pdflatex` directamente

### Stack Web (Opcional)
- **Flask**: Backend para demos y visualizaciones interactivas
- **HTML/CSS/JavaScript**: Reportes interactivos
- **SVG**: Diagramas P&ID y esquemas de proceso

---

## Estructura del Proyecto

```
Proyecto-P2611/
├── src/                          # Código fuente Python
│   ├── propiedades_glucosa.py   # Propiedades termofísicas de glucosa Globe 42 DE
│   ├── coeficiente_U.py         # Cálculo del coeficiente global U
│   ├── geometria_tanque.py      # Parámetros geométricos del tanque
│   ├── espesores_tanque.py      # Cálculos API 650 y ASME VIII
│   ├── escenarios.py            # Escenarios 1-3 de calentamiento
│   ├── escenario4_ciclo.py      # Escenario 4: ciclo de descargas
│   ├── ciclo_descargas.py       # Funciones para análisis de ciclo
│   ├── graficar_resistencias.py # Visualización de resistencias térmicas
│   ├── aislamiento.py           # Cálculos del aislamiento
│   └── ciclo_vida.py            # Análisis de vida útil por corrosión
│
├── data/                        # Datos de referencia y documentación técnica
│   ├── datasheets/              # Fichas técnicas (PDF)
│   ├── planos/                  # Planos de referencia (PNG/PDF)
│   ├── normas/                  # Referencias normativas
│   ├── properties/              # Propiedades de materiales
│   ├── investigacionUtranf.txt          # Investigación técnica completa
│   ├── investigacion_normas.md          # Normas sanitarias y estructurales
│   └── investigacion_propiedades_glucosa_y_SS316L.md  # Propiedades glucosa y SS316L
│
├── docs/                        # Documentación y reportes
│   ├── report/                  # Documento principal LaTeX
│   │   ├── P2611-PR-INF-001_R0.tex
│   │   ├── sections/            # Capítulos del informe (00-13)
│   │   ├── config/              # Configuración LaTeX
│   │   ├── references/          # Bibliografía
│   │   ├── assets/              # Figuras específicas del informe
│   │   └── logos/               # Logos corporativos
│   └── project-management/      # Planes y seguimiento
│       ├── estado-avance.md
│       ├── plan-maestro.md
│       └── ferrotex-issue.md
│
├── results/                     # Resultados y análisis
│   ├── figures/                 # Figuras generadas (PDF/PNG)
│   │   └── generated/           # Figuras generadas por Python
│   └── analysis/                # Análisis intermedios y logs
│
├── examples/                    # Ejemplos y demos
│   └── web-demo/                # Demo Flask interactiva
│       ├── app.py
│       ├── static/
│       └── templates/
│
├── notebooks/                   # Jupyter notebooks (opcional)
├── tests/                       # Pruebas unitarias (si se implementan)
│
├── .gitignore                   # Archivos a ignorar en Git
├── README.md                    # Descripción del proyecto
├── LICENSE                      # Licencia del proyecto
├── AGENTS.md                    # Guía para agentes de IA
└── CLAUDE.md                    # Documentación maestra
```

---

## Proceso de Construcción y Runtime

### Para cálculos Python

**Sin dependencias externas declaradas**: el proyecto NO usa `requirements.txt`, `pyproject.toml` ni `environment.yml`. Las dependencias deben instalarse manualmente según los imports de cada módulo.

**Ejecutar cálculos**:
```bash
# Activar Python 3.12 (ruta configurada en .vscode/settings.json)
C:\Users\ingen\AppData\Local\Programs\Python\Python312\python.exe

# Ejecutar script individual
python src/escenarios.py
python src/espesores_tanque.py
```

**Flujo de trabajo típico**:
1. Modificar parámetros en `src/propiedades_glucosa.py` (si cambian propiedades)
2. Ejecutar scripts de escenarios (`escenarios.py`, `escenario4_ciclo.py`)
3. Las figuras se generan automáticamente en `figures/`
4. Recompilar informe LaTeX para incorporar resultados actualizados

### Para compilación LaTeX

**Requisitos previos**:
- MiKTeX instalado y en PATH
- VS Code con extensión LaTeX Workshop (recomendado)
- **NO usar FerroTeX** (causa error `spawn ferrotexd ENOENT`)

**Compilar informe**:
```bash
# Método 1: LaTeX Workshop (recomendado)
- Abrir plantillalatex/P2611-PR-INF-001 R0.tex en VS Code
- Usar comando "Build LaTeX project" (Ctrl+Alt+B)
- Compilar 2 veces para resolver referencias

# Método 2: pdflatex directo
cd plantillalatex
pdflatex P2611-PR-INF-001 R0.tex
pdflatex P2611-PR-INF-001 R0.tex  # Segunda pasada
```

**Archivos generados**:
- `P2611-PR-INF-001 R0.pdf`: Informe final (56 páginas en versión actual)
- `*.aux`, `*.log`, `*.toc`, `*.lof`, `*.lot`: Archivos auxiliares (no versionar)

### Para demo web (opcional)

```bash
cd ejemplo_web
python app.py
# Abrir navegador en http://localhost:5000
```

---

## Configuraciones Clave

### VS Code (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "C:\\\\Users\\\\ingen\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe",
    "editor.formatOnSave": true,
    "[python]": { "editor.defaultFormatter": "ms-python.python" },
    "liveServer.settings.port": 5500
}
```

### Datos del proyecto (plantillalatex/config/datos_proyecto.tex)
```latex
% Actualizar para cada nuevo proyecto
\newcommand{\documentcode}{P2611-PR-INF-001 REV0}
\newcommand{\projecttitle}{ANÁLISIS TÉRMICO Y ESTRUCTURAL DEL FONDO TORISFÉRICO...}
\newcommand{\authors}{J. Arboleda, H. Rosero}
```

### Propiedades de glucosa (src/propiedades_glucosa.py)
- **Brix_GLUCOSA = 80.6**: Valor nominal de ficha técnica Ingredion 011420
- **VFT calibrado**: `ln(mu) = -9.350 + 1278.0/(T + 66.90)` (ajuste exacto a 3 puntos)
- **Densidad**: `rho = 1435.4 - 0.540*T` [kg/m³]

### Parámetros geométricos (src/geometria_tanque.py)
- OD shell = 5,276 mm, ID = 5,264 mm, Altura = 9,670 mm
- Fondo toriesférico: OD = 5,282 mm, espesor = 9 mm
- Media caña: 45.5 × 141 mm, espesor 4.5 mm, paso 196 mm

---

## Flujo de Trabajo de Desarrollo

### 1. Planificación
- Crear/actualizar `tasks/todo.md` con hitos concretos
- Fases dependientes: Investigación → Cálculos → Redacción → Revisión

### 2. Investigación
- Consolidar hallazgos en `investigacionUtranf.txt` (Temas 1 y 2)
- Documentar fuentes con referencias completas (autor, año, página)
- Guardar PDFs de datasheets en `Data/`

### 3. Cálculos
- **Unidades**: SI exclusivamente (documentar conversiones si aplica)
- **Nomenclatura**: Variables físicamente descriptivas (`T_entrada`, `Q_calor`)
- **Validación**: Comparar contra casos conocidos de literatura
- **Comentarios**: Explicar ecuaciones y correlaciones con referencias bibliográficas

### 4. Redacción LaTeX
- **Estilo**: Prosa humanizada estilo Elsevier (NO listas con viñetas, NO enumeraciones)
- **Ecuaciones**: Presentar desarrollos paso a paso con sustitución de valores
- **Referencias**: Inline con autor-año o numéricas, NO inventar referencias
- **Idioma**: Español técnico, nomenclatura estándar de ingeniería

### 5. Generación de figuras
- **Resolución**: Mínimo 300 dpi
- **Formatos**: `.pdf` (LaTeX) + `.png` (reportes web)
- **Estilo**: Fuente serif, ejes etiquetados con unidades `[unidad]`
- **Paleta**: Accesible (evitar rojo/verde puros juntos)

### 6. Revisión
- Validar cálculos manualmente
- Verificar consistencia entre Python y LaTeX
- Revisar unidades y conversiones
- Compilar LaTeX sin errores/warnings

---

## Estándares de Código

### Python
```python
def coeficiente_peliculaexterna(Re, Pr, D, k):
    """
    Calcula h por correlación de Dittus-Boelter (flujo turbulento en tubos).
    Ref: Incropera, Fundamentals of Heat and Mass Transfer, 7th ed., Ec. 8.60

    Parámetros
    ----------
    Re : float  — Número de Reynolds (adimensional)
    Pr : float  — Número de Prandtl (adimensional)
    D  : float  — Diámetro interno [m]
    k  : float  — Conductividad térmica del fluido [W/m·K]

    Retorna
    -------
    h  : float  — Coeficiente convectivo [W/m²·K]
    """
```

**Principios**:
- Simplicidad: cada cambio mínimo y aislado
- Una función = un problema físico
- Comentarios que explican la ecuación/correlación
- Validar resultados contra conocido

### LaTeX
- **Comentarios**: Usar `%` para explicar secciones complejas
- **Ecuaciones**: Usar `equation` environment, numerar si se referencia
- **Tablas**: Usar `booktabs` (`\toprule`, `\midrule`, `\bottomrule`)
- **Unidades**: Usar `siunitx` (`\SI{25}{\watt\per\meter\squared\per\kelvin}`)

---

## Estrategia de Testing

**No hay tests automatizados**. La validación es manual y consiste en:

1. **Validación de cálculos**:
   - Comparar resultados contra casos de libro de texto
   - Verificar órdenes de magnitud (U ~ 15-35 W/m²·°C para glucosa)
   - Revisar convergencia de solvers numéricos

2. **Validación de datos**:
   - Propiedades de glucosa vs. ficha técnica Ingredion
   - Dimensiones de tanque vs. planos `Data/fondo.png`, `Data/espiral.png`

3. **Validación de integración**:
   - Valores Python → Tablas LaTeX: consistencia numérica
   - Figuras en `figures/` → Referencias en `plantillalatex/sections/09_resultados.tex`

4. **Validación de compilación**:
   - PDF compila sin errores
   - Referencias cruzadas resueltas correctamente
   - Membrete corporativo aparece en todas las páginas

**Criterios de aceptación**:
- Tiempos de calentamiento: Escenario 1 (5-6 días), Escenarios 2-3 (15-35 días)
- Coeficiente U: 15-35 W/m²·°C (promedio ponderado)
- Espesores: Cumplir API 650 y ASME VIII con margen positivo
- Vida útil: ≥30 años considerando tasa de corrosión 0.0625 mm/año

---

## Proceso de Despliegue

### Entregables al cliente
1. **PDF final**: `plantillalatex/P2611-PR-INF-001 R0.pdf`
   - Compilado con `pdflatex` (2 pasadas)
   - Sin errores ni warnings
   - Todos los metadatos actualizados

2. **Anexos digitales** (si solicita):
   - Código Python fuente (`src/`)
   - Figuras de resultados (`figures/`)
   - Investigación técnica (`investigacionUtranf.txt`)

### Proceso interno
- Actualizar `estadoavance.txt` con resumen ejecutivo
- Respaldar archivos `.tex` y `.py` en OneDrive (dirección actual del proyecto)
- Mantener versionado de PDFs con sufijo `R0`, `R1`, etc.

---

## Consideraciones Especiales

### Secciones Pendientes (CFD y FEA)
- **CFD (COMSOL)**: Sección metodológica completada, placeholder para resultados
  - El usuario realiza simulaciones personalmente
  - Cuando entregue resultados: integrar en `09_resultados.tex` con figuras

- **FEA (ANSYS)**: Sección metodológica completada, placeholder para resultados
  - El usuario realiza simulaciones personalmente
  - Cuando entregue resultados: integrar en `09_resultados.tex` con figuras

### Limites de Diseño Críticos
- **Llenado máximo**: 90% (fondo NO cumple ASME VIII al 100%)
- **Temperatura de operación**: 49-54°C (recomendación Ingredion)
- **Tasa de corrosión**: 0.0625 mm/año (tasa base 0.05 mm/año × factor 25%)
- **Corrosion allowance**: 1.875 mm para 30 años de vida útil
- **Viento**: 120 km/h (cargas dinámicas)
- **Sismo**: NSR-10 zona de amenaza intermedia

### Normas Aplicables
| Norma | Aplicación |
|-------|------------|
| API 650 | Espesores de cuerpo, fondo, tapa; cargas de viento/sismo |
| ASME VIII Div. 1 | Diseño a presión del fondo toriesférico |
| ASME B31.1 | Tuberías de entrada/salida (2" agua, 8" glucosa) |
| NSR-10 (Colombia) | Coeficientes sísmicos para Cali |
| 3-A Sanitary Standards | Acabado superficial, materiales, soldadura |
| FDA 21 CFR 177 | Materiales en contacto con alimentos |
| ASME Section II Part D | Propiedades mecánicas SS316L a temperatura de diseño |

### Recomendaciones de Operación (Derivadas del Análisis)
- **Setpoint de temperatura**: 60°C para balance entre viscosidad y tiempo de calentamiento
- **Ciclo de descarga**: 8 cargas de 24 toneladas en 24 horas (una cada ~2.5 horas)
- **Recalentamiento entre descargas**: ~25.5 horas para mantener temperatura
- **Lazo de control**: Sensor en fondo toriesférico (temperatura local, NO promedio)
- **Mantenimiento**: Inspección de corrosión cada 3 años (zonas de pitting por cloruros)

---

## Contactos y Responsables

**Elaboró**:
- J. Arboleda (proyectos2@dmlsas.com)
- H. Rosero (herminsul.rosero@dmlsas.com) - Gerente de Ingeniería

**Revisó**:
- W. Camelo

**Aprueba**:
- H. Rosero (Gerente de Ingeniería)

**Cliente**:
- INGREDION S.A. - Planta Cali, Colombia

---

## Notas para Agentes de IA

1. **Siempre** leer `CLAUDE.md` y `estadoavance.txt` antes de realizar cambios
2. **Actualizar** `estadoavance.txt` después de modificaciones importantes
3. **Versionar** PDF con nueva revisión si se cambia contenido técnico
4. **Validar**: Cálculos → Gráficas → Tablas → Texto → Compilación
5. **No inventar**: Referencias, datos de literatura, resultados de simulación
6. **Idioma principal**: Español técnico (comentarios en código pueden ser inglés)
7. **Landscape cultural**: Proyecto de ingeniería de consultoría colombiana, normas locales aplican
