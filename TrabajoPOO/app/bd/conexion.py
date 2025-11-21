import mysql.connector

def getConexion():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="concesionaria"
        )
        return con
    except mysql.connector.Error as ex:
        print(f"Error de conexión: {ex}")
        return None