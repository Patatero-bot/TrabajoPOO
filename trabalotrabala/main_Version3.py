from DAO.Conexion_Version3 import ConexionBD
from DTO.Empleado_Version3 import Empleado
from DTO.Departamento_Version3 import Departamento
from DTO.Proyecto_Version3 import Proyecto
from DTO.AsignacionProyecto_Version3 import AsignacionProyecto
from DTO.Registro_Version3 import Registro
from DTO.ExportarPDF_Version3 import ExportadorPDF
from DTO.ExportarExcel_Version3 import ExportadorExcel
from datetime import datetime
import getpass

def login(conexion):
    print("=== LOGIN DE USUARIO ===")
    print("1- Iniciar Sesión\n2- Salir")
    opcion = input("Opción: ")
    if opcion == '1':
        username = input("Usuario: ").strip()
        password = getpass.getpass("Contraseña: ").strip()
        hashed_password = conexion.hash_password(password)
        sql = """
            SELECT u.idusuario, u.username, t.descripcion AS tipo, p.idpersona
            FROM usuario u
            INNER JOIN tipo_usuario t ON u.id_tipo = t.idtipo_usuario
            LEFT JOIN persona p ON u.idusuario = p.idusuario
            WHERE u.username = %s AND u.password = %s
        """
        cursor = conexion.ejecutar(sql, (username, hashed_password))
        usuario = cursor.fetchone() if cursor else None
        if usuario:
            print(f"\nBienvenido {usuario['username']} ({usuario['tipo']})")
            tipo = usuario["tipo"].lower()
            if tipo == "administrador": menu_administrador(conexion)
            elif tipo == "empleado": menu_empleado(conexion, usuario['idpersona'])
            else: print("Tipo de usuario desconocido.")
        else:
            print("Usuario o contraseña incorrectos.")
        return True
    elif opcion == '2':
        return False
    print("Opción no válida.")
    return True

def menu_administrador(conexion):
    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Gestión de Empleados\n2. Gestión de Departamentos\n3. Gestión de Proyectos")
        print("4. Asignar Empleado a Proyecto\n5. Generar informe PDF\n6. Generar plantilla EXCEL\n0. Salir")
        opc = input("Opción: ")
        if   opc == "1": menu_gestion_empleado(conexion)
        elif opc == "2": menu_gestion_departamento(conexion)
        elif opc == "3": menu_gestion_proyecto(conexion)
        elif opc == "4": menu_asignar_empleado_proyecto(conexion)
        elif opc == "5": menu_generar_pdf(conexion)
        elif opc == "6": menu_generar_excel(conexion)
        elif opc == "0": print("Cerrando sesión..."); break
        else: print("Opción inválida.")

def menu_gestion_empleado(conexion):
    while True:
        print("====== Gestionar Empleado ======")
        print("1. Crear empleado\n2. Listar empleados\n3. Modificar empleado\n0. Volver")
        opc = input("Opción: ")
        if opc == '1':
            username = input("Usuario: ").strip()
            password = conexion.hash_password(input("Contraseña: ").strip())
            nombre = input("Nombre completo: ").strip()
            fono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            direccion = input("Dirección: ").strip()
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
            salario = input("Salario: ").strip()
            cargo = input("Cargo: ").strip()
            departamentos = conexion.ejecutar("SELECT iddepartamento, nombre FROM departamento").fetchall()
            if not departamentos: print("No hay departamentos."); continue
            for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
            while True:
                try:
                    iddepto = int(input("ID departamento: ").strip())
                    if any(d['iddepartamento'] == iddepto for d in departamentos): break
                    print("ID inválido.")
                except: print("Ingrese un número válido.")
            emp = Empleado(username, password, nombre, fono, email, direccion, fecha_inicio, salario, cargo, iddepto)
            emp.guardar(conexion)
        elif opc == '2':
            empleados = Empleado.listar(conexion)
            if empleados:
                for e in empleados:
                    print(f"ID: {e['idpersona']}\nUsuario: {e['username']}\nNombre: {e['nombre_completo']}\nCargo: {e['cargo']}\nSalario: {e['salario']}\nEmail: {e['email']}\nTeléfono: {e['fono']}\nDirección: {e['direccion']}\nDepartamento: {e['departamento']}\n----------------")
            else: print("No hay empleados.")
        elif opc == '3': Empleado.modificar(conexion)
        elif opc == '0': break
        else: print("Opción no válida.")

def menu_gestion_departamento(conexion):
    while True:
        print("\n=== GESTIÓN DE DEPARTAMENTOS ===")
        print("1. Crear departamento\n2. Modificar departamento\n3. Eliminar departamento\n4. Listar departamentos\n0. Volver")
        opc = input("Opción: ")
        if opc == "1":
            nombre = input("Nombre departamento: ").strip()
            Departamento(nombre).guardar(conexion)
        elif opc == "2":
            departamentos = Departamento.listar(conexion)
            if departamentos:
                for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
                id_sel = int(input("ID departamento a modificar: "))
                nuevo_nombre = input("Nuevo nombre: ").strip()
                Departamento(nuevo_nombre, iddepartamento=id_sel).modificar(conexion, nuevo_nombre)
            else: print("No hay departamentos.")
        elif opc == "3":
            departamentos = Departamento.listar(conexion)
            if departamentos:
                for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
                id_sel = int(input("ID departamento a eliminar: "))
                nombre_sel = next((d['nombre'] for d in departamentos if d['iddepartamento']==id_sel), None)
                if nombre_sel:
                    Departamento(nombre_sel, iddepartamento=id_sel).eliminar(conexion)
                else: print("ID inválido.")
            else: print("No hay departamentos.")
        elif opc == "4":
            departamentos = Departamento.listar(conexion)
            if departamentos:
                for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
            else: print("No hay departamentos.")
        elif opc == "0": break
        else: print("Opción inválida.")

def menu_gestion_proyecto(conexion):
    while True:
        print("\n=== GESTIÓN DE PROYECTOS ===")
        print("1. Crear proyecto\n2. Modificar proyecto\n3. Eliminar proyecto\n4. Listar proyectos\n0. Volver")
        opc = input("Opción: ")
        if opc == "1":
            nombre = input("Nombre proyecto: ").strip()
            descripcion = input("Descripción: ").strip()
            departamentos = conexion.ejecutar("SELECT iddepartamento, nombre FROM departamento").fetchall()
            if not departamentos: print("No hay departamentos."); continue
            for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
            while True:
                try:
                    iddepto = int(input("ID departamento: ").strip())
                    if any(d['iddepartamento'] == iddepto for d in departamentos): break
                    print("ID inválido.")
                except: print("Ingrese un número válido.")
            Proyecto(nombre, descripcion, iddepto).guardar(conexion)
        elif opc == "2":
            proyectos = Proyecto.listar(conexion)
            if not proyectos: print("No hay proyectos."); continue
            for p in proyectos: print(f"{p['idproyecto']}. {p['nombre']} - {p['departamento']}")
            id_sel = int(input("ID de proyecto a modificar: "))
            proyecto_sel = next((p for p in proyectos if p['idproyecto'] == id_sel), None)
            if proyecto_sel:
                nuevo_nombre = input(f"Nuevo nombre ({proyecto_sel['nombre']}): ").strip()
                nueva_descrip = input(f"Nueva descripción ({proyecto_sel['descripcion']}): ").strip()
                departamentos = conexion.ejecutar("SELECT iddepartamento, nombre FROM departamento").fetchall()
                for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
                print("0. Sin departamento asignado")
                nuevo_depto_str = input(f"Nuevo ID departamento ({proyecto_sel['departamento']}): ").strip()
                if nuevo_depto_str == "": iddepto = proyecto_sel.get('iddepartamento')
                elif nuevo_depto_str == "0": iddepto = None
                else: iddepto = int(nuevo_depto_str)
                Proyecto(proyecto_sel['nombre'], proyecto_sel['descripcion'], proyecto_sel.get('iddepartamento'), idproyecto=id_sel).modificar(conexion, nuevo_nombre or None, nueva_descrip or None, iddepto)
            else: print("ID inválido.")
        elif opc == "3":
            proyectos = Proyecto.listar(conexion)
            if not proyectos: print("No hay proyectos."); continue
            for p in proyectos: print(f"{p['idproyecto']}. {p['nombre']} - {p['departamento']}")
            id_sel = int(input("ID proyecto a eliminar: "))
            proyecto_sel = next((p for p in proyectos if p['idproyecto'] == id_sel), None)
            if proyecto_sel:
                Proyecto(proyecto_sel['nombre'], proyecto_sel['descripcion'],
                         proyecto_sel['iddepartamento'], idproyecto=id_sel).eliminar(conexion)
            else: print("ID inválido.")
        elif opc == "4":
            proyectos = Proyecto.listar(conexion)
            if proyectos:
                for p in proyectos: print(f"{p['idproyecto']}. {p['nombre']} - {p['descripcion']} - Departamento: {p['departamento']}")
            else: print("No hay proyectos.")
        elif opc == "0": break
        else: print("Opción inválida.")

