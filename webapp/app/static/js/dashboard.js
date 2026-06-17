/**
 * Dashboard Dinámico - W2605
 * KPIs calculados vía API, SVG animado, gráficas Plotly
 */

// Configuración de escenarios predefinidos
const ESCENARIOS = {
    '1': { T_agua: 65, v_agua: 1.34, T_inicial: 20, T_objetivo: 60, nivel_pct: 7.6, nombre: 'Escenario 1 - Volumen parcial' },
    '2': { T_agua: 65, v_agua: 2.5, T_inicial: 20, T_objetivo: 57, nivel_pct: 80, nombre: 'Escenario 2 - Caso base conservador' },
    '3': { T_agua: 75, v_agua: 2.5, T_inicial: 20, T_objetivo: 57, nivel_pct: 80, nombre: 'Escenario 3 - Optimización térmica' }
};

// Estado actual
let estadoActual = {
    escenario: '2',
    datosSimulacion: null,
    params: { ...ESCENARIOS['2'] }
};

// Layout base para Plotly
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 12 },
    paper_bgcolor: 'white',
    plot_bgcolor: '#fafafa',
    xaxis: { gridcolor: '#e0e0e0', showgrid: true },
    yaxis: { gridcolor: '#e0e0e0', showgrid: true },
    margin: { l: 60, r: 20, t: 40, b: 50 },
    legend: { orientation: 'h', y: -0.15 },
    hovermode: 'x unified'
};

/**
 * Inicializar dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    cargarEscenario('2');
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    // Selector de escenario
    document.querySelectorAll('input[name="escenario"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'custom') {
                estadoActual.escenario = 'custom';
            } else {
                cargarEscenario(e.target.value);
            }
        });
    });

    // Botón recalcular
    const btnRecalcular = document.getElementById('btnRecalcular');
    if (btnRecalcular) {
        btnRecalcular.addEventListener('click', () => {
            const esc = document.querySelector('input[name="escenario"]:checked').value;
            if (esc !== 'custom') cargarEscenario(esc);
        });
    }

    // Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
}

/**
 * Cargar escenario y ejecutar simulación completa
 */
async function cargarEscenario(idEscenario) {
    mostrarSpinner(true);
    
    try {
        const params = ESCENARIOS[idEscenario];
        estadoActual.escenario = idEscenario;
        estadoActual.params = { ...params };

        // Llamar API transitorio completo
        const response = await fetch('/api/calcular/transitorio-completo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                T_inicial: params.T_inicial,
                T_objetivo_inicio_descarga: params.T_objetivo,
                T_agua: params.T_agua,
                velocidad_m_s: params.v_agua,
                area_m2: 13.0,
                nivel_inicial_pct: params.nivel_pct,
                num_descargas: 5,
                masa_por_descarga_ton: 24,
                tiempo_descarga_h: 1.5,
                periodo_ciclo_h: 4.8,
                temp_minima_aceptable: 55
            })
        });

        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        
        estadoActual.datosSimulacion = result.data;
        
        // Actualizar UI
        await actualizarKPIs(result.data, params);
        actualizarSVGTanque(result.data, params);
        renderizarGraficaTvsT(result.data);
        renderizarGantt(result.data);
        renderizarGraficaU(result.data);

    } catch (error) {
        console.error('Error cargando escenario:', error);
        mostrarError('Error al cargar escenario: ' + error.message);
    } finally {
        mostrarSpinner(false);
    }
}

/**
 * Actualizar los 8 KPI cards
 */
