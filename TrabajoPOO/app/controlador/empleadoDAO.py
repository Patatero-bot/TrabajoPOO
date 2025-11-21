from app.modelo.empleado import Empleado
from app.modelo.persona import Persona
from app.bd.conexion import getConexion
from app.controlador.personaDAO import PersonaDAO
from datetime import date, datetime

class EmpleadoDAO:

    def _crearEmpleadoDesdeDB(self, r):

        nombre = r["nombre"] if r["nombre"] else "SinNombre"
        apellido = r["apellido"] if r["apellido"] else "SinApellido"
        telefono = r["telefono"] if r["telefono"] else "00000000"
        email = r["email"] if r["email"] else "sinemail@empresa.com"

        fecha = r["fechaInicio"]
        if isinstance(fecha, datetime):
            fecha = fecha.date().strftime("%Y-%m-%d")
        if isinstance(fecha, date):
            fecha = fecha.strftime("%Y-%m-%d")

        salario = r["salario"] if r["salario"] else 0
        departamento = r["departamento"] if r["departamento"] else "SinDepto"

        return Empleado(
            idEmpleado=r["idEmpleado"],
            idPersona=r["idPersona"],
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            fechaInicio=fecha,
            salario=salario,
            departamento=departamento,
            cargando_desde_bd=True
        )

    # GUARDAR EMPLEADO
    def guardar(self, empleado: Empleado):

        con = None
        cur = None
        
        try:
            personaDAO = PersonaDAO()
            
            persona = Persona(
                nombre=empleado.getNombre(),
                apellido=empleado.getApellido(),
                telefono=empleado.getTelefono(),
                email=empleado.getEmail()
            )

            persona = personaDAO.guardar(persona)

            if persona is None:
                print("[EmpleadoDAO.guardar] No se pudo crear la persona.")
                return None

            empleado.setIdPersona(persona.getIdPersona())

            con = getConexion()
            cur = con.cursor()

            sql = """
                INSERT INTO empleado (idPersona, fechaInicio, salario, departamento)
                VALUES (%s, %s, %s, %s)
            """

            cur.execute(sql, (
                empleado.getIdPersona(),
                empleado.getFechaInicio(),
                empleado.getSalario(),
                empleado.getDepartamento()
            ))

            con.commit()
            empleado.setIdEmpleado(cur.lastrowid)

            return empleado

        except Exception as ex:
            print(f"[EmpleadoDAO.guardar] Error: {ex}")
            return None

        finally:
            if cur: cur.close()
            if con: con.close()

    #LISTAR EMPLEADOS
    def listar(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT e.idEmpleado, p.idPersona, p.nombre, p.apellido,
                       p.telefono, p.email,
                       e.fechaInicio, e.salario, e.departamento
                FROM empleado e
                JOIN persona p ON e.idPersona = p.idPersona
                ORDER BY e.idEmpleado
            """

            cur.execute(sql)
            rows = cur.fetchall()

            empleados = [self._crearEmpleadoDesdeDB(r) for r in rows]
            return empleados

        except Exception as ex:
            print(f"[EmpleadoDAO.listar] Error: {ex}")
            return []

        finally:
            cur.close()
            con.close()

    def buscarPorId(self, idEmpleado):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT e.idEmpleado, e.idPersona, p.nombre, p.apellido,
                       p.telefono, p.email,
                       e.fechaInicio, e.salario, e.departamento
                FROM empleado e
                JOIN persona p ON e.idPersona = p.idPersona
                WHERE e.idEmpleado = %s
            """

            cur.execute(sql, (idEmpleado,))
            row = cur.fetchone()

            if not row:
                print(f"No existe empleado con ID {idEmpleado}.")
                return None

            return self._crearEmpleadoDesdeDB(row)

        except Exception as ex:
            print(f"[EmpleadoDAO.buscarPorId] Error: {ex}")
            return None

        finally:
            cur.close()
            con.close()

    def departamentoExiste(self, nombreDepartamento):
        try:
            con = getConexion()
            cur = con.cursor()

            sql = "SELECT idDepartamento FROM departamento WHERE nombre = %s LIMIT 1"
            cur.execute(sql, (nombreDepartamento,))
            return cur.fetchone() is not None

        except Exception as ex:
            print(f"Error verificando departamento: {ex}")
            return False

        finally:
            cur.close()
            con.close()

    def reasignarDepartamento(self, idEmpleado, nuevoDepartamento):
        try:
            con = getConexion()
            cur = con.cursor()

            sql = "UPDATE empleado SET departamento = %s WHERE idEmpleado = %s"
            cur.execute(sql, (nuevoDepartamento, idEmpleado))

            con.commit()
            return True

        except Exception as ex:
            print(f"Error al reasignar departamento: {ex}")
            return False

        finally:
            cur.close()
            con.close()
