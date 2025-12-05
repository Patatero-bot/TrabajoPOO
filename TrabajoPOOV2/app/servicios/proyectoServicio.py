class ProyectoService:

    def __init__(self, dao):
        self._dao = dao

    def crear(self, proyecto):
        return self._dao.guardar(proyecto)

    def listar(self):
        return self._dao.listar()