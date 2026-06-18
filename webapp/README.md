# W2605 WebApp - Balance de Materia y Energía

Aplicación web para el análisis de transferencia de calor y balance de materia en el sistema de calentamiento de glucosa Globe 1130.

## Características

- **Calculadora de Transferencia de Calor**: Cálculo de coeficiente U, potencia térmica, tiempo de calentamiento
- **Simulador de Ciclo de Descargas**: Simulación de operación de carga/descarga a carrotanques
- **Dashboard de KPIs**: Visualizaciones interactivas con gráficos y tablas
- **Exportación**: Descarga de resultados en JSON, CSV y Excel

## Instalación

### Requisitos

- Python 3.12+
- Dependencias del proyecto base (numpy, scipy, matplotlib)

### Instalación de dependencias

```bash
cd webapp
pip install -r requirements.txt
```

### Ejecución

```bash
python run.py
```

La aplicación estará disponible en: http://localhost:5000

## Estructura del Proyecto

```
webapp/
├── app/
│   ├── api/              # Endpoints REST API
│   │   ├── calculos.py
│   │   ├── simulacion.py
│   │   └── exportar.py
│   ├── core/             # Lógica de negocio
│   │   ├── balance_energia.py
│   │   ├── balance_masa.py
│   │   ├── area_fija.py
│   │   └── props_calculadas.py
│   ├── static/           # CSS, JS, imágenes
│   │   ├── css/
│   │   └── js/
│   ├── templates/        # Plantillas HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── calculadora.html
│   │   ├── simulador.html
│   │   └── dashboard.html
│   ├── __init__.py
│   └── routes.py
├── config.py
├── requirements.txt
└── run.py
```

## API Endpoints

### Cálculos

- `POST /api/calcular/transferencia-calor` - Calcular parámetros de transferencia de calor
- `POST /api/calcular/simular-calentamiento` - Simular calentamiento transitorio
- `POST /api/calcular/masa-glucosa` - Calcular masa de glucosa
- `GET /api/calcular/tabla-propiedades` - Generar tabla de propiedades termofísicas

### Simulación

- `POST /api/simular/flujo-maximo` - Calcular flujo máximo de descarga
- `POST /api/simular/capacidad` - Calcular capacidad operativa
- `POST /api/simular/ciclo-descargas` - Simular ciclo completo
- `POST /api/simular/comparar-escenarios` - Comparar Escenario 2 vs 3

### Exportación

- `POST /api/exportar/csv` - Exportar a CSV
- `POST /api/exportar/excel` - Exportar a Excel
- `POST /api/exportar/reporte-json` - Exportar reporte JSON

## Uso

### Calculadora

1. Ingrese los parámetros de operación (flujo de agua, temperaturas, volumen)
2. Presione "Calcular"
3. Visualice los resultados en las tarjetas KPI, gráfico y tabla

### Simulador

1. Seleccione un escenario predefinido (2 o 3) o configure manualmente
2. Ajuste el número de descargas, masa por descarga, etc.
3. Presione "Simular"
4. Analice los resultados en el gráfico de evolución, Gantt y tabla de descargas

### Dashboard

- Visualice KPIs principales
- Explore gráficos interactivos
- Consulte tablas de propiedades termofísicas
- Exporte datos según necesidad

## Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Gráficos**: Plotly.js, Chart.js
- **Tablas**: DataTables.js
- **Cálculos**: NumPy, SciPy (integración con proyecto base)

## Notas

- Las correlaciones termofísicas están calibradas a la ficha técnica Ingredion 011420
- El área de contacto por defecto es 14 m² (media caña propuesta)
- Las simulaciones utilizan el modelo de coeficiente U con resistencias en serie

## Desarrollo

Para agregar nuevas funcionalidades:

1. Crear endpoints en `app/api/`
2. Agregar lógica de negocio en `app/core/`
3. Crear plantillas en `app/templates/`
4. Agregar JavaScript en `app/static/js/`

## Licencia

Proyecto propiedad de DMV S.A.S. para INGREDION S.A.
