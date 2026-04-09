/**
 * JavaScript del Módulo Calculadora - P2611
 */

// Variables globales para resultados actuales
let resultadosActuales = null;
let serieTemporalActual = null;

/**
 * Inicializar módulo calculadora
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('calculadoraForm');
    const btnReset = document.getElementById('btnReset');
    const btnExportar = document.getElementById('btnExportar');
    
    if (form) {
        form.addEventListener('submit', handleCalcular);
    }
    
    if (btnReset) {
        btnReset.addEventListener('click', handleReset);
    }
    
    if (btnExportar) {
        btnExportar.addEventListener('click', handleExportar);
    }
});

/**
 * Manejar envío del formulario
 */
async function handleCalcular(e) {
    e.preventDefault();
    
    // Obtener valores
    const flujoAgua = parseFloat(document.getElementById('flujoAgua').value);
    const tempAgua = parseFloat(document.getElementById('tempAgua').value);
    const tempGlucosaIni = parseFloat(document.getElementById('tempGlucosaIni').value);
    const tempGlucosaObj = parseFloat(document.getElementById('tempGlucosaObj').value);
    const volumenGlucosa = parseFloat(document.getElementById('volumenGlucosa').value);
    const areaContacto = parseFloat(document.getElementById('areaContacto').value);
    
    // Validaciones
    if (tempAgua <= tempGlucosaIni) {
        showToast('La temperatura del agua debe ser mayor que la glucosa', 'danger');
        return;
    }
    
    if (tempGlucosaObj <= tempGlucosaIni) {
        showToast('La temperatura objetivo debe ser mayor que la inicial', 'danger');
        return;
    }
    
    // Mostrar carga
    showLoading('graficoTemperatura');
    
    try {
        // 1. Calcular transferencia de calor
        const responseCalculo = await fetchAPI('/api/calcular/transferencia-calor', {
            method: 'POST',
            body: JSON.stringify({
                flujo_agua_m3h: flujoAgua,
                temp_agua_entrada: tempAgua,
                temp_glucosa_inicial: tempGlucosaIni,
                temp_glucosa_objetivo: tempGlucosaObj,
                volumen_glucosa_m3: volumenGlucosa,
                area_contacto_m2: areaContacto
            })
        });
        
        resultadosActuales = responseCalculo.data;
        
        // 2. Simular calentamiento transitorio
        const responseSimulacion = await fetchAPI('/api/calcular/simular-calentamiento', {
            method: 'POST',
            body: JSON.stringify({
                temp_inicial: tempGlucosaIni,
                temp_agua: tempAgua,
                flujo_agua_m3h: flujoAgua,
                volumen_glucosa_m3: volumenGlucosa,
                tiempo_final_h: Math.min(resultadosActuales.tiempo_calentamiento_h * 1.2, 200),
                dt_min: 30
            })
        });
        
        serieTemporalActual = responseSimulacion.data.serie_temporal;
        
        // Actualizar UI
        actualizarKPIs(resultadosActuales);
        actualizarGrafico(serieTemporalActual, tempAgua, tempGlucosaObj);
        actualizarTabla(resultadosActuales);
        
        showToast('Cálculo completado exitosamente', 'success');
        
    } catch (error) {
        console.error('Error en cálculo:', error);
        document.getElementById('graficoTemperatura').innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Error en el cálculo: ${error.message}
            </div>
        `;
    }
}

/**
 * Actualizar tarjetas KPI
 */
function actualizarKPIs(data) {
    document.getElementById('kpiU').textContent = formatNumber(data.coeficiente_U, 1);
    document.getElementById('kpiPotencia').textContent = formatNumber(data.potencia_termica_kW, 1);
    document.getElementById('kpiTiempo').textContent = formatNumber(data.tiempo_calentamiento_h, 1);
    
    document.getElementById('resultadosCards').style.display = 'flex';
}

/**
 * Actualizar gráfico de temperatura
 */
function actualizarGrafico(serie, tempAgua, tempObjetivo) {
    const tiempo = serie.map(p => p.t_h);
    const temperatura = serie.map(p => p.T_glucosa);
    const U = serie.map(p => p.U);
    
    const traces = [
        {
            x: tiempo,
            y: temperatura,
            type: 'scatter',
            mode: 'lines',
            name: 'Temperatura Glucosa',
            line: { color: '#0d6efd', width: 3 },
            fill: 'tozeroy',
            fillcolor: 'rgba(13, 110, 253, 0.1)'
        },
        {
            x: [Math.min(...tiempo), Math.max(...tiempo)],
            y: [tempAgua, tempAgua],
            type: 'scatter',
            mode: 'lines',
            name: 'Temperatura Agua',
            line: { color: '#dc3545', width: 2, dash: 'dash' }
        },
        {
            x: [Math.min(...tiempo), Math.max(...tiempo)],
            y: [tempObjetivo, tempObjetivo],
            type: 'scatter',
            mode: 'lines',
            name: 'Objetivo',
            line: { color: '#198754', width: 2, dash: 'dot' }
        }
    ];
    
    const layout = {
        title: {
            text: 'Perfil de Calentamiento de Glucosa',
            font: { size: 16 }
        },
        xaxis: {
            title: 'Tiempo (h)',
            gridcolor: '#e9ecef'
        },
        yaxis: {
            title: 'Temperatura (°C)',
            gridcolor: '#e9ecef'
        },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        hovermode: 'x unified'
    };
    
    createPlotlyChart('graficoTemperatura', traces, layout);
}

/**
 * Actualizar tabla de resultados
 */
function actualizarTabla(data) {
    const tbody = document.getElementById('tbodyResultados');
    const filas = [
        ['Coeficiente Global U', data.coeficiente_U, 'W/m²·°C'],
        ['Coeficiente Interno hᵢ', data.h_i, 'W/m²·°C'],
        ['Coeficiente Externo hₒ', data.h_o, 'W/m²·°C'],
        ['Resistencia Total', data.R_total, 'm²·°C/W'],
        ['Resistencia Interna', `${data.pct_R_i}%`, 'del total'],
        ['Resistencia Pared', `${data.pct_R_w}%`, 'del total'],
        ['Resistencia Externa', `${data.pct_R_o}%`, 'del total'],
        ['Potencia Térmica', data.potencia_termica_kW, 'kW'],
        ['Temperatura Agua Salida', data.temp_agua_salida_c, '°C'],
        ['ΔT Agua', data.delta_T_agua_c, '°C'],
        ['Densidad Glucosa', data.densidad_glucosa_kg_m3, 'kg/m³'],
        ['Viscosidad Glucosa', data.viscosidad_glucosa_cP, 'cP'],
        ['Calor Específico', data.cp_glucosa_J_kg_C, 'J/kg·°C'],
        ['Conductividad Térmica', data.k_glucosa_W_m_C, 'W/m·°C'],
        ['Número de Prandtl', data.prandtl_glucosa, '-'],
        ['Número de Reynolds', data.reynolds_agua, '-'],
        ['Número de Nusselt', data.nusselt_agua, '-'],
        ['Tiempo de Calentamiento', data.tiempo_calentamiento_h, 'horas'],
        ['Área de Contacto', data.area_contacto_m2, 'm²']
    ];
    
    tbody.innerHTML = filas.map(([param, val, unit]) => `
        <tr>
            <td>${param}</td>
            <td class="fw-bold text-primary">${typeof val === 'number' ? formatNumber(val, 3) : val}</td>
            <td><span class="badge bg-light text-dark">${unit}</span></td>
        </tr>
    `).join('');
    
    document.getElementById('tablaResultados').style.display = 'table';
    document.getElementById('mensajeInicial').style.display = 'none';
    document.getElementById('btnExportar').style.display = 'inline-block';
}

/**
 * Resetear formulario
 */
function handleReset() {
    document.getElementById('calculadoraForm').reset();
    document.getElementById('resultadosCards').style.display = 'none';
    document.getElementById('tablaResultados').style.display = 'none';
    document.getElementById('mensajeInicial').style.display = 'block';
    document.getElementById('btnExportar').style.display = 'none';
    document.getElementById('graficoTemperatura').innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="bi bi-graph-up fs-1"></i>
            <p class="mt-3">Ingrese parámetros y presione "Calcular" para ver resultados</p>
        </div>
    `;
    
    resultadosActuales = null;
    serieTemporalActual = null;
}

/**
 * Exportar resultados
 */
function handleExportar() {
    if (!serieTemporalActual) return;
    
    const datosExportar = {
        parametros: {
            flujo_agua: document.getElementById('flujoAgua').value,
            temp_agua: document.getElementById('tempAgua').value,
            temp_glucosa_ini: document.getElementById('tempGlucosaIni').value,
            temp_glucosa_obj: document.getElementById('tempGlucosaObj').value,
            volumen: document.getElementById('volumenGlucosa').value,
            area: document.getElementById('areaContacto').value
        },
        resultados: resultadosActuales,
        serie_temporal: serieTemporalActual
    };
    
    // Exportar como JSON
    const blob = new Blob([JSON.stringify(datosExportar, null, 2)], { type: 'application/json' });
    downloadFile(blob, 'resultados_calculadora_p2611.json');
    
    showToast('Resultados exportados correctamente', 'success');
}

/**
 * Cargar escenario predefinido
 */
function cargarEscenario(num) {
    switch(num) {
        case 1:
            document.getElementById('flujoAgua').value = 30.9;
            document.getElementById('tempAgua').value = 65;
            document.getElementById('tempGlucosaIni').value = 20;
            document.getElementById('tempGlucosaObj').value = 60;
            document.getElementById('volumenGlucosa').value = 24;
            document.getElementById('areaContacto').value = 13;
            break;
        case 2:
            document.getElementById('flujoAgua').value = 57.7;
            document.getElementById('tempAgua').value = 65;
            document.getElementById('tempGlucosaIni').value = 20;
            document.getElementById('tempGlucosaObj').value = 60;
            document.getElementById('volumenGlucosa').value = 169;
            document.getElementById('areaContacto').value = 13;
            break;
        case 3:
            document.getElementById('flujoAgua').value = 57.7;
            document.getElementById('tempAgua').value = 75;
            document.getElementById('tempGlucosaIni').value = 20;
            document.getElementById('tempGlucosaObj').value = 57;
            document.getElementById('volumenGlucosa').value = 169;
            document.getElementById('areaContacto').value = 13;
            break;
    }
    
    showToast(`Escenario ${num} cargado`, 'info');
}
