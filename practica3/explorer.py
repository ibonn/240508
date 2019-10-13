import sys
import json
import os.path
import sqlite3

from flask import Flask, Response, render_template

# Funciones auxiliares
def lista_tablas():
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tablas = [tabla[1] for tabla in c.fetchall()]
    conn.close()
    return tablas

def mostrar_json(d, s='OK', m=''):
    r = Response(
        json.dumps({
            'estado': s, 
            'mensaje': m, 
            'resultado': d
    }))
    r.headers["Content-Type"] = 'application/json'
    return r

def mostrar_tabla(table):
    tablas = lista_tablas()
    if table in tablas:
        conn = sqlite3.connect(sys.argv[1])
        c = conn.cursor()
        c.execute("SELECT * FROM '{}';".format(table))
        columnas = [description[0] for description in c.description]
        tabla = [dict(zip(columnas, r)) for r in c.fetchall()]
        conn.close()
        return tabla
    return None

def mostrar_info_tabla(table):
    tablas = lista_tablas()
    if table in tablas:
        conn = sqlite3.connect(sys.argv[1])
        c = conn.cursor()
        c.execute("SELECT * FROM '{}';".format(table))
        num_rows = len(list(c.fetchall()))
        columnas = [description[0] for description in c.description]
        conn.close()
        return {'columnas': columnas, 'num_registros': num_rows}
    return None

# Servidor Flask
app = Flask(__name__)

@app.route('/')
def mostrar_inicio():
    return render_template('index.html')

@app.route('/tablas/')
def mostrar_tablas_json():
    return mostrar_json(lista_tablas())

@app.route('/tablas/<table>/')
def mostrar_tabla_json(table):
    tabla = mostrar_tabla(table)
    if tabla is None:
        return mostrar_json(None, s='error', m='La tabla "{}" no existe'.format(table))
    else:
        return mostrar_json(tabla)

@app.route('/tablas/<table>/info/')
def mostrar_info_tabla_json(table):
    info = mostrar_info_tabla(table)
    if info is None:
        return mostrar_json(None, s='error', m='La tabla "{}" no existe'.format(table))
    else:
        return mostrar_json(info)

@app.route('/html/tablas/')
def mostrar_tablas_html():
    return render_template('tablas.html', tables=lista_tablas())

@app.route('/html/tablas/<table>/')
def mostrar_tabla_html(table):
    return render_template('tabla.html', table=table, data=mostrar_tabla(table))

@app.route('/html/tablas/<table>/info/')
def mostrar_info_tabla_html(table):
    return render_template('info_tabla.html', table=table, data=mostrar_info_tabla(table))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Se necesita una base de datos')
    else:
        if os.path.isfile(sys.argv[1]):
            app.run()
        else:
            print('Error: No existe el fichero {}'.format(sys.argv[1]))