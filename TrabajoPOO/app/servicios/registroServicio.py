from app.modelo.registro import RegistroTiempo

class RegistroService:

    def __init__(self, dao):
        self._dao = dao

  
    def crear(self, data: dict):
        try:
            registro = RegistroTiempo(
                idRegistro=None,
                idEmpleado=data["idEmpleado"],
                idProyecto=data["idProyecto"],
                fecha=data["fecha"],
                horas=data["horas"],
                descripcion=data.get("descripcion")
            )
            return self._dao.guardar(registro)

        except Exception as ex:
            print(f"Error en RegistroService.crear: {ex}")
            return None

   
    def registrar(self, idEmpleado, idProyecto, fecha, horas, descripcion=None):
        try:
            registro = RegistroTiempo(
                idRegistro=None,
                idEmpleado=idEmpleado,
                idProyecto=idProyecto,
                fecha=fecha,
                horas=horas,
                descripcion=descripcion
            )
            return self._dao.guardar(registro)

        except Exception as ex:
            print(f"Error en RegistroService.registrar: {ex}")
            return None


    def listar(self):
        return self._dao.listar()

    def listarPorEmpleado(self, idEmpleado):
        return self._dao.listarPorEmpleado(idEmpleado)

    def buscarPorEmpleado(self, idEmpleado):
        return self._dao.listarPorEmpleado(idEmpleado)
