// ==================== CARRUSEL ====================

const slides = document.querySelectorAll('.slide');
const puntos = document.querySelectorAll('.punto');
const flechaIzq = document.getElementById('flechaIzq');
const flechaDer = document.getElementById('flechaDer');

let slideActual = 0;
let autoplay;

function mostrarSlide(indice) {
    slides.forEach(s => s.classList.remove('activo'));
    puntos.forEach(p => p.classList.remove('activo'));

    slides[indice].classList.add('activo');
    puntos[indice].classList.add('activo');

    slideActual = indice;
}

function siguienteSlide() {
    let siguiente = slideActual + 1;
    if (siguiente >= slides.length) siguiente = 0;
    mostrarSlide(siguiente);
}

function anteriorSlide() {
    let anterior = slideActual - 1;
    if (anterior < 0) anterior = slides.length - 1;
    mostrarSlide(anterior);
}

// Reinicia el temporizador cada vez que el usuario toca una flecha
function reiniciarAutoplay() {
    clearInterval(autoplay);
    autoplay = setInterval(siguienteSlide, 6000);
}

// Flechas
flechaDer.addEventListener('click', () => {
    siguienteSlide();
    reiniciarAutoplay();
});

flechaIzq.addEventListener('click', () => {
    anteriorSlide();
    reiniciarAutoplay();
});

// Puntitos
puntos.forEach((punto, i) => {
    punto.addEventListener('click', () => {
        mostrarSlide(i);
        reiniciarAutoplay();
    });
});

// Arranca el autoplay
autoplay = setInterval(siguienteSlide, 6000);

// ==================== MENU HAMBURGUESA ====================

const btnHamburguesa = document.getElementById('btnHamburguesa');
const menuMobile = document.getElementById('menuMobile');

btnHamburguesa.addEventListener('click', () => {
    menuMobile.classList.toggle('abierto');
});