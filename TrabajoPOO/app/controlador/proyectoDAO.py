from app.modelo.proyecto import Proyecto
from app.bd.conexion import getConexion

class ProyectoDAO:

    def guardar(self, proyecto: Proyecto):
        con = getConexion()
        cur = con.cursor()
        sql = """
            INSERT INTO proyecto (nombre, descripcion, idDepartamento)
            VALUES (%s,%s,%s)
        """
        cur.execute(sql, (proyecto.getNombre(), proyecto.getDescripcion(),
                          proyecto.getIdDepartamento()))
        con.commit()
        proyecto.setIdProyecto(cur.lastrowid)
        cur.close()
        con.close()
        return proyecto

    def listar(self):
        con = getConexion()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT p.idProyecto, p.nombre, p.descripcion, d.nombre AS departamento
            FROM proyecto p
            LEFT JOIN departamento d ON p.idDepartamento = d.idDepartamento
        """)
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows