# app.py (VERSIÓN FINAL CON TU ESTRUCTURA)
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB_NAME = 'inventario.db' 

# ---------------------------------------------
# Configuraciones de la Base de Datos
# ---------------------------------------------
# Nombre de la tabla principal
TABLE_NAME = 'POSICIONES' 

# Columnas de tu tabla:
# POSICION: Columna principal para listado y búsqueda.
# ZONA: Columna secundaria.
# OBSERVACIONES: Columna para la descripción larga.
# CODIGO_QR: Columna que contiene el valor a codificar en el QR.
# ---------------------------------------------


def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    # Usamos alias (AS) para que el frontend (index.html) reciba siempre 'DESCRIPCION' y 'CODIGO'
    # Esto mantiene limpio el código de la plantilla HTML/JS.
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/')
def index():
    """Ruta principal: carga la plantilla inicial."""
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar_items():
    """Ruta AJAX para la búsqueda y el listado inicial."""
    
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Mapeo de columnas: el frontend espera DESCRIPCION y CODIGO
    select_cols = f"""
        SELECT 
            POSICION, 
            ZONA, 
            OBSERVACIONES AS DESCRIPCION,  
            CODIGO_QR AS CODIGO
        FROM {TABLE_NAME}
    """
    
    if query:
        # La búsqueda se hace por POSICION, usando LIKE para el filtrado
        search_term = '%' + query + '%'
        sql_query = f"{select_cols} WHERE POSICION LIKE ? ORDER BY POSICION"
        cursor.execute(sql_query, (search_term,))
    else:
        # Listar todos los elementos si no hay búsqueda
        sql_query = f"{select_cols} ORDER BY POSICION"
        cursor.execute(sql_query)

    items = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(items)

if __name__ == '__main__':
    # Usar debug=True para desarrollo
    app.run(debug=True)