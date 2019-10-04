import json
import sqlite3
from flask import Flask, Response, render_template

# Funciones auxiliares
def lista_tablas():
    conn = sqlite3.connect('ejemplo.db')
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

# Servidor Flask
app = Flask(__name__)

@app.route('/')
def mostrar_inicio():
    return render_template('index.html')

@app.route('/tablas')
def mostrar_tablas():
    return mostrar_json(lista_tablas())

@app.route('/tablas/<table>')
def mostrar_tabla(table):
    tablas = lista_tablas()
    if table in tablas:
        conn = sqlite3.connect('ejemplo.db')
        c = conn.cursor()
        c.execute("SELECT * FROM '{}';".format(table))
        columnas = [description[0] for description in c.description]
        tabla = [dict(zip(columnas, r)) for r in c.fetchall()]
        conn.close()
        return mostrar_json(tabla)
    else:
        return mostrar_json(None, s='error', m='La tabla "{}" no existe'.format(table))

if __name__ == '__main__':
    app.run()