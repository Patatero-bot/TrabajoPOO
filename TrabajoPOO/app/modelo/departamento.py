class Departamento:

    def __init__(self, idDepartamento=None, nombre=None, idGerente=None):
        self._idDepartamento = idDepartamento
        self._nombre = nombre
        self._idGerente = idGerente

    def getIdDepartamento(self):
        return self._idDepartamento
    def getNombre(self):
        return self._nombre
    def getIdGerente(self):
        return self._idGerente

    def setIdDepartamento(self, value):
        self._idDepartamento = value
    def setNombre(self, value):
        self._nombre = value
    def setIdGerente(self, value):
        self._idGerente = value