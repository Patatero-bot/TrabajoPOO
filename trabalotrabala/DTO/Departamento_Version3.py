from DAO.Conexion import ConexionBD

class Departamento:
    def __init__(self, nombre, iddepartamento=None):
        self.nombre = nombre
        self.iddepartamento = iddepartamento

    def guardar(self, conexion: ConexionBD):
        cursor = conexion.ejecutar(
            "INSERT INTO departamento (nombre) VALUES (%s)",
            (self.nombre,)
        )
        self.iddepartamento = cursor.lastrowid if cursor else None
        print(f"Departamento '{self.nombre}' creado." if cursor else "Error al crear.")

    def modificar(self, conexion: ConexionBD, nuevo_nombre):
        if not self.iddepartamento:
            print("Departamento sin ID.")
            return
        cursor = conexion.ejecutar(
            "UPDATE departamento SET nombre=%s WHERE iddepartamento=%s",
            (nuevo_nombre, self.iddepartamento)
        )
        self.nombre = nuevo_nombre if cursor else self.nombre
        print(f"Modificado a '{self.nombre}'." if cursor else "Error al modificar.")

    def eliminar(self, conexion):
        try:
            emp = conexion.ejecutar(
                "SELECT COUNT(*) total FROM persona WHERE iddepartamento=%s",
                (self.iddepartamento,)
            ).fetchone()["total"]
            proy = conexion.ejecutar(
                "SELECT COUNT(*) total FROM proyecto WHERE iddepartamento=%s",
                (self.iddepartamento,)
            ).fetchone()["total"]
            if emp or proy:
                print("No se puede eliminar; tiene empleados/proyectos asociados.")
                return
            conexion.ejecutar(
                "DELETE FROM departamento WHERE iddepartamento=%s",
                (self.iddepartamento,)
            )
            print(f"Departamento '{self.nombre}' eliminado.")
        except Exception as e:
            print(f"Error al eliminar: {e}")

    @staticmethod
    def listar(conexion: ConexionBD):
        cursor = conexion.ejecutar("SELECT iddepartamento, nombre FROM departamento")
        return cursor.fetchall() if cursor else []