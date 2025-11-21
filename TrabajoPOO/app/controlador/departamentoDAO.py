from app.modelo.departamento import Departamento
from app.bd.conexion import getConexion


class DepartamentoDAO:

    #GUARDAR DEPARTAMENTO
    def guardar(self, departamento: Departamento):
        try:
            con = getConexion()
            cur = con.cursor()

            sql = "INSERT INTO departamento (nombre, idGerente) VALUES (%s, %s)"
            cur.execute(sql, (departamento.getNombre(), departamento.getIdGerente()))
            con.commit()

            departamento.setIdDepartamento(cur.lastrowid)

            return departamento

        except Exception as ex:
            print(f"Error en DAO al guardar departamento: {ex}")
            return None

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    #LISTA DEPARTAMENTOS
    def listar(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            cur.execute("""
                SELECT d.idDepartamento, d.nombre, d.idGerente,
                       g.departamentoACargo
                FROM departamento d
                LEFT JOIN gerente g ON d.idGerente = g.idGerente
            """)

            rows = cur.fetchall()
            deps = []

            for r in rows:
                dep = Departamento(
                    idDepartamento=r["idDepartamento"],
                    nombre=r["nombre"],
                    idGerente=r["idGerente"]
                )
                deps.append(dep)

            return deps

        except Exception as ex:
            print(f"Error DAO listar departamentos: {ex}")
            return []

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def buscarPorId(self, idDepartamento):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            cur.execute(
                "SELECT idDepartamento, nombre, idGerente FROM departamento WHERE idDepartamento = %s",
                (idDepartamento,)
            )
            row = cur.fetchone()

            if not row:
                return None

            return Departamento(
                idDepartamento=row["idDepartamento"],
                nombre=row["nombre"],
                idGerente=row["idGerente"]
            )

        except Exception as ex:
            print(f"Error DAO buscarPorId departamento: {ex}")
            return None

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def gerenteExiste(self, idGerente):
        try:
            con = getConexion()
            cur = con.cursor()

            cur.execute("SELECT idGerente FROM gerente WHERE idGerente = %s", (idGerente,))
            row = cur.fetchone()

            return row is not None

        except Exception as ex:
            print(f"Error DAO gerenteExiste: {ex}")
            return False

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def departamentoExiste(self, idDepartamento):
        try:
            con = getConexion()
            cur = con.cursor()

            cur.execute("SELECT idDepartamento FROM departamento WHERE idDepartamento = %s", (idDepartamento,))
            row = cur.fetchone()

            return row is not None

        except Exception as ex:
            print(f"Error DAO departamentoExiste: {ex}")
            return False

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def gerenteOcupado(self, idGerente):
        try:
            con = getConexion()
            cur = con.cursor()

            cur.execute("SELECT idDepartamento FROM departamento WHERE idGerente = %s", (idGerente,))
            row = cur.fetchone()

            return row is not None

        except Exception as ex:
            print(f"Error DAO gerenteOcupado: {ex}")
            return True 

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def asignarGerente(self, idDepartamento, idGerente):

        if not self.departamentoExiste(idDepartamento):
            return "DEP_NO_EXISTE"

        if not self.gerenteExiste(idGerente):
            return "GER_NO_EXISTE"

        if self.gerenteOcupado(idGerente):
            return "GER_OCUPADO"

        try:
            con = getConexion()
            cur = con.cursor()

            sql = "UPDATE departamento SET idGerente=%s WHERE idDepartamento=%s"
            cur.execute(sql, (idGerente, idDepartamento))
            con.commit()

            return True

        except Exception as ex:
            print(f"Error DAO asignarGerente: {ex}")
            return False

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    def quitarGerente(self, idDepartamento):

        try:
            con = getConexion()
            cur = con.cursor()

            sql = "UPDATE departamento SET idGerente = NULL WHERE idDepartamento = %s"
            cur.execute(sql, (idDepartamento,))
            con.commit()

            return True

        except Exception as ex:
            print(f"Error DAO quitarGerente: {ex}")
            return False

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass
