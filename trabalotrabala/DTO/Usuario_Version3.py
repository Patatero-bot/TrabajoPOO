class Usuario:
    def __init__(self, username, password, idusuario=None, id_tipo=None):
        self.username = username
        self.__password = password
        self.idusuario = idusuario
        self.id_tipo = id_tipo

    def get_password(self):
        return self.__password

    def set_password(self, nueva_password):
        self.__password = nueva_password