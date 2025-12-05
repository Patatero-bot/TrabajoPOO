from app.controlador.gerenteDAO import GerenteDAO
from app.controlador.empleadoDAO import EmpleadoDAO
from app.controlador.departamentoDAO import DepartamentoDAO
from app.modelo.gerente import Gerente


class GerenteService:

    def __init__(self):
        self.gerDAO = GerenteDAO()
        self.empDAO = EmpleadoDAO()
        self.depDAO = DepartamentoDAO()

    # ==========================================================
    # CREAR EMPLEADO (PARTE PREVIA AL GERENTE)
    # ==========================================================
    def crearEmpleado(self, empleado):
        try:
            nuevoEmpleado = self.empDAO.guardar(empleado)

            if nuevoEmpleado is None:
                print("No se pudo crear el empleado antes de crear al gerente.")
                return None

            if nuevoEmpleado.getIdEmpleado() is None:
                print("ERROR: No se generó idEmpleado al guardar.")
                return None

            return nuevoEmpleado

        except Exception as ex:
            print("Error en crearEmpleado:", ex)
            return None

    # ==========================================================
    # CREAR GERENTE (departamentoACargo = ID DEL DEPARTAMENTO)
    # ==========================================================
    def crear(self, gerente: Gerente):
        try:
            idDepartamento = gerente.getDepartamentoACargo()

            # Validar tipo
            if not isinstance(idDepartamento, int):
                print("ERROR: departamentoACargo debe ser un ID (int).")
                return None

            # Validar que el departamento exista
            dep = self.depDAO.buscarPorId(idDepartamento)
            if not dep:
                print("El departamento no existe.")
                return None

            # Validar que NO tenga gerente asignado
            if dep.getIdGerente() is not None:
                print("Este departamento ya tiene un gerente asignado.")
                return None

            # Validar ID del gerente
            if gerente.getIdGerente() is None:
                print("Error: gerente.getIdGerente() es None.")
                return None

            # Crear el gerente en la tabla
            creado = self.gerDAO.guardar(gerente)
            if not creado:
                print("No se pudo crear el gerente en la base de datos.")
                return None

            # Asignar gerente al departamento
            asignado = self.depDAO.asignarGerente(idDepartamento, gerente.getIdGerente())

            if asignado not in (True, "OK"):
                print("Error al asignar gerente al departamento:", asignado)
                return None

            return creado

        except Exception as ex:
            print("Error al crear gerente:", ex)
            return None

    # ==========================================================
    # LISTAR
    # ==========================================================
    def listar(self):
        return self.gerDAO.listar()

    # ==========================================================
    # BUSCAR POR ID
    # ==========================================================
    def buscarPorId(self, idGerente):
        return self.gerDAO.buscarPorId(idGerente)

    # ==========================================================
    # REASIGNAR GERENTE A OTRO DEPARTAMENTO (por ID)
    # ==========================================================
    def reasignarDepartamento(self, idGerente, idNuevoDep):

        # Validar gerente existe
        gerente = self.gerDAO.buscarPorId(idGerente)
        if not gerente:
            return "GER_NO_EXISTE"

        # Validar departamento destino existe
        depDestino = self.depDAO.buscarPorId(idNuevoDep)
        if not depDestino:
            return "DEP_NO_EXISTE"

        # Validar que NO esté ocupado
        if depDestino.getIdGerente() is not None:
            return "DEP_OCUPADO"

        # Actualizar departamentoACargo en el modelo
        gerente.setDepartamentoACargo(idNuevoDep)

        # Actualizar en BD
        self.gerDAO.actualizarDepartamento(idGerente, idNuevoDep)

        # Asignar en tabla departamento
        self.depDAO.asignarGerente(idNuevoDep, idGerente)

        return True
