/**
 * JavaScript del Dashboard - P2611
 */

// Datos del dashboard
let datosDashboard = {
    propiedades: [],
    capacidad: null
};

/**
 * Inicializar dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    cargarDatosDashboard();
    
    // Evento cambio de escenario
    const selectEscenario = document.getElementById('selectEscenarioGraf');
    if (selectEscenario) {
        selectEscenario.addEventListener('change', function() {
            actualizarGraficoEscenario(this.value);
        });
    }
});

/**
 * Cargar todos los datos del dashboard
 */
async function cargarDatosDashboard() {
    try {
        // Cargar tabla de propiedades
        const propsResponse = await fetchAPI('/api/calcular/tabla-propiedades?temp_min=20&temp_max=80&paso=5');
        datosDashboard.propiedades = propsResponse.data;
        actualizarTablaPropiedades(datosDashboard.propiedades);
        
        // Cargar capacidad del tanque
        const capResponse = await fetchAPI('/api/calcular/capacidad-tanque');
        datosDashboard.capacidad = capResponse.data;
        actualizarInfoTanque(datosDashboard.capacidad);
        
        // Cargar gráficos iniciales
        await cargarGraficosIniciales();
        
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        showToast('Error cargando datos del dashboard', 'danger');
    }
}

/**
 * Actualizar tabla de propiedades
 */
function actualizarTablaPropiedades(data) {
    const tbody = document.getElementById('tbodyPropiedades');
    if (!tbody) return;
    
    tbody.innerHTML = data.map(row => `
        <tr>
            <td class="fw-bold">${row.temperatura_c}</td>
            <td>${row.rho_glucosa}</td>
            <td>${formatNumber(row.mu_glucosa_cP, 1)}</td>
            <td>${row.cp_glucosa}</td>
            <td>${row.k_glucosa}</td>
            <td>${formatNumber(row.Pr_glucosa, 0)}</td>
        </tr>
    `).join('');
}

/**
 * Actualizar info del tanque
 */
function actualizarInfoTanque(data) {
    document.getElementById('volTotal').textContent = data.volumen_total_m3;
    document.getElementById('cap80').textContent = data.masa_80pct_ton;
}

/**
 * Cargar gráficos iniciales
 */
async function cargarGraficosIniciales() {
    // Gráfico de temperatura (Escenario 2 por defecto)
    await actualizarGraficoEscenario('2');
    
    // Gráfico de distribución de energía
    crearGraficoDistribucion();
    
    // Gráfico comparativo
    crearGraficoComparativo();
    
    // Gráfico radar
    crearGraficoRadar();
}

/**
 * Actualizar gráfico de temperatura según escenario
 */
async function actualizarGraficoEscenario(escenario) {
    const tempAgua = escenario === '2' ? 65 : 75;
    
    try {
        const response = await fetchAPI('/api/simular/ciclo-descargas', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: 57,
                temp_agua: tempAgua,
                num_descargas: 8,
                masa_por_descarga_ton: 24,
                tiempo_descarga_h: 1.5,
                nivel_inicial_pct: 80
            })
        });
        
        const serie = response.data.serie_temporal;
        const descargas = response.data.descargas;
        
        const tiempo = serie.map(p => p.t_h);
        const temperatura = serie.map(p => p.T_glucosa);
        
        // Shapes para descargas
        const shapes = descargas.map(d => ({
            type: 'rect',
            x0: d.t_inicio_h,
            x1: d.t_fin_h,
            y0: 0,
            y1: 1,
            yref: 'paper',
            fillcolor: 'rgba(255, 193, 7, 0.3)',
            line: { width: 0 },
            layer: 'below'
        }));
        
        const trace = {
            x: tiempo,
            y: temperatura,
            type: 'scatter',
            mode: 'lines',
            name: 'Temperatura Glucosa',
            line: { color: '#0d6efd', width: 2.5 },
            fill: 'tozeroy',
            fillcolor: 'rgba(13, 110, 253, 0.1)'
        };
        
        const layout = {
            xaxis: { 
                title: 'Tiempo (h)',
                gridcolor: '#e9ecef',
                range: [0, 24]
            },
            yaxis: { 
                title: 'Temperatura (°C)',
                gridcolor: '#e9ecef',
                range: [55, 75]
            },
            shapes: shapes,
            showlegend: false,
            margin: { t: 20, r: 20, b: 50, l: 60 },
            annotations: [{
                x: 0.5,
                y: 1.1,
                xref: 'paper',
                yref: 'paper',
                text: `Escenario ${escenario}: Agua a ${tempAgua}°C`,
                showarrow: false,
                font: { size: 14, weight: 'bold' }
            }]
        };
        
        createPlotlyChart('dashGraficoTemp', [trace], layout);
        
    } catch (error) {
        console.error('Error cargando gráfico:', error);
    }
}

