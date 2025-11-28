import requests 

def obtener_pokemones():
    try:
        respuesta = requests.get("https://pokeapi.co/api/v2/pokemon")
        pokemones = respuesta.json()
        print(pokemones)
    except:
        return "Error al obtener datos"
    
obtener_pokemones()