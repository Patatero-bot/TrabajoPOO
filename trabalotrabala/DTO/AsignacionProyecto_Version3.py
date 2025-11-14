from DAO.Conexion import ConexionBD

class AsignacionProyecto:
    @staticmethod
    def asignar_empleado(conexion: ConexionBD):
        empleados = conexion.ejecutar(
            "SELECT p.idpersona, p.nombre_completo, d.iddepartamento, d.nombre AS departamento FROM persona p JOIN departamento d ON p.iddepartamento = d.iddepartamento"
        ).fetchall()
        if not empleados:
            print("No hay empleados registrados.")
            return
        for e in empleados:
            print(f"{e['idpersona']}. {e['nombre_completo']} - Departamento: {e['departamento']}")
        id_empleado = int(input("ID empleado: ").strip())
        empleado = next((e for e in empleados if e['idpersona'] == id_empleado), None)
        if not empleado:
            print("ID de empleado inválido.")
            return
        proyectos = conexion.ejecutar(
            "SELECT idproyecto, nombre FROM proyecto WHERE iddepartamento = %s",
            (empleado['iddepartamento'],)
        ).fetchall()
        if not proyectos:
            print(f"No hay proyectos en el departamento {empleado['departamento']}")
            return
        for p in proyectos:
            print(f"{p['idproyecto']}. {p['nombre']}")
        id_proyecto = int(input("ID proyecto: ").strip())
        proyecto = next((p for p in proyectos if p['idproyecto'] == id_proyecto), None)
        if not proyecto:
            print("ID de proyecto inválido.")
            return
        existente = conexion.ejecutar("SELECT * FROM inscripcion_proyecto WHERE idproyecto=%s AND idpersona=%s", (id_proyecto, id_empleado)).fetchone()
        if existente:
            print(f"Empleado ya asignado al proyecto '{proyecto['nombre']}'.")
            return
        conexion.ejecutar("INSERT INTO inscripcion_proyecto (idproyecto, idpersona) VALUES (%s, %s)", (id_proyecto, id_empleado))
        print(f"Empleado '{empleado['nombre_completo']}' asignado al proyecto '{proyecto['nombre']}' correctamente.")

    @staticmethod
    def listar_asignaciones(conexion: ConexionBD):
        asignaciones = conexion.ejecutar(
            """
            SELECT ip.idproyecto, ip.idpersona, pr.nombre AS proyecto, p.nombre_completo AS empleado, d.nombre AS departamento
            FROM inscripcion_proyecto ip
            JOIN proyecto pr ON ip.idproyecto = pr.idproyecto
            JOIN persona p ON ip.idpersona = p.idpersona
            JOIN departamento d ON pr.iddepartamento = d.iddepartamento
            """
        ).fetchall()
        if asignaciones:
            for a in asignaciones:
                print(f"Empleado: {a['empleado']} | Proyecto: {a['proyecto']} | Departamento: {a['departamento']}")
        else:
            print("No hay asignaciones registradas.")

    @staticmethod
    def eliminar_asignacion(conexion: ConexionBD):
        asignaciones = conexion.ejecutar(
            """
            SELECT ip.idinscripcion, pr.nombre AS proyecto, p.nombre_completo AS empleado, d.nombre AS departamento
            FROM inscripcion_proyecto ip
            JOIN proyecto pr ON ip.idproyecto = pr.idproyecto
            JOIN persona p ON ip.idpersona = p.idpersona
            JOIN departamento d ON pr.iddepartamento = d.iddepartamento ORDER BY d.nombre, pr.nombre
            """
        ).fetchall()
        if not asignaciones:
            print("No hay asignaciones registradas.")
            return
        for a in asignaciones:
            print(f"ID: {a['idinscripcion']} | Empleado: {a['empleado']} | Proyecto: {a['proyecto']} | Dept: {a['departamento']}")
        try:
            idinsc = int(input("ID a eliminar: ").strip())
        except:
            print("ID inválido.")
            return
        existe = conexion.ejecutar("SELECT * FROM inscripcion_proyecto WHERE idinscripcion=%s", (idinsc,)).fetchone()
        if not existe:
            print("No existe esa asignación.")
            return
        conexion.ejecutar("DELETE FROM inscripcion_proyecto WHERE idinscripcion=%s", (idinsc,))
        print("Asignación eliminada correctamente.")