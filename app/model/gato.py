from app.model.mascota import Mascota

class Gato(Mascota):
    __color=None
    
    def __init__(self, chip, nombre, edad, color):
        super().__init__(chip, nombre, edad)
        self.__color=color

    def getColor(self):
        return self.__color
    
    def setColor(self,color):
        self.__color=color

    def __str__(self):
        return super().__str__() + f" - color: {self.__color}"    
    