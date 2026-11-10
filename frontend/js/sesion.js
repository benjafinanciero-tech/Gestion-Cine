const rolSesion = sessionStorage.getItem('rol');

if (rolSesion === 'admin') {
    mostrarUsuario();
    centrarMenuActivo();
} else {
    location.replace('index.html');
}

function centrarMenuActivo() {
    const menu = document.querySelector('.menu');
    const activo = document.querySelector('.menu-item.activo');

    if (menu && activo) {
        menu.scrollLeft = activo.offsetLeft - (menu.clientWidth - activo.offsetWidth) / 2;
    }
}

function mostrarUsuario() {
    const usuarioGuardado = sessionStorage.getItem('usuario') || 'Admin';
    const usuarioSesion = usuarioGuardado.charAt(0).toUpperCase() + usuarioGuardado.slice(1);

    const nombres = document.querySelectorAll('.admin-nombre');

    for (let i = 0; i < nombres.length; i++) {
        nombres[i].textContent = usuarioSesion;
    }

    const avatar = document.getElementById('avatarUsuario');

    if (avatar) {
        avatar.textContent = usuarioSesion.substring(0, 2).toUpperCase();
    }

    const rolUsuario = document.getElementById('rolUsuario');

    if (rolUsuario) {
        rolUsuario.textContent = 'Administrador';
    }

    const botonSalir = document.querySelector('.menu-item.salir');

    if (botonSalir) {
        botonSalir.addEventListener('click', function () {
            sessionStorage.clear();
        });
    }
}
