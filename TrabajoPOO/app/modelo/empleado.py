import re
from datetime import date, datetime

class Empleado:

    def __init__(self, idEmpleado=None, idPersona=None, nombre=None, apellido=None,
                 telefono=None, email=None, fechaInicio=None,
                 salario=None, departamento=None,
                 cargando_desde_bd=False):

        self._cargando_desde_bd = cargando_desde_bd  

        self._idEmpleado = idEmpleado
        self._idPersona = idPersona

        self.setNombre(nombre)
        self.setApellido(apellido)
        self.setTelefono(telefono)
        self.setEmail(email)
        self.setFechaInicio(fechaInicio)
        self.setSalario(salario)
        self.setDepartamento(departamento)

        self._cargando_desde_bd = False


    def getIdEmpleado(self):
        return self._idEmpleado
    def getIdPersona(self):
        return self._idPersona
    def getNombre(self):
        return self._nombre
    def getApellido(self):
        return self._apellido
    def getTelefono(self):
        return self._telefono
    def getEmail(self):
        return self._email
    def getFechaInicio(self):
        return self._fechaInicio
    def getSalario(self):
        return self._salario
    def getDepartamento(self):
        return self._departamento

    def setIdEmpleado(self, value):
        self._idEmpleado = value
    def setIdPersona(self, value):
        self._idPersona = value
    def setNombre(self, value):
        if self._cargando_desde_bd:
            self._nombre = value
            return
        if value is None or len(value.strip()) < 2 or not value.replace(" ", "").isalpha():
            raise ValueError("El nombre debe tener al menos 2 letras y no contener números.")
        self._nombre = value.strip()
    def setApellido(self, value):
        if self._cargando_desde_bd:
            self._apellido = value
            return
        if value is None or len(value.strip()) < 2 or not value.replace(" ", "").isalpha():
            raise ValueError("El apellido debe tener al menos 2 letras y no contener números.")
        self._apellido = value.strip()
    def setTelefono(self, value):
        if self._cargando_desde_bd:
            self._telefono = value
            return
        if value is None:
            raise ValueError("El teléfono no puede estar vacío.")
        value = value.strip()
        if not re.fullmatch(r"[0-9]{8,15}", value):
            raise ValueError("El teléfono debe contener solo números y tener entre 8 y 15 dígitos.")
        self._telefono = value
    def setEmail(self, value):
        if self._cargando_desde_bd:
            self._email = value
            return
        if value is None or "@" not in value or "." not in value:
            raise ValueError("El email no es válido.")
        self._email = value.strip()
    def setFechaInicio(self, value):
        if self._cargando_desde_bd:
            self._fechaInicio = value
            return

        if isinstance(value, date):
            value = value.strftime("%Y-%m-%d")

        if isinstance(value, datetime):
            value = value.date().strftime("%Y-%m-%d")

        if isinstance(value, str):
            partes = value.split("-")
            if len(partes) != 3:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")
            self._fechaInicio = value
            return

        raise ValueError("Formato de fecha inválido.")
    def setSalario(self, value):
        if self._cargando_desde_bd:
            self._salario = value
            return

        try:
            value = float(value)
        except:
            raise ValueError("El salario debe ser un número válido.")

        if value <= 0:
            raise ValueError("El salario debe ser mayor a 0.")

        self._salario = value
    def setDepartamento(self, value):
        if self._cargando_desde_bd:
            self._departamento = value
            return

        if value is not None and len(value.strip()) < 2:
            raise ValueError("El nombre del departamento es demasiado corto.")
        self._departamento = value

    def __str__(self):
        return (
            f"Empleado {self._idEmpleado} - {self._nombre} {self._apellido} "
            f"- Departamento: {self._departamento}"
        )
