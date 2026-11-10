import datetime
import os
import threading
import webbrowser

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA, 'data')
CARPETA_FRONTEND = os.path.join(CARPETA, 'frontend')

app = Flask(__name__, static_folder=CARPETA_FRONTEND, static_url_path='')
app.json.ensure_ascii = False
CORS(app)


@app.after_request
def permitir_red_privada(respuesta):
    respuesta.headers['Access-Control-Allow-Private-Network'] = 'true'
    return respuesta


def ruta_archivo(nombre):
    return os.path.join(CARPETA_DATOS, nombre)


def leer_tabla(nombre):
    return pd.read_csv(ruta_archivo(nombre))


def guardar_tabla(nombre, tabla):
    tabla.to_csv(ruta_archivo(nombre), index=False)


def proximo_id(tabla):
    if tabla.empty:
        return 1
    return int(tabla['id'].max()) + 1


def faltan_datos(datos, campos):
    for campo in campos:
        if campo not in datos:
            return True
        if str(datos[campo]).strip() == '':
            return True
    return False


def filas_a_lista(tabla):
    lista = tabla.to_dict(orient='records')
    for fila in lista:
        for clave in fila:
            valor = fila[clave]
            if isinstance(valor, np.integer):
                fila[clave] = int(valor)
            elif isinstance(valor, np.floating):
                fila[clave] = float(valor)
    return lista


def funciones_con_nombres():
    funciones = leer_tabla('funciones.csv')
    peliculas = leer_tabla('peliculas.csv')
    salas = leer_tabla('salas.csv')

    filas = []

    for i in range(len(funciones)):
        fila = funciones.iloc[i]

        titulo = 'Sin pelicula'
        for j in range(len(peliculas)):
            if peliculas['id'].iloc[j] == fila['id_pelicula']:
                titulo = peliculas['titulo'].iloc[j]

        nombre_sala = 'Sin sala'
        capacidad = 0
        for k in range(len(salas)):
            if salas['id'].iloc[k] == fila['id_sala']:
                nombre_sala = salas['nombre'].iloc[k]
                capacidad = int(salas['capacidad'].iloc[k])

        vendidas = int(fila['entradas_vendidas'])
        if capacidad > 0:
            ocupacion = round((vendidas / capacidad) * 100, 1)
        else:
            ocupacion = 0

        filas.append({
            'id': int(fila['id']),
            'id_pelicula': int(fila['id_pelicula']),
            'titulo': titulo,
            'id_sala': int(fila['id_sala']),
            'sala': nombre_sala,
            'fecha': fila['fecha'],
            'hora': fila['hora'],
            'precio': int(fila['precio']),
            'entradas_vendidas': vendidas,
            'capacidad': capacidad,
            'ocupacion': ocupacion
        })

    columnas = ['id', 'id_pelicula', 'titulo', 'id_sala', 'sala', 'fecha', 'hora', 'precio', 'entradas_vendidas', 'capacidad', 'ocupacion']

    return pd.DataFrame(filas, columns=columnas)


@app.route('/')
def inicio():
    return app.send_static_file('index.html')


@app.route('/api/peliculas', methods=['GET'])
def obtener_peliculas():
    tabla = leer_tabla('peliculas.csv')
    return jsonify(filas_a_lista(tabla))


@app.route('/api/peliculas', methods=['POST'])
def agregar_pelicula():
    datos = request.json or {}

    if faltan_datos(datos, ['titulo', 'genero', 'duracion', 'clasificacion']):
        return jsonify({'error': 'Faltan datos de la pelicula'}), 400

    tabla = leer_tabla('peliculas.csv')

    pelicula = {
        'id': proximo_id(tabla),
        'titulo': datos['titulo'].strip(),
        'genero': datos['genero'].strip(),
        'duracion': int(datos['duracion']),
        'clasificacion': datos['clasificacion'].strip(),
        'poster_url': datos.get('poster_url', ''),
        'estado': datos.get('estado', 'Cartelera')
    }

    tabla = pd.concat([tabla, pd.DataFrame([pelicula])], ignore_index=True)
    guardar_tabla('peliculas.csv', tabla)

    return jsonify({'mensaje': 'Pelicula agregada', 'id': pelicula['id']}), 201


