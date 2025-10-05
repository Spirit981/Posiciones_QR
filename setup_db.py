# setup_db.py
import sqlite3

DB_NAME = 'inventario.db'

def setup_database():
    """Crea la tabla y algunos datos de prueba."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Eliminar la tabla si existe (para empezar de cero)
    cursor.execute("DROP TABLE IF EXISTS items;")

    # 2. Crear la tabla 'items'
    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            POSICION TEXT NOT NULL,
            ZONA TEXT,
            DESCRIPCION TEXT,
            CODIGO TEXT NOT NULL,
            FABRICANTE TEXT
        );
    """)

    # 3. Insertar datos de ejemplo
    data = [
        ('A01-10', 'Almacén 1', 'Destornillador Phillips', 'DSTPH001', 'Marca X'),
        ('A01-11', 'Almacén 1', 'Llave inglesa de 12mm', 'LLAVE12M', 'Marca Y'),
        ('B02-05', 'Zona de Herramientas', 'Taladro percutor 220V', 'TDP220Z', 'Marca Z'),
        ('C03-01', 'Taller Mecánico', 'Caja de fusibles 10A', 'FUSBX10A', 'Marca X'),
        ('A01-15', 'Almacén 1', 'Tornillos M8 (Caja)', 'TOR8M090', 'Marca X'),
    ]

    cursor.executemany("""
        INSERT INTO items (POSICION, ZONA, DESCRIPCION, CODIGO, FABRICANTE)
        VALUES (?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()
    print(f"Base de datos '{DB_NAME}' creada y poblada exitosamente.")

if __name__ == '__main__':
    setup_database()