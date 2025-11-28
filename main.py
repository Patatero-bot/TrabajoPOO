from app.view.mascota_view import *
import msvcrt, os 

menu="""MENU
1.Crear gato
2.Crear perro
3.Ver mascotas
4.Buscar mascota
5.actualizar mascota
6.elimnar mascota
0.Salir"""

while True:
    os.system('cls')
    print(menu)
    opcion=input("Ingrese opción del menú: ")
    os.system('cls')
    if opcion=="0":
        print("Gracias, chau (～￣▽￣)～")
        break
    elif opcion=="1":
        crear_gato()
    elif opcion=="2":
        crear_perro()
    elif opcion=="3":
        listar_mascotas()
    elif opcion=="4":
        buscar_mascota()
    elif opcion=="5":
        actualizar_mascota()
    elif opcion=="6":
        elminar_mascota()
    else:
        print("Error, opcion no valida")
    print("\n...presione una tecla para continuar...")
    msvcrt.getch()