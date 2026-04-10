/**
 * Calculadora Paramétrica - P2611
 * Cálculo instantáneo con debounce, gráficas Plotly
 */

// Constantes
const A_SEC_MC = 0.0455 * 0.141; // m² - sección media caña
const DH_MC = 4 * A_SEC_MC / (2 * (0.0455 + 0.141)); // ~0.069 m

// Estado
let estado = {
    modo: 'flujo', // 'flujo' o 'velocidad'
    parametros: {},
    resultadoInstantaneo: null,
    graficaViscosidad: null,
    graficaDonut: null,
    graficaTransitorio: null
};

// Layout Plotly
const plotlyLayout = {
    font: { family: 'Georgia, serif', size: 11 },
    paper_bgcolor: 'white',
    plot_bgcolor: '#fafafa',
    xaxis: { gridcolor: '#e0e0e0', showgrid: true },
    yaxis: { gridcolor: '#e0e0e0', showgrid: true },
    margin: { l: 50, r: 20, t: 30, b: 40 },
    hovermode: 'x unified'
};

/**
 * Inicializar calculadora
 */
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    initGraficaViscosidad();
    // Cálculo inicial después de un momento
    setTimeout(() => calcularInstantaneo(), 500);
});

/**
 * Configurar event listeners
 */
function initEventListeners() {
    // Modo flujo/velocidad
    document.querySelectorAll('input[name="modoFlujo"]').forEach(radio => {
        radio.addEventListener('change', (e) => cambiarModo(e.target.value));
    });

    // Sliders y inputs sincronizados
    setupSliderInput('sliderFlujo', 'inputFlujo', calcularInstantaneo);
    setupSliderInput('sliderVelocidad', 'inputVelocidad', calcularInstantaneo);
    setupSliderInput('sliderTAgua', 'inputTAgua', calcularInstantaneo);
    setupSliderInput('sliderTInicial', 'inputTInicial', calcularInstantaneo);
    setupSliderInput('sliderTObjetivo', 'inputTObjetivo', () => {});
    setupSliderInput('sliderNivel', 'inputNivel', actualizarVolumenMasa);

    // Inputs numéricos directos
    document.getElementById('inputArea').addEventListener('change', calcularInstantaneo);
    document.getElementById('inputRfAgua').addEventListener('change', calcularInstantaneo);
    document.getElementById('inputRfGlucosa').addEventListener('change', calcularInstantaneo);

    // Botones
    document.getElementById('btnCalcularTransitorio').addEventListener('click', calcularTransitorio);
    document.getElementById('btnSimTransitorio').addEventListener('click', calcularTransitorio);
    document.getElementById('btnCargarEscenario').addEventListener('click', mostrarSelectorEscenario);

    // Actualizar volumen/masa inicial
    actualizarVolumenMasa();
}

/**
 * Configurar sincronización slider-input con debounce
 */
function setupSliderInput(sliderId, inputId, callback) {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);
    if (!slider || !input) return;

    // Slider cambia → actualizar input
    slider.addEventListener('input', () => {
        input.value = slider.value;
        if (estado.modo === 'flujo' && sliderId === 'sliderFlujo') {
            actualizarVelocidadEquivalente();
        }
        if (estado.modo === 'velocidad' && sliderId === 'sliderVelocidad') {
            actualizarFlujoEquivalente();
        }
        if (sliderId === 'sliderTAgua') {
            if (estado.modo === 'velocidad') actualizarFlujoEquivalente();
        }
        debounceCalcular(callback);
    });

    // Input cambia → actualizar slider
    input.addEventListener('change', () => {
        let val = parseFloat(input.value);
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);
        if (val < min) val = min;
        if (val > max) val = max;
        input.value = val;
        slider.value = val;
        if (estado.modo === 'flujo' && sliderId === 'sliderFlujo') {
            actualizarVelocidadEquivalente();
        }
        if (estado.modo === 'velocidad' && sliderId === 'sliderVelocidad') {
            actualizarFlujoEquivalente();
        }
        if (sliderId === 'sliderTAgua') {
            if (estado.modo === 'velocidad') actualizarFlujoEquivalente();
        }
        calcularInstantaneo();
    });
}

/**
 * Debounce para cálculos
 */
let debounceTimer;
function debounceCalcular(callback) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        if (callback) callback();
        else calcularInstantaneo();
    }, 300);
}

/**
 * Cambiar modo flujo/velocidad
 */
