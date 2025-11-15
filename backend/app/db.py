# app/db.py

import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host": "localhost",
    "database": "delevery_app",
    "user": "postgres",
    "password": "123",
    "port": "5432"
}


def get_connection():
    """
    Crea una conexión nueva a PostgreSQL.
    Devuelve conexiones con dict cursor (clave → valor).
    """
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding("UTF8")
    return conn


def query(sql, params=None):
    """
    Ejecuta consultas SELECT y devuelve una lista de diccionarios.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def execute(sql, params=None):
    """
    Ejecuta INSERT, UPDATE o DELETE.
    Devuelve número de filas afectadas.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return cur.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
