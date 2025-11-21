class Gerente:

    def __init__(self, idGerente=None, nombre=None, apellido=None, departamentoACargo=None):
        self._idGerente = idGerente
        self._nombre = nombre
        self._apellido = apellido
        self._departamentoACargo = departamentoACargo

    def getIdGerente(self):
        return self._idGerente

    def getNombre(self):
        return self._nombre

    def getApellido(self):
        return self._apellido

    def getDepartamentoACargo(self):
        return self._departamentoACargo

    def setIdGerente(self, value):
        self._idGerente = value

    def setNombre(self, value):
        self._nombre = value

    def setApellido(self, value):
        self._apellido = value

    def setDepartamentoACargo(self, value):
        self._departamentoACargo = value

    def __str__(self):
        return f"Gerente {self._idGerente} - {self._nombre} {self._apellido} - Departamento: {self._departamentoACargo}"