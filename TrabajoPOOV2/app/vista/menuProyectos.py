from app.modelo.proyecto import Proyecto

class MenuProyecto:

    def __init__(self, proSrv):
        self.proSrv = proSrv

    def menu(self):
        while True:
            print("\n--- MENÚ PROYECTOS ---")
            print("1) Crear proyecto")
            print("2) Listar proyectos")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1":
                self.crear()
            elif op == "2":
                self.listar()
            elif op == "0":
                break
            else:
                print("Opción inválida")

    def crear(self):
        print("\n--- CREAR PROYECTO ---")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        
        try:
            idDepartamento = int(input("ID departamento: "))
        except:
            print("ID de departamento inválido, debe ser numérico.")
            return

        proyecto = Proyecto(
            nombre=nombre,
            descripcion=descripcion,
            idDepartamento=idDepartamento
        )

        resultado = self.proSrv.crear(proyecto)

        if resultado is None:
            print("No se pudo crear el proyecto. Verifique el ID del departamento.")
        else:
            print("Proyecto creado correctamente.")

    def listar(self):
        print("\n--- LISTADO DE PROYECTOS ---")
        proyectos = self.proSrv.listar()
        for p in proyectos:
            print(f"ID {p['idProyecto']} - {p['nombre']} - Departamento: {p['departamento']}")
