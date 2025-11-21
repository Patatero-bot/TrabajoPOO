import re

class Persona:

    def __init__(
        self,
        idPersona=None,
        nombre=None,
        apellido=None,
        telefono=None,
        email=None,
        cargando_desde_bd=False
    ):

        self._cargando_desde_bd = cargando_desde_bd

        self._idPersona = idPersona

        self.setNombre(nombre)
        self.setApellido(apellido)
        self.setTelefono(telefono)
        self.setEmail(email)

        self._cargando_desde_bd = False


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
            raise ValueError("El teléfono debe tener entre 8 y 15 dígitos y ser solo números.")

        self._telefono = value

    def setEmail(self, value):
        if self._cargando_desde_bd:
            self._email = value
            return

        if value is None or "@" not in value or "." not in value:
            raise ValueError("El email no es válido.")

        self._email = value.strip()


    def __str__(self):
        return (
            f"Persona {self._idPersona}: {self._nombre} {self._apellido} "
            f"- Tel: {self._telefono} - Email: {self._email}"
        )
