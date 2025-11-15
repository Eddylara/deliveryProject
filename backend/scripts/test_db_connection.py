import psycopg2

try:
    conexion = psycopg2.connect(
        host="localhost",
        database="delevery_app",
        user="postgres",
        password="123",
        port="5432"   # puerto por defecto de PostgreSQL
    )

    cursor = conexion.cursor()

    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("Conectado a PostgreSQL:", version)

except Exception as e:
    print("Error al conectar:", e)

finally:
    if 'conexion' in locals():
        conexion.close()