function cambiarModo(modo) {
    estado.modo = modo;
    const grupoFlujo = document.getElementById('grupoFlujo');
    const grupoVel = document.getElementById('grupoVelocidad');
    
    if (modo === 'flujo') {
        grupoFlujo.classList.remove('d-none');
        grupoVel.classList.add('d-none');
        actualizarVelocidadEquivalente();
    } else {
        grupoFlujo.classList.add('d-none');
        grupoVel.classList.remove('d-none');
        actualizarFlujoEquivalente();
    }
    calcularInstantaneo();
}

/**
 * Actualizar velocidad equivalente
 */
function actualizarVelocidadEquivalente() {
    const flujo = parseFloat(document.getElementById('sliderFlujo').value);
    const v = (flujo / 3600) / A_SEC_MC;
    document.getElementById('velEquiv').textContent = v.toFixed(2);
}

/**
 * Actualizar flujo equivalente
 */
function actualizarFlujoEquivalente() {
    const v = parseFloat(document.getElementById('sliderVelocidad').value);
    const flujo = v * A_SEC_MC * 3600;
    
    // Densidad aproximada del agua en kg/m3 (fórmula simplificada)
    const T_agua = parseFloat(document.getElementById('sliderTAgua').value);
    const rho_agua = 999.8 - 0.06 * T_agua - 0.0036 * Math.pow(T_agua, 2);
    
    const masa_flujo = flujo * rho_agua; // kg/h
    
    const elVol = document.getElementById('fluVolEquiv');
    const elMas = document.getElementById('fluMasEquiv');
    if (elVol) elVol.textContent = flujo.toFixed(1);
    if (elMas) elMas.textContent = masa_flujo.toFixed(0);
}

/**
 * Actualizar volumen y masa mostrados
 */
function actualizarVolumenMasa() {
    const nivel = parseFloat(document.getElementById('sliderNivel').value);
    // Volumen total aproximado del tanque
    const volTotal = 99.5; // m³ (aprox)
    const volumen = volTotal * (nivel / 100);
    const masa = volumen * 1.43; // densidad aprox 1430 kg/m³
    
    document.getElementById('volDisplay').textContent = volumen.toFixed(1);
    document.getElementById('masaDisplay').textContent = masa.toFixed(1);
}

/**
 * Calcular resultado instantáneo vía API
 */
