import sqlite3
import os

# Base de datos en la raíz del backend
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tickets.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    # Esto permite acceder a las columnas por nombre como si fuera un diccionario
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Creamos la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id TEXT PRIMARY KEY,
            ap_name TEXT NOT NULL,
            region TEXT,
            issue_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL,
            generated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
