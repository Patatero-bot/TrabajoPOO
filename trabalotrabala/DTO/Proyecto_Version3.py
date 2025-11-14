from DAO.Conexion import ConexionBD

class Proyecto:
    def __init__(self, nombre, descripcion, iddepartamento, idproyecto=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.iddepartamento = iddepartamento
        self.idproyecto = idproyecto

    def guardar(self, conexion: ConexionBD):
        cursor = conexion.ejecutar(
            "INSERT INTO proyecto (nombre, descripcion, iddepartamento) VALUES (%s,%s,%s)",
            (self.nombre, self.descripcion, self.iddepartamento)
        )
        self.idproyecto = cursor.lastrowid if cursor else None
        print(f"Proyecto '{self.nombre}' creado." if cursor else "Error.")

    def modificar(self, conexion, nuevo_nombre=None, nueva_descripcion=None, nuevo_iddepartamento=None):
        try:
            conexion.ejecutar(
                """
                UPDATE proyecto 
                SET nombre = COALESCE(%s, nombre), 
                    descripcion = COALESCE(%s, descripcion), 
                    iddepartamento = %s
                WHERE idproyecto = %s
                """,
                (nuevo_nombre, nueva_descripcion, nuevo_iddepartamento, self.idproyecto)
            )
            print("Proyecto modificado correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def eliminar(self, conexion):
        try:
            insc = conexion.ejecutar(
                "SELECT COUNT(*) total FROM inscripcion_proyecto WHERE idproyecto = %s", 
                (self.idproyecto,)
            ).fetchone()["total"]
            regs = conexion.ejecutar(
                "SELECT COUNT(*) total FROM registros WHERE idproyecto = %s", 
                (self.idproyecto,)
            ).fetchone()["total"]
            if insc or regs:
                print("No se puede eliminar; hay asignaciones o registros.")
                return
            if input(f"¿Eliminar '{self.nombre}'? (SI/NO): ").lower() != "si":
                print("Cancelado.")
                return
            conexion.ejecutar("DELETE FROM proyecto WHERE idproyecto = %s", (self.idproyecto,))
            print(f"Proyecto '{self.nombre}' eliminado.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def listar(conexion):
        try:
            cursor = conexion.ejecutar(
                """
                SELECT p.idproyecto, p.nombre, p.descripcion, p.iddepartamento, d.nombre AS departamento
                FROM proyecto p LEFT JOIN departamento d ON p.iddepartamento = d.iddepartamento
                ORDER BY p.idproyecto
                """
            )
            proyectos = cursor.fetchall() if cursor else []
            for p in proyectos:
                p['departamento'] = p['departamento'] or "Sin asignar"
            return proyectos
        except Exception as e:
            print(f"Error: {e}")
            return []