async function calcularInstantaneo() {
    try {
        const params = leerParametros();
        estado.parametros = params;

        const response = await fetch('/api/calcular/instantaneo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });

        const result = await response.json();
        if (!result.success) throw new Error(result.error);

        estado.resultadoInstantaneo = result.data;
        actualizarUI(result.data);

    } catch (error) {
        console.error('Error cálculo instantáneo:', error);
    }
}

/**
 * Leer parámetros de los inputs
 */
function leerParametros() {
    const T_agua = parseFloat(document.getElementById('inputTAgua').value);
    const T_glucosa = parseFloat(document.getElementById('inputTInicial').value);
    const area = parseFloat(document.getElementById('inputArea').value);
    const rfAgua = parseFloat(document.getElementById('inputRfAgua').value);
    const rfGlucosa = parseFloat(document.getElementById('inputRfGlucosa').value);

    let velocidad, flujo;
    if (estado.modo === 'flujo') {
        flujo = parseFloat(document.getElementById('inputFlujo').value);
        velocidad = (flujo / 3600) / A_SEC_MC;
    } else {
        velocidad = parseFloat(document.getElementById('inputVelocidad').value);
        flujo = velocidad * A_SEC_MC * 3600;
    }

    return {
        temp_agua: T_agua,
        temp_glucosa: T_glucosa,
        velocidad_m_s: velocidad,
        area_m2: area,
        fouling_agua: rfAgua,
        fouling_glucosa: rfGlucosa
    };
}

/**
 * Actualizar UI con resultados
 */
function actualizarUI(data) {
    // KPIs principales
    document.getElementById('resU').textContent = data.U.toFixed(1);
    document.getElementById('resQ').textContent = data.Q_kW.toFixed(1);
    document.getElementById('resLMTD').textContent = data.LMTD.toFixed(1);
    document.getElementById('resRe').textContent = data.Re.toFixed(0);

    // Régimen
    const badge = document.getElementById('badgeRegimen');
    badge.textContent = data.regimen.toUpperCase();
    badge.className = 'badge ' + (data.regimen === 'turbulento' ? 'bg-success' : 
                                   (data.regimen === 'transicion' ? 'bg-warning text-dark' : 'bg-danger'));
    document.getElementById('resRegimen').textContent = data.regimen;

    // Detalles
    document.getElementById('resHi').textContent = data.h_i.toFixed(0);
    document.getElementById('resHo').textContent = data.h_o.toFixed(2);
    document.getElementById('resRi').textContent = data.R_i.toExponential(3);
    document.getElementById('resRo').textContent = data.R_o.toExponential(3);
    document.getElementById('resRw').textContent = data.R_w.toExponential(3);
    document.getElementById('resRf').textContent = (data.R_f_agua + data.R_f_glucosa).toExponential(3);

    // T salida agua
    document.getElementById('TAguaSalida').value = data.T_agua_salida.toFixed(1);

    // Propiedades glucosa
    const prop = data.propiedades_glucosa;
    document.getElementById('propRho').textContent = prop.rho.toFixed(0);
    document.getElementById('propMu').textContent = prop.mu_cP.toFixed(1);
    document.getElementById('propCp').textContent = prop.Cp.toFixed(0);
    document.getElementById('propK').textContent = prop.k.toFixed(4);
    document.getElementById('propPr').textContent = prop.Pr.toFixed(1);

    // Gráfica donut
    actualizarGraficaDonut(data);
}

/**
 * Actualizar gráfica donut de resistencias
 */
function actualizarGraficaDonut(data) {
    const valores = [data.pct_R_i, data.pct_R_w, data.pct_R_o, 
                     (data.R_f_agua/(1/data.U))*100, (data.R_f_glucosa/(1/data.U))*100];
    const etiquetas = ['Rᵢ (agua)', 'Rₚ (pared)', 'Rₒ (glucosa)', 'Rf (agua)', 'Rf (glucosa)'];
    const colores = ['#2196F3', '#9E9E9E', '#FF5722', '#4CAF50', '#FFC107'];

    const trace = {
        values: valores,
        labels: etiquetas,
        type: 'pie',
        hole: 0.5,
        marker: { colors: colores },
        textinfo: 'label+percent',
        textposition: 'outside',
        textfont: { size: 10 }
    };

    const layout = {
        ...plotlyLayout,
        showlegend: false,
        margin: { l: 10, r: 10, t: 10, b: 10 },
        annotations: [{
            text: 'Resistencias',
            x: 0.5, y: 0.5, xref: 'paper', yref: 'paper',
            showarrow: false, font: { size: 12 }
        }]
    };

    Plotly.newPlot('graficaDonut', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Inicializar gráfica de viscosidad
 */
function initGraficaViscosidad() {
    const temps = [];
    const viscosidades = [];
    for (let T = 20; T <= 70; T += 2) {
        temps.push(T);
        // Aproximación de viscosidad glucosa 85 Brix
        const mu = 0.0001 * Math.exp(2500 / (T + 273.15));
        viscosidades.push(mu * 1000); // cP
    }

    const trace = {
        x: temps,
        y: viscosidades,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#1a3a6c', width: 2 },
        fill: 'tozeroy',
        fillcolor: 'rgba(26, 58, 108, 0.1)',
        name: 'μ (cP)'
    };

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'T (°C)' },
        yaxis: { ...plotlyLayout.yaxis, title: 'μ (cP)', type: 'log' },
        showlegend: false
    };

    Plotly.newPlot('graficaViscosidad', [trace], layout, {responsive: true, displayModeBar: false});
}

/**
 * Calcular simulación transitoria
 */
async function calcularTransitorio() {
    mostrarSpinner(true, 'Simulando transitorio...');

    try {
        const params = leerParametros();
        const T_objetivo = parseFloat(document.getElementById('inputTObjetivo').value);
        const nivel = parseFloat(document.getElementById('inputNivel').value);

        const response = await fetch('/api/calcular/transitorio-completo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                T_inicial: params.temp_glucosa,
                T_objetivo_inicio_descarga: T_objetivo,
                T_agua: params.temp_agua,
                velocidad_m_s: params.velocidad_m_s,
                area_m2: params.area_m2,
                nivel_inicial_pct: nivel,
                num_descargas: 1,  // Solo calentamiento para la calculadora
                masa_por_descarga_ton: 0,
                tiempo_descarga_h: 0.01,
                periodo_ciclo_h: 0.01,
                temp_minima_aceptable: 55
            })
        });

        const result = await response.json();
        if (!result.success) throw new Error(result.error);

        renderizarTransitorio(result.data);

    } catch (error) {
        console.error('Error transitorio:', error);
        alert('Error en simulación: ' + error.message);
    } finally {
        mostrarSpinner(false);
    }
}