/**
 * Crear gráfico de distribución de energía (pie)
 */
function crearGraficoDistribucion() {
    const data = [{
        values: [65, 25, 10],
        labels: ['Calor útil (glucosa)', 'Pérdidas pared', 'Pérdidas aislamiento'],
        type: 'pie',
        marker: {
            colors: ['#198754', '#ffc107', '#dc3545']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    }];
    
    const layout = {
        showlegend: true,
        legend: { orientation: 'h', y: -0.1 },
        margin: { t: 20, r: 20, b: 60, l: 20 }
    };
    
    createPlotlyChart('dashGraficoPie', data, layout);
}

/**
 * Crear gráfico comparativo de escenarios
 */
async function crearGraficoComparativo() {
    try {
        const response = await fetchAPI('/api/simular/comparar-escenarios', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: 57,
                num_descargas: 8
            })
        });
        
        const data = response.data;
        
        const trace1 = {
            x: ['Temp Final (°C)', 'U Promedio', 'Masa Final (ton)'],
            y: [
                data.escenario_2_65C.temp_final, 
                data.escenario_2_65C.U_promedio,
                data.escenario_2_65C.masa_final_ton
            ],
            type: 'bar',
            name: 'Escenario 2 (65°C)',
            marker: { color: '#0d6efd' }
        };
        
        const trace2 = {
            x: ['Temp Final (°C)', 'U Promedio', 'Masa Final (ton)'],
            y: [
                data.escenario_3_75C.temp_final,
                data.escenario_3_75C.U_promedio,
                data.escenario_3_75C.masa_final_ton
            ],
            type: 'bar',
            name: 'Escenario 3 (75°C)',
            marker: { color: '#ffc107' }
        };
        
        const layout = {
            barmode: 'group',
            xaxis: { title: '' },
            yaxis: { title: 'Valor' },
            legend: { orientation: 'h', y: -0.2 },
            margin: { t: 20, r: 20, b: 80, l: 60 }
        };
        
        createPlotlyChart('dashGraficoComp', [trace1, trace2], layout);
        
    } catch (error) {
        console.error('Error en comparativo:', error);
    }
}

/**
 * Crear gráfico radar de parámetros
 */
function crearGraficoRadar() {
    const data = [{
        type: 'scatterpolar',
        r: [80, 65, 90, 75, 85, 80],
        theta: ['Eficiencia', 'U', 'ΔT', 'Flujo', 'Tiempo', 'Eficiencia'],
        fill: 'toself',
        name: 'Actual',
        line: { color: '#0d6efd' },
        fillcolor: 'rgba(13, 110, 253, 0.3)'
    }, {
        type: 'scatterpolar',
        r: [90, 80, 95, 85, 90, 90],
        theta: ['Eficiencia', 'U', 'ΔT', 'Flujo', 'Tiempo', 'Eficiencia'],
        fill: 'toself',
        name: 'Óptimo',
        line: { color: '#198754' },
        fillcolor: 'rgba(25, 135, 84, 0.2)'
    }];
    
    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 100]
            }
        },
        showlegend: true,
        legend: { orientation: 'h', y: -0.1 },
        margin: { t: 40, r: 40, b: 60, l: 40 }
    };
    
    createPlotlyChart('dashGraficoRadar', data, layout);
}

/**
 * Exportar tabla
 */
function exportarTabla(tipo) {
    if (tipo === 'propiedades' && datosDashboard.propiedades) {
        const csvContent = convertToCSV(datosDashboard.propiedades);
        const blob = new Blob([csvContent], { type: 'text/csv' });
        downloadFile(blob, 'propiedades_termofisicas_p2611.csv');
        showToast('Tabla exportada', 'success');
    }
}

/**
 * Convertir datos a CSV
 */
function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(row => headers.map(h => row[h]).join(','));
    
    return [headers.join(','), ...rows].join('\n');
}
