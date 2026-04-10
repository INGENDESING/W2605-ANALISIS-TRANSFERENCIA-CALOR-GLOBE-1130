# Plan de Auditoría y Corrección — WebApp P2611

## Hallazgos de la Auditoría

### Bug 1: SVG del Dashboard muestra masa post-descargas (~61.9 ton)
- [/] **A.1** Corregir `dashboard.js` → `actualizarSVGTanque()` para tomar el **primer punto** (condiciones iniciales) en vez del último.

### Bug 2: Número de descargas NO debe ser un dato de entrada
- [ ] **B.1** Crear función `simular_ciclo_automatico()` en `balance_energia.py` que itere descargas hasta incumplir restricciones.
- [ ] **B.2** Crear endpoint `/api/calcular/ciclo-automatico` en `calculos.py`.
- [ ] **B.3** Modificar `simulador.js` para llamar al nuevo endpoint y mostrar descargas como resultado.
- [ ] **B.4** Modificar `simulador.html` para eliminar el input de num_descargas y agregar KPI calculado.

### Bug 3: Datos estáticos incorrectos en index.html
- [ ] **C.1** Corregir "211 m³" → "222.8 m³" y "~300 ton" → "~314 ton" en `index.html`.

---

## Sección de Revisión
*(Se completará al finalizar la ejecución del plan)*
