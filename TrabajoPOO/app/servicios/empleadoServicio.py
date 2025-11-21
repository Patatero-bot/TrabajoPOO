class EmpleadoService:

    def __init__(self, dao):
        self._dao = dao

    def crear(self, empleado):
        try:
            return self._dao.guardar(empleado)
        except Exception as ex:
            print(f"Error Servicio crear empleado: {ex}")
            return None

    def listar(self):
        try:
            return self._dao.listar()
        except Exception as ex:
            print(f"Error Servicio listar empleados: {ex}")
            return []

    def buscarPorId(self, idEmpleado):
        
        try:
            return self._dao.buscarPorId(idEmpleado)
        except Exception as ex:
            print(f"Error Servicio buscarPorId: {ex}")
            return None

    def reasignarDepartamento(self, idEmpleado, nuevoDepartamento):
        
        try:
            # Validar que el empleado exista
            emp = self.buscarPorId(idEmpleado)
            if not emp:
                
                return False

            if not self._dao.departamentoExiste(nuevoDepartamento):
               
                return False

            # Realizar reasignación
            return self._dao.reasignarDepartamento(idEmpleado, nuevoDepartamento)

        except Exception as ex:
            print(f"Error Servicio reasignarDepartamento: {ex}")
            return False