class EmpleadoService:

    def __init__(self, dao):
        self._dao = dao

    # ============================================================
    # CREAR EMPLEADO
    # ============================================================
    def crear(self, empleado):
        try:
            return self._dao.guardar(empleado)
        except Exception as ex:
            print(f"Error Servicio crear empleado: {ex}")
            return None

    # ============================================================
    # LISTAR EMPLEADOS
    # ============================================================
    def listar(self):
        try:
            return self._dao.listar()
        except Exception as ex:
            print(f"Error Servicio listar empleados: {ex}")
            return []

    # ============================================================
    # BUSCAR POR ID
    # ============================================================
    def buscarPorId(self, idEmpleado):
        try:
            return self._dao.buscarPorId(idEmpleado)
        except Exception as ex:
            print(f"Error Servicio buscarPorId: {ex}")
            return None

    # ============================================================
    # REASIGNAR DEPARTAMENTO (CORREGIDO)
    # ============================================================
    def reasignarDepartamento(self, idEmpleado, nuevoDepartamento):

        try:
            # 1) Validar que el empleado exista
            emp = self.buscarPorId(idEmpleado)
            if not emp:
                print("❌ El empleado no existe.")
                return False

            # 2) Usar resolverDepartamento() para validar el departamento
            idDep = self._dao._resolverDepartamento(nuevoDepartamento)

            if idDep is None:
                print("❌ El departamento no existe.")
                return False

            # 3) Reasignar en BD
            return self._dao.reasignarDepartamento(idEmpleado, idDep)

        except Exception as ex:
            print(f"Error Servicio reasignarDepartamento: {ex}")
            return False
