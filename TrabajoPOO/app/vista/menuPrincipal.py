from app.vista.menuEmpleado import MenuEmpleado
from app.vista.menuDepartamento import MenuDepartamento
from app.vista.menuProyectos import MenuProyecto
from app.vista.menuRegistro import MenuRegistro
from app.vista.menuGerente import MenuGerente
from app.vista.menuInformes import MenuInformes  

class MenuPrincipal:

    def __init__(self, empSrv, depSrv, proSrv, regSrv, gerSrv):
        self.empSrv = empSrv
        self.depSrv = depSrv
        self.proSrv = proSrv
        self.regSrv = regSrv
        self.gerSrv = gerSrv

    def menu(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1) Empleados")
            print("2) Departamentos")
            print("3) Proyectos")
            print("4) Registros de Tiempo")
            print("5) Gerentes")
            print("6) Informes")        
            print("0) Salir")
            op = input("Opción: ")

            if op == "1":
                MenuEmpleado(self.empSrv).menu()
            elif op == "2":
                MenuDepartamento(self.depSrv, self.empSrv, self.gerSrv).menu()
            elif op == "3":
                MenuProyecto(self.proSrv).menu()
            elif op == "4":
                MenuRegistro(self.regSrv).menu()
            elif op == "5":
                MenuGerente(self.gerSrv).menu()
            elif op == "6":
                MenuInformes(self.regSrv, self.empSrv).menu()   
            elif op == "0":
                break
            else:
                print("Opción inválida")
