from app.modelo.departamento import Departamento
from app.bd.conexion import getConexion

class DepartamentoDAO:

    # ======================================================
    # GUARDAR DEPARTAMENTO
    # ======================================================
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

    # ======================================================
    # LISTAR DEPARTAMENTOS
    # ======================================================
    def listar(self):
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            cur.execute("""
                SELECT idDepartamento, nombre, idGerente
                FROM departamento
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

    # ======================================================
    # BUSCAR POR ID
    # ======================================================
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

    # ======================================================
    # VER SI DEPARTAMENTO EXISTE
    # ======================================================
    def departamentoExiste(self, idDepartamento):
        try:
            con = getConexion()
            cur = con.cursor()

            cur.execute(
                "SELECT idDepartamento FROM departamento WHERE idDepartamento = %s",
                (idDepartamento,)
            )
            return cur.fetchone() is not None

        except Exception as ex:
            print(f"Error DAO departamentoExiste: {ex}")
            return False

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    # ======================================================
    # VER SI UN DEPARTAMENTO YA TIENE GERENTE
    # ======================================================
    def departamentoTieneGerente(self, idDepartamento):
        try:
            con = getConexion()
            cur = con.cursor()

            cur.execute(
                "SELECT idGerente FROM departamento WHERE idDepartamento = %s AND idGerente IS NOT NULL",
                (idDepartamento,)
            )
            return cur.fetchone() is not None

        except Exception as ex:
            print(f"Error DAO departamentoTieneGerente: {ex}")
            return True

        finally:
            try:
                cur.close()
                con.close()
            except:
                pass

    # ======================================================
    # ASIGNAR GERENTE A UN DEPARTAMENTO
    # ======================================================
    def asignarGerente(self, idDepartamento, idGerente):

        # verificar existencia
        if not self.departamentoExiste(idDepartamento):
            return "DEP_NO_EXISTE"

        # verificar si departamento ya tiene gerente
        if self.departamentoTieneGerente(idDepartamento):
            return "DEP_OCUPADO"

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

    # ======================================================
    # QUITAR GERENTE
    # ======================================================
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
