/**
 * JavaScript del Módulo Simulador - P2611
 */

// Variables globales
let resultadosSimulacion = null;
let vistaActual = 'temp';

/**
 * Inicializar módulo simulador
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('simuladorForm');
    const btnComparar = document.getElementById('btnComparar');
    const btnExportar = document.getElementById('btnExportarSim');
    const sliderNivel = document.getElementById('nivelInicial');
    
    if (form) {
        form.addEventListener('submit', handleSimular);
    }
    
    if (btnComparar) {
        btnComparar.addEventListener('click', handleComparar);
    }
    
    if (btnExportar) {
        btnExportar.addEventListener('click', handleExportarSim);
    }
    
    if (sliderNivel) {
        sliderNivel.addEventListener('input', function() {
            document.getElementById('nivelInicialValor').textContent = this.value + '%';
        });
    }
});

/**
 * Manejar simulación
 */
async function handleSimular(e) {
    e.preventDefault();
    
    const tempAgua = parseFloat(document.getElementById('tempAguaSim').value);
    const tempInicial = parseFloat(document.getElementById('tempInicialSim').value);
    const numDescargas = parseInt(document.getElementById('numDescargas').value);
    const masaDescarga = parseFloat(document.getElementById('masaDescarga').value);
    const tiempoDescarga = parseFloat(document.getElementById('tiempoDescarga').value);
    const nivelInicial = parseFloat(document.getElementById('nivelInicial').value);
    
    showLoading('graficoCiclo');
    
    try {
        // 1. Calcular capacidad
        const responseCap = await fetchAPI('/api/simular/capacidad', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: tempInicial,
                temp_agua: tempAgua,
                num_descargas: numDescargas,
                masa_por_descarga_ton: masaDescarga,
                tiempo_descarga_h: tiempoDescarga,
                nivel_inicial_pct: nivelInicial
            })
        });
        
        // 2. Simular ciclo completo
        const responseCiclo = await fetchAPI('/api/simular/ciclo-descargas', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: tempInicial,
                temp_agua: tempAgua,
                num_descargas: numDescargas,
                masa_por_descarga_ton: masaDescarga,
                tiempo_descarga_h: tiempoDescarga,
                nivel_inicial_pct: nivelInicial,
                periodo_ciclo_h: 3.0
            })
        });
        
        resultadosSimulacion = {
            capacidad: responseCap.data,
            ciclo: responseCiclo.data
        };
        
        // Actualizar UI
        actualizarKPISim(resultadosSimulacion);
        actualizarGraficoCiclo(resultadosSimulacion.ciclo);
        actualizarGantt(resultadosSimulacion.ciclo);
        actualizarTablaDescargas(resultadosSimulacion.ciclo);
        
        showToast('Simulación completada', 'success');
        
    } catch (error) {
        console.error('Error en simulación:', error);
        document.getElementById('graficoCiclo').innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Error: ${error.message}
            </div>
        `;
    }
}

/**
 * Actualizar KPIs del simulador
 */
function actualizarKPISim(data) {
    document.getElementById('kpiCapacidad').textContent = data.capacidad.capacidad_maxima_ton_dia || '-';
    document.getElementById('kpiDescargasDia').textContent = data.capacidad.descargas_por_dia || '-';
    document.getElementById('kpiFlujo').textContent = formatNumber(data.capacidad.flujo_maximo_ton_h, 1);
    document.getElementById('kpiTempFinal').textContent = formatNumber(data.ciclo.temp_final, 1);
    
    document.getElementById('resultadosSimCards').style.display = 'flex';
}

/**
 * Actualizar gráfico principal del ciclo
 */
function actualizarGraficoCiclo(data) {
    const serie = data.serie_temporal;
    const tiempo = serie.map(p => p.t_h);
    const temperatura = serie.map(p => p.T_glucosa);
    const masa = serie.map(p => p.m_ton);
    const U = serie.map(p => p.U);
    
    // Encontrar fases de descarga para sombreado
    const descargas = data.descargas;
    const shapes = descargas.map(d => ({
        type: 'rect',
        x0: d.t_inicio_h,
        x1: d.t_fin_h,
        y0: 0,
        y1: 1,
        yref: 'paper',
        fillcolor: 'rgba(255, 193, 7, 0.2)',
        line: { width: 0 },
        layer: 'below'
    }));
    
    // Anotaciones de descargas
    const annotations = descargas.map(d => ({
        x: (d.t_inicio_h + d.t_fin_h) / 2,
        y: 1.05,
        yref: 'paper',
        text: `D${d.descarga}`,
        showarrow: false,
        font: { size: 10, color: '#856404' }
    }));
    
    let trace, yaxis;
    
    switch(vistaActual) {
        case 'temp':
            trace = {
                x: tiempo,
                y: temperatura,
                type: 'scatter',
                mode: 'lines',
                name: 'Temperatura',
                line: { color: '#0d6efd', width: 2 }
            };
            yaxis = { title: 'Temperatura (°C)', range: [50, 80] };
            break;
        case 'masa':
            trace = {
                x: tiempo,
                y: masa,
                type: 'scatter',
                mode: 'lines',
                name: 'Masa',
                line: { color: '#198754', width: 2 },
                fill: 'tozeroy'
            };
            yaxis = { title: 'Masa (ton)' };
            break;
        case 'U':
            trace = {
                x: tiempo,
                y: U,
                type: 'scatter',
                mode: 'lines',
                name: 'Coef. U',
                line: { color: '#6f42c1', width: 2 }
            };
            yaxis = { title: 'U (W/m²·°C)' };
            break;
    }
    
    const layout = {
        xaxis: { title: 'Tiempo (h)', gridcolor: '#e9ecef' },
        yaxis: { ...yaxis, gridcolor: '#e9ecef' },
        shapes: shapes,
        annotations: annotations,
        showlegend: false,
        margin: { t: 40, r: 40, b: 60, l: 60 },
        hovermode: 'x unified'
    };
    
    createPlotlyChart('graficoCiclo', [trace], layout);
}

/**
 * Cambiar vista del gráfico
 */
function cambiarVistaGrafico(vista) {
    vistaActual = vista;
    
    // Actualizar botones
    document.getElementById('btnVerTemp').classList.toggle('active', vista === 'temp');
    document.getElementById('btnVerMasa').classList.toggle('active', vista === 'masa');
    document.getElementById('btnVerU').classList.toggle('active', vista === 'U');
    
    if (resultadosSimulacion) {
        actualizarGraficoCiclo(resultadosSimulacion.ciclo);
    }
}

/**
 * Actualizar gráfico de Gantt
 */
function actualizarGantt(data) {
    const fases = data.fases;
    
    const traces = fases.map((fase, i) => ({
        x: [fase.t_fin_h - fase.t_inicio_h],
        y: [fase.tipo === 'descarga' ? 'Descarga' : 'Calentamiento'],
        type: 'bar',
        orientation: 'h',
        base: [fase.t_inicio_h],
        name: fase.tipo === 'descarga' ? `Descarga ${fase.descarga_num}` : `Calentamiento ${i}`,
        marker: {
            color: fase.tipo === 'descarga' ? '#ffc107' : '#0d6efd'
        },
        showlegend: false
    }));
    
    const layout = {
        xaxis: { title: 'Tiempo (h)', range: [0, data.tiempo_total_h] },
        yaxis: { title: '' },
        barmode: 'stack',
        margin: { t: 20, r: 20, b: 60, l: 100 }
    };
    
    createPlotlyChart('graficoGantt', traces, layout);
    document.getElementById('cardGantt').style.display = 'block';
}

/**
 * Actualizar tabla de descargas
 */
function actualizarTablaDescargas(data) {
    const tbody = document.getElementById('tbodyDescargas');
    
    tbody.innerHTML = data.descargas.map(d => `
        <tr>
            <td class="fw-bold">${d.descarga}</td>
            <td>${formatNumber(d.t_inicio_h, 2)}</td>
            <td>${formatNumber(d.t_fin_h, 2)}</td>
            <td>${formatNumber(d.T_inicio, 2)}</td>
            <td>${formatNumber(d.T_fin, 2)}</td>
            <td>${formatNumber(d.m_inicio_kg / 1000, 2)}</td>
            <td>${formatNumber(d.m_fin_kg / 1000, 2)}</td>
            <td class="fw-bold text-success">${formatNumber(d.masa_descargada_kg / 1000, 2)}</td>
        </tr>
    `).join('');
    
    document.getElementById('tablaDescargas').style.display = 'table';
    document.getElementById('mensajeInicialSim').style.display = 'none';
    document.getElementById('btnExportarSim').style.display = 'inline-block';
}

/**
 * Comparar escenarios
 */
async function handleComparar() {
    const tempInicial = parseFloat(document.getElementById('tempInicialSim').value);
    const numDescargas = parseInt(document.getElementById('numDescargas').value);
    
    showLoading('graficoComparacion');
    
    try {
        const response = await fetchAPI('/api/simular/comparar-escenarios', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: tempInicial,
                num_descargas: numDescargas
            })
        });
        
        const data = response.data;
        
        // Gráfico de comparación
        const trace1 = {
            x: ['Temp Final', 'U Promedio', 'Masa Final'],
            y: [data.escenario_2_65C.temp_final, data.escenario_2_65C.U_promedio, 
                data.escenario_2_65C.masa_final_ton],
            type: 'bar',
            name: 'Escenario 2 (65°C)',
            marker: { color: '#0d6efd' }
        };
        
        const trace2 = {
            x: ['Temp Final', 'U Promedio', 'Masa Final'],
            y: [data.escenario_3_75C.temp_final, data.escenario_3_75C.U_promedio,
                data.escenario_3_75C.masa_final_ton],
            type: 'bar',
            name: 'Escenario 3 (75°C)',
            marker: { color: '#ffc107' }
        };
        
        const layout = {
            barmode: 'group',
            xaxis: { title: 'Parámetro' },
            yaxis: { title: 'Valor' },
            margin: { t: 40, r: 40, b: 60, l: 60 }
        };
        
        createPlotlyChart('graficoComparacion', [trace1, trace2], layout);
        
        // Tabla de comparación
        const tbody = document.getElementById('tbodyComparacion');
        tbody.innerHTML = `
            <tr>
                <td>Temperatura Final</td>
                <td>${formatNumber(data.escenario_2_65C.temp_final, 2)} °C</td>
                <td>${formatNumber(data.escenario_3_75C.temp_final, 2)} °C</td>
                <td class="text-success">+${formatNumber(data.comparacion.mejora_temp_final, 2)} °C</td>
            </tr>
            <tr>
                <td>U Promedio</td>
                <td>${formatNumber(data.escenario_2_65C.U_promedio, 2)} W/m²·°C</td>
                <td>${formatNumber(data.escenario_3_75C.U_promedio, 2)} W/m²·°C</td>
                <td class="text-success">+${formatNumber(data.comparacion.mejora_U_promedio, 2)}</td>
            </tr>
            <tr>
                <td>Masa Final</td>
                <td>${formatNumber(data.escenario_2_65C.masa_final_ton, 2)} ton</td>
                <td>${formatNumber(data.escenario_3_75C.masa_final_ton, 2)} ton</td>
                <td>-</td>
            </tr>
        `;
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('modalComparacion'));
        modal.show();
        
    } catch (error) {
        showToast('Error en comparación: ' + error.message, 'danger');
    }
}

/**
 * Exportar simulación
 */
function handleExportarSim() {
    if (!resultadosSimulacion) return;
    
    const datosExportar = {
        parametros: {
            temp_agua: document.getElementById('tempAguaSim').value,
            temp_inicial: document.getElementById('tempInicialSim').value,
            num_descargas: document.getElementById('numDescargas').value,
            masa_descarga: document.getElementById('masaDescarga').value
        },
        capacidad: resultadosSimulacion.capacidad,
        descargas: resultadosSimulacion.ciclo.descargas,
        serie_temporal: resultadosSimulacion.ciclo.serie_temporal
    };
    
    fetchAPI('/api/exportar/excel', {
        method: 'POST',
        body: JSON.stringify({
            serie_temporal: datosExportar.serie_temporal,
            descargas: datosExportar.descargas,
            filename: 'simulacion_p2611.xlsx'
        })
    }).then(response => {
        // La respuesta es un blob para descargar
        return fetch('/api/exportar/excel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                serie_temporal: datosExportar.serie_temporal,
                descargas: datosExportar.descargas,
                filename: 'simulacion_p2611.xlsx'
            })
        });
    }).then(response => response.blob())
    .then(blob => {
        downloadFile(blob, 'simulacion_p2611.xlsx');
        showToast('Archivo exportado', 'success');
    });
}

/**
 * Cargar escenario predefinido
 */
function cargarEscenarioSim(num) {
    if (num === 2) {
        document.getElementById('tempAguaSim').value = 65;
        document.getElementById('tempInicialSim').value = 57;
    } else if (num === 3) {
        document.getElementById('tempAguaSim').value = 75;
        document.getElementById('tempInicialSim').value = 57;
    }
    
    showToast(`Escenario ${num} cargado`, 'info');
}
