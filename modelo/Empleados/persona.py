class Persona:
    _nombre = None
    _apellido = None
    _telefono = None
    _email = None

    def __init__(self, nombre, apellido, telefono, email):
        self._nombre = nombre
        self._apellido = apellido
        self._telefono = telefono
        self._email = email

    # Getters
    def getNombre(self):
        return self._nombre
    def getApellido(self):
        return self._apellido
    def getTelefono(self):
        return self._telefono
    def getEmail(self):
        return self._email

    # Setters
    def setNombre(self, nombre):
        self._nombre = nombre
    def setApellido(self, apellido):
        self._apellido = apellido
    def setTelefono(self, telefono):
        self._telefono = telefono
    def setEmail(self, email):
        self._email = email

    def __str__(self):
        return f"Nombre: {self._nombre} {self._apellido}\nTeléfono: {self._telefono}\nEmail: {self._email}"