async function actualizarKPIs(data, params) {
    const serie = data.serie_temporal;
    const metricas = data.metricas;
    const descargas = data.descargas;
    
    // Obtener valores calculados del punto medio del calentamiento inicial
    const T_mid = params.T_inicial + (params.T_objetivo - params.T_inicial) / 2;
    
    try {
        const respInstant = await fetch('/api/calcular/instantaneo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                temp_agua: params.T_agua,
                temp_glucosa: T_mid,
                velocidad_m_s: params.v_agua,
                area_m2: 13.0
            })
        });
        const inst = await respInstant.json();
        
        if (inst.success) {
            const d = inst.data;
            
            // KPI 1: Coeficiente U
            actualizarKPICard('kpiU', d.U, 'W/m²·°C', d.U > 30 ? 'ok' : (d.U > 20 ? 'warn' : 'error'));
            
            // KPI 2: Potencia Térmica
            actualizarKPICard('kpiQ', d.Q_kW, 'kW', d.Q_kW > 50 ? 'ok' : 'warn');
            
            // KPI 3: Tiempo Calentamiento
            const tCal = metricas.tiempo_calentamiento_inicial_h;
            actualizarKPICard('kpiTiempo', tCal.toFixed(1), 'h', tCal < 8 ? 'ok' : (tCal < 12 ? 'warn' : 'error'));
            
            // KPI 4: Capacidad Diaria
            const cap = metricas.masa_total_descargada_ton;
            actualizarKPICard('kpiCapacidad', Math.round(cap), 'ton/día', cap > 150 ? 'ok' : (cap > 120 ? 'warn' : 'error'));
            
            // KPI 5: T Final
            const Tfin = metricas.T_final;
            actualizarKPICard('kpiTFinal', Tfin.toFixed(1), '°C', Tfin >= 55 ? 'ok' : (Tfin >= 50 ? 'warn' : 'error'));
            
            // KPI 6: Masa Descargada
            actualizarKPICard('kpiMasaDesc', metricas.masa_total_descargada_ton.toFixed(1), 'ton', 'ok');
            
            // KPI 7: Eficiencia (aproximada)
            const eff = Math.min(95, (d.U / 45) * 100);
            actualizarKPICard('kpiEfic', eff.toFixed(0), '%', eff > 70 ? 'ok' : 'warn');
            
            // KPI 8: Reynolds
            const Re = d.Re;
            const reg = Re > 10000 ? 'Turbulento' : (Re > 2300 ? 'Transición' : 'Laminar');
            actualizarKPICard('kpiRe', d.Re.toFixed(0), reg, Re > 10000 ? 'ok' : (Re > 2300 ? 'warn' : 'error'));
        }
    } catch (e) {
        console.error('Error obteniendo valores instantáneos:', e);
    }
}

/**
 * Actualizar un KPI card individual
 */
function actualizarKPICard(id, valor, unidad, estado) {
    const card = document.getElementById(id + 'Card');
    const valEl = document.getElementById(id + 'Val');
    const unitEl = card.querySelector('.kpi-unit');
    
    if (valEl) valEl.textContent = valor;
    if (unitEl) unitEl.textContent = unidad;
    
    // Estado visual
    card.classList.remove('kpi-status-ok', 'kpi-status-warn', 'kpi-status-error');
    card.classList.add('kpi-status-' + estado);
}

/**
 * Actualizar SVG del tanque
 */
function actualizarSVGTanque(data, params) {
    const serie = data.serie_temporal;
    const puntoActual = serie[0];  // Condiciones iniciales del tanque
    
    const nivel_pct = params.nivel_pct;
    const temp = puntoActual.T_glucosa;
    const masa = puntoActual.m_ton;
    
    // Calcular color según temperatura (azul 210° → naranja 30°)
    const t_norm = Math.max(0, Math.min(1, (temp - 15) / 55));
    const hue = Math.round(210 - t_norm * 180);
    const color = `hsl(${hue}, 80%, 55%)`;
    
    // Actualizar nivel (rectángulo de relleno)
    const nivelRect = document.getElementById('nivelRect');
    const nivelFondo = document.getElementById('nivelFondo');
    
    // Altura del cilindro: 225 unidades, desde y=70
    const alturaCilindro = 225;
    const yBase = 295;  // Base del cilindro
    const alturaLleno = alturaCilindro * (nivel_pct / 100);
    const yNivel = yBase - alturaLleno;
    
    if (nivelRect) {
        nivelRect.setAttribute('y', yNivel);
        nivelRect.setAttribute('height', alturaLleno);
        nivelRect.setAttribute('fill', color);
    }
    if (nivelFondo) {
        nivelFondo.setAttribute('fill', color);
    }
    
    // Actualizar textos
    const svgNivel = document.getElementById('svgNivelPct');
    const svgTemp = document.getElementById('svgTemp');
    const svgMasa = document.getElementById('svgMasa');
    
    if (svgNivel) svgNivel.textContent = nivel_pct.toFixed(0) + '%';
    if (svgTemp) svgTemp.textContent = temp.toFixed(1) + ' °C';
    if (svgMasa) svgMasa.textContent = masa.toFixed(1) + ' ton';
}

/**
 * Renderizar gráfica Temperatura vs Tiempo
 */
