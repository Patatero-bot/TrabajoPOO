from app.modelo.empleado import Empleado

class MenuEmpleado:

    def __init__(self, empSrv, depSrv):
        self.empSrv = empSrv
        self.depSrv = depSrv

    def menu(self):
        while True:
            print("\n--- MENÚ EMPLEADOS ---")
            print("1) Registrar empleado")
            print("2) Listar empleados")
            print("3) Reasignar empleado a departamento")
            print("0) Volver")
            op = input("Opción: ").strip()

            if op == "1":
                self.registrar()
            elif op == "2":
                self.listar()
            elif op == "3":
                self.reasignarDepartamento()
            elif op == "0":
                break
            else:
                print("Opción inválida")

    # REGISTRAR EMPLEADO
    def registrar(self):
        print("\n--- REGISTRO DE EMPLEADO ---")

        try:
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            telefono = input("Telefono: ").strip()
            email = input("Email: ").strip()
            fechaInicio = input("Fecha inicio (YYYY-MM-DD): ").strip()

            salarioTexto = input("Salario: ").strip()
            if not salarioTexto.replace(".", "", 1).isdigit():
                print("El salario debe ser numérico.")
                return

            salario = float(salarioTexto)

            depNombre = input("Departamento (nombre): ").strip()

            # Buscar departamento por nombre
            dep = None
            for d in self.depSrv.listar():
                if d.getNombre().lower() == depNombre.lower():
                    dep = d
                    break

            if not dep:
                print("❌ ERROR: El departamento NO existe.")
                return

            emp = Empleado(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                fechaInicio=fechaInicio,
                salario=salario,
                departamento=dep.getIdDepartamento()
            )

            self.empSrv.crear(emp)
            print("Empleado registrado correctamente.")

        except Exception as e:
            print("Error inesperado:", str(e))

    # LISTAR EMPLEADOS
    def listar(self):
        print("\n--- LISTADO DE EMPLEADOS ---")

        try:
            empleados = self.empSrv.listar()

            if not empleados:
                print("No hay empleados registrados.")
                return

            for e in empleados:
                print(
                    f"ID {e.getIdEmpleado()} - "
                    f"{e.getNombre()} {e.getApellido()} - "
                    f"Departamento ID: {e.getDepartamento()}"
                )

        except Exception as ex:
            print(f"Error al listar empleados: {ex}")

    # RE-ASIGNAR EMPLEADO
    def reasignarDepartamento(self):
        print("\n--- REASIGNAR EMPLEADO ---")

        try:
            idInput = input("ID del empleado: ").strip()
            if not idInput.isdigit():
                print("El ID debe ser numérico.")
                return

            idEmpleado = int(idInput)

            empleado = self.empSrv.buscarPorId(idEmpleado)
            if not empleado:
                print("El empleado no existe.")
                return

            nuevoDepNombre = input("Nuevo departamento: ").strip()

            # Buscar departamento por nombre
            dep = None
            for d in self.depSrv.listar():
                if d.getNombre().lower() == nuevoDepNombre.lower():
                    dep = d
                    break

            if not dep:
                print("❌ ERROR: El departamento NO existe.")
                return

            if self.empSrv.reasignarDepartamento(idEmpleado, dep.getIdDepartamento()):
                print("Departamento actualizado.")
            else:
                print("No se pudo actualizar el departamento.")

        except Exception as ex:
            print(f"Error al reasignar departamento: {ex}")
