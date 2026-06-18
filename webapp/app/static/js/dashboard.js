/**
 * Dashboard del Escenario 5 — W2605
 * Consume /api/proyecto/ciclo-escenario5 y renderiza KPIs,
 * gráficas por fase separada, vista completa y Gantt.
 */

// Estado actual
let estadoActual = {
    datosSimulacion: null,
};

// Layout base para Plotly — tema oscuro cyberpunk
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 12, color: '#e0e6ed' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    xaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    yaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    margin: { l: 60, r: 20, t: 40, b: 50 },
    legend: { orientation: 'h', y: -0.18, font: { color: '#e0e6ed' } },
    hovermode: 'x unified'
};

const COLORES_FASE = [
    '#39ff14', '#00f0ff', '#ff8c00', '#ff2a6d', '#bd00ff'
];

/**
 * Inicializar dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    cargarEscenario5();
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    const btnRecalcular = document.getElementById('btnRecalcular');
    if (btnRecalcular) {
        btnRecalcular.addEventListener('click', cargarEscenario5);
    }

    // Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
}

/**
 * Cargar Escenario 5 desde la API
 */
async function cargarEscenario5() {
    mostrarSpinner(true);

    try {
        const response = await fetch('/api/proyecto/ciclo-escenario5');
        const result = await response.json();
        if (!result.success) throw new Error(result.error);

        estadoActual.datosSimulacion = result.data;

        actualizarKPIs(result.data);
        renderizarGraficaDescargas(result.data);
        renderizarGraficaRecalentamiento(result.data);
        renderizarGraficaTvsT(result.data);
        renderizarGantt(result.data);
    } catch (error) {
        console.error('Error cargando Escenario 5:', error);
        mostrarError('Error al cargar Escenario 5: ' + error.message);
    } finally {
        mostrarSpinner(false);
    }
}

/**
 * Actualizar KPI cards del Escenario 5
 */
function actualizarKPIs(data) {
    const metricas = data.metricas;

    document.getElementById('kpiTMin').textContent = metricas.T_min_C.toFixed(1) + ' °C';
    document.getElementById('kpiTiempoTotal').textContent = metricas.t_total_h.toFixed(1) + ' h';
    document.getElementById('kpiDescargasOK').textContent = `${metricas.descargas_ok}/${data.configuracion.n_descargas}`;
    document.getElementById('kpiMasaTotal').textContent = (metricas.masa_total_descargada_kg / 1000).toFixed(1) + ' ton';
}

/**
 * Renderizar gráfica de descargas (con flujo) — tiempo normalizado por descarga
 */
function renderizarGraficaDescargas(data) {
    const serie = data.series;
    const t = serie.t_h;
    const T = serie.T_g_C;
    const descargas = data.descargas;

    const traces = descargas.map((d, i) => {
        const color = COLORES_FASE[i % COLORES_FASE.length];
        const t0 = d.t_ini_h;
        const t1 = d.t_fin_h;
        const tNorm = [];
        const TPhase = [];
        for (let j = 0; j < t.length; j++) {
            if (t[j] >= t0 - 1e-6 && t[j] <= t1 + 1e-6) {
                tNorm.push(t[j] - t0);
                TPhase.push(T[j]);
            }
        }
        return {
            x: tNorm,
            y: TPhase,
            type: 'scatter',
            mode: 'lines',
            name: `Descarga ${d.descarga}`,
            line: { color: color, width: 2 }
        };
    });

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo desde inicio de descarga (h)', range: [0, data.configuracion.duracion_descarga_h * 1.05] },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)', range: [50, 65] },
        showlegend: true,
        legend: { orientation: 'h', y: -0.22 }
    };

    Plotly.newPlot('graficaDescargas', traces, layout, {responsive: true});
}

/**
 * Renderizar gráfica de recalentamiento (sin flujo) — tiempo normalizado por fase
 */
