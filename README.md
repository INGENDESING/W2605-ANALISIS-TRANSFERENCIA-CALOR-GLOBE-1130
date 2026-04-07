# Proyecto P2611 - Análisis Térmico y Estructural del Fondo Toriesférico

## Descripción

Estudio de transferencia de calor y análisis estructural del fondo toriesférico de un tanque de almacenamiento de glucosa para INGREDION S.A. (Planta Cali, Colombia).

**Código del documento**: `P2611-PR-INF-001 R0`

### Alcance Técnico
- **Parte I**: Transferencia de calor en chaqueta de media caña (espiral rectangular) sobre fondo toriesférico
  - Cálculo del coeficiente global de transferencia de calor (U)
  - Perfiles de temperatura y análisis de ciclo de descargas a carrotanques
  
- **Parte II**: Validación de espesores del tanque
  - Normas API 650 y ASME VIII
  - Cargas hidrostáticas, viento (120 km/h), sismo (NSR-10 zona intermedia)
  - Corrosión en SS316L

## Estructura del Proyecto

```
.
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
│   └── properties/              # Propiedades de materiales
│
├── docs/                        # Documentación y reportes
│   ├── report/                  # Documento principal LaTeX
│   │   ├── P2611-PR-INF-001_R0.tex
│   │   ├── sections/            # Capítulos del informe
│   │   ├── config/              # Configuración LaTeX
│   │   ├── references/          # Bibliografía
│   │   └── assets/              # Figuras específicas del informe
│   └── project-management/      # Planes y seguimiento del proyecto
│
├── results/                     # Resultados y análisis
│   ├── figures/                 # Figuras generadas (PDF/PNG)
│   └── analysis/                # Análisis intermedios y logs
│
├── examples/                    # Ejemplos y demos
│   └── web-demo/                # Demo Flask interactiva
│
├── notebooks/                   # Jupyter notebooks (opcional)
├── tests/                       # Pruebas unitarias (si se implementan)
│
├── .gitignore                   # Archivos a ignorar en Git
├── README.md                    # Este archivo
└── LICENSE                      # Licencia del proyecto

```

## Tecnologías Utilizadas

### Stack Principal
- **Python 3.12**: Cálculos científicos y numéricos
- **MiKTeX**: Compilación de documentos LaTeX
- **VS Code**: Editor de código con extensiones LaTeX Workshop y Python

### Bibliotecas Python
- `numpy`, `scipy`: Cálculos numéricos
- `matplotlib`, `plotly`: Generación de gráficas
- `thermo`, `CoolProp`: Propiedades termofísicas
- `pandas`: Procesamiento de datos

### Documentación
- **Clase LaTeX**: `elsarticle.cls` (Elsevier)
- **Paquetes**: `siunitx`, `mhchem`, `graphicx`, `booktabs`, `tikz`
- **Compilador**: `pdflatex`

## Requisitos

- Python 3.12 o superior
- MiKTeX (Windows) o TeX Live (Linux/Mac)
- Git (opcional, para control de versiones)

### Instalación de Dependencias Python

El proyecto usa las siguientes bibliotecas Python:
- `numpy` (2.4.3)
- `scipy` (1.17.1)
- `matplotlib` (3.10.8)

Para instalar todas las dependencias automáticamente:

```bash
pip install -r requirements.txt
```

Para instalar manualmente o ver detalles completos, ver `INSTALACION_DEPENDENCIAS.md`.

## Uso

**IMPORTANTE**: Antes de ejecutar los cálculos, asegúrate de tener instaladas las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución de Cálculos

```bash
# Activar Python 3.12
python src/escenarios.py
python src/espesores_tanque.py
```

### Compilación del Informe

```bash
cd docs/report
pdflatex P2611-PR-INF-001_R0.tex
pdflatex P2611-PR-INF-001_R0.tex  # Segunda pasada para referencias
```

O usando LaTeX Workshop en VS Code:
- Abrir el archivo `.tex`
- Usar `Ctrl+Alt+B` (Build LaTeX project)
- Compilar 2 veces para resolver referencias

### Demo Web (Opcional)

```bash
cd examples/web-demo
python app.py
```

Abrir navegador en `http://localhost:5000`

## Resultados Clave

- **Coeficiente U**: 18-36 W/m²·°C (promedio ponderado)
- **Tiempos de calentamiento**:
  - Escenario 1: 5.5 días
  - Escenario 2: 32.2 días
  - Escenario 3: 17.3 días
- **Espesores**: Cumplen API 650 y ASME VIII con márgenes positivos
- **Vida útil**: ≥30 años considerando tasa de corrosión

## Autores

- **Elaboró**: J. Arboleda, H. Rosero
- **Revisó**: W. Camelo
- **Aprobó**: H. Rosero (Gerente de Ingeniería)

## Cliente

**INGREDION S.A.** - Planta Cali, Colombia

## Licencia

Este proyecto es propiedad de DML S.A.S. y se encuentra destinado exclusivamente para uso interno y entrega al cliente INGREDION S.A.

## Contacto

Para consultas técnicas:
- proyectos2@dmlsas.com
- herminsul.rosero@dmlsas.com

## Estado del Proyecto

**Estado**: Completado y entregado (03 de abril de 2026)

Última actualización: Recalibración del modelo a ficha técnica Ingredion 011420