@app.route('/api/salas', methods=['GET'])
def obtener_salas():
    tabla = leer_tabla('salas.csv')
    return jsonify(filas_a_lista(tabla))


@app.route('/api/funciones', methods=['GET'])
def obtener_funciones():
    tabla = funciones_con_nombres()
    tabla = tabla.sort_values('hora')
    return jsonify(filas_a_lista(tabla))


@app.route('/api/funciones', methods=['POST'])
def agregar_funcion():
    datos = request.json or {}

    if faltan_datos(datos, ['id_pelicula', 'id_sala', 'hora', 'precio']):
        return jsonify({'error': 'Faltan datos de la funcion'}), 400

    tabla = leer_tabla('funciones.csv')

    if datos.get('fecha'):
        fecha = datos['fecha']
    else:
        fecha = datetime.date.today().isoformat()

    if datos.get('entradas_vendidas'):
        vendidas = int(datos['entradas_vendidas'])
    else:
        vendidas = 0

    funcion = {
        'id': proximo_id(tabla),
        'id_pelicula': int(datos['id_pelicula']),
        'id_sala': int(datos['id_sala']),
        'fecha': fecha,
        'hora': datos['hora'],
        'precio': int(datos['precio']),
        'entradas_vendidas': vendidas
    }

    tabla = pd.concat([tabla, pd.DataFrame([funcion])], ignore_index=True)
    guardar_tabla('funciones.csv', tabla)

    return jsonify({'mensaje': 'Funcion agregada', 'id': funcion['id']}), 201


@app.route('/api/funciones/<int:id_funcion>', methods=['DELETE'])
def borrar_funcion(id_funcion):
    tabla = leer_tabla('funciones.csv')

    if id_funcion not in tabla['id'].values:
        return jsonify({'error': 'La funcion no existe'}), 404

    tabla = tabla[tabla['id'] != id_funcion]
    guardar_tabla('funciones.csv', tabla)

    return jsonify({'mensaje': 'Funcion eliminada'})


@app.route('/api/combos', methods=['GET'])
def obtener_combos():
    tabla = leer_tabla('combos.csv')
    return jsonify(filas_a_lista(tabla))


@app.route('/api/combos', methods=['POST'])
def agregar_combo():
    datos = request.json or {}

    if faltan_datos(datos, ['nombre', 'precio', 'stock']):
        return jsonify({'error': 'Faltan datos del combo'}), 400

    tabla = leer_tabla('combos.csv')

    combo = {
        'id': proximo_id(tabla),
        'nombre': datos['nombre'].strip(),
        'precio': int(datos['precio']),
        'stock': int(datos['stock'])
    }

    tabla = pd.concat([tabla, pd.DataFrame([combo])], ignore_index=True)
    guardar_tabla('combos.csv', tabla)

    return jsonify({'mensaje': 'Combo agregado', 'id': combo['id']}), 201


@app.route('/api/combos/<int:id_combo>', methods=['PUT'])
def actualizar_combo(id_combo):
    datos = request.json or {}

    if faltan_datos(datos, ['stock']):
        return jsonify({'error': 'Falta el stock'}), 400

    tabla = leer_tabla('combos.csv')

    if id_combo not in tabla['id'].values:
        return jsonify({'error': 'El combo no existe'}), 404

    tabla.loc[tabla['id'] == id_combo, 'stock'] = int(datos['stock'])
    guardar_tabla('combos.csv', tabla)

    return jsonify({'mensaje': 'Stock actualizado'})


@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    tabla = leer_tabla('usuarios.csv')
    return jsonify(filas_a_lista(tabla[['id', 'usuario', 'rol']]))


