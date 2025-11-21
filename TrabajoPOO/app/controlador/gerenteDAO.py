from app.bd.conexion import getConexion
from app.modelo.gerente import Gerente

class GerenteDAO:

    def guardar(self, gerente: Gerente):
        """Guarda un gerente recién creado (idGerente = idEmpleado)."""
        try:
            con = getConexion()
            cur = con.cursor()

            sql = "INSERT INTO gerente (idGerente, departamentoACargo) VALUES (%s, %s)"
            cur.execute(sql, (gerente.getIdGerente(), gerente.getDepartamentoACargo()))
            con.commit()

            cur.close()
            con.close()
            return gerente

        except Exception as ex:
            print("Error DAO guardar gerente:", ex)
            return None

    #LISTAR GERENTES
    def listar(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT 
                    g.idGerente,
                    p.nombre,
                    p.apellido,
                    g.departamentoACargo
                FROM gerente g
                INNER JOIN empleado e ON g.idGerente = e.idEmpleado
                INNER JOIN persona p ON e.idPersona = p.idPersona
            """
            cur.execute(sql)
            rows = cur.fetchall()

            gerentes = []
            for r in rows:
                ger = Gerente(
                    idGerente=r["idGerente"],
                    nombre=r["nombre"],
                    apellido=r["apellido"],
                    departamentoACargo=r["departamentoACargo"]
                )
                gerentes.append(ger)

            cur.close()
            con.close()
            return gerentes

        except Exception as ex:
            print("Error DAO listar gerentes:", ex)
            return []

    # BUSCAR POR ID
    def buscarPorId(self, idGerente):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = """
                SELECT 
                    g.idGerente,
                    p.nombre,
                    p.apellido,
                    g.departamentoACargo
                FROM gerente g
                INNER JOIN empleado e ON g.idGerente = e.idEmpleado
                INNER JOIN persona p ON e.idPersona = p.idPersona
                WHERE g.idGerente = %s
            """
            cur.execute(sql, (idGerente,))
            row = cur.fetchone()

            cur.close()
            con.close()

            if not row:
                return None

            return Gerente(
                idGerente=row["idGerente"],
                nombre=row["nombre"],
                apellido=row["apellido"],
                departamentoACargo=row["departamentoACargo"]
            )

        except Exception as ex:
            print("Error DAO buscarPorId:", ex)
            return None

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
            return True  


    def existeGerente(self, idGerente):
        return self.buscarPorId(idGerente) is not None

    #ACTUALIZAR DEPARTAMENTO A CARGO
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
