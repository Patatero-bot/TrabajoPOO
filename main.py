class Usuario:
    #Atributos (Falta añadir, Mati debe de hacer el diagrama)
    _nombre = None
    _correo = None 
    _rol = None

    def __init__(self, nombre, correo, rol):
        self._nombre = nombre
        self._correo = correo
        self._rol = rol

    def getNombre(self):
        return self._nombre
    def getCorreo(self):
        return self._correo
    def getRol(self):
        return self._rol
    
    def setNombre(self,nombre):
        self._nombre = nombre
    def setCorreo(self,correo):
        self._correo = correo
    def setRol(self,rol):
        self._rol = rol
        
    def __str__(self):
        return f"Nombre: {self._nombre}\nCorreo: {self._correo}\nRol: {self._rol}"


