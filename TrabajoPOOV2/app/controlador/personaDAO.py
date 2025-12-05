from app.bd.conexion import getConexion
from app.modelo.persona import Persona

class PersonaDAO:

    #INSERTAR PERSONA
    def guardar(self, persona: Persona):
        con = None
        cur = None
        try:
            if not isinstance(persona, Persona):
                print("[PersonaDAO.guardar] Se esperaba un objeto Persona.")
                return None

            con = getConexion()
            cur = con.cursor()

            sql = """
                INSERT INTO persona (nombre, apellido, telefono, email)
                VALUES (%s, %s, %s, %s)
            """

            cur.execute(sql, (
                persona.getNombre(),
                persona.getApellido(),
                persona.getTelefono(),
                persona.getEmail()
            ))

            con.commit()
            persona.setIdPersona(cur.lastrowid)
            return persona

        except Exception as ex:
            print(f"[PersonaDAO.guardar] Error al guardar persona: {ex}")
            return None

        finally:
            try:
                if cur: cur.close()
                if con: con.close()
            except:
                pass

    #BUSCAR PERSONA POR ID
    def buscar(self, idPersona):
        con = None
        cur = None
        try:
            con = getConexion()
            cur = con.cursor(dictionary=True)

            sql = "SELECT * FROM persona WHERE idPersona = %s"
            cur.execute(sql, (idPersona,))
            row = cur.fetchone()

            if not row:
                print(f"[PersonaDAO.buscar] No existe persona con ID {idPersona}.")
                return None

            return Persona(
                idPersona=row["idPersona"],
                nombre=row["nombre"],
                apellido=row["apellido"],
                telefono=row["telefono"],
                email=row["email"],
                cargando_desde_bd=True
            )

        except Exception as ex:
            print(f"[PersonaDAO.buscar] Error al buscar persona: {ex}")
            return None

        finally:
            try:
                if cur: cur.close()
                if con: con.close()
            except:
                pass
