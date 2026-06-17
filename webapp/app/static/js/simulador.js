/**
 * Simulador de Ciclo Completo - W2605
 * Calentamiento inicial + ciclo de descargas
 */

// Layout Plotly — tema oscuro cyberpunk
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 11, color: '#e0e6ed' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    xaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, title: 'Tiempo (h)', zerolinecolor: 'rgba(0,150,255,0.2)' },
    yaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    margin: { l: 60, r: 60, t: 40, b: 50 },
    hovermode: 'x unified'
};

// Estado
let estadoSim = {
    datos: null,
    escenario: null
};

/**
 * Inicializar
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    document.getElementById('btnSimular').addEventListener('click', simular);
    document.getElementById('btnExportar').addEventListener('click', exportarCSV);
}

/**
 * Ejecutar simulación
 */
async function simular() {
    mostrarSpinner(true);
    
    try {
        const params = leerParametros();
        
        const response = await fetch('/api/calcular/ciclo-automatico', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        
        estadoSim.datos = result.data;
        
        // Actualizar UI
        actualizarKPIs(result.data);
        renderizarGraficaTyM(result.data);
        renderizarGantt(result.data);
        renderizarGraficaUyQ(result.data);
        renderizarTabla(result.data);
        
        document.getElementById('kpiResumen').style.display = 'flex';
        
    } catch (error) {
        console.error('Error en simulación:', error);
        alert('Error: ' + error.message);
    } finally {
        mostrarSpinner(false);
    }
}

/**
 * Leer parámetros del formulario
 */
function leerParametros() {
    const saltarCalentamiento = document.getElementById('saltarCalentamiento').checked;
    const T_inicial_input = parseFloat(document.getElementById('TInicial').value);
    const T_objetivo = parseFloat(document.getElementById('TObjetivo').value);
    
    // Solo permitir saltar calentamiento si T_inicial >= T_objetivo
    let T_inicial;
    if (saltarCalentamiento && T_inicial_input >= T_objetivo) {
        T_inicial = T_objetivo;
    } else {
        T_inicial = T_inicial_input;
        if (saltarCalentamiento && T_inicial_input < T_objetivo) {
            // Desmarcar checkbox y advertir al usuario
            document.getElementById('saltarCalentamiento').checked = false;
            console.warn('No se puede omitir calentamiento: T inicial (' + 
                T_inicial_input + '°C) < T objetivo (' + T_objetivo + '°C)');
        }
    }
    
    return {
        T_inicial: T_inicial,
        T_objetivo_inicio_descarga: T_objetivo,
        T_agua: parseFloat(document.getElementById('TAgua').value),
        velocidad_m_s: parseFloat(document.getElementById('VAgua').value),
        area_m2: parseFloat(document.getElementById('Area').value),
        nivel_inicial_pct: parseFloat(document.getElementById('NivelInicial').value),
        masa_por_descarga_ton: parseFloat(document.getElementById('MasaDescarga').value),
        tiempo_descarga_h: parseFloat(document.getElementById('TiempoDescarga').value),
        periodo_ciclo_h: parseFloat(document.getElementById('Periodo').value),
        temp_minima_aceptable: parseFloat(document.getElementById('TMinima').value),
        tiempo_maximo_h: 24.0
    };
}

/**
 * Actualizar KPIs de resumen
 */
function actualizarKPIs(data) {
    const m = data.metricas;
    
    document.getElementById('resTiempoCal').textContent = m.tiempo_calentamiento_inicial_h.toFixed(1);
    document.getElementById('resMasaTotal').textContent = m.masa_total_descargada_ton.toFixed(1);
    document.getElementById('resDescargasOk').textContent = m.descargas_ok;
    document.getElementById('resTotalDesc').textContent = m.descargas_calculadas;
    document.getElementById('resTFinal').textContent = m.T_final.toFixed(1);
    document.getElementById('resDescCalc').textContent = m.descargas_calculadas;
    
    // Motivo de corte
    const motivoMap = {
        'tiempo_maximo': 'Límite 24h',
        'masa_insuficiente': 'Masa agotada',
        'temperatura_baja': 'T < mínima',
        'completado': 'Completado'
    };
    document.getElementById('resMotivo').textContent = motivoMap[m.motivo_corte] || m.motivo_corte;
    
    // Color según estado
    const cardTFinal = document.getElementById('resTFinal').closest('.kpi-card-new');
    cardTFinal.classList.remove('kpi-status-ok', 'kpi-status-warn', 'kpi-status-error');
    if (m.T_final >= 55) cardTFinal.classList.add('kpi-status-ok');
    else if (m.T_final >= 50) cardTFinal.classList.add('kpi-status-warn');
    else cardTFinal.classList.add('kpi-status-error');
}

/**
 * Renderizar gráfica Temperatura y Masa vs Tiempo
 */
function renderizarGraficaTyM(data) {
    const serie = data.serie_temporal;
    const fases = data.fases;
    const T_min = parseFloat(document.getElementById('TMinima').value);
    
    const tiempo = serie.map(p => p.t_h);
    const temperatura = serie.map(p => p.T_glucosa);
    const masa = serie.map(p => p.m_ton);
    
    // Shapes para fases
    const shapes = [];
    const coloresFase = {
        'calentamiento_inicial': 'rgba(0, 150, 255, 0.10)',
        'descarga': 'rgba(255, 94, 0, 0.10)',
        'mantenimiento': 'rgba(57, 255, 20, 0.08)'
    };
    
    fases.forEach(f => {
        if (coloresFase[f.tipo]) {
            shapes.push({
                type: 'rect',
                x0: f.t_inicio_h, x1: f.t_fin_h,
                y0: 0, y1: 1, yref: 'paper',
                fillcolor: coloresFase[f.tipo],
                line: { width: 0 }, layer: 'below'
            });
        }
    });
    
    // Línea de temperatura mínima
    shapes.push({
        type: 'line',
        x0: 0, x1: 1, xref: 'paper',
        y0: T_min, y1: T_min,
        line: { color: '#ff2a6d', width: 1, dash: 'dash' }
    });
    
    const traceT = {
        x: tiempo, y: temperatura,
        type: 'scatter', mode: 'lines',
        name: 'T Glucosa (°C)',
        line: { color: '#39ff14', width: 2.5 },
        yaxis: 'y1'
    };
    
    const traceM = {
        x: tiempo, y: masa,
        type: 'scatter', mode: 'lines',
        name: 'Masa (ton)',
        line: { color: '#ff8c00', width: 2, dash: 'dash' },
        yaxis: 'y2'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, range: [0, Math.max(24, tiempo[tiempo.length-1])] },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)', side: 'left', range: [10, 80] },
        yaxis2: { title: 'Masa (ton)', side: 'right', overlaying: 'y', range: [0, 200] },
        shapes: shapes,
        annotations: [{
            x: tiempo[tiempo.length-1], y: T_min,
            text: 'T mínima', showarrow: false,
            yshift: -10, font: { size: 9, color: '#ff2a6d' }
        }],
        legend: { orientation: 'h', y: -0.2 }
    };
    
    Plotly.newPlot('graficaTyM', [traceT, traceM], layout, {responsive: true});
}

