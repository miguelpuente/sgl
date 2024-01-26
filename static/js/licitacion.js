$(function () {

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'accion': 'buscardata'},
            dataSrc: ""
        },
        columns: [
            // { "data": "creado" },
            { "data": "vehiculo" },
            { "data": "dominio" },
            { "data": "numero_presupuesto" },
            { "data": "aseguradora" },
            { "data": "numero_siniestro" },
            { "data": "monto" },
            // { "data": "localidad" },
            { "data": "user" },
            { "data": "sucursal" },
            { "data": "sucursal" },
        ],
        columnDefs: [
            {
                targets: [-1],
                className: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data;
                }
            },
        ],
        initComplete: function(settings, json) {

        }
    });
});