function renderizarGraficaRecalentamiento(data) {
    const serie = data.series;
    const t = serie.t_h;
    const T = serie.T_g_C;
    const fasesRecalentamiento = data.fases.filter(f => f.tipo === 'recalentamiento');

    const traces = fasesRecalentamiento.map((f, i) => {
        const color = COLORES_FASE[i % COLORES_FASE.length];
        const t0 = f.t_inicio_h;
        const t1 = f.t_fin_h;
        const tNorm = [];
        const TPhase = [];
        for (let j = 0; j < t.length; j++) {
            if (t[j] >= t0 - 1e-6 && t[j] <= t1 + 1e-6) {
                tNorm.push(t[j] - t0);
                TPhase.push(T[j]);
            }
        }
        return {
            x: tNorm,
            y: TPhase,
            type: 'scatter',
            mode: 'lines',
            name: `Recalentamiento ${f.descarga_num}`,
            line: { color: color, width: 2 }
        };
    });

    const maxDuracion = fasesRecalentamiento.length
        ? Math.max(...fasesRecalentamiento.map(f => f.duracion_h))
        : 1;

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo desde inicio de recalentamiento (h)', range: [0, maxDuracion * 1.05] },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)', range: [50, 65] },
        showlegend: true,
        legend: { orientation: 'h', y: -0.22 }
    };

    Plotly.newPlot('graficaRecalentamiento', traces, layout, {responsive: true});
}

/**
 * Renderizar gráfica Temperatura vs Tiempo — vista completa
 */
function renderizarGraficaTvsT(data) {
    const serie = data.series;
    const t = serie.t_h;
    const T = serie.T_g_C;
    const descargas = data.descargas;

    // Shapes para bandas de descarga
    const shapes = descargas.map(d => ({
        type: 'rect',
        x0: d.t_ini_h,
        x1: d.t_fin_h,
        y0: 0,
        y1: 1,
        yref: 'paper',
        fillcolor: 'rgba(255, 140, 0, 0.12)',
        line: { width: 0 },
        layer: 'below'
    }));

    const trace = {
        x: t,
        y: T,
        type: 'scatter',
        mode: 'lines',
        name: 'T Glucosa',
        line: { color: '#39ff14', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(57, 255, 20, 0.08)'
    };

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)' },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)', range: [20, 70] },
        shapes: shapes,
        showlegend: false,
        annotations: [{
            x: 0.5, y: 1.1, xref: 'paper', yref: 'paper',
            text: data.configuracion.nombre,
            showarrow: false, font: { size: 12, color: '#8b95a8' }
        }]
    };

    Plotly.newPlot('graficaTvsT', [trace], layout, {responsive: true});
}

/**
 * Renderizar diagrama de Gantt
 */
function renderizarGantt(data) {
    const fases = data.fases;
    const tareas = [];

    fases.forEach(f => {
        const esRecalentamiento = f.tipo === 'recalentamiento';
        const label = esRecalentamiento
            ? `Recalentamiento ${f.descarga_num}`
            : `Descarga ${f.descarga_num}`;
        tareas.push({
            x: [f.duracion_h],
            y: [label],
            base: [f.t_inicio_h],
            type: 'bar',
            orientation: 'h',
            marker: {
                color: esRecalentamiento ? '#0096ff' : '#ff8c00'
            },
            text: [`${f.T_inicio_C.toFixed(1)}°C → ${f.T_fin_C.toFixed(1)}°C`],
            textposition: 'inside',
            hovertemplate: `${label}<br>Inicio: %{base:.1f}h<br>Duración: %{x:.1f}h<extra></extra>`
        });
    });

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)' },
        yaxis: { ...plotlyLayout.yaxis, autorange: 'reversed' },
        showlegend: false,
        margin: { l: 160, r: 20, t: 30, b: 50 }
    };

    Plotly.newPlot('graficaGantt', tareas, layout, {responsive: true});
}

/**
 * Mostrar/ocultar spinner
 */
function mostrarSpinner(mostrar) {
    const spinner = document.getElementById('spinnerEscenario');
    if (spinner) {
        spinner.classList.toggle('d-none', !mostrar);
    }
}

/**
 * Mostrar error
 */
function mostrarError(mensaje) {
    console.error(mensaje);
    if (typeof showToast === 'function') {
        showToast(mensaje, 'danger');
    } else {
        alert(mensaje);
    }
}
