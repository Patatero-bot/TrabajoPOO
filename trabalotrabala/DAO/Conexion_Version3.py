import pymysql
from pymysql.err import MySQLError
import hashlib

class ConexionBD:
    def __init__(self, host='localhost', user='root', password='', db='mydb'):
        try:
            self.db = pymysql.connect(
                host=host, user=user, password=password, database=db,
                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.db.cursor()
        except MySQLError as e:
            print("Error conexión:", e)
            self.db = None

    def ejecutar(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.db.commit()
            return self.cursor
        except MySQLError as e:
            print("Error SQL:", e)
            return None

    def commit(self):
        self.db.commit()

    def cerrar(self):
        if self.db:
            self.cursor.close()
            self.db.close()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
