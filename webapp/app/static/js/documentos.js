/**
 * Vista de Documentos / Tabla de Transmittal
 */

document.addEventListener('DOMContentLoaded', function() {
    const tabla = document.getElementById('tablaTransmittal');
    if (!tabla) return;

    // Inicializar DataTable
    const dataTable = new DataTable('#tablaTransmittal', {
        language: {
            url: '//cdn.datatables.net/plug-ins/2.0.7/i18n/es-ES.json'
        },
        pageLength: 15,
        responsive: true,
        order: [[5, 'asc'], [0, 'asc']],
        columnDefs: [
            { orderable: false, targets: [7] }
        ]
    });

    // Filtro por categoría
    const filtro = document.getElementById('filtroCategoria');
    if (filtro) {
        filtro.addEventListener('change', function() {
            const categoria = this.value;
            if (categoria) {
                dataTable.column(5).search(categoria).draw();
            } else {
                dataTable.column(5).search('').draw();
            }
        });
    }
});
