class Departamento:
    _idDepartamento = None
    _nombre = None
    _gerente = None  # instancia de Gerente

    def __init__(self, idDepartamento, nombre, gerente=None):
        self._idDepartamento = idDepartamento
        self._nombre = nombre
        self._gerente = gerente


    def getIdDepartamento(self):
        return self._idDepartamento
    def getNombre(self):
        return self._nombre
    def getGerente(self):
        return self._gerente


    def setIdDepartamento(self, idDepartamento):
        self._idDepartamento = idDepartamento
    def setNombre(self, nombre):
        self._nombre = nombre
    def setGerente(self, gerente):
        self._gerente = gerente

    def __str__(self):
        return f"Departamento: {self._nombre}\nID: {self._idDepartamento}\nGerente: {self._gerente}"
