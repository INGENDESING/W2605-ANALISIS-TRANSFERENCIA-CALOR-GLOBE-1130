# Plan de Auditoría y Corrección — WebApp P2611

## Hallazgos de la Auditoría

### Bug 1: SVG del Dashboard muestra masa post-descargas (~61.9 ton)
- [x] **A.1** Corregir `dashboard.js` → `actualizarSVGTanque()` para tomar el **primer punto** (condiciones iniciales) en vez del último.

### Bug 2: Número de descargas NO debe ser un dato de entrada
- [x] **B.1** Crear función `simular_ciclo_automatico()` en `balance_energia.py` que itere descargas hasta incumplir restricciones.
- [x] **B.2** Crear endpoint `/api/calcular/ciclo-automatico` en `calculos.py`.
- [x] **B.3** Modificar `simulador.js` para llamar al nuevo endpoint y mostrar descargas como resultado.
- [x] **B.4** Modificar `simulador.html` para eliminar el input de num_descargas y agregar KPI calculado.

### Bug 3: Datos estáticos incorrectos en index.html
- [x] **C.1** Corregir "211 m³" → "222.8 m³" y "~300 ton" → "~314 ton" en `index.html`.

### Bug 4: Casilla de "Pre-calentado" salta calentamiento a 50°C
- [x] **D.1** Analizar inconsistencia en la temperatura inicial del pantallazo (T_ini = 50°C reportando la gráfica arrancar en 57°C).
- [x] **D.2** Corregir `simulador.js` (`leerParametros`) para ignorar checkbox "Pre-calentado" si `T_inicial < T_objetivo`.
- [x] **D.3** Corregir `balance_energia.py` para validar la temperatura desde la **primera** descarga (`i_descargas > 0` removido).
- [x] **D.4** Probar con parámetros exactos del pantallazo.

---

## Sección de Revisión
- Se analizaron y solucionaron de fondo los cálculos del ciclo automático (se re-escribió la lógica para que las descargas sean calculadas por un motor ODE, no como inputs fijos).
- Se descubrió que el usuario tenía la casilla **"Pre-calentado (omitir fase)" marcada**. Debido a un error previo, esto forzaba la T_inicial enviada a 57°C, saltando la fase de calentamiento pero manteniendo "50°C" visualmente en el campo de texto. 
- Se deshabilitó lógicamente el uso de esta casilla en JS cuando la temperatura del tanque es menor al objetivo mínimo, lanzando un warning e imponiendo la fase de calentamiento obligatoria. Además, el backend ahora bloquea matemáticamente la descarga desde el bloque 1 si la T < mínima.
- Una simulación realista con Agua a 65°C y Glucosa a 50°C toma ~36h y su temperatura final a duras penas llega a ~51.5°C, mostrando claramente que en esas condiciones no se logran descargar los primeros carrotanques. En el anterior código, la restricción de descarga sólo actuaba después del primer viaje. Se corrigieron todas las inconsistencias detectadas.
