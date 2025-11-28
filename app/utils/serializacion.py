import json 

def guardar_json(datos):
    try:
        with open("datos.json","w", encoding='UTF-8') as f:
            json.dump(datos,f,indent=4)
        print("Archivo guardado con éxito")
    except Exception as e:
        print("Error al guardad",e)