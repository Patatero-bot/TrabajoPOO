from app.controlador.departamentoDAO import DepartamentoDAO
from app.controlador.gerenteDAO import GerenteDAO
from app.modelo.departamento import Departamento


class DepartamentoService:

    def __init__(self, departamentoDAO: DepartamentoDAO):
        self.depDAO = departamentoDAO
        self.gerDAO = GerenteDAO()

    #CREAR DEPARTAMENTO
    def crear(self, departamento: Departamento):
        try:
            #Validar el largo del nombre
            if not departamento.getNombre() or len(departamento.getNombre().strip()) < 2:
                print("Error: nombre de departamento inválido.")
                return None

            if departamento.getIdGerente():
                gerente = self.gerDAO.buscarPorId(departamento.getIdGerente())
                if gerente is None:
                    print("Error: el gerente asignado no existe.")
                    return None

            return self.depDAO.guardar(departamento)

        except Exception as ex:
            print(f"Error al crear departamento: {ex}")
            return None


    #LISTAR LOS DEPARTAMENTOS
    def listar(self):
        try:
            return self.depDAO.listar()
        except Exception as ex:
            print(f"Error al listar departamentos: {ex}")
            return []


    #ASIGNAR GERENTE
    def asignarGerente(self, idDepartamento, idGerente):
        try:
            dep = self.depDAO.buscarPorId(idDepartamento)
            if not dep:
                return "DEP_NO_EXISTE"

            gerente = self.gerDAO.buscarPorId(idGerente)
            if not gerente:
                return "GER_NO_EXISTE"

            #Verifica si el gerente ya está asignado
            deps = self.depDAO.listar()
            for d in deps:
                if d.getIdGerente() == idGerente:
                    return "GER_OCUPADO"

            #Asignar Gerente
            self.depDAO.asignarGerente(idDepartamento, idGerente)
            return True

        except Exception as ex:
            print(f"Error al asignar gerente: {ex}")
            return None

    # QUITAR GERENTE
    def quitarGerente(self, idDepartamento):
        try:
            dep = self.depDAO.buscarPorId(idDepartamento)
            if not dep:
                return False

            return self.depDAO.quitarGerente(idDepartamento)

        except Exception as ex:
            print(f"Error al quitar gerente: {ex}")
            return False