def menu_asignar_empleado_proyecto(conexion):
    while True:
        print("\n=== ASIGNAR EMPLEADOS A PROYECTOS ===")
        print("1. Asignar empleado\n2. Listar asignaciones\n3. Eliminar asignación\n0. Volver")
        opc = input("Opción: ")
        if   opc == "1": AsignacionProyecto.asignar_empleado(conexion)
        elif opc == "2": AsignacionProyecto.listar_asignaciones(conexion)
        elif opc == "3": AsignacionProyecto.eliminar_asignacion(conexion)
        elif opc == "0": break
        else: print("Opción inválida.")

def menu_generar_pdf(conexion):
    while True:
        print("\n=== GENERAR INFORMES PDF ===")
        print("1. Empleados\n2. Proyectos\n0. Volver")
        opc = input("Opción: ")
        if opc == "1":
            filename = input("Nombre archivo (sin extensión) [informe_empleados]: ").strip() or "informe_empleados"
            ExportadorPDF.generar_informe_empleados(conexion, f"{filename}.pdf")
        elif opc == "2":
            filename = input("Nombre archivo (sin extensión) [informe_proyectos]: ").strip() or "informe_proyectos"
            ExportadorPDF.generar_informe_proyectos(conexion, f"{filename}.pdf")
        elif opc == "0": break
        else: print("Opción inválida.")

def menu_generar_excel(conexion):
    while True:
        print("\n=== GENERAR PLANTILLAS EXCEL ===")
        print("1. Empleados\n2. Proyectos\n0. Volver")
        opc = input("Opción: ")
        if opc == "1":
            filename = input("Nombre archivo (sin extensión) [plantilla_empleados]: ").strip() or "plantilla_empleados"
            ExportadorExcel.generar_plantilla_empleados(conexion, f"{filename}.xlsx")
        elif opc == "2":
            filename = input("Nombre archivo (sin extensión) [plantilla_proyectos]: ").strip() or "plantilla_proyectos"
            ExportadorExcel.generar_plantilla_proyectos(conexion, f"{filename}.xlsx")
        elif opc == "0": break
        else: print("Opción inválida.")

def menu_empleado(conexion, idpersona):
    while True:
        print("\n=== MENÚ EMPLEADO ===")
        print("1. Gestión de registros\n0. Salir")
        opc = input("Opción: ")
        if   opc == "1": menu_gestion_registros(conexion, idpersona)
        elif opc == "0": print("Cerrando sesión..."); break
        else: print("Opción inválida.")

def menu_gestion_registros(conexion, idpersona):
    while True:
        print("\n=== GESTIÓN DE REGISTROS ===")
        print("1. Crear registro\n2. Listar registros\n0. Volver")
        opc = input("Opción: ")
        if opc == '1':
            sql_proyectos = """
                SELECT ip.idproyecto, pr.nombre
                FROM inscripcion_proyecto ip
                JOIN proyecto pr ON ip.idproyecto = pr.idproyecto
                WHERE ip.idpersona = %s
            """
            cursor = conexion.ejecutar(sql_proyectos, (idpersona,))
            proyectos = cursor.fetchall()
            if not proyectos: print("No está asignado a ningún proyecto."); continue
            for p in proyectos: print(f"{p['idproyecto']}. {p['nombre']}")
            idproyecto = int(input("ID proyecto: "))
            descripcion = input("Descripción: ").strip()
            horas = input("Horas trabajadas: ").strip()
            fecha = input("Fecha (YYYY-MM-DD) [vacío=hoy]: ").strip() or datetime.now().strftime('%Y-%m-%d')
            Registro(descripcion, horas, idpersona, idproyecto, fecha).guardar(conexion)
        elif opc == '2':
            registros = Registro.listar_por_empleado(conexion, idpersona)
            if registros:
                for r in registros:
                    print(f"ID: {r['idregistros']}\nProyecto: {r['proyecto']}\nFecha: {r['fecha']}\nHoras: {r['horas_laborales']}\nDesc: {r['descripcion']}\n---------------")
            else: print("No tienes registros aún.")
        elif opc == '0': break
        else: print("Opción no válida.")

if __name__ == "__main__":
    conexion = ConexionBD()
    while True:
        if conexion.db:
            if not login(conexion): break
            conexion.cerrar()
        else:
            print("No se pudo conectar a la base de datos.")
