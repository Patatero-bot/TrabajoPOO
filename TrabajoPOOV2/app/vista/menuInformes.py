import pandas as pd

class MenuInformes:

    def __init__(self, regSrv, empSrv):
        self.regSrv = regSrv
        self.empSrv = empSrv

    def menu(self):
        while True:
            print("\n--- INFORMES ---")
            print("1) Exportar horas trabajadas (todos los empleados)")
            print("2) Exportar horas por empleado")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1":
                self.exportarHorasTodos()
            elif op == "2":
                self.exportarHorasEmpleado()
            elif op == "0":
                break
            else:
                print("Opción inválida")

    #Exportar las horas de todos los empleados
    def exportarHorasTodos(self):
        registros = self.regSrv.listar()

        if not registros:
            print("No hay registros de horas.")
            return

        data = []
        for r in registros:
            emp = self.empSrv.buscarPorId(r.getIdEmpleado())
            data.append({
                "Empleado": f"{emp.getNombre()} {emp.getApellido()}",
                "Proyecto ID": r.getIdProyecto(),
                "Fecha": r.getFecha(),
                "Horas": r.getHoras(),
                "Descripción": r.getDescripcion()
            })

        df = pd.DataFrame(data)
        df.to_excel("informe_horas_todos.xlsx", index=False)

        print("Informe generado: informe_horas_todos.xlsx")

    #Exportar horas por empleado
    def exportarHorasEmpleado(self):
        try:
            idEmp = int(input("ID del empleado: "))
        except:
            print("ID inválido")
            return

        emp = self.empSrv.buscarPorId(idEmp)
        if not emp:
            print("Empleado no encontrado")
            return

        registros = self.regSrv.buscarPorEmpleado(idEmp)
        if not registros:
            print("El empleado no tiene registros de horas")
            return

        data = []
        for r in registros:
            data.append({
                "Empleado": f"{emp.getNombre()} {emp.getApellido()}",
                "Proyecto ID": r.getIdProyecto(),
                "Fecha": r.getFecha(),
                "Horas": r.getHoras(),
                "Descripción": r.getDescripcion()
            })

        df = pd.DataFrame(data)
        nombre_archivo = f"informe_horas_empleado_{idEmp}.xlsx"
        df.to_excel(nombre_archivo, index=False)

        print(f"Informe generado: {nombre_archivo}")
