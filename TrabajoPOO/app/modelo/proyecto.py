class Proyecto:
    _idProyecto = None
    _nombre = None
    _descripcion = None
    _idDepartamento = None

    def __init__(self, idProyecto=None, nombre=None, descripcion=None, idDepartamento=None):
        self._idProyecto = idProyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._idDepartamento = idDepartamento

    def getIdProyecto(self): return self._idProyecto
    def getNombre(self): return self._nombre
    def getDescripcion(self): return self._descripcion
    def getIdDepartamento(self): return self._idDepartamento

    def setIdProyecto(self, v): self._idProyecto = v
    def setNombre(self, v): self._nombre = v
    def setDescripcion(self, v): self._descripcion = v
    def setIdDepartamento(self, v): self._idDepartamento = v

    def __str__(self):
        return f"Proyecto {self._idProyecto} - {self._nombre}"