/**
 * Renderizar curva transitoria
 */
function renderizarTransitorio(data) {
    const serie = data.serie_temporal;
    const faseCalentamiento = data.fases.find(f => f.tipo === 'calentamiento_inicial');
    
    const tiempo = serie.map(p => p.t_h);
    const temperatura = serie.map(p => p.T_glucosa);

    const trace = {
        x: tiempo,
        y: temperatura,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#1a3a6c', width: 2.5 },
        fill: 'tozeroy',
        fillcolor: 'rgba(26, 58, 108, 0.1)',
        name: 'T Glucosa'
    };

    const layout = {
        ...plotlyLayout,
        xaxis: { ...plotlyLayout.xaxis, title: 'Tiempo (h)' },
        yaxis: { ...plotlyLayout.yaxis, title: 'Temperatura (°C)' },
        shapes: [{
            type: 'line',
            x0: 0, x1: 1, xref: 'paper',
            y0: faseCalentamiento.T_fin, y1: faseCalentamiento.T_fin,
            line: { dash: 'dash', color: '#e8750a', width: 2 }
        }],
        annotations: [{
            x: tiempo[temperatura.length - 1],
            y: faseCalentamiento.T_fin,
            text: `Objetivo: ${faseCalentamiento.T_fin}°C`,
            showarrow: true,
            arrowhead: 2,
            ax: 40, ay: -30
        }]
    };

    Plotly.newPlot('graficaTransitorio', [trace], layout, {responsive: true});

    // Generar tabla de hitos
    generarTablaHitos(serie, [30, 45, 57]);
}

/**
 * Generar tabla de hitos
 */
function generarTablaHitos(serie, hitos) {
    const tbody = document.getElementById('tbodyHitos');
    const container = document.getElementById('tablaHitosContainer');
    
    let html = '';
    hitos.forEach(hito => {
        const punto = serie.find(p => p.T_glucosa >= hito);
        if (punto) {
            html += `<tr>
                <td><span class="badge bg-primary">T = ${hito}°C</span></td>
                <td>${punto.T_glucosa.toFixed(1)} °C</td>
                <td>${punto.t_h.toFixed(2)} h</td>
            </tr>`;
        }
    });
    
    tbody.innerHTML = html;
    container.style.display = 'block';
}

/**
 * Mostrar selector de escenario
 */
function mostrarSelectorEscenario() {
    const esc = prompt('Seleccione escenario (1, 2 o 3):', '2');
    if (esc && ['1', '2', '3'].includes(esc)) {
        cargarEscenarioPredefinido(esc);
    }
}

/**
 * Cargar escenario predefinido
 */
function cargarEscenarioPredefinido(esc) {
    const escenarios = {
        '1': { flujo: 30.9, T_agua: 65, T_ini: 20, T_obj: 60, nivel: 7.6 },
        '2': { flujo: 57.7, T_agua: 65, T_ini: 20, T_obj: 57, nivel: 80 }, // 2.5 m/s
        '3': { flujo: 57.7, T_agua: 75, T_ini: 20, T_obj: 57, nivel: 80 }
    };
    
    const e = escenarios[esc];
    if (!e) return;

    document.getElementById('sliderFlujo').value = e.flujo;
    document.getElementById('inputFlujo').value = e.flujo;
    document.getElementById('sliderTAgua').value = e.T_agua;
    document.getElementById('inputTAgua').value = e.T_agua;
    document.getElementById('sliderTInicial').value = e.T_ini;
    document.getElementById('inputTInicial').value = e.T_ini;
    document.getElementById('sliderTObjetivo').value = e.T_obj;
    document.getElementById('inputTObjetivo').value = e.T_obj;
    document.getElementById('sliderNivel').value = e.nivel;
    document.getElementById('inputNivel').value = e.nivel;

    actualizarVelocidadEquivalente();
    actualizarVolumenMasa();
    calcularInstantaneo();
}

/**
 * Mostrar/ocultar spinner
 */
function mostrarSpinner(mostrar, texto = 'Calculando...') {
    const overlay = document.getElementById('spinnerOverlay');
    const textEl = document.getElementById('spinnerText');
    if (overlay) {
        overlay.classList.toggle('d-none', !mostrar);
    }
    if (textEl) {
        textEl.textContent = texto;
    }
}
