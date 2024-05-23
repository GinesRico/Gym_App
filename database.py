import sqlite3
from config import bd_path

def initialize_database():
    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT
    )
    """)

    # Verificar si la tabla de favoritos tiene las columnas correctas
    cursor.execute("PRAGMA table_info(favoritos)")
    columns = [info[1] for info in cursor.fetchall()]
    if "user_id" not in columns or "ejercicio_id" not in columns:
        cursor.execute("DROP TABLE IF EXISTS favoritos")
        cursor.execute("""
        CREATE TABLE favoritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            ejercicio_id INTEGER, 
            FOREIGN KEY (user_id) REFERENCES usuarios(id), 
            FOREIGN KEY (ejercicio_id) REFERENCES ejercicios(id)
        )
        """)
    conn.close()

def get_connection():
    return sqlite3.connect(bd_path)
