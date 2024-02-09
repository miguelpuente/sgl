function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

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
