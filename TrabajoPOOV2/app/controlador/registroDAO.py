from app.modelo.registro import RegistroTiempo
from app.bd.conexion import getConexion
import mysql.connector

class RegistroDAO:

    # VALIDACIÓN: EMPLEADO EXISTE
    def _empleadoExiste(self, idEmpleado):
        con = getConexion()
        cur = con.cursor()
        cur.execute("SELECT 1 FROM empleado WHERE idEmpleado = %s", (idEmpleado,))
        existe = cur.fetchone() is not None
        cur.close()
        con.close()
        return existe

    # VALIDACIÓN: PROYECTO EXISTE
    def _proyectoExiste(self, idProyecto):
        con = getConexion()
        cur = con.cursor()
        cur.execute("SELECT 1 FROM proyecto WHERE idProyecto = %s", (idProyecto,))
        existe = cur.fetchone() is not None
        cur.close()
        con.close()
        return existe

    # GUARDAR REGISTRO
    def guardar(self, reg: RegistroTiempo):
        try:
            # Validación de tipo
            if not isinstance(reg, RegistroTiempo):
                print("ERROR: Se esperaba un objeto RegistroTiempo.")
                return None

            # Validación de horas
            if not isinstance(reg.getHoras(), int):
                print("ERROR: Las horas deben ser un número entero.")
                return None

            # Validar existencia de empleado
            if not self._empleadoExiste(reg.getIdEmpleado()):
                print(f"No existe el empleado con ID {reg.getIdEmpleado()}.")
                return None

            # Validar existencia de proyecto
            if not self._proyectoExiste(reg.getIdProyecto()):
                print(f"No existe el proyecto con ID {reg.getIdProyecto()}.")
                return None

            # Guardar en BD
            con = getConexion()
            cur = con.cursor()

            sql = """
                INSERT INTO registro_tiempo
                (idEmpleado, idProyecto, fecha, horasTrabajadas, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """

            cur.execute(sql, (
                reg.getIdEmpleado(),
                reg.getIdProyecto(),
                reg.getFecha(),
                reg.getHoras(),
                reg.getDescripcion()
            ))

            con.commit()
            reg.setIdRegistro(cur.lastrowid)

            cur.close()
            con.close()
            return reg

        except mysql.connector.IntegrityError as ex:
            print("ERROR SQL (clave foránea): No se pudo guardar el registro.")
            print("Detalle:", ex)
            return None

        except Exception as ex:
            print(f"Error DAO guardar registro: {ex}")
            return None

    # ============================================================
    # LISTAR POR EMPLEADO
    # ============================================================
    def listarPorEmpleado(self, idEmpleado):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT r.idRegistro, r.fecha, r.horasTrabajadas, r.descripcion,
                       r.idProyecto
                FROM registro_tiempo r
                WHERE r.idEmpleado = %s
                ORDER BY r.fecha DESC
            """

            cur.execute(sql, (idEmpleado,))
            rows = cur.fetchall()

            registros = []
            for row in rows:

                horas = row["horasTrabajadas"]
                try:
                    horas = int(horas)
                except:
                    print(f"Horas inválidas '{horas}', se usa 0.")
                    horas = 0

                reg = RegistroTiempo(
                    idRegistro=row["idRegistro"],
                    idEmpleado=idEmpleado,
                    idProyecto=row["idProyecto"],
                    fecha=row["fecha"],
                    horas=horas,
                    descripcion=row["descripcion"]
                )
                registros.append(reg)

            cur.close()
            con.close()
            return registros

        except Exception as ex:
            print(f"Error DAO listarPorEmpleado: {ex}")
            return []

    # ============================================================
    # LISTAR COMPLETO
    # ============================================================
    def listarCompleto(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT r.idRegistro,
                       r.idEmpleado,
                       r.idProyecto,
                       r.fecha,
                       r.horasTrabajadas,
                       r.descripcion
                FROM registro_tiempo r
                ORDER BY r.fecha DESC
            """

            cur.execute(sql)
            rows = cur.fetchall()

            registros = []
            for row in rows:

                horas = row["horasTrabajadas"]
                try:
                    horas = int(horas)
                except:
                    print(f"Advertencia: horas inválidas '{horas}', se reemplaza por 0.")
                    horas = 0

                reg = RegistroTiempo(
                    idRegistro=row["idRegistro"],
                    idEmpleado=row["idEmpleado"],
                    idProyecto=row["idProyecto"],
                    fecha=row["fecha"],
                    horas=horas,
                    descripcion=row["descripcion"]
                )
                registros.append(reg)

            cur.close()
            con.close()
            return registros

        except Exception as ex:
            print(f"Error DAO listarCompleto: {ex}")
            return []

    # Alias para compatibilidad
    def listar(self):
        return self.listarCompleto()
