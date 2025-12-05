from app.modelo.empleado import Empleado
from app.modelo.persona import Persona
from app.bd.conexion import getConexion
from app.controlador.personaDAO import PersonaDAO
from datetime import date, datetime

class EmpleadoDAO:

    # ============================================================
    #  CREAR OBJETO EMPLEADO DESDE BD
    # ============================================================
    def _crearEmpleadoDesdeDB(self, r):

        nombre = r.get("nombre") or "SinNombre"
        apellido = r.get("apellido") or "SinApellido"
        telefono = r.get("telefono") or "00000000"
        email = r.get("email") or "sinemail@empresa.com"

        fecha = r.get("fechaInicio")
        if isinstance(fecha, (datetime, date)):
            fecha = fecha.strftime("%Y-%m-%d")

        salario = r.get("salario") or 0
        departamento = r.get("departamento")  # nombre del departamento

        return Empleado(
            idEmpleado=r.get("idEmpleado"),
            idPersona=r.get("idPersona"),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            fechaInicio=fecha,
            salario=salario,
            departamento=departamento,
            cargando_desde_bd=True
        )

    # ============================================================
    #  RESOLVER DEPARTAMENTO (acepta ID o nombre)
    # ============================================================
    def _resolverDepartamento(self, dep):
        if dep is None:
            return None

        dep = str(dep).strip()  # limpiar espacios

        con = getConexion()
        cur = con.cursor(dictionary=True)

        # Si es numérico → ID directo
        if dep.isdigit():
            sql = "SELECT idDepartamento FROM departamento WHERE idDepartamento = %s"
            cur.execute(sql, (dep,))
        else:
            # Comparación case-insensitive
            sql = "SELECT idDepartamento FROM departamento WHERE LOWER(nombre) = LOWER(%s)"
            cur.execute(sql, (dep,))

        row = cur.fetchone()
        cur.close()
        con.close()

        return row["idDepartamento"] if row else None

    # ============================================================
    #  GUARDAR EMPLEADO
    # ============================================================
    def guardar(self, empleado: Empleado):

        con = None
        cur = None

        try:
            # 1) Resolver ID del departamento
            depIngresado = empleado.getDepartamento()
            idDep = self._resolverDepartamento(depIngresado)

            if idDep is None:
                print("[EmpleadoDAO.guardar] ❌ Departamento inexistente (nombre o ID no válido).")
                return None

            # 2) Crear persona
            personaDAO = PersonaDAO()
            persona = Persona(
                nombre=empleado.getNombre(),
                apellido=empleado.getApellido(),
                telefono=empleado.getTelefono(),
                email=empleado.getEmail()
            )
            persona = personaDAO.guardar(persona)

            if persona is None:
                print("[EmpleadoDAO.guardar] ❌ No se pudo crear la persona.")
                return None

            empleado.setIdPersona(persona.getIdPersona())

            # 3) Insertar empleado
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
                idDep
            ))

            con.commit()
            empleado.setIdEmpleado(cur.lastrowid)

            return empleado

        except Exception as ex:
            print(f"[EmpleadoDAO.guardar] ERROR SQL: {ex}")
            if con:
                con.rollback()
            return None

        finally:
            if cur: cur.close()
            if con: con.close()

    # ============================================================
    #  LISTAR EMPLEADOS
    # ============================================================
    def listar(self):
        con = None
        cur = None
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT e.idEmpleado, e.idPersona, p.nombre, p.apellido,
                       p.telefono, p.email,
                       e.fechaInicio, e.salario,
                       d.nombre AS departamento
                FROM empleado e
                JOIN persona p ON e.idPersona = p.idPersona
                LEFT JOIN departamento d ON e.departamento = d.idDepartamento
                ORDER BY e.idEmpleado
            """

            cur.execute(sql)
            rows = cur.fetchall()

            return [self._crearEmpleadoDesdeDB(r) for r in rows]

        except Exception as ex:
            print(f"[EmpleadoDAO.listar] Error: {ex}")
            return []

        finally:
            if cur: cur.close()
            if con: con.close()

    # ============================================================
    #  BUSCAR POR ID
    # ============================================================
    def buscarPorId(self, idEmpleado):
        con = None
        cur = None
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT e.idEmpleado, e.idPersona, p.nombre, p.apellido,
                       p.telefono, p.email,
                       e.fechaInicio, e.salario,
                       d.nombre AS departamento
                FROM empleado e
                JOIN persona p ON e.idPersona = p.idPersona
                LEFT JOIN departamento d ON e.departamento = d.idDepartamento
                WHERE e.idEmpleado = %s
            """

            cur.execute(sql, (idEmpleado,))
            row = cur.fetchone()

            if not row:
                print(f"❌ No existe empleado con ID {idEmpleado}")
                return None

            return self._crearEmpleadoDesdeDB(row)

        except Exception as ex:
            print(f"[EmpleadoDAO.buscarPorId] Error: {ex}")
            return None

        finally:
            if cur: cur.close()
            if con: con.close()

    # ============================================================
    #  REASIGNAR DEPARTAMENTO
    # ============================================================
    def reasignarDepartamento(self, idEmpleado, nuevoDep):
        con = None
        cur = None
        try:
            idDep = self._resolverDepartamento(nuevoDep)
            if idDep is None:
                print("❌ El departamento NO existe (nombre o ID inválido).")
                return False

            con = getConexion()
            cur = con.cursor()

            sql = "UPDATE empleado SET departamento = %s WHERE idEmpleado = %s"
            cur.execute(sql, (idDep, idEmpleado))

            con.commit()
            return True

        except Exception as ex:
            print(f"Error al reasignar departamento: {ex}")
            if con:
                con.rollback()
            return False

        finally:
            if cur: cur.close()
            if con: con.close()
