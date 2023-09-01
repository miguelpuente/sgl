let listaContestados = [];

const objContestado = {
    id: '',
    licitacion: '',
    siniestro: '',
    presupuesto: '',
    dominio: '',
    sucursal: '',
    aseguradora: ''
}

let editando = false;

const formulario = document.querySelector('#formulario');
const licitacion = document.querySelector('#licitacion');
const siniestro = document.querySelector('#siniestro');
const dominio = document.querySelector('#dominio');
const sucursal = document.querySelector('#sucursales');
const aseguradora = document.querySelector('#aseuradoras');
const guardar = document.querySelector('#guardar');

formulario.addEventListener('submit', validarFormulario);

function validarFormulario(e) {
    e.preventDefault();

    if (editando) {
        // editarContestado();
        editando = false;
    } else {
        objContestado.id = Date.now();
        objContestado.licitacion = licitacion.value;
        objContestado.siniestro = siniestro.value;
        objContestado.dominio = dominio.value;
        objContestado.sucursal = sucursal.options[sucursal.selectedIndex].value;
        objContestado.aseguradora = aseguradora.options[aseguradora.selectedIndex].value;

        agregarContestado();
    }
}

function agregarContestado() {
    listaContestados.push({ ...objContestado });

    mostrarContestado();
}

function mostrarContestado() {
    const listado = document.querySelector('.listado-contestados');
    listaContestados.forEach(contestado => {
        const { id, licitacion, siniestro, dominio, sucursal, aseguradora } = contestado
        const parrafo = document.createElement('p');
        parrafo.textContent = `${id} - ${licitacion} - ${siniestro} - ${dominio} - ${sucursal} - ${aseguradora}`;
        parrafo.dataset.id = id;

        const editarBoton = document.createElement('button');
        // editarBoton.onclick = () => cargarContestado(contestado);
        editarBoton.textContent = 'Editar';
        parrafo.append(editarBoton);

        const eliminarBoton = document.createElement('button');
        // eliminarBoton.onclick = () => eliminarContestado(id);
        eliminarBoton.textContent = 'Eliminar';
        parrafo.append(eliminarBoton);

        const hr = document.createElement('hr');

        listado.appendChild(parrafo);
        listado.appendChild(hr);
    })
}