function renderizarGraficaTvsT(data) {
    const serie = data.serie_temporal;
    const fases = data.fases;
    
    const tiempo = serie.map(p => p.t_h);
    const temperatura = serie.map(p => p.T_glucosa);
    
    // Shapes para fases
    const shapes = [];
    const colores = {
        'calentamiento_inicial': 'rgba(33, 150, 243, 0.15)',
        'descarga': 'rgba(255, 87, 34, 0.15)',
        'mantenimiento': 'rgba(76, 175, 80, 0.1)'
    };
    
    fases.forEach(f => {
        if (colores[f.tipo]) {
            shapes.push({
                type: 'rect',
                x0: f.t_inicio_h,
                x1: f.t_fin_h,
                y0: 0,
                y1: 1,
                yref: 'paper',
                fillcolor: colores[f.tipo],
                line: { width: 0 },
                layer: 'below'
            });
        }
    });
    
    const trace = {
        x: tiempo,
        y: temperatura,
        type: 'scatter',
        mode: 'lines',
        name: 'T Glucosa',
        line: { color: '#1a3a6c', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(26, 58, 108, 0.05)'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)', range: [0, Math.max(24, tiempo[tiempo.length-1])] },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)', range: [15, 80] },
        shapes: shapes,
        annotations: [{
            x: 0.5, y: 1.1, xref: 'paper', yref: 'paper',
            text: estadoActual.params.nombre,
            showarrow: false, font: { size: 12, color: '#666' }
        }]
    };
    
    Plotly.newPlot('graficaTvsT', [trace], layout, {responsive: true});
}

/**
 * Renderizar diagrama de Gantt
 */
function renderizarGantt(data) {
    const fases = data.fases;
    const descargas = data.descargas;
    
    const tareas = [];
    
    // Fase de calentamiento inicial
    const calIni = fases.find(f => f.tipo === 'calentamiento_inicial');
    if (calIni) {
        tareas.push({
            x: [calIni.t_fin_h - calIni.t_inicio_h],
            y: ['Calentamiento Inicial'],
            base: [calIni.t_inicio_h],
            type: 'bar',
            orientation: 'h',
            marker: { color: '#2196F3' },
            text: [`${calIni.T_inicio}°C → ${calIni.T_fin}°C`],
            textposition: 'inside',
            hovertemplate: 'Inicio: %{base:.1f}h<br>Duración: %{x:.1f}h<br>T: %{text}<extra></extra>'
        });
    }
    
    // Descargas
    descargas.forEach((d, i) => {
        tareas.push({
            x: [d.t_fin_h - d.t_inicio_h],
            y: [`Descarga ${d.descarga}`],
            base: [d.t_inicio_h],
            type: 'bar',
            orientation: 'h',
            marker: { color: d.T_fin >= 55 ? '#4CAF50' : (d.T_fin >= 50 ? '#FFC107' : '#F44336') },
            text: [`${d.T_inicio}°C → ${d.T_fin}°C`],
            textposition: 'inside',
            hovertemplate: `Descarga ${d.descarga}<br>Inicio: %{base:.1f}h<br>Duración: %{x:.1f}h<br>Masa: ${d.masa_descargada_ton} ton<extra></extra>`
        });
    });
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)', range: [0, 24] },
        yaxis: { ...plotlyLayout.yaxis, autorange: 'reversed' },
        showlegend: false,
        margin: { l: 140, r: 20, t: 30, b: 50 }
    };
    
    Plotly.newPlot('graficaGantt', tareas, layout, {responsive: true});
}

/**
 * Renderizar evolución del coeficiente U
 */
function renderizarGraficaU(data) {
    const serie = data.serie_temporal;
    
    const tiempo = serie.map(p => p.t_h);
    const Uvals = serie.map(p => p.U);
    const Qvals = serie.map(p => p.Q_kW);
    
    const traceU = {
        x: tiempo,
        y: Uvals,
        type: 'scatter',
        mode: 'lines',
        name: 'U (W/m²·°C)',
        line: { color: '#1a3a6c', width: 2 },
        yaxis: 'y1'
    };
    
    const traceQ = {
        x: tiempo,
        y: Qvals,
        type: 'scatter',
        mode: 'lines',
        name: 'Q (kW)',
        line: { color: '#e8750a', width: 2, dash: 'dash' },
        yaxis: 'y2'
    };
    
    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)' },
        yaxis: { ...plotlyLayout.yaxis, title: 'U (W/m²·°C)', side: 'left', range: [0, Math.max(...Uvals) * 1.1] },
        yaxis2: { title: 'Q (kW)', side: 'right', overlaying: 'y', range: [0, Math.max(...Qvals) * 1.1] },
        showlegend: true,
        legend: { orientation: 'h', y: -0.2 }
    };
    
    Plotly.newPlot('graficaU', [traceU, traceQ], layout, {responsive: true});
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
    // Usar toast si está disponible, si no, alert
    if (typeof showToast === 'function') {
        showToast(mensaje, 'danger');
    } else {
        alert(mensaje);
    }
}
