from app.controller.mascota_dao import *
from app.model.gato import Gato
from app.model.perro import Perro

def crear_perro():
    print("CREAR PERRO")
    chip=int(input("Ingrese número chip: "))
    nombre=input("Ingrese nombre: ")
    edad=int(input("Ingrese edad: "))
    raza=input("Ingrese raza: ")
    perro = Perro(chip,nombre,edad,raza)
    if crearMascota(perro):
        print("Perro creado con éxito")
    else:
        print("No se pudo crear un perro")

def crear_gato():
    print("CREAR GATO")
    chip=int(input("Ingrese número chip: "))
    nombre=input("Ingrese nombre: ")
    edad=int(input("Ingrese edad: "))
    color=input("Ingrese color: ")
    gato = Gato(chip,nombre,edad,color)
    if crearMascota(gato):
        print("Gato creado con éxito")
    else:
        print("No se pudo crear el gato")        

def listar_mascotas():
    print("LISTA DE MASCOTAS")
    datos=listarMascotas()
    if datos:
        for m in datos:
            print(m)

def buscar_mascota():
    print("BUSCAR MASCOTA")
    chip = int(input("Ingrese chip de mascota a buscar:"))
    dato=buscarMascota(chip)
    if dato:
        print(dato)
    else: 
        print("Número de chip de mascota no existe ಠಿ_ಠ")

def actualizar_mascota():
    print("ACTUALIZAR MASCOTA")
    chip=int(input("Ingrese número chip mascota para actualizar: "))
    if buscarMascota(chip):
        nuevo_nombre=input("Ingrese nuevo nombre: ")
        nueva_edad=int(input("Ingrese nueva edad: "))
        tipo = int(input("INgrese tipo de mascota(1:perro, 2:gato): "))
        if tipo==1:
            atributo=input("Ingrese nueva raza: ")
            mascota=Perro(chip,nuevo_nombre,nueva_edad,atributo)
        elif tipo ==2:
            atributo=input("ingrese nuevo color: ")
            mascota=Gato(chip,nuevo_nombre,nueva_edad,atributo)
        else:
            print("Opcion incorrecta")
            return 
        if actualizarMascota(mascota):
            print("Mascota actualizada correctamente")
        else:
            print("No se pudo actualizar la mascota")
    else:
        print("Mascota no existe")

def elminar_mascota():
    print("ELIMINAR MASCOTA")
    chip=int(input("Ingrese número chip mascota a eliminar: "))
    if eliminarMascotas(chip):
        print("Mascota eliminada con éxito")
    else:
        print("No se pudo eliminar la mascota")
        