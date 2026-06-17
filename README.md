# Proyecto W2605 — Análisis térmico del fondo toriesférico del tanque de glucosa

## Descripción

Estudio de transferencia de calor del fondo toriesférico del tanque de almacenamiento de glucosa **Tag 53A-90A-0056** en la planta **Ingredion S.A.** de Cali, Colombia. El proyecto evalúa el desempeño térmico de la chaqueta de media caña rectangular en espiral, las pérdidas térmicas con aislamiento de lana mineral y el ciclo operativo de descargas a carrotanques.

**Empresa ejecutora:** DMV SAS  
**Cliente:** Ingredion S.A., Planta Cali  
**Fluido:** Glucosa Globe 42 DE (~80,6 °Brix)  
**Material del fondo:** Acero inoxidable SS316L

---

## Documentos oficiales

| Código | Documento | Ubicación |
|---|---|---|
| W2605PRINF001 | Informe técnico principal (memoria descriptiva) | `docs/report/W2605PRINF001.tex` / `.pdf` |
| W2605PRINF002 | Resumen ejecutivo gerencial | `docs/report/W2605PRINF002.tex` / `.pdf` |

---

## Estructura del proyecto

| Carpeta | Contenido |
|---|---|
| `docs/report/` | Maestros LaTeX, secciones, configuración, bibliografía y logos del informe oficial. |
| `src/` | Scripts Python de cálculo, simulación y generación de figuras. |
| `results/` | Figuras (PDF/PNG) y tablas (CSV) generadas por los scripts. |
| `Data/` | Datasheets, planos, normas y documentos de referencia del proyecto. |
| `webapp/` | Aplicación Flask interactiva para simulación de balance de materia y energía. |
| `task/` | Plan de trabajo, tests de validación y scripts de soporte. |
| `InformeTercero/` | Informe técnico de tercero auditado y documento de auditoría crítica. |
| `reciclaje/` | Archivos generados, auxiliares, duplicados o desactualizados conservados por trazabilidad. |

---

## Tecnologías

### Cálculo y simulación
- **Python 3.12** con `numpy`, `scipy` y `matplotlib`.
- Correlaciones de transferencia de calor: Sieder-Tate (lado agua) y Churchill-Chu (lado glucosa).
- Propiedades termofísicas de la glucosa mediante implementación propia ajustada a ficha técnica Ingredion.

### Documentación
- **MiKTeX** con `pdflatex` y `bibtex`.
- Clase `elsarticle` y paquetes `booktabs`, `siunitx`, `graphicx` y `tikz`.

### Aplicación web
- **Flask 3.0.3** con CORS, exportación a PDF (`reportlab`) y Excel (`openpyxl`, `xlsxwriter`).

---

## Requisitos

- Python 3.12 o superior.
- MiKTeX (Windows) o TeX Live (Linux/Mac) para compilar los informes LaTeX.
- Git para control de versiones.

---

## Instalación de dependencias

Para el núcleo de cálculo:

```bash
pip install -r requirements.txt
```

Para la aplicación web:

```bash
pip install -r webapp/requirements.txt
```

---

## Compilación de los informes

Desde `docs/report/`:

```bash
# Informe técnico principal
pdflatex -interaction=nonstopmode W2605PRINF001.tex
bibtex W2605PRINF001
pdflatex -interaction=nonstopmode W2605PRINF001.tex
pdflatex -interaction=nonstopmode W2605PRINF001.tex

# Resumen ejecutivo
pdflatex -interaction=nonstopmode W2605PRINF002.tex
pdflatex -interaction=nonstopmode W2605PRINF002.tex
```

---

## Ejecución de tests

```bash
# Tests del ciclo operativo oficial
venv/Scripts/python.exe task/test_ciclo.py
venv/Scripts/python.exe task/test_simulacion_50C.py

# Tests de la API web
cd webapp
../venv/Scripts/python.exe tests/test_api.py
```

---

## Uso de la aplicación web

```bash
cd webapp
../venv/Scripts/python.exe run.py
```

