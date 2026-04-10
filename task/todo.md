# Plan Maestro: Auditoría y Despliegue en Render (Proyecto P2611)

## 1. ANÁLISIS DEL PROBLEMA Y AUDITORÍA
### Estado Actual de `webapp/`
1. **Verificación de Entorno**: El archivo `webapp/requirements.txt` cubre efectivamente todos los módulos científicos de `src/` (`numpy`, `scipy`) sumados a los requeridos para la API (`flask`, `gunicorn`).
2. **Endpoint Funcional**: La invocación local arranca exitosamente; el `wsgi.py` inyecta `../src` sin corromper dependencias.
3. **Puntos de mejora detectados**:
   - Falta directiva estricta de versión de Python. Render emplea por defecto Python 3.7, el cual puede chocar con módulos actualizados.
   - Falta el Blueprint oficial de Render (`render.yaml`) para simplificarle el trabajo al equipo de ingeniería de DML (Infraestructura como Código).
   - `CORS_ORIGINS` en `config.py` está cerrado a `localhost`. Hay que flexibilizarlo para asimilar el ambiente de Producción subministrado por la URL autogenerada de Render.

---

## 2. LISTA DE TAREAS PENDIENTES (Ejecución Minimalista)

### Fase A: Parches de Código / Configuraciones
- [ ] **A.1** Modificar `webapp/config.py`: En la clase `ProductionConfig`, asignar variable `CORS_ORIGINS = '*'` para habilitar CORS universal desde el entorno desplegado.
- [ ] **A.2** Crear `.python-version` en la raíz del proyecto, especificando `3.12.0` de forma limpia.

### Fase B: Infraestructura como Código (IaC)
- [ ] **B.1** Crear en la raíz el archivo `render.yaml` indicando:
  - Tipo de servicio: `web`
  - Entorno: Python
  - Comando Build: `pip install -r webapp/requirements.txt`
  - Comando Start: `gunicorn -c webapp/wsgi.py` (ajustado de requerir parámetros). Aquí pasaremos directo `cd webapp && gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app`
- [ ] **B.2** Añadir el proceso o entorno secreto `SECRET_KEY` recomendado en el archivo `render.yaml` para asegurar la arquitectura.

---

## 3. SECCIÓN DE REVISIÓN
*(Esta sección será completada una vez finalizado el trabajo de configuración para despliegue)*
