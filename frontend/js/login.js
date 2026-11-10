const API = (location.protocol === 'file:') ? 'http://127.0.0.1:5000' : '';

const formLogin = document.getElementById('formLogin');
const estadoServidor = document.getElementById('estadoServidor');
const mensajeError = document.getElementById('mensajeError');
const botonIngresar = document.querySelector('.btn-ingresar');

let intentos = 0;

function mostrarError(texto) {
    mensajeError.textContent = texto;
    mensajeError.style.display = 'block';
}

function ocultarError() {
    mensajeError.style.display = 'none';
}

function marcarConectado() {
    intentos = 0;
    estadoServidor.textContent = 'Servidor conectado';
    estadoServidor.className = 'estado-servidor conectado';
}

function revisarServidor() {
    fetch(API + '/api/peliculas', { cache: 'no-store' })
        .then(function (respuesta) {
            if (respuesta.ok === false) {
                throw new Error('respuesta');
            }

            marcarConectado();
        })
        .catch(function () {
            intentos = intentos + 1;

            if (intentos <= 5) {
                estadoServidor.textContent = 'Conectando con el servidor...';
                estadoServidor.className = 'estado-servidor';
                setTimeout(revisarServidor, 1500);
            } else {
                estadoServidor.textContent = 'Servidor apagado';
                estadoServidor.className = 'estado-servidor desconectado';
            }
        });
}

function abrirSistema(datos) {
    sessionStorage.setItem('usuario', datos.usuario);
    sessionStorage.setItem('rol', datos.rol);

    if (datos.rol === 'admin') {
        location.href = 'dashboard.html';
    } else {
        location.href = 'index.html';
    }
}

function enviarLogin(usuario, contrasena, restantes) {
    fetch(API + '/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario: usuario, contrasena: contrasena })
    })
        .then(function (respuesta) {
            return respuesta.json().then(function (datos) {
                return { ok: respuesta.ok, datos: datos };
            });
        })
        .then(function (resultado) {
            if (resultado.ok) {
                abrirSistema(resultado.datos);
                return;
            }

            mostrarError(resultado.datos.error || 'Usuario o contrasena incorrectos');
            botonIngresar.disabled = false;
            botonIngresar.textContent = 'Iniciar Sesion';
        })
        .catch(function () {
            if (restantes > 1) {
                setTimeout(function () {
                    enviarLogin(usuario, contrasena, restantes - 1);
                }, 1500);
                return;
            }

            if (location.protocol === 'file:') {
                mostrarError('No se pudo conectar. Abri la pagina desde http://127.0.0.1:5000');
            } else {
                mostrarError('No se pudo conectar. Revisa que app.py este encendido');
            }

            botonIngresar.disabled = false;
            botonIngresar.textContent = 'Iniciar Sesion';
            revisarServidor();
        });
}

formLogin.addEventListener('submit', function (evento) {
    evento.preventDefault();

    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value;

    ocultarError();

    if (usuario === '' || contrasena === '') {
        mostrarError('Completa usuario y contrasena');
        return;
    }

    botonIngresar.disabled = true;
    botonIngresar.textContent = 'Ingresando...';

    enviarLogin(usuario, contrasena, 3);
});

estadoServidor.addEventListener('click', function () {
    intentos = 0;
    estadoServidor.textContent = 'Verificando servidor...';
    estadoServidor.className = 'estado-servidor';
    revisarServidor();
});

if (location.protocol === 'file:') {
    document.getElementById('abrirServidor').className = 'btn-servidor visible';
    mostrarError('Estas abriendo el archivo directamente. Entra desde http://127.0.0.1:5000');
}

revisarServidor();
