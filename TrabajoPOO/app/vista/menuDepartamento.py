from app.modelo.departamento import Departamento

class MenuDepartamento:

    def __init__(self, depSrv, empSrv, gerSrv):
        self.depSrv = depSrv
        self.empSrv = empSrv
        self.gerSrv = gerSrv

    def menu(self):
        while True:
            print("\n--- MENÚ DEPARTAMENTOS ---")
            print("1) Crear departamento")
            print("2) Listar departamentos")
            print("3) Asignar gerente a departamento")
            print("4) Quitar gerente de departamento")
            print("5) Listar gerentes disponibles")
            print("0) Volver")
            op = input("Opción: ").strip()

            if op == "1":
                self.crear()
            elif op == "2":
                self.listar()
            elif op == "3":
                self.asignarGerente()
            elif op == "4":
                self.quitarGerente()
            elif op == "5":
                self.listarGerentesDisponibles()
            elif op == "0":
                break
            else:
                print("Opción inválida.")

    #CREAR UN DEPARTAMENTO
    def crear(self):
        print("\n--- CREAR DEPARTAMENTO ---")
        nombre = input("Nombre del departamento: ").strip()

        if len(nombre) < 2:
            print("El nombre es demasiado corto.")
            return

        print("\n¿Desea asignar un gerente ahora?")
        print("1) Sí")
        print("2) No")
        op = input("Opción: ").strip()

        idGerente = None

        if op == "1":
            self.listarGerentesDisponibles()
            _id = input("ID del gerente: ").strip()
            if _id.isdigit():
                idGerente = int(_id)
            else:
                print("ID inválido. Creando sin gerente.")
                idGerente = None

        dep = Departamento(nombre=nombre, idGerente=idGerente)
        resp = self.depSrv.crear(dep)

        if resp:
            print("Departamento creado.")
        else:
            print("Error al crear el departamento.")


    #LISTAR LOS DEPARTAMENTOS
    def listar(self):
        print("\n--- LISTADO DE DEPARTAMENTOS ---")
        deps = self.depSrv.listar()

        if not deps:
            print("No hay departamentos.")
            return

        for d in deps:
            gerente = d.getIdGerente() if d.getIdGerente() else "Sin gerente asignado"
            print(f"ID {d.getIdDepartamento()} - {d.getNombre()} - Gerente ID: {gerente}")


    #ASIGNAR A UN GERENTE A UN DEPARTAMENTO
    def asignarGerente(self):
        print("\n--- ASIGNAR GERENTE ---")

        self.listar()
        idDepInput = input("ID del departamento: ").strip()
        if not idDepInput.isdigit():
            print("El ID debe ser numérico.")
            return
        idDepartamento = int(idDepInput)

        self.listarGerentesDisponibles()
        idGerInput = input("ID del gerente a asignar: ").strip()
        if not idGerInput.isdigit():
            print("El ID debe ser numérico.")
            return
        idGerente = int(idGerInput)

        resultado = self.depSrv.asignarGerente(idDepartamento, idGerente)

        if resultado == True:
            print("Gerente asignado correctamente.")
        elif resultado == "DEP_NO_EXISTE":
            print("El departamento no existe.")
        elif resultado == "GER_NO_EXISTE":
            print("Este ID no corresponde a un gerente.")
        elif resultado == "GER_OCUPADO":
            print("Este gerente ya está asignado a un departamento.")
        else:
            print("Error inesperado.")

    #QUITAR EL GERENTE 
    def quitarGerente(self):
        print("\n--- QUITAR GERENTE ---")

        self.listar()
        idDepInput = input("ID del departamento: ").strip()

        if not idDepInput.isdigit():
            print("El ID debe ser numérico.")
            return

        idDepartamento = int(idDepInput)

        if self.depSrv.quitarGerente(idDepartamento):
            print("Gerente removido.")
        else:
            print("No se pudo remover el gerente.")

    #LISTAR LOS GERENTES DISPONIBLES
    def listarGerentesDisponibles(self):
        print("\n--- GERENTES DISPONIBLES ---")

        gerentes = self.gerSrv.listar()

        if not gerentes:
            print("No hay gerentes registrados.")
            return

        deps = self.depSrv.listar()
        ocupados = {d.getIdGerente() for d in deps if d.getIdGerente()}

        disponibles = [g for g in gerentes if g.getIdGerente() not in ocupados]

        if not disponibles:
            print("No hay gerentes disponibles.")
            return

        for g in disponibles:
            print(f"ID {g.getIdGerente()} - {g.getNombre()} {g.getApellido()}")