@app.route('/api/usuarios', methods=['POST'])
def agregar_usuario():
    datos = request.json or {}

    if faltan_datos(datos, ['usuario', 'contrasena']):
        return jsonify({'error': 'Faltan datos del usuario'}), 400

    tabla = leer_tabla('usuarios.csv')
    nombre = datos['usuario'].strip()

    if nombre in tabla['usuario'].values:
        return jsonify({'error': 'Ese usuario ya existe'}), 400

    usuario = {
        'id': proximo_id(tabla),
        'usuario': nombre,
        'contrasena': datos['contrasena'],
        'rol': datos.get('rol', 'user')
    }

    tabla = pd.concat([tabla, pd.DataFrame([usuario])], ignore_index=True)
    guardar_tabla('usuarios.csv', tabla)

    return jsonify({'mensaje': 'Usuario agregado', 'id': usuario['id']}), 201


@app.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def borrar_usuario(id_usuario):
    tabla = leer_tabla('usuarios.csv')

    if id_usuario not in tabla['id'].values:
        return jsonify({'error': 'El usuario no existe'}), 404

    usuario = tabla[tabla['id'] == id_usuario].iloc[0]

    if usuario['usuario'] == 'admin':
        return jsonify({'error': 'El usuario admin no se puede borrar'}), 400

    tabla = tabla[tabla['id'] != id_usuario]
    guardar_tabla('usuarios.csv', tabla)

    return jsonify({'mensaje': 'Usuario eliminado'})


@app.route('/api/reportes', methods=['GET'])
def obtener_reportes():
    tabla = funciones_con_nombres()

    if tabla.empty:
        return jsonify({
            'recaudacion_total': 0,
            'entradas_vendidas': 0,
            'pelicula_mas_vista': 'Sin datos',
            'entradas_pelicula': 0,
            'funciones_totales': 0,
            'ocupacion_promedio': 0
        })

    tabla['recaudacion'] = tabla['precio'] * tabla['entradas_vendidas']
    entradas_por_pelicula = tabla.groupby('titulo')['entradas_vendidas'].sum()

    return jsonify({
        'recaudacion_total': int(tabla['recaudacion'].sum()),
        'entradas_vendidas': int(tabla['entradas_vendidas'].sum()),
        'pelicula_mas_vista': entradas_por_pelicula.idxmax(),
        'entradas_pelicula': int(entradas_por_pelicula.max()),
        'funciones_totales': int(len(tabla)),
        'ocupacion_promedio': float(np.round(tabla['ocupacion'].mean(), 1))
    })


@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    tabla = funciones_con_nombres()

    entradas = int(tabla['entradas_vendidas'].sum())
    recaudacion = int((tabla['precio'] * tabla['entradas_vendidas']).sum())
    capacidad_total = int(tabla['capacidad'].sum())

    if capacidad_total > 0:
        ocupacion = float(np.round((entradas / capacidad_total) * 100, 1))
    else:
        ocupacion = 0

    proximas = tabla.sort_values('hora').head(5)
    proximas = proximas[['id', 'titulo', 'sala', 'hora', 'ocupacion']]

    return jsonify({
        'entradas_hoy': entradas,
        'recaudacion_hoy': recaudacion,
        'ocupacion': ocupacion,
        'funciones_hoy': int(len(tabla)),
        'proximas_funciones': filas_a_lista(proximas)
    })


@app.route('/api/login', methods=['POST'])
def login():
    datos = request.json or {}

    if faltan_datos(datos, ['usuario', 'contrasena']):
        return jsonify({'error': 'Completa usuario y contrasena'}), 400

    tabla = leer_tabla('usuarios.csv')
    nombre = datos['usuario'].strip()
    clave = str(datos['contrasena'])

    encontrado = None

    for i in range(len(tabla)):
        fila = tabla.iloc[i]
        if fila['usuario'] == nombre and str(fila['contrasena']) == clave:
            encontrado = fila

    if encontrado is None:
        return jsonify({'error': 'Usuario o contrasena incorrectos'}), 401

    return jsonify({
        'mensaje': 'Login correcto',
        'usuario': encontrado['usuario'],
        'rol': encontrado['rol']
    })


def abrir_navegador():
    webbrowser.open('http://127.0.0.1:5000/login.html')


if __name__ == '__main__':
    print('CineMax disponible en http://127.0.0.1:5000')
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(2.0, abrir_navegador).start()
    try:
        app.run(debug=True, port=5000)
    except OSError:
        print('El puerto 5000 esta ocupado. Cierra la otra ventana del servidor.')
