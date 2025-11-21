from app.modelo.registro import RegistroTiempo
from app.bd.conexion import getConexion

class RegistroDAO:

    #GUARDAR REGISTRO
    def guardar(self, reg: RegistroTiempo):
        try:
            # Validación de tipo
            if not isinstance(reg, RegistroTiempo):
                print("ERROR: Se esperaba un objeto RegistroTiempo, pero se recibió:", type(reg))
                return None

            # Validación de horas (debe ser int)
            if not isinstance(reg.getHoras(), int):
                print("ERROR: Las horas deben ser un número entero.")
                return None

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

        except Exception as ex:
            print(f"Error DAO guardar registro: {ex}")
            return None

    #LISTAR POR EMPLEADO 
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
                    print(f"⚠ Advertencia: horas inválidas '{horas}', se reemplaza por 0.")
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

    def listar(self):
        return self.listarCompleto()
