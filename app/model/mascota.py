#clase padre para crear gatos y perros 
class Mascota:
    _chip=None
    _nombre= None
    _edad=None

    def __init__(self,chip,nombre,edad):
        self._chip=chip
        self._nombre=nombre
        self._edad=edad

    
    def getChip(self):
        return self._chip
    def getNombre(self):
        return self._nombre
    def getEdad(self):
        return self._edad

   #set: mutador 
    def setChip(self,chip):
        self._chip=chip
    def setNombre(self,nombre):
        self._nombre=nombre
    def setEdad(self,edad):
        self._edad=edad
    
    #metodo imprimir
    def __str__(self):
        return f"Chip: {self._chip} - Nombre:{self._nombre}({self._edad})"