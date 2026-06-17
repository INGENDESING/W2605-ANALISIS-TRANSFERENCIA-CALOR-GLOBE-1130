/**
 * Propiedades Termofísicas - W2605
 * Glucosa Globe 1130 (85 Brix)
 */

// Layout Plotly — tema oscuro cyberpunk
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 10, color: '#e0e6ed' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    xaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, title: 'T (°C)', zerolinecolor: 'rgba(0,150,255,0.2)' },
    yaxis: { gridcolor: 'rgba(0,150,255,0.12)', showgrid: true, zerolinecolor: 'rgba(0,150,255,0.2)' },
    margin: { l: 50, r: 20, t: 20, b: 40 },
    hovermode: 'x unified',
    showlegend: false
};

// Estado
let estadoProps = {
    datos: null,
    shapesCursor: []
};

/**
 * Inicializar
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    cargarDatos();
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    document.getElementById('btnActualizarProps').addEventListener('click', cargarDatos);
    document.getElementById('btnExportarProps').addEventListener('click', exportarCSV);
    document.getElementById('tempCursor').addEventListener('change', actualizarCursor);
    
    // Actualizar cursor al hacer click en gráficas
    ['graficaRho', 'graficaMu', 'graficaCp', 'graficaK'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.on('plotly_click', function(data) {
                const temp = data.points[0].x;
                document.getElementById('tempCursor').value = temp;
                actualizarCursor();
            });
        }
    });
}

/**
 * Cargar datos de propiedades
 */
async function cargarDatos() {
    const tempMin = parseFloat(document.getElementById('tempMin').value);
    const tempMax = parseFloat(document.getElementById('tempMax').value);
    const paso = parseFloat(document.getElementById('tempPaso').value);
    
    try {
        const response = await fetch(`/api/propiedades-glucosa?temp_min=${tempMin}&temp_max=${tempMax}&paso=${paso}`);
        const result = await response.json();
        
        if (!result.success) throw new Error(result.error);
        
        estadoProps.datos = result.data;
        
        actualizarUI(result.data);
        actualizarCursor();
        
    } catch (error) {
        console.error('Error cargando propiedades:', error);
        alert('Error cargando datos: ' + error.message);
    }
}

/**
 * Actualizar UI
 */
function actualizarUI(data) {
    renderizarGraficaRho(data);
    renderizarGraficaMu(data);
    renderizarGraficaCp(data);
    renderizarGraficaK(data);
    renderizarTabla(data);
}

/**
 * Renderizar gráfica de densidad
 */
function renderizarGraficaRho(data) {
    const temps = data.map(d => d.temperatura_c);
    const rhos = data.map(d => d.rho_glucosa);
    
    const trace = {
        x: temps,
        y: rhos,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#00f0ff', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 240, 255, 0.10)',
        name: 'ρ'
    };
    
    const layout = {
        ...plotlyLayout,
        yaxis: { ...plotlyLayout.yaxis, title: 'ρ [kg/m³]', range: [1400, 1500] }
    };
    
    Plotly.newPlot('graficaRho', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de viscosidad
 */
function renderizarGraficaMu(data) {
    const temps = data.map(d => d.temperatura_c);
    const mus = data.map(d => d.mu_glucosa_cP);
    
    const trace = {
        x: temps,
        y: mus,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ff8c00', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(255, 140, 0, 0.12)',
        name: 'μ'
    };
    
    const layout = {
        ...plotlyLayout,
        yaxis: { ...plotlyLayout.yaxis, title: 'μ [cP]', type: 'log', range: [0, 3] } // 1 a 1000 cP
    };
    
    Plotly.newPlot('graficaMu', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de Cp
 */
function renderizarGraficaCp(data) {
    const temps = data.map(d => d.temperatura_c);
    const cps = data.map(d => d.cp_glucosa);
    
    const trace = {
        x: temps,
        y: cps,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#39ff14', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(57, 255, 20, 0.10)',
        name: 'Cp'
    };
    
    const layout = {
        ...plotlyLayout,
        yaxis: { ...plotlyLayout.yaxis, title: 'Cp [J/kg·K]', range: [2400, 2800] }
    };
    
    Plotly.newPlot('graficaCp', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar gráfica de k
 */
function renderizarGraficaK(data) {
    const temps = data.map(d => d.temperatura_c);
    const ks = data.map(d => d.k_glucosa);
    
    const trace = {
        x: temps,
        y: ks,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#0096ff', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 150, 255, 0.12)',
        name: 'k'
    };
    
    const layout = {
        ...plotlyLayout,
        yaxis: { ...plotlyLayout.yaxis, title: 'k [W/m·K]', range: [0.3, 0.4] }
    };
    
    Plotly.newPlot('graficaK', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Renderizar tabla
 */
function renderizarTabla(data) {
    const tbody = document.getElementById('tbodyPropiedades');
    
    let html = '';
    data.forEach(d => {
        html += `<tr>
            <td class="fw-semibold">${d.temperatura_c}</td>
            <td>${d.rho_glucosa.toFixed(1)}</td>
            <td>${d.mu_glucosa_Pa_s.toExponential(3)}</td>
            <td>${d.mu_glucosa_cP.toFixed(1)}</td>
            <td>${d.cp_glucosa.toFixed(0)}</td>
            <td>${d.k_glucosa.toFixed(4)}</td>
            <td>${d.Pr_glucosa.toFixed(0)}</td>
        </tr>`;
    });
    
    tbody.innerHTML = html;
}

/**
 * Actualizar valores del cursor
 */
async function actualizarCursor() {
    const temp = parseFloat(document.getElementById('tempCursor').value);
    
    try {
        // Buscar en datos existentes o hacer petición
        let dato = null;
        if (estadoProps.datos) {
            dato = estadoProps.datos.find(d => Math.abs(d.temperatura_c - temp) < 0.5);
        }
        
        // Si no está, hacer petición específica
        if (!dato) {
            const response = await fetch(`/api/propiedades-glucosa?temp_min=${temp}&temp_max=${temp}&paso=1`);
            const result = await response.json();
            if (result.success && result.data.length > 0) {
                dato = result.data[0];
            }
        }
        
        if (dato) {
            document.getElementById('valRho').textContent = dato.rho_glucosa.toFixed(0);
            document.getElementById('valMu').textContent = dato.mu_glucosa_Pa_s.toExponential(2);
            document.getElementById('valCp').textContent = dato.cp_glucosa.toFixed(0);
            document.getElementById('valK').textContent = dato.k_glucosa.toFixed(4);
            document.getElementById('valPr').textContent = dato.Pr_glucosa.toFixed(0);
            
            // Actualizar líneas verticales en gráficas
            actualizarLineasCursor(temp);
        }
        
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Actualizar líneas verticales en todas las gráficas
 */
function actualizarLineasCursor(temp) {
    const shape = {
        type: 'line',
        x0: temp, x1: temp,
        y0: 0, y1: 1, yref: 'paper',
        line: { color: '#ff2a6d', width: 2, dash: 'dash' }
    };
    
    ['graficaRho', 'graficaMu', 'graficaCp', 'graficaK'].forEach(id => {
        const el = document.getElementById(id);
        if (el && el.data) {
            Plotly.relayout(id, { shapes: [shape] });
        }
    });
}

/**
 * Exportar CSV
 */
function exportarCSV() {
    if (!estadoProps.datos) return;
    
    let csv = 'temperatura_C,rho_kg_m3,mu_Pa_s,mu_cP,Cp_J_kg_K,k_W_m_K,Pr\n';
    estadoProps.datos.forEach(d => {
        csv += `${d.temperatura_c},${d.rho_glucosa},${d.mu_glucosa_Pa_s},${d.mu_glucosa_cP},${d.cp_glucosa},${d.k_glucosa},${d.Pr_glucosa}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `propiedades_glucosa_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}
