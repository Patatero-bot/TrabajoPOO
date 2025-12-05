from app.modelo.proyecto import Proyecto
from app.bd.conexion import getConexion
import mysql.connector

class ProyectoDAO:

    # ============================================================
    # GUARDAR PROYECTO
    # ============================================================
    def guardar(self, proyecto: Proyecto):
        con = None
        cur = None
        try:
            con = getConexion()
            cur = con.cursor()

            sql = """
                INSERT INTO proyecto (nombre, descripcion, idDepartamento)
                VALUES (%s, %s, %s)
            """

            cur.execute(sql, (
                proyecto.getNombre(),
                proyecto.getDescripcion(),
                proyecto.getIdDepartamento()
            ))

            con.commit()
            proyecto.setIdProyecto(cur.lastrowid)
            return proyecto

        except mysql.connector.IntegrityError as ex:
            
            if ex.errno == 1452:
                print(f"   El idDepartamento '{proyecto.getIdDepartamento()}' NO EXISTE.")
            else:
                print(f"❌ Error de integridad al guardar proyecto: {ex}")
            return None

        except Exception as ex:
            print(f"Error general en ProyectoDAO.guardar: {ex}")
            return None

        finally:
            if cur: cur.close()
            if con: con.close()


    # ============================================================
    # LISTAR PROYECTOS
    # ============================================================
    def listar(self):
        con = None
        cur = None
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            cur.execute("""
                SELECT p.idProyecto, p.nombre, p.descripcion, d.nombre AS departamento
                FROM proyecto p
                LEFT JOIN departamento d ON p.idDepartamento = d.idDepartamento
            """)

            return cur.fetchall()

        except Exception as ex:
            print(f"Error en ProyectoDAO.listar: {ex}")
            return []

        finally:
            if cur: cur.close()
            if con: con.close()
