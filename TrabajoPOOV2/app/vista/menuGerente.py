from app.modelo.empleado import Empleado
from app.modelo.gerente import Gerente

class MenuGerente:

    def __init__(self, gerSrv, empSrv, depSrv):
        self.gerSrv = gerSrv
        self.empSrv = empSrv
        self.depSrv = depSrv

    def menu(self):
        while True:
            print("\n--- MENÚ GERENTES ---")
            print("1) Registrar gerente")
            print("2) Reasignar gerente a nuevo departamento")
            print("0) Volver")
            op = input("Opción: ").strip()

            if op == "1":
                self.registrar()
            elif op == "2":
                self.reasignar()
            elif op == "0":
                break
            else:
                print("Opción inválida")

    def buscarDepartamentoPorNombre(self, nombre):
        deps = self.depSrv.listar()
        for d in deps:
            if d.getNombre().lower() == nombre.lower():
                return d
        return None

    # =======================================================
    # REGISTRAR GERENTE (CORREGIDO)
    # =======================================================
    def registrar(self):
        print("\n--- REGISTRO DE GERENTE ---")

        try:
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            telefono = input("Telefono: ").strip()
            email = input("Email: ").strip()
            fechaInicio = input("Fecha inicio (YYYY-MM-DD): ").strip()

            # SALARIO
            try:
                salario = float(input("Salario: ").strip())
            except:
                print("❌ ERROR: El salario debe ser un número.")
                return

            # DEP NOMBRE
            depNombre = input("Departamento que dirigirá (nombre): ").strip()

            dep = self.buscarDepartamentoPorNombre(depNombre)
            if not dep:
                print("❌ ERROR: El departamento NO existe.")
                return

            if dep.getIdGerente():
                print("❌ ERROR: Este departamento ya tiene un gerente.")
                return

            # =============================
            # CREAR EMPLEADO
            # =============================
            empleado = Empleado(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                fechaInicio=fechaInicio,
                salario=salario,
                departamento=dep.getIdDepartamento()
            )

            nuevoEmpleado = self.gerSrv.crearEmpleado(empleado)
            if not nuevoEmpleado:
                print("❌ ERROR: No se pudo crear el empleado.")
                return

            idGerente = nuevoEmpleado.getIdEmpleado()

            # =============================
            # CREAR GERENTE
            # =============================
            gerente = Gerente(
                idGerente=idGerente,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                fechaInicio=fechaInicio,
                salario=salario,
                departamento=dep.getIdDepartamento(),
                departamentoACargo=dep.getIdDepartamento()
            )

            res = self.gerSrv.crear(gerente)
            if not res:
                print("❌ ERROR: No se pudo registrar el gerente en la BD.")
                return

            print("✅ Gerente registrado correctamente.")

        except Exception as ex:
            print("❌ Error inesperado:", ex)

    # =======================================================
    # RE-ASIGNAR GERENTE
    # =======================================================
    def reasignar(self):
        print("\n--- RE-ASIGNAR GERENTE ---")

        try:
            try:
                idGerente = int(input("ID del gerente: ").strip())
            except:
                print("❌ ERROR: El ID debe ser numérico.")
                return

            gerente = self.gerSrv.buscarPorId(idGerente)
            if not gerente:
                print("❌ ERROR: No existe un gerente con ese ID.")
                return

            depNombre = input("Nuevo departamento (nombre): ").strip()

            dep = self.buscarDepartamentoPorNombre(depNombre)
            if not dep:
                print("❌ ERROR: El departamento NO existe.")
                return

            if dep.getIdGerente():
                print("❌ ERROR: El departamento ya tiene un gerente.")
                return

            result = self.gerSrv.reasignarDepartamento(idGerente, dep.getIdDepartamento())

            if result is True:
                print("✅ Gerente reasignado correctamente.")
            else:
                print("❌ No se pudo reasignar el gerente.")

        except Exception as ex:
            print("❌ Error inesperado:", ex)
