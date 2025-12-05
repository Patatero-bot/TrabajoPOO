from app.bd.conexion import getConexion
from app.modelo.gerente import Gerente

class GerenteDAO:

    # ============================================================
    # GUARDAR GERENTE
    # ============================================================
    def guardar(self, gerente: Gerente):
        """Inserta un gerente recién creado (idGerente = idEmpleado)."""
        try:
            con = getConexion()
            cur = con.cursor()

            sql = """
                INSERT INTO gerente (idGerente, departamentoACargo)
                VALUES (%s, %s)
            """
            cur.execute(sql, (
                gerente.getIdGerente(),
                gerente.getDepartamentoACargo()
            ))

            con.commit()
            cur.close()
            con.close()
            return gerente

        except Exception as ex:
            print("Error DAO guardar gerente:", ex)
            return None

    # ============================================================
    # LISTAR GERENTES
    # ============================================================
    def listar(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT 
                    g.idGerente,
                    g.departamentoACargo,
                    
                    e.idPersona,
                    e.fechaInicio,
                    e.salario,
                    e.departamento,

                    p.nombre,
                    p.apellido,
                    p.telefono,
                    p.email

                FROM gerente g
                INNER JOIN empleado e ON g.idGerente = e.idEmpleado
                INNER JOIN persona p ON e.idPersona = p.idPersona
                ORDER BY g.idGerente
            """

            cur.execute(sql)
            rows = cur.fetchall()

            gerentes = []

            for r in rows:
                gerente = Gerente(
                    idGerente=r["idGerente"],
                    idPersona=r["idPersona"],
                    nombre=r["nombre"],
                    apellido=r["apellido"],
                    telefono=r["telefono"],
                    email=r["email"],
                    fechaInicio=r["fechaInicio"],
                    salario=r["salario"],
                    departamento=r["departamento"],
                    departamentoACargo=r["departamentoACargo"],
                    cargando_desde_bd=True
                )
                gerentes.append(gerente)

            cur.close()
            con.close()
            return gerentes

        except Exception as ex:
            print("Error DAO listar gerentes:", ex)
            return []

    # ============================================================
    # BUSCAR POR ID
    # ============================================================
    def buscarPorId(self, idGerente):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT 
                    g.idGerente,
                    g.departamentoACargo,
                    
                    e.idPersona,
                    e.fechaInicio,
                    e.salario,
                    e.departamento,

                    p.nombre,
                    p.apellido,
                    p.telefono,
                    p.email

                FROM gerente g
                INNER JOIN empleado e ON g.idGerente = e.idEmpleado
                INNER JOIN persona p ON e.idPersona = p.idPersona
                WHERE g.idGerente = %s
            """

            cur.execute(sql, (idGerente,))
            r = cur.fetchone()

            cur.close()
            con.close()

            if not r:
                return None

            return Gerente(
                idGerente=r["idGerente"],
                idPersona=r["idPersona"],
                nombre=r["nombre"],
                apellido=r["apellido"],
                telefono=r["telefono"],
                email=r["email"],
                fechaInicio=r["fechaInicio"],
                salario=r["salario"],
                departamento=r["departamento"],
                departamentoACargo=r["departamentoACargo"],
                cargando_desde_bd=True
            )

        except Exception as ex:
            print("Error DAO buscarPorId:", ex)
            return None


    # ============================================================
    # VERIFICAR SI ESTÁ ASIGNADO A UN DEPTO
    # ============================================================
    def estaAsignado(self, idGerente):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = "SELECT idDepartamento FROM departamento WHERE idGerente = %s"
            cur.execute(sql, (idGerente,))
            row = cur.fetchone()

            cur.close()
            con.close()

            return row is not None

        except Exception as ex:
            print("Error DAO estaAsignado:", ex)
            return False

    # ============================================================
    # EXISTE GERENTE
    # ============================================================
    def existeGerente(self, idGerente):
        return self.buscarPorId(idGerente) is not None

    # ============================================================
    # ACTUALIZAR DEPARTAMENTO A CARGO
    # ============================================================
    def actualizarDepartamento(self, idGerente, nuevoDep):
        try:
            con = getConexion()
            cur = con.cursor()

            sql = "UPDATE gerente SET departamentoACargo=%s WHERE idGerente=%s"
            cur.execute(sql, (nuevoDep, idGerente))
            con.commit()

            cur.close()
            con.close()
            return True

        except Exception as ex:
            print("Error DAO actualizar departamento del gerente:", ex)
            return False
