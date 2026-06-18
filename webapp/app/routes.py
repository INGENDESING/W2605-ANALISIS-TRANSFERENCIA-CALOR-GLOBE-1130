"""
Rutas principales de la aplicación
"""
import io
import zipfile
from datetime import datetime
from pathlib import Path

from flask import (
    Blueprint, render_template, jsonify, send_from_directory,
    abort, send_file, current_app
)

from .core.ciclo_12m3h import simular_ciclo_12m3h, simular_ciclo_parametrico
from .core.perdidas_aislamiento import (
    resumen_perdidas_termicas,
    tabla_espesores_aislamiento,
    sensibilidad_espesor_aislamiento,
)
from .core.escenarios_extras import capacidad_operativa_diaria
from .core.arranque_niveles import calentamiento_arranque_niveles

main_bp = Blueprint('main', __name__)

# Directorios del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FIGURES_DIR = PROJECT_ROOT / 'results' / 'figures'
REPORTS_DIR = PROJECT_ROOT / 'docs' / 'report'
SRC_DIR = PROJECT_ROOT / 'src'
CORE_DIR = Path(__file__).resolve().parent / 'core'


@main_bp.route('/')
def index():
    """Página principal redirige al Dashboard Ejecutivo."""
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard Ejecutivo tipo Power BI."""
    ciclo = simular_ciclo_12m3h()
    perdidas = resumen_perdidas_termicas()
    capacidad = capacidad_operativa_diaria()
    return render_template(
        'dashboard.html',
        ciclo=ciclo,
        perdidas=perdidas,
        capacidad=capacidad,
    )


@main_bp.route('/calculadora')
def calculadora():
    """Módulo calculadora de transferencia de calor"""
    return render_template('calculadora.html')


@main_bp.route('/simulador')
def simulador():
    """Módulo simulador de ciclo de descargas"""
    return render_template('simulador.html')


@main_bp.route('/about')
def about():
    """Información del proyecto"""
    return render_template('about.html')


@main_bp.route('/sensibilidad')
def sensibilidad():
    """Módulo de análisis de sensibilidad"""
    return render_template('sensibilidad.html')


@main_bp.route('/propiedades')
def propiedades():
    """Propiedades termofísicas de la glucosa"""
    return render_template('propiedades.html')


@main_bp.route('/factibilidad')
def factibilidad():
    """Factibilidad térmica de cinco descargas diarias a 12 m³/h"""
    ciclo = simular_ciclo_12m3h()
    perdidas = resumen_perdidas_termicas()
    capacidad = capacidad_operativa_diaria()
    return render_template(
        'factibilidad.html',
        ciclo=ciclo,
        perdidas=perdidas,
        capacidad=capacidad
    )


@main_bp.route('/perdidas-aislamiento')
def perdidas_aislamiento():
    """Pérdidas térmicas y análisis de aislamiento"""
    return render_template(
        'perdidas_aislamiento.html',
        perdidas=resumen_perdidas_termicas(),
        espesores=tabla_espesores_aislamiento(),
        sensibilidad=sensibilidad_espesor_aislamiento(),
    )


@main_bp.route('/escenarios')
def escenarios():
    """Resumen de escenarios del proyecto"""
    return render_template('escenarios.html')


@main_bp.route('/ciclo-parametrico')
def ciclo_parametrico():
    """Análisis paramétrico del ciclo oficial de descargas."""
    return render_template(
        'ciclo_parametrico.html',
        escenarios=simular_ciclo_parametrico()['escenarios'],
    )


@main_bp.route('/arranque-niveles')
def arranque_niveles():
    """Arranque del 50 % y 80 % del tanque con pérdidas térmicas."""
    return render_template(
        'arranque_niveles.html',
        escenarios=calentamiento_arranque_niveles()['escenarios'],
    )


@main_bp.route('/documentos')
def documentos():
    """Tabla de transmittal con documentos descargables."""
    docs = _construir_transmittal()
    return render_template('documentos.html', documentos=docs)


def _construir_transmittal():
    """Construye la lista de documentos para la tabla de transmittal."""
    fecha_inf001 = datetime.fromtimestamp(
        (REPORTS_DIR / 'W2605PRINF001.pdf').stat().st_mtime
    ).strftime('%Y-%m-%d') if (REPORTS_DIR / 'W2605PRINF001.pdf').exists() else '—'

    docs = [
        {
            'codigo': 'W2605PRINF001',
            'nombre_archivo': 'W2605PRINF001.pdf',
            'titulo': 'Informe Técnico Principal — Análisis térmico del fondo toriesférico del tanque de glucosa Tag 53A-90A-0056',
            'revision': 'Rev.0',
            'fecha': fecha_inf001,
            'tipo': 'PDF',
            'categoria': 'Informe',
            'tamano': _format_size((REPORTS_DIR / 'W2605PRINF001.pdf').stat().st_size) if (REPORTS_DIR / 'W2605PRINF001.pdf').exists() else '—',
            'descripcion': 'Memoria técnica completa con metodología, resultados, análisis CFD y conclusiones del proyecto.',
            'ruta': 'informes/W2605PRINF001.pdf',
        },
    ]

    categorias_codigo = {
        'Core térmico': [
            ('coeficiente_U.py', 'Cálculo del coeficiente global de transferencia de calor U por resistencias térmicas en serie.'),
            ('perdidas_termicas_real.py', 'Cálculo de pérdidas térmicas con área real expuesta y sensibilidad de espesor de aislamiento.'),
            ('propiedades_glucosa.py', 'Correlaciones de propiedades termofísicas de la glucosa Globe 1130 y el agua.'),
            ('geometria_tanque.py', 'Parámetros geométricos del tanque: volúmenes, áreas, nivel y diámetro hidráulico de media caña.'),
            ('aislamiento.py', 'Dimensionamiento de espesor de aislamiento de lana mineral.'),
        ],
        'Simulación': [
            ('calentamiento_24ton_40_60.py', 'Simulación de arranque de glucosa de 40 °C a 60 °C para 24 ton, 50 % y 80 % del tanque.'),
            ('ciclo_descargas_14m2_75C_12m3h.py', 'Simulación del ciclo oficial de 5 descargas/día con chaqueta de 14 m² y agua a 75 °C.'),
            ('escenario4_capacidad.py', 'Evaluación de capacidad operativa diaria para rangos 54→57 °C y 55→57 °C.'),
            ('ciclo_descargas.py', 'Simulación del ciclo de descargas a carrotanques (Escenarios 2 y 3).'),
            ('escenarios.py', 'Simulación transitoria de los Escenarios 1, 2 y 3 de calentamiento.'),
        ],
        'Visualización': [
            ('diagramas_bloques_ciclo.py', 'Generador de diagramas de bloques del ciclo global, descarga y calentamiento.'),
            ('graficar_resistencias.py', 'Generador de gráfica de resistencias térmicas individuales y porcentuales.'),
        ],
    }

    for categoria, archivos in categorias_codigo.items():
        for archivo, descripcion in archivos:
            ruta = SRC_DIR / archivo
            if ruta.exists():
                docs.append({
                    'codigo': archivo,
                    'nombre_archivo': archivo,
                    'titulo': descripcion,
                    'revision': 'Rev.0',
                    'fecha': datetime.fromtimestamp(ruta.stat().st_mtime).strftime('%Y-%m-%d'),
                    'tipo': 'Python',
                    'categoria': categoria,
                    'tamano': _format_size(ruta.stat().st_size),
                    'descripcion': descripcion,
                    'ruta': f'codigo/src/{archivo}',
                })

    # Wrappers de webapp/app/core/
    for archivo in sorted(CORE_DIR.glob('*.py')):
        if archivo.name.startswith('_'):
            continue
        docs.append({
            'codigo': archivo.name,
            'nombre_archivo': archivo.name,
            'titulo': f'Wrapper Flask: {archivo.stem.replace("_", " ").title()}',
            'revision': 'Rev.0',
            'fecha': datetime.fromtimestamp(archivo.stat().st_mtime).strftime('%Y-%m-%d'),
            'tipo': 'Python',
            'categoria': 'Webapp Core',
            'tamano': _format_size(archivo.stat().st_size),
            'descripcion': f'Adaptador entre los scripts de cálculo de src/ y los endpoints JSON de la API para {archivo.stem}.',
            'ruta': f'codigo/webapp/app/core/{archivo.name}',
        })

    return docs


def _format_size(size_bytes):
    """Formatea tamaño en bytes a unidades legibles."""
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.1f} KB'
    else:
        return f'{size_bytes / (1024 * 1024):.1f} MB'


@main_bp.route('/figures/<path:filename>')
def serve_figure(filename):
    """Servir figuras generadas en results/figures/"""
    return send_from_directory(str(FIGURES_DIR), filename)


@main_bp.route('/informes/<path:filename>')
def serve_informe(filename):
    """Servir informes PDF desde docs/report/ como descarga."""
    if not filename.lower().endswith('.pdf'):
        abort(404)
    return send_from_directory(str(REPORTS_DIR), filename, as_attachment=True)


@main_bp.route('/codigo/<path:filename>')
def serve_codigo(filename):
    """Servir archivos Python de src/ o webapp/app/core/ como descarga."""
    # Validar extensión
    if not filename.lower().endswith('.py'):
        abort(404)

    # Validar que la ruta solicitada esté dentro de src/ o webapp/app/core/
    partes = Path(filename).parts
    if len(partes) < 2:
        abort(404)

    raiz = partes[0]
    resto = '/'.join(partes[1:])

    if raiz == 'src':
        base = SRC_DIR
    elif raiz == 'webapp' and partes[1:3] == ('app', 'core'):
        base = CORE_DIR
        resto = '/'.join(partes[3:])
    else:
        abort(404)

    archivo = (base / resto).resolve()
    if not str(archivo).startswith(str(base.resolve())) or not archivo.is_file():
        abort(404)

    return send_from_directory(str(base), resto, as_attachment=True)


@main_bp.route('/descargar-codigo-fuente')
def descargar_codigo_fuente():
    """Genera y sirve un ZIP con el código fuente Python del proyecto."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Archivos de src/
        if SRC_DIR.exists():
            for archivo in SRC_DIR.rglob('*.py'):
                rel = archivo.relative_to(PROJECT_ROOT)
                zf.write(archivo, rel)

        # Archivos de webapp/app/core/
        if CORE_DIR.exists():
            for archivo in CORE_DIR.rglob('*.py'):
                rel = Path('webapp') / archivo.relative_to(PROJECT_ROOT / 'webapp')
                zf.write(archivo, rel)

    zip_buffer.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d')
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'W2605_Codigo_Fuente_{timestamp}.zip'
    )


@main_bp.route('/health')
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'service': 'W2605 WebApp',
        'version': '2.2.0'
    })
