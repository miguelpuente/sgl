// function alerta_error(obj) {
//     let html = '';
//     if (typeof (obj) === 'object') {
//         html = '<ul style="text-align: left;">';
//         $.each(obj, function (key, value) {
//             html+='<li>' + key + ': ' + value + '</li>';
            
//         });
//         html+='</ul>';
//     } else {
//         html = '<p>' + obj + '</p>';
//     }
//     Swal.fire({
//         title: 'Error!',
//         html: html,
//         icon: 'error',
//     });
// }

function alerta_error(errors) {
    let html = '';
    if (errors && typeof errors === 'object') {
        if (errors.hasOwnProperty('error')) {
            html += '<p>' + errors.error + '</p>';
        }
        if (errors.hasOwnProperty('form_errors')) {
            html += '<ul style="text-align: left;">';
            for (let field in errors.form_errors) {
                if (errors.form_errors.hasOwnProperty(field)) {
                    html += '<li>' + field + ': ' + errors.form_errors[field].join(', ') + '</li>';
                }
            }
            html += '</ul>';
        }
    } else if (typeof errors === 'string') {
        html = '<p>' + errors + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error',
    });
}
