#Herencia de Persona

from persona import Persona
class Empleado(Persona):
    _idEmpleado = None
    _direccion = None
    _fechaInicio = None
    _salario = None
    _departamento = None

    def __init__(self, idEmpleado, nombre, apellido, telefono, email, direccion, fechaInicio, salario, departamento=None):
        super().__init__(nombre, apellido, telefono, email)
        self._idEmpleado = idEmpleado
        self._direccion = direccion
        self._fechaInicio = fechaInicio
        self._salario = salario
        self._departamento = departamento

    def getIdEmpleado(self):
        return self._idEmpleado
    def getDireccion(self):
        return self._direccion
    def getFechaInicio(self):
        return self._fechaInicio
    def getSalario(self):
        return self._salario
    def getDepartamento(self):
        return self._departamento

    def setIdEmpleado(self, idEmpleado):
        self._idEmpleado = idEmpleado
    def setDireccion(self, direccion):
        self._direccion = direccion
    def setFechaInicio(self, fechaInicio):
        self._fechaInicio = fechaInicio
    def setSalario(self, salario):
        self._salario = salario
    def setDepartamento(self, departamento):
        self._departamento = departamento

    def __str__(self):
        return f"{super().__str__()}\nID: {self._idEmpleado}\nDirección: {self._direccion}\nFecha Inicio: {self._fechaInicio}\nSalario: {self._salario}\nDepartamento: {self._departamento}"
