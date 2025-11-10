from empleado import Empleado
class Gerente(Empleado):
    _departamentoACargo = None
    _equipo = None  # lista de empleados

    def __init__(self, idEmpleado, nombre, apellido, telefono, email, direccion, fechaInicio, salario, departamentoACargo=None, equipo=None):
        super().__init__(idEmpleado, nombre, apellido, telefono, email, direccion, fechaInicio, salario, departamentoACargo)
        self._departamentoACargo = departamentoACargo
        self._equipo = equipo if equipo is not None else []

    # Getters
    def getDepartamentoACargo(self):
        return self._departamentoACargo
    def getEquipo(self):
        return self._equipo

    # Setters
    def setDepartamentoACargo(self, departamento):
        self._departamentoACargo = departamento
    def setEquipo(self, equipo):
        self._equipo = equipo
    def agregarEmpleado(self, empleado):
        self._equipo.append(empleado)

    def __str__(self):
        equipo_nombres = ", ".join([e.getNombre() for e in self._equipo]) if self._equipo else "Sin equipo asignado"
        return (f"{super().__str__()}\nCargo: Gerente\n"
                f"Departamento a cargo: {self._departamentoACargo.getNombre() if self._departamentoACargo else 'Ninguno'}\n"
                f"Equipo: {equipo_nombres}")
