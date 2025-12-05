from app.modelo.empleado import Empleado

class Gerente(Empleado):

    def __init__(
        self,
        idGerente=None,
        idPersona=None,
        nombre=None,
        apellido=None,
        telefono=None,
        email=None,
        fechaInicio=None,
        salario=None,
        departamento=None,
        departamentoACargo=None,
        cargando_desde_bd=False
    ):

        # ============================================
        #  PASO 1 — Constructor de Empleado
        # ============================================
        super().__init__(
            idEmpleado=idGerente,
            idPersona=idPersona,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            fechaInicio=fechaInicio,
            salario=salario,
            departamento=departamento,
            cargando_desde_bd=cargando_desde_bd
        )

        # ============================================
        #  PASO 2 — Atributos propios del Gerente
        # ============================================
        self._idGerente = idGerente

        # Si viene desde BD → no validar nada
        if cargando_desde_bd:
            self._departamentoACargo = departamentoACargo
            return

        # Validación normal: debe existir, pero ES UN INT
        if departamentoACargo is None:
            raise ValueError("El departamento a cargo no es válido.")

        # Guardamos el ID del departamento sin usar strip
        self._departamentoACargo = departamentoACargo

    # ============================================================
    # GETTERS / SETTERS
    # ============================================================
    def getIdGerente(self):
        return self._idGerente

    def setIdGerente(self, value):
        self._idGerente = value

    def getDepartamentoACargo(self):
        return self._departamentoACargo

    def setDepartamentoACargo(self, value):
        if value is None:
            raise ValueError("El nombre del departamento no es válido.")
        self._departamentoACargo = value

    # ============================================================
    # REPRESENTACIÓN
    # ============================================================
    def __str__(self):
        return (
            f"Gerente {self._idGerente} - {self._nombre} {self._apellido} "
            f"- Departamento a cargo: {self._departamentoACargo}"
        )
