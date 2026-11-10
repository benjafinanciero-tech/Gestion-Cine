# CineMax - Sistema de Gestión de Cine

Proyecto escolar de un sistema de gestión de cine. Frontend en HTML, CSS y JavaScript vanilla. Backend en Python con Flask, Pandas y NumPy. Los datos se guardan en archivos CSV, sin base de datos SQL.

## Estructura

```
Gestion-Cine/
├── iniciar.bat
├── backend/
│   └── app.py
├── data/
│   ├── peliculas.csv
│   ├── salas.csv
│   ├── funciones.csv
│   ├── usuarios.csv
│   └── combos.csv
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── cartelera.html
│   ├── horarios.html
│   ├── precios.html
│   ├── reportes.html
│   ├── usuarios.html
│   ├── assets/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md
```

## Cómo ejecutarlo

Doble clic en `iniciar.bat`. El archivo instala las dependencias la primera vez, arranca el servidor y abre el navegador en http://127.0.0.1:5000

También se puede arrancar a mano:

```
pip install -r requirements.txt
python backend/app.py
```

Después abrir http://127.0.0.1:5000 (el servidor también entrega las páginas del frontend, no hace falta Live Server).

## Íconos

Los íconos de la interfaz usan la fuente Font Awesome Free (licencia CC BY 4.0), guardada en `frontend/assets/fonts/fa-solid-900.woff2` para que funcione sin conexión.

## Usuarios de prueba

| Usuario | Contraseña | Rol   |
|---------|------------|-------|
| admin   | admin123   | admin |
| user    | user123    | user  |

## Páginas

| Página           | Qué hace                                             |
|------------------|------------------------------------------------------|
| index.html       | Landing pública del cine                             |
| login.html       | Ingreso con validación por roles                     |
| dashboard.html   | Resumen del día y próximas funciones                 |
| cartelera.html   | Alta y listado de películas                          |
| horarios.html    | Alta y listado de funciones por sala                 |
| precios.html     | Dulcería: combos y control de stock                  |
| reportes.html    | Recaudación, película más vista y exportar a PDF      |
| usuarios.html    | Alta y baja de usuarios del sistema                  |

## Endpoints

| Método | Ruta                     | Descripción                                       |
|--------|--------------------------|---------------------------------------------------|
| POST   | /api/login               | Valida usuario y contraseña, devuelve el rol       |
| GET    | /api/estadisticas        | Totales del día y próximas funciones               |
| GET    | /api/reportes            | Recaudación, entradas y película más vista         |
| GET    | /api/peliculas           | Lista de películas                                 |
| POST   | /api/peliculas           | Agrega una película                                |
| GET    | /api/salas               | Lista de salas                                     |
| GET    | /api/funciones           | Grilla con nombre de película, sala y ocupación    |
| POST   | /api/funciones           | Agrega una función                                 |
| DELETE | /api/funciones/<id>      | Elimina una función                                |
| GET    | /api/combos              | Lista de combos de dulcería                        |
| POST   | /api/combos              | Agrega un combo                                    |
| PUT    | /api/combos/<id>         | Actualiza el stock de un combo                     |
| GET    | /api/usuarios            | Lista de usuarios (sin contraseñas)                |
| POST   | /api/usuarios            | Agrega un usuario                                  |
| DELETE | /api/usuarios/<id>       | Elimina un usuario                                 |

## Manual del proyecto

`documentacion/Manual-CineMax.pdf` es un manual tecnico de 34 paginas que explica archivo por archivo como funciona el sistema: cada funcion del backend y del JavaScript, la logica de los CSV, las decisiones de diseno, los problemas resueltos, preguntas probables del profesor y un glosario.

Se puede volver a generar con:

```
pip install reportlab
python documentacion/generar_manual.py
```
