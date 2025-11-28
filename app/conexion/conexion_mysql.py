import mysql.connector

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mascotas_db"
        )
    except Exception as e:
        print("Error de conexión a la BD:",e)
        return None
    