from app.modelo.empleado import Empleado

class MenuEmpleado:

    def __init__(self, empSrv):
        self.empSrv = empSrv

    # MENÚ PRINCIPAL
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
            departamento = input("Departamento: ").strip()

            # Validar fecha formato
            if not self._validarFecha(fechaInicio):
                print("Formato de fecha inválido (use YYYY-MM-DD).")
                return

            emp = Empleado(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                fechaInicio=fechaInicio,
                salario=salario,
                departamento=departamento
            )

            self.empSrv.crear(emp)
            print("Empleado registrado correctamente.")

        except ValueError as e:
            print("Error:", str(e))

        except Exception as e:
            print("Error inesperado:", str(e))

    #LISTAR EMPLEADOS
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
                    f"{e.getDepartamento()}"
                )

        except Exception as ex:
            print(f"Error al listar empleados: {ex}")

    #Re-ASIGNAR EMPLEADO A UN DEPARTAMENTO
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

            nuevoDep = input("Nuevo departamento: ").strip()
            if len(nuevoDep) < 2:
                print("Nombre de departamento inválido.")
                return

            if self.empSrv.reasignarDepartamento(idEmpleado, nuevoDep):
                print("Departamento actualizado.")
            else:
                print("No se pudo actualizar el departamento.")

        except Exception as ex:
            print(f"Error al reasignar departamento: {ex}")

    #VALIDA FECHA
    def _validarFecha(self, fecha):
        try:
            partes = fecha.split("-")
            if len(partes) != 3:
                return False
            año, mes, dia = partes
            int(año), int(mes), int(dia)
            return len(año) == 4 and len(mes) == 2 and len(dia) == 2
        except:
            return False