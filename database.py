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

    # Crear tabla de ejercicios si no existe y agregar la columna secundaryMuscles si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ejercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        bodyPart TEXT,
        equipment TEXT,
        gifUrl TEXT,
        target TEXT,
        instructions TEXT,
        secundaryMuscles TEXT
    )
    """)

    # Verificar si la columna secundaryMuscles existe, si no, agregarla
    cursor.execute("PRAGMA table_info(ejercicios)")
    columns = [info[1] for info in cursor.fetchall()]
    if "secundaryMuscles" not in columns:
        cursor.execute("ALTER TABLE ejercicios ADD COLUMN secundaryMuscles TEXT")
    
    conn.close()

def get_connection():
    return sqlite3.connect(bd_path)
