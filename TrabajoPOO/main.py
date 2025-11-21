from app.bd.conexion import getConexion

from app.controlador.empleadoDAO import EmpleadoDAO
from app.controlador.departamentoDAO import DepartamentoDAO
from app.controlador.proyectoDAO import ProyectoDAO
from app.controlador.registroDAO import RegistroDAO

from app.servicios.empleadoServicio import EmpleadoService
from app.servicios.departamentoServicio import DepartamentoService
from app.servicios.proyectoServicio import ProyectoService
from app.servicios.registroServicio import RegistroService
from app.servicios.gerenteServicio import GerenteService

from app.vista.menuPrincipal import MenuPrincipal


def main():
    if not getConexion():
        print("No se pudo conectar a la base de datos.")
        return

   
    empleadoDAO = EmpleadoDAO()
    departamentoDAO = DepartamentoDAO()
    proyectoDAO = ProyectoDAO()
    registroDAO = RegistroDAO()

    empleadoService = EmpleadoService(empleadoDAO)
    departamentoService = DepartamentoService(departamentoDAO)
    proyectoService = ProyectoService(proyectoDAO)
    registroService = RegistroService(registroDAO)
    gerenteService = GerenteService()  

    menu = MenuPrincipal(
        empleadoService,
        departamentoService,
        proyectoService,
        registroService,
        gerenteService
    )
    menu.menu()


if __name__ == "__main__":
    main()