Abrir el navegador en `http://localhost:5000` (o el puerto indicado en la consola).

### Páginas principales

| Ruta | Descripción |
|---|---|
| `/` | Página de inicio con resumen del proyecto. |
| `/dashboard` | Dashboard de KPIs con resultados del ciclo a 12 m³/h, pérdidas térmicas y capacidad operativa. |
| `/calculadora` | Calculadora interactiva de transferencia de calor (área base 13 m²). |
| `/simulador` | Simulador del ciclo de descargas. |
| `/factibilidad` | Resultado del ciclo de 5 descargas diarias a 12 m³/h: área de chaqueta 14 m², agua a 75 °C, temperatura mínima alcanzada y verificación contra el límite de 57 °C. |
| `/perdidas-aislamiento` | Pérdidas térmicas con el área real expuesta y comparativa de espesores de aislamiento. |
| `/escenarios` | Resumen de escenarios del proyecto. |
| `/sensibilidad` | Análisis de sensibilidad de parámetros. |
| `/propiedades` | Propiedades termofísicas de la glucosa. |
| `/about` | Información del proyecto, normas y metodología. |

La calculadora (`/calculadora`) y el simulador base emplean el área histórica de **13 m²**. La página `/factibilidad` y el dashboard emplean el área de diseño del caso a 12 m³/h, **14 m²**, para el ciclo de descargas. Ambos valores se presentan de forma explícita para mantener la trazabilidad entre el modelo original y el caso de estudio.

### API del proyecto

Los siguientes endpoints exponen los análisis técnicos en formato JSON:

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/proyecto/ciclo-12m3h` | Simulación del ciclo de 5 descargas a 12 m³/h con 14 m². |
| `GET` | `/api/proyecto/perdidas-termicas` | Resumen de pérdidas térmicas con aislamiento de referencia. |
| `GET` | `/api/proyecto/aislamiento/espesores` | Tabla comparativa de espesores de aislamiento. |
| `GET` | `/api/proyecto/aislamiento/sensibilidad` | Sensibilidad del espesor de aislamiento a 60 °C. |
| `GET` | `/api/proyecto/calentamiento-24ton` | Tiempo de calentamiento de 24 ton desde 40 °C hasta 60 °C. |
| `GET` | `/api/proyecto/capacidad-operativa` | Capacidad operativa diaria con área 13 m². |

### Figuras

Las gráficas generadas por los scripts de `src/` y guardadas en `results/figures/` se sirven estáticamente desde la ruta `/figures/<nombre_de_archivo>`.

---

## Resultados clave

| Parámetro | Valor |
|---|---|
| Temperatura objetivo de la glucosa | 60 °C |
| Ciclo operativo | 5 descargas/día, 24 ton/descarga, 2,0 h de descarga, período 4,8 h |
| Flujo medio de glucosa | 5 000 kg/h |
| Área de transferencia de la chaqueta | 13 m² (base); 14 m² (caso de estudio 24 ton) |
| Coeficiente global con aislamiento (U) | ~0,38 W/(m²·°C) |
| Pérdidas térmicas con aislamiento a 60 °C | 14,7 MJ/h |
| Pérdidas térmicas sin aislamiento a 60 °C | 175,4 MJ/h |
| Reducción de pérdidas por aislamiento | 91,6 % |
| Balance neto a 60 °C | +15,3 MJ/h |
| Tiempo para perder 3 °C en parada | ~4,5 días |

---

## Autoría y contacto

**Elaboró, revisó y aprobó:** DMV SAS  
**Contacto técnico:** [correo@dmvsas.com]

---

## Licencia

Este proyecto es propiedad de DMV SAS y está destinado exclusivamente a uso interno y entrega al cliente Ingredion S.A.

---

## Estado del proyecto

Entrega final en preparación. Sincronización con el repositorio remoto completada. Pendiente: definición del logo corporativo correcto de DMV SAS para el membrete de los informes.

Última actualización: 17 de junio de 2026.
