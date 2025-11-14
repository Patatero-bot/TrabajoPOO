from DTO.Usuario import Usuario
from DAO.Conexion import ConexionBD

class Empleado(Usuario):
    def __init__(self, username, password, nombre_completo, fono, email, direccion, fecha_inicio, salario, cargo, iddepartamento, idusuario=None, id_tipo=2):
        super().__init__(username, password, idusuario, id_tipo)
        self.nombre_completo = nombre_completo
        self.fono = fono
        self.email = email
        self.direccion = direccion
        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.cargo = cargo
        self.iddepartamento = iddepartamento

    def guardar(self, conexion: ConexionBD):
        cursor = conexion.ejecutar("INSERT INTO usuario (username, password, id_tipo) VALUES (%s,%s,%s)",
                                   (self.username, self.get_password(), self.id_tipo))
        if not cursor:
            print("Error al guardar usuario."); return
        self.idusuario = cursor.lastrowid
        conexion.ejecutar("""
            INSERT INTO persona (nombre_completo, fono, email, direccion, fecha_inicio, salario, cargo, idusuario, iddepartamento)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (self.nombre_completo, self.fono, self.email, self.direccion, self.fecha_inicio, self.salario, self.cargo, self.idusuario, self.iddepartamento))
        print(f"Empleado '{self.nombre_completo}' registrado.")

    @staticmethod
    def listar(conexion: ConexionBD):
        cursor = conexion.ejecutar("""
            SELECT p.idpersona, u.username, p.nombre_completo, p.fono, p.email, p.direccion,
                   p.fecha_inicio, p.salario, p.cargo, d.nombre AS departamento
            FROM persona p JOIN usuario u ON p.idusuario = u.idusuario
            LEFT JOIN departamento d ON p.iddepartamento = d.iddepartamento
            ORDER BY p.idpersona
        """)
        return cursor.fetchall() if cursor else []

    @staticmethod
    def modificar(conexion: ConexionBD):
        empleados = Empleado.listar(conexion)
        if not empleados:
            print("No hay empleados registrados."); return
        for e in empleados:
            print(f"{e['idpersona']}. {e['nombre_completo']} - Usuario: {e['username']} - Dep: {e['departamento']}")
        try:
            idp = int(input("ID empleado a modificar: ").strip())
        except:
            print("ID inválido."); return
        datos = conexion.ejecutar("SELECT * FROM persona WHERE idpersona = %s", (idp,)).fetchone()
        if not datos: print("Empleado no encontrado."); return
        def pmod(campo): return input(f"¿Modificar {campo}? [{datos[campo]}] SI/NO: ").lower() == "si"
        nombre_completo = input("Nuevo Nombre completo: ").strip() if pmod('nombre_completo') else datos['nombre_completo']
        fono = input("Nuevo Teléfono: ").strip() if pmod('fono') else datos['fono']
        email = input("Nuevo Email: ").strip() if pmod('email') else datos['email']
        direccion = input("Nueva Dirección: ").strip() if pmod('direccion') else datos['direccion']
        fecha_inicio = input("Nueva Fecha de inicio: ").strip() if pmod('fecha_inicio') else datos['fecha_inicio']
        salario = input("Nuevo Salario: ").strip() if pmod('salario') else datos['salario']
        cargo = input("Nuevo Cargo: ").strip() if pmod('cargo') else datos['cargo']
        departamentos = conexion.ejecutar("SELECT iddepartamento, nombre FROM departamento").fetchall()
        for d in departamentos: print(f"{d['iddepartamento']}. {d['nombre']}")
        print("0. Ninguno")
        iddepartamento = int(input("Nuevo ID de departamento (0 para Ninguno): ").strip()) if input(f"¿Modificar dept? [{datos['iddepartamento']}] SI/NO: ").lower() == "si" else datos['iddepartamento']
        if iddepartamento == 0: iddepartamento = None
        conexion.ejecutar("""
            UPDATE persona SET nombre_completo=%s, fono=%s, email=%s, direccion=%s,
            fecha_inicio=%s, salario=%s, cargo=%s, iddepartamento=%s WHERE idpersona=%s
        """, (nombre_completo, fono, email, direccion, fecha_inicio, salario, cargo, iddepartamento, idp))
        print(f"Empleado '{nombre_completo}' modificado.")