/**
 * Renderizar diagrama de Gantt
 */
function renderizarGantt(data) {
    const fases = data.fases;
    const descargas = data.descargas;
    const T_min = parseFloat(document.getElementById('TMinima').value);
    
    const tareas = [];
    const etiquetas = [];
    const colores = [];
    const textos = [];
    
    // Fase de calentamiento inicial
    const calIni = fases.find(f => f.tipo === 'calentamiento_inicial');
    if (calIni) {
        tareas.push(calIni.t_fin_h - calIni.t_inicio_h);
        etiquetas.push('🔥 Calentamiento Inicial');
        colores.push('#0096ff');
        textos.push(`${calIni.T_inicio}°C → ${calIni.T_fin}°C`);
    }
    
    // Descargas y mantenimientos
    for (let i = 0; i < descargas.length; i++) {
        const d = descargas[i];
        
        // Descarga
        tareas.push(d.t_fin_h - d.t_inicio_h);
        etiquetas.push(`🚛 Descarga ${d.descarga}`);
        colores.push(d.T_fin >= T_min ? '#39ff14' : (d.T_fin >= T_min - 5 ? '#ffaa00' : '#ff2a6d'));
        textos.push(`${d.T_inicio}°C → ${d.T_fin}°C`);
        
        // Mantenimiento (si no es la última)
        const mant = fases.find(f => f.tipo === 'mantenimiento' && f.t_inicio_h >= d.t_fin_h);
        if (mant && i < descargas.length - 1) {
            tareas.push(mant.t_fin_h - mant.t_inicio_h);
            etiquetas.push(`⏱️ Mantenimiento ${d.descarga}`);
            colores.push('#8b95a8');
            textos.push(`${mant.T_inicio}°C → ${mant.T_fin}°C`);
        }
    }
    
    const trace = {
        x: tareas,
        y: etiquetas,
        type: 'bar',
        orientation: 'h',
        marker: { color: colores },
        text: textos,
        textposition: 'inside',
        hovertemplate: '%{y}<br>Inicio: %{base:.1f}h<br>Duración: %{x:.1f}h<br>%{text}<extra></extra>'
    };
    
    // Calcular bases (acumulado)
    let base = 0;
    const bases = [];
    for (let i = 0; i < tareas.length; i++) {
        bases.push(base);
        base += tareas[i];
    }
    trace.base = bases;
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, range: [0, 24] },
        yaxis: { ...plotlyLayout.yaxis, autorange: 'reversed' },
        margin: { l: 180, r: 20, t: 20, b: 50 },
        showlegend: false
    };
    
    Plotly.newPlot('graficaGantt', [trace], layout, {responsive: true});
}

