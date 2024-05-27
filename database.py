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

    # Crear tabla de entrenamientos si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrenamientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nombre TEXT,
        FOREIGN KEY (user_id) REFERENCES usuarios(id)
    )
    """)

    # Crear tabla de relacion entre entrenamientos y ejercicios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrenamiento_ejercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrenamiento_id INTEGER,
        ejercicio_id INTEGER,
        FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id),
        FOREIGN KEY (ejercicio_id) REFERENCES ejercicios(id)
    )
    """)

    conn.close()

def get_connection():
    return sqlite3.connect(bd_path)
