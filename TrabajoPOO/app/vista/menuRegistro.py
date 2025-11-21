class MenuRegistro:

    def __init__(self, regSrv):
        self.regSrv = regSrv
    def menu(self):
        while True:
            print("\n--- MENÚ REGISTRO DE TIEMPO ---")
            print("1) Registrar horas")
            print("2) Listar registros por empleado")
            print("0) Volver")
            op = input("Opción: ").strip()

            if op == "1":
                self.registrar()
            elif op == "2":
                self.listar()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    #REGISTRAR HORAS
    def registrar(self):
        print("\n--- REGISTRAR HORAS DE TRABAJO ---")

        try:
            idEmpleado = input("ID Empleado: ").strip()
            idProyecto = input("ID Proyecto: ").strip()
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            horas = input("Horas trabajadas: ").strip()
            descripcion = input("Descripción (opcional): ").strip()

            if not idEmpleado.isdigit() or not idProyecto.isdigit():
                print("El ID debe ser numérico.")
                return

            if not horas.isdigit():
                print("Las horas deben ser un número entero.")
                return

            registro = self.regSrv.registrar(
                int(idEmpleado),
                int(idProyecto),
                fecha,
                int(horas),
                descripcion if descripcion else None
            )

            if registro:
                print("Registro guardado correctamente.")
            else:
                print("Error al guardar el registro.")

        except Exception as ex:
            print(f"Error inesperado al registrar: {ex}")

    #LISTAR REGISTROS POR EMPLEADO
    def listar(self):
        print("\n--- LISTAR REGISTROS POR EMPLEADO ---")

        try:
            idEmpleado = input("ID Empleado: ").strip()

            if not idEmpleado.isdigit():
                print("ID inválido.")
                return

            registros = self.regSrv.listarPorEmpleado(int(idEmpleado))

            if not registros:
                print("No hay registros para este empleado.")
                return

            print("\n--- RESULTADOS ---")
            for r in registros:
                print(
                    f"ID {r.getIdRegistro()} | "
                    f"Empleado: {r.getIdEmpleado()} | "
                    f"Proyecto: {r.getIdProyecto()} | "
                    f"Fecha: {r.getFecha()} | "
                    f"Horas: {r.getHoras()} | "
                    f"Descripción: {r.getDescripcion()}"
                )

        except Exception as ex:
            print(f"Error al listar registros: {ex}")
