/**
 * Análisis de Sensibilidad - W2605
 * Análisis univariable de impacto de parámetros en KPIs
 */

// Layout Plotly — tema oscuro cyberpunk
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 11, color: '#e0e6ed' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    xaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    yaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    margin: { l: 60, r: 40, t: 30, b: 50 },
    hovermode: 'x unified'
};

// Estado
let estadoSens = {
    datos: null,
    variable: null
};

// Configuración de rangos por variable
const RANGOS_DEFAULT = {
    'T_agua': { min: 50, max: 90, paso: 5 },
    'velocidad_m_s': { min: 0.5, max: 4.0, paso: 0.25 },
    'area_m2': { min: 5, max: 25, paso: 1 },
    'T_glucosa_inicial': { min: 10, max: 50, paso: 5 },
    'nivel_pct': { min: 40, max: 100, paso: 5 },
    'num_descargas': { min: 1, max: 12, paso: 1 }
};

const UNIDADES = {
    'T_agua': '°C',
    'velocidad_m_s': 'm/s',
    'area_m2': 'm²',
    'T_glucosa_inicial': '°C',
    'nivel_pct': '%',
    'num_descargas': 'descargas'
};

/**
 * Inicializar
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    actualizarRangos();
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    document.getElementById('selectVariable').addEventListener('change', () => {
        actualizarRangos();
        actualizarParamsFijos();
    });
    document.getElementById('btnCalcularSensibilidad').addEventListener('click', calcularSensibilidad);
    document.getElementById('btnExportarSens').addEventListener('click', exportarCSV);
}

/**
 * Actualizar rangos según variable seleccionada
 */
function actualizarRangos() {
    const variable = document.getElementById('selectVariable').value;
    const rango = RANGOS_DEFAULT[variable];
    
    document.getElementById('rangoMin').value = rango.min;
    document.getElementById('rangoMax').value = rango.max;
    document.getElementById('rangoPaso').value = rango.paso;
}

/**
 * Actualizar parámetros fijos (deshabilitar el que es variable)
 */
function actualizarParamsFijos() {
    const variable = document.getElementById('selectVariable').value;
    
    // Mapeo de variables a IDs de inputs
    const mapVars = {
        'T_agua': 'fijoTAgua',
        'velocidad_m_s': 'fijoV',
        'T_glucosa_inicial': 'fijoTIni',
        'nivel_pct': 'fijoNivel',
        'area_m2': 'fijoArea',
        'num_descargas': 'fijoNumDesc'
    };
    
    // Habilitar todos
    Object.values(mapVars).forEach(id => {
        document.getElementById(id).disabled = false;
        document.getElementById(id).classList.remove('bg-light');
    });
    
    // Deshabilitar el que es variable
    if (mapVars[variable]) {
        const input = document.getElementById(mapVars[variable]);
        input.disabled = true;
        input.classList.add('bg-light');
    }
}

/**
 * Calcular análisis de sensibilidad
 */
async function calcularSensibilidad() {
    const variable = document.getElementById('selectVariable').value;
    const min = parseFloat(document.getElementById('rangoMin').value);
    const max = parseFloat(document.getElementById('rangoMax').value);
    const paso = parseFloat(document.getElementById('rangoPaso').value);
    
    // Generar lista de valores
    const valores = [];
    for (let v = min; v <= max + 0.001; v += paso) {
        valores.push(parseFloat(v.toFixed(4)));
    }
    
    mostrarSpinner(true);
    actualizarProgress(10);
    
    try {
        const paramsFijos = leerParamsFijos();
        
        const response = await fetch('/api/sensibilidad', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                variable_nombre: variable,
                valores_lista: valores,
                params_fijos: paramsFijos
            })
        });
        
        actualizarProgress(80);
        
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        
        estadoSens.datos = result.data;
        estadoSens.variable = variable;
        
        actualizarUI(result.data, variable);
        
        document.getElementById('estadoInicial').style.display = 'none';
        document.getElementById('resultadosSensibilidad').style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error en cálculo: ' + error.message);
    } finally {
        actualizarProgress(100);
        setTimeout(() => mostrarSpinner(false), 300);
    }
}

/**
 * Leer parámetros fijos
 */
function leerParamsFijos() {
    return {
        T_agua: parseFloat(document.getElementById('fijoTAgua').value),
        velocidad_m_s: parseFloat(document.getElementById('fijoV').value),
        T_glucosa_inicial: parseFloat(document.getElementById('fijoTIni').value),
        T_objetivo: parseFloat(document.getElementById('fijoTObj').value),
        nivel_pct: parseFloat(document.getElementById('fijoNivel').value),
        area_m2: parseFloat(document.getElementById('fijoArea').value),
        num_descargas: parseInt(document.getElementById('fijoNumDesc').value),
        masa_por_descarga_ton: parseFloat(document.getElementById('fijoMasa').value),
        tiempo_descarga_h: 1.5,
        periodo_ciclo_h: 4.8
    };
}

/**
 * Actualizar UI con resultados
 */
