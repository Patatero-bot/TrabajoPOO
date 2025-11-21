from app.modelo.empleado import Empleado
from app.modelo.gerente import Gerente

class MenuGerente:

    def __init__(self, gerSrv):
        self.gerSrv = gerSrv

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

    #REGISTRAR GERENTE
    def registrar(self):
        print("\n--- REGISTRO DE GERENTE ---")

        try:
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            telefono = input("Telefono: ").strip()
            email = input("Email: ").strip()
            fechaInicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
            salario = float(input("Salario: ").strip())
            departamentoACargo = input("Departamento que dirigirá: ").strip()

            empleado = Empleado(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                fechaInicio=fechaInicio,
                salario=salario,
                departamento=departamentoACargo
            )

            nuevoEmpleado = self.gerSrv.crearEmpleado(empleado)
            idGerente = nuevoEmpleado.getIdEmpleado()

            gerente = Gerente(
                idGerente=idGerente,
                nombre=nombre,
                apellido=apellido,
                departamentoACargo=departamentoACargo
            )

            self.gerSrv.crear(gerente)

            print("Gerente registrado correctamente.")

        except ValueError as ex:
            print("Error:", ex)

        except Exception as ex:
            print("Error inesperado:", ex)

#Re-ASIGNAR GERENTE
    def reasignar(self):
        print("\n--- REASIGNAR GERENTE ---")

        try:
            idGerente = int(input("ID del gerente: ").strip())
            nuevoDep = input("Nuevo departamento: ").strip()

            result = self.gerSrv.reasignarDepartamento(idGerente, nuevoDep)

            if result:
                print("Gerente reasignado correctamente.")
            else:
                print("No se pudo reasignar el gerente.")

        except Exception as ex:
            print("Error inesperado:", ex)