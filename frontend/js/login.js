// ==================== USUARIOS DE PRUEBA ====================
// Cuando tengamos backend, esto se valida contra la base de datos.

const usuarios = [
    { usuario: "admin", contrasena: "admin123", rol: "admin" },
    { usuario: "user", contrasena: "user123", rol: "user" }
];

// ==================== LOGIN ====================

const formLogin = document.getElementById("formLogin");
const mensajeError = document.getElementById("mensajeError");

formLogin.addEventListener("submit", function(e) {
    e.preventDefault(); // Evita que la página se recargue

    // Tomo los valores de los inputs
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value.trim();

    // Busco si existe un usuario con esos datos
    const encontrado = usuarios.find(
        u => u.usuario === usuario && u.contrasena === contrasena
    );

    if (!encontrado) {
        mensajeError.textContent = "Usuario o contraseña incorrectos";
        mensajeError.style.display = "block";
        return;
    }

    // Si encontró al usuario, guardo el rol y redirijo
    mensajeError.style.display = "none";

    if (encontrado.rol === "admin") {
        // Admin va al dashboard de gestión
        window.location.href = "dashboard.html";
    } else {
        // Usuario común va a la landing
        window.location.href = "index.html";
    }
});