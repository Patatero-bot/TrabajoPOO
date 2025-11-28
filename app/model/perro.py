from app.model.mascota import Mascota

class Perro(Mascota):
    __raza=None
    
    def __init__(self, chip, nombre, edad, raza):
        super().__init__(chip, nombre, edad)
        self.__raza=raza

    def getRaza(self):
        return self.__raza
    
    def setRaza(self,raza):
        self.__raza=raza

    def __str__(self):
        return super().__str__() + f" - Raza: {self.__raza}"    
    