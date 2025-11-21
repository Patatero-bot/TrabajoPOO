class RegistroTiempo:

    def __init__(self, idRegistro=None, idEmpleado=None, idProyecto=None,
                 fecha=None, horas=None, descripcion=None):

        #Validaciones básicas
        if idEmpleado is None or not str(idEmpleado).isdigit():
            raise ValueError("El idEmpleado debe ser numérico.")

        if idProyecto is None or not str(idProyecto).isdigit():
            raise ValueError("El idProyecto debe ser numérico.")

        if fecha is None or len(str(fecha).split("-")) != 3:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD.")

        if horas is None or not str(horas).isdigit():
            raise ValueError("Las horas deben ser un número entero.")

        self._idRegistro = idRegistro
        self._idEmpleado = int(idEmpleado)
        self._idProyecto = int(idProyecto)
        self._fecha = str(fecha)
        self._horas = int(horas)
        self._descripcion = descripcion if descripcion else ""


    def getIdRegistro(self): 
        return self._idRegistro
    def getIdEmpleado(self): 
        return self._idEmpleado
    def getIdProyecto(self): 
        return self._idProyecto
    def getFecha(self): 
        return self._fecha
    def getHoras(self): 
        return self._horas
    def getDescripcion(self): 
        return self._descripcion


    def setIdRegistro(self, v): 
        self._idRegistro = v
    def setIdEmpleado(self, v): 
        if not str(v).isdigit():
            raise ValueError("El idEmpleado debe ser numérico.")
        self._idEmpleado = int(v)
    def setIdProyecto(self, v): 
        if not str(v).isdigit():
            raise ValueError("El idProyecto debe ser numérico.")
        self._idProyecto = int(v)
    def setFecha(self, v):
        if v is None or len(str(v).split("-")) != 3:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD.")
        self._fecha = str(v)
    def setHoras(self, v):
        if not str(v).isdigit():
            raise ValueError("Las horas deben ser numéricas.")
        self._horas = int(v)
    def setDescripcion(self, v):
        self._descripcion = v if v else ""


    def __str__(self):
        return (
            f"Registro {self._idRegistro} | Emp:{self._idEmpleado} | "
            f"Proy:{self._idProyecto} | {self._fecha} | {self._horas}h"
        )