function actualizarUI(data, variable) {
    const unidad = UNIDADES[variable];
    const valores = data.map(d => d.valor);
    
    // Actualizar encabezado de tabla
    document.getElementById('thVariable').textContent = `${variable} [${unidad}]`;
    
    // Renderizar gráficas
    renderizarGraficaU(valores, data, unidad);
    renderizarGraficaTiempo(valores, data, unidad);
    renderizarGraficaCapacidad(valores, data, unidad);
    renderizarGraficaTFinal(valores, data, unidad);
    
    // Renderizar tabla
    renderizarTabla(data, unidad);
}

/**
 * Renderizar gráfica de U
 */
function renderizarGraficaU(valores, data, unidadX) {
    const Uvals = data.map(d => d.U);
    
    const trace = {
        x: valores,
        y: Uvals,
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#00f0ff', width: 2 },
        marker: { size: 6, color: '#ff8c00' },
        name: 'U'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: `Variable [${unidadX}]` },
        yaxis: { ...plotlyLayout.yaxis, title: 'U [W/m²·°C]' },
        showlegend: false
    };
    
    Plotly.newPlot('graficaU', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de tiempo de calentamiento
 */
function renderizarGraficaTiempo(valores, data, unidadX) {
    const tiempos = data.map(d => d.tiempo_calentamiento_h);
    
    const trace = {
        x: valores,
        y: tiempos,
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#0096ff', width: 2 },
        marker: { size: 6 },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 150, 255, 0.12)'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: `Variable [${unidadX}]` },
        yaxis: { ...plotlyLayout.yaxis, title: 'Tiempo [h]' },
        showlegend: false
    };
    
    Plotly.newPlot('graficaTiempo', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de capacidad
 */
function renderizarGraficaCapacidad(valores, data, unidadX) {
    const caps = data.map(d => d.capacidad_ton || 0);
    const maxCap = Math.max(...caps);
    
    const trace = {
        x: valores,
        y: caps,
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#39ff14', width: 2 },
        marker: { size: 6 },
        fill: 'tozeroy',
        fillcolor: 'rgba(57, 255, 20, 0.10)'
    };
    
    // Línea de referencia a 120 ton (5 descargas x 24 ton)
    const traceRef = {
        x: [valores[0], valores[valores.length-1]],
        y: [120, 120],
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ff2a6d', width: 1, dash: 'dash' },
        name: 'Meta 120 ton'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: `Variable [${unidadX}]` },
        yaxis: { ...plotlyLayout.yaxis, title: 'Capacidad [ton/día]', range: [0, Math.max(200, maxCap * 1.1)] },
        showlegend: true,
        legend: { orientation: 'h', y: -0.2 }
    };
    
    Plotly.newPlot('graficaCapacidad', [trace, traceRef], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de T final
 */
function renderizarGraficaTFinal(valores, data, unidadX) {
    const T finals = data.map(d => d.T_final || 0);
    
    const trace = {
        x: valores,
        y: T finals,
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#ff8c00', width: 2 },
        marker: { size: 6 }
    };
    
    // Línea de referencia a 55°C
    const traceRef = {
        x: [valores[0], valores[valores.length-1]],
        y: [55, 55],
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ff2a6d', width: 1, dash: 'dash' },
        name: 'T mínima 55°C'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: `Variable [${unidadX}]` },
        yaxis: { ...plotlyLayout.yaxis, title: 'T final [°C]' },
        showlegend: true,
        legend: { orientation: 'h', y: -0.2 }
    };
    
    Plotly.newPlot('graficaTFinal', [trace, traceRef], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar tabla
 */
function renderizarTabla(data, unidad) {
    const tbody = document.getElementById('tbodySensibilidad');
    
    let html = '';
    data.forEach(d => {
        html += `<tr>
            <td class="fw-semibold">${d.valor} ${unidad}</td>
            <td>${d.U?.toFixed(2) || '—'}</td>
            <td>${d.tiempo_calentamiento_h?.toFixed(2) || '—'}</td>
            <td>${d.capacidad_ton?.toFixed(1) || '—'}</td>
            <td>${d.T_final?.toFixed(1) || '—'}</td>
        </tr>`;
    });
    
    tbody.innerHTML = html;
}

/**
 * Exportar CSV
 */
function exportarCSV() {
    if (!estadoSens.datos) return;
    
    const variable = estadoSens.variable;
    const unidad = UNIDADES[variable];
    
    let csv = `${variable} [${unidad}],U [W/m2C],tiempo_calentamiento_h,capacidad_ton,T_final_C\n`;
    estadoSens.datos.forEach(d => {
        csv += `${d.valor},${d.U || ''},${d.tiempo_calentamiento_h || ''},${d.capacidad_ton || ''},${d.T_final || ''}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sensibilidad_${variable}_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Mostrar/ocultar spinner
 */
function mostrarSpinner(mostrar) {
    document.getElementById('spinnerSens').classList.toggle('d-none', !mostrar);
    if (!mostrar) actualizarProgress(0);
}

/**
 * Actualizar barra de progreso
 */
function actualizarProgress(pct) {
    document.getElementById('progressSens').style.width = pct + '%';
}
