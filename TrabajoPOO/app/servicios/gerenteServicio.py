from app.controlador.gerenteDAO import GerenteDAO
from app.controlador.empleadoDAO import EmpleadoDAO
from app.controlador.departamentoDAO import DepartamentoDAO
from app.modelo.gerente import Gerente


class GerenteService:

    def __init__(self):
        self.gerDAO = GerenteDAO()
        self.empDAO = EmpleadoDAO()
        self.depDAO = DepartamentoDAO()

    #CREAR EMPLEADO
    def crearEmpleado(self, empleado):
        
        try:
            nuevoEmpleado = self.empDAO.guardar(empleado)

           
            if nuevoEmpleado is None:
                print("No se pudo crear el empleado antes de crear al gerente.")
                return None

            if getattr(nuevoEmpleado, "getIdPersona", None) is None:
                print("ERROR: El modelo Empleado DEBE tener getter/setter para idPersona.")
                return None

            if nuevoEmpleado.getIdEmpleado() is None:
                print("ERROR: No se generó idEmpleado al guardar.")
                return None

            return nuevoEmpleado

        except Exception as ex:
            print("Error en crearEmpleado:", ex)
            return None


    #CREAR GERENTE
    def crear(self, gerente: Gerente):
       
        try:
            depNombre = gerente.getDepartamentoACargo()

            if not depNombre or len(depNombre.strip()) < 2:
                print("Departamento inválido.")
                return None

            #Buscar departamento por nombre
            departamentos = self.depDAO.listar()
            depEncontrado = None
            for d in departamentos:
                if d.getNombre().lower() == depNombre.lower():
                    depEncontrado = d
                    break

            if not depEncontrado:
                print("El departamento no existe.")
                return None

            # Verificar si ya tiene gerente asignado
            if depEncontrado.getIdGerente() is not None:
                print("Este departamento ya tiene un gerente asignado.")
                return None

            #Verificar que el gerente tenga idGerente válido
            if gerente.getIdGerente() is None:
                print("Error: gerente.getIdGerente() es None.")
                return None

            #Crear registro en tabla gerente
            creado = self.gerDAO.guardar(gerente)

            if not creado:
                print("No se pudo crear el gerente en la base de datos.")
                return None

            #Asignar gerente al departamento
            asignado = self.depDAO.asignarGerente(
                depEncontrado.getIdDepartamento(),
                gerente.getIdGerente()
            )

            if asignado != "OK" and asignado is not True:
                print("Error al asignar gerente al departamento:", asignado)
                return None

            return creado

        except Exception as ex:
            print("Error al crear gerente:", ex)
            return None

    #LISTAR LOS GERENTES
    def listar(self):
        return self.gerDAO.listar()

    #BUSCAR POR ID
    def buscarPorId(self, idGerente):
        return self.gerDAO.buscarPorId(idGerente)

    #RE-ASIGNAR GERENTE A OTRO DEPARTAMENTO
    def reasignarDepartamento(self, idGerente, nuevoDep):

        #Validar gerente existe
        gerente = self.gerDAO.buscarPorId(idGerente)
        if not gerente:
            return "GER_NO_EXISTE"

        #Validar El departamento destino
        departamentos = self.depDAO.listar()
        depDestino = None

        for d in departamentos:
            if d.getNombre().lower() == nuevoDep.lower():
                depDestino = d
                break

        if not depDestino:
            return "DEP_NO_EXISTE"

        if depDestino.getIdGerente() is not None:
            return "DEP_OCUPADO"

        gerente.setDepartamentoACargo(nuevoDep)
        self.gerDAO.actualizarDepartamento(idGerente, nuevoDep)

        self.depDAO.asignarGerente(depDestino.getIdDepartamento(), idGerente)

        return True