/**
 * Renderizar gráfica de U y Q
 */
function renderizarGraficaUyQ(data) {
    const serie = data.serie_temporal;
    
    const tiempo = serie.map(p => p.t_h);
    const Uvals = serie.map(p => p.U);
    const Qvals = serie.map(p => p.Q_kW);
    
    const traceU = {
        x: tiempo, y: Uvals,
        type: 'scatter', mode: 'lines',
        name: 'U (W/m²·°C)',
        line: { color: '#00f0ff', width: 2 },
        yaxis: 'y1'
    };
    
    const traceQ = {
        x: tiempo, y: Qvals,
        type: 'scatter', mode: 'lines',
        name: 'Q (kW)',
        line: { color: '#ff8c00', width: 2, dash: 'dash' },
        yaxis: 'y2'
    };
    
    const layout = {
        ...plotlyLayout,
        yaxis: { ...plotlyLayout.yaxis, title: 'U (W/m²·°C)', side: 'left' },
        yaxis2: { title: 'Q (kW)', side: 'right', overlaying: 'y' },
        legend: { orientation: 'h', y: -0.25 }
    };
    
    Plotly.newPlot('graficaUyQ', [traceU, traceQ], layout, {responsive: true});
}

/**
 * Renderizar tabla de descargas
 */
function renderizarTabla(data) {
    const descargas = data.descargas;
    const tbody = document.getElementById('tbodyDescargas');
    
    let html = '';
    descargas.forEach(d => {
        const badgeClass = d.estado === 'OK' ? 'bg-success' : 
                          (d.estado === 'Marginal' ? 'bg-warning text-dark' : 'bg-danger');
        
        html += `<tr>
            <td class="fw-bold">${d.descarga}</td>
            <td>${d.t_inicio_h.toFixed(2)}</td>
            <td>${d.t_fin_h.toFixed(2)}</td>
            <td>${d.T_inicio.toFixed(1)}</td>
            <td>${d.T_fin.toFixed(1)}</td>
            <td>${d.m_inicio_ton.toFixed(1)}</td>
            <td>${d.m_fin_ton.toFixed(1)}</td>
            <td class="fw-semibold">${d.masa_descargada_ton.toFixed(1)}</td>
            <td>${d.U_prom.toFixed(1)}</td>
            <td><span class="badge ${badgeClass}">${d.estado}</span></td>
        </tr>`;
    });
    
    tbody.innerHTML = html;
}

/**
 * Exportar CSV
 */
function exportarCSV() {
    if (!estadoSim.datos) return;
    
    const descargas = estadoSim.datos.descargas;
    const metricas = estadoSim.datos.metricas;
    
    let csv = 'Descarga,T_inicio_h,T_fin_h,T_inicial_C,T_final_C,Masa_inicio_ton,Masa_fin_ton,Descargada_ton,U_prom,Estado\n';
    descargas.forEach(d => {
        csv += `${d.descarga},${d.t_inicio_h},${d.t_fin_h},${d.T_inicio},${d.T_fin},${d.m_inicio_ton},${d.m_fin_ton},${d.masa_descargada_ton},${d.U_prom},${d.estado}\n`;
    });
    
    csv += `\nResumen del Ciclo\n`;
    csv += `Tiempo calentamiento inicial (h),${metricas.tiempo_calentamiento_inicial_h}\n`;
    csv += `Tiempo total (h),${metricas.tiempo_total_h}\n`;
    csv += `Temperatura final (°C),${metricas.T_final}\n`;
    csv += `Masa total descargada (ton),${metricas.masa_total_descargada_ton}\n`;
    csv += `Descargas OK,${metricas.descargas_ok}/${metricas.descargas_totales}\n`;
    csv += `T mínima en ciclo (°C),${metricas.T_min_ciclo}\n`;
    csv += `T promedio ciclo (°C),${metricas.T_promedio_ciclo}\n`;
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `simulacion_ciclo_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Mostrar/ocultar spinner
 */
function mostrarSpinner(mostrar) {
    document.getElementById('spinnerSim').classList.toggle('d-none', !mostrar);
}
