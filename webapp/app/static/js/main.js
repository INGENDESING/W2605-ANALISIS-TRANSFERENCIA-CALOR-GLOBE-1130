/**
 * JavaScript Principal - P2611 WebApp
 * Funciones compartidas entre todos los módulos
 */

// Configuración global
const CONFIG = {
    API_BASE_URL: '',  // Mismo origen
    DEFAULT_DECIMALS: 2,
    CHART_COLORS: {
        primary: '#0d6efd',
        success: '#198754',
        warning: '#ffc107',
        danger: '#dc3545',
        info: '#0dcaf0',
        secondary: '#6c757d'
    }
};

/**
 * Formatear número con decimales
 */
function formatNumber(value, decimals = CONFIG.DEFAULT_DECIMALS) {
    if (value === null || value === undefined || isNaN(value)) {
        return '-';
    }
    return parseFloat(value).toFixed(decimals);
}

/**
 * Formatear número en notación científica
 */
function formatScientific(value, decimals = 2) {
    if (value === null || value === undefined || isNaN(value)) {
        return '-';
    }
    return parseFloat(value).toExponential(decimals);
}

/**
 * Mostrar toast de notificación
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

/**
 * Crear contenedor de toasts
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

/**
 * Mostrar indicador de carga
 */
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-3 text-muted">Procesando cálculos...</p>
            </div>
        `;
    }
}

/**
 * Ocultar indicador de carga
 */
function hideLoading(containerId, defaultContent = '') {
    const container = document.getElementById(containerId);
    if (container && defaultContent) {
        container.innerHTML = defaultContent;
    }
}

/**
 * Realizar petición fetch con manejo de errores
 */
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `Error HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en fetchAPI:', error);
        showToast(error.message, 'danger');
        throw error;
    }
}

/**
 * Descargar archivo
 */
function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
}

/**
 * Inicializar DataTable
 */
function initDataTable(tableId, options = {}) {
    const defaultOptions = {
        language: {
            url: '//cdn.datatables.net/plug-ins/2.0.7/i18n/es-ES.json'
        },
        pageLength: 10,
        responsive: true,
        ...options
    };
    
    return new DataTable(`#${tableId}`, defaultOptions);
}

/**
 * Crear gráfico con Plotly
 */
function createPlotlyChart(containerId, data, layout = {}, config = {}) {
    const defaultLayout = {
        font: { family: 'Segoe UI, sans-serif' },
        margin: { t: 40, r: 40, b: 60, l: 60 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        ...layout
    };
    
    const defaultConfig = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
        ...config
    };
    
    Plotly.newPlot(containerId, data, defaultLayout, defaultConfig);
}

/**
 * Validar input numérico
 */
function validateNumber(value, min, max) {
    const num = parseFloat(value);
    if (isNaN(num)) return false;
    if (min !== undefined && num < min) return false;
    if (max !== undefined && num > max) return false;
    return true;
}

/**
 * Obtener valores de formulario como objeto
 */
function getFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    
    for (const [key, value] of formData.entries()) {
        // Convertir a número si es posible
        const numValue = parseFloat(value);
        data[key] = isNaN(numValue) ? value : numValue;
    }
    
    return data;
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    // Activar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Activar popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    console.log('P2611 WebApp - Cargada correctamente');
});
