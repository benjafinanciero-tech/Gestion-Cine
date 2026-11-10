const slides = document.querySelectorAll('.slide');
const puntos = document.querySelectorAll('.punto');
const flechaIzq = document.getElementById('flechaIzq');
const flechaDer = document.getElementById('flechaDer');

let slideActual = 0;
let autoplay;

function mostrarSlide(indice) {
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove('activo');
        puntos[i].classList.remove('activo');
    }

    slides[indice].classList.add('activo');
    puntos[indice].classList.add('activo');

    slideActual = indice;
}

function siguienteSlide() {
    let siguiente = slideActual + 1;

    if (siguiente >= slides.length) {
        siguiente = 0;
    }

    mostrarSlide(siguiente);
}

function anteriorSlide() {
    let anterior = slideActual - 1;

    if (anterior < 0) {
        anterior = slides.length - 1;
    }

    mostrarSlide(anterior);
}

function reiniciarAutoplay() {
    clearInterval(autoplay);
    autoplay = setInterval(siguienteSlide, 6000);
}

flechaDer.addEventListener('click', function () {
    siguienteSlide();
    reiniciarAutoplay();
});

flechaIzq.addEventListener('click', function () {
    anteriorSlide();
    reiniciarAutoplay();
});

for (let i = 0; i < puntos.length; i++) {
    puntos[i].addEventListener('click', function () {
        mostrarSlide(i);
        reiniciarAutoplay();
    });
}

autoplay = setInterval(siguienteSlide, 6000);

const btnHamburguesa = document.getElementById('btnHamburguesa');
const menuMobile = document.getElementById('menuMobile');

btnHamburguesa.addEventListener('click', function () {
    menuMobile.classList.toggle('abierto');
});

const usuarioGuardado = sessionStorage.getItem('usuario');

if (usuarioGuardado) {
    const nombreUsuario = usuarioGuardado.charAt(0).toUpperCase() + usuarioGuardado.slice(1);

    const chip = document.getElementById('usuarioChip');
    chip.textContent = nombreUsuario;
    chip.className = 'usuario-chip visible';

    document.getElementById('btnLogin').className = 'btn-login oculto';

    const botonSalir = document.getElementById('btnSalir');
    botonSalir.className = 'btn-salir visible';

    const menuUsuario = document.getElementById('menuUsuario');
    menuUsuario.textContent = 'Sesion iniciada como ' + nombreUsuario;
    menuUsuario.className = 'menu-mobile-usuario visible';

    const menuAccion = document.getElementById('menuAccion');
    menuAccion.textContent = 'Cerrar Sesion';
    menuAccion.href = '#';

    botonSalir.addEventListener('click', cerrarSesion);
    menuAccion.addEventListener('click', cerrarSesion);
}

function cerrarSesion(evento) {
    evento.preventDefault();
    sessionStorage.clear();
    location.reload();
}
