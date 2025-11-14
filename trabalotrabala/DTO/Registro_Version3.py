from DAO.Conexion_Version3 import ConexionBD

class Registro:
    def __init__(self, descripcion, horas_laborales, idpersona, idproyecto, fecha):
        self.descripcion = descripcion
        self.horas_laborales = horas_laborales
        self.idpersona = idpersona
        self.idproyecto = idproyecto
        self.fecha = fecha

    def guardar(self, conexion: ConexionBD):
        cursor = conexion.ejecutar(
            "INSERT INTO registros (descripcion, horas_laborales, idpersona, idproyecto, fecha) VALUES (%s, %s, %s, %s, %s)",
            (self.descripcion, self.horas_laborales, self.idpersona, self.idproyecto, self.fecha)
        )
        print("Registro guardado." if cursor else "Error.")

    @staticmethod
    def listar_por_empleado(conexion: ConexionBD, idpersona):
        cursor = conexion.ejecutar(
            """
            SELECT r.idregistros, r.fecha, r.descripcion, r.horas_laborales, p.nombre AS proyecto
            FROM registros r
            JOIN proyecto p ON r.idproyecto = p.idproyecto
            WHERE r.idpersona = %s ORDER BY r.fecha DESC
            """, 
            (idpersona,)
        )
        return cursor.fetchall() if cursor else []
