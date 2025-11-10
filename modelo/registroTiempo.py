class RegistroTiempo:
    _idRegistro = None
    _empleado = None
    _proyecto = None
    _fecha = None
    _horasTrabajadas = None
    _descripcion = None

    def __init__(self, idRegistro, empleado, proyecto, fecha, horasTrabajadas, descripcion):
        self._idRegistro = idRegistro
        self._empleado = empleado
        self._proyecto = proyecto
        self._fecha = fecha
        self._horasTrabajadas = horasTrabajadas
        self._descripcion = descripcion

    # Getters
    def getIdRegistro(self):
        return self._idRegistro
    def getEmpleado(self):
        return self._empleado
    def getProyecto(self):
        return self._proyecto
    def getFecha(self):
        return self._fecha
    def getHorasTrabajadas(self):
        return self._horasTrabajadas
    def getDescripcion(self):
        return self._descripcion

    # Setters
    def setIdRegistro(self, idRegistro):
        self._idRegistro = idRegistro
    def setEmpleado(self, empleado):
        self._empleado = empleado
    def setProyecto(self, proyecto):
        self._proyecto = proyecto
    def setFecha(self, fecha):
        self._fecha = fecha
    def setHorasTrabajadas(self, horasTrabajadas):
        self._horasTrabajadas = horasTrabajadas
    def setDescripcion(self, descripcion):
        self._descripcion = descripcion

    def __str__(self):
        return f"Registro #{self._idRegistro}\nEmpleado: {self._empleado.getNombre()} {self._empleado.getApellido()}\nProyecto: {self._proyecto.getNombre()}\nFecha: {self._fecha}\nHoras: {self._horasTrabajadas}\nDescripción: {self._descripcion}"
