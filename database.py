import mysql.connector
from mysql.connector import Error

def initialize_database():
    try:
        conn = mysql.connector.connect(
            host='192.168.31.238',
            port=3306,
            database='Gym_app',
            user='User_Gym_app',
            password='Pass_Gym_app'
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Crear tabla de usuarios si no existe
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
            """)

            # Crear tabla de ejercicios si no existe
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ejercicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                bodyPart VARCHAR(255),
                equipment VARCHAR(255),
                gifUrl VARCHAR(255),
                instructions TEXT,
                secondaryMuscles TEXT
            )
            """)

            # Crear tabla de entrenamientos si no existe
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS entrenamientos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                nombre VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
            """)

            # Crear tabla de entrenamiento_ejercicios si no existe
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS entrenamiento_ejercicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                entrenamiento_id INT,
                ejercicio_id INT,
                FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id),
                FOREIGN KEY (ejercicio_id) REFERENCES ejercicios(id)
            )
            """)

            conn.commit()
            cursor.close()
            conn.close()

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='192.168.31.238',
            port=3306,
            database='Gym_app',
            user='User_Gym_app',
            password='Pass_Gym_app'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
