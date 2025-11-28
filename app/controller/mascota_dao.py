#DAO=data access object
#se encarga de la lógica de validar y trabajar con la BD:
from app.conexion.conexion_mysql import obtener_conexion
from app.model.perro import Perro
from app.model.gato import Gato

def crearMascota(mascota):

    try:
      cone=obtener_conexion()
      if not cone:
            return
      cursor =cone.cursor()

      if isinstance(mascota,Perro):
            atributo = mascota.getRaza()
      elif isinstance(mascota,Gato):
            atributo=mascota.getColor()
      else:
          raise Exception("Tipo de mascota incorrecta!")
      sql="INSERT INTO mascota VALUES(%s,%s,%s,%s)"
      cursor.execute(sql,(mascota.getChip(),
                            mascota.getNombre(),
                            mascota.getEdad(),
                            atributo))
      cone.commit()
      return True
    except Exception as e:
        print("Error al crear mascota:",e)
    finally:
         if cone:
              cone.close()

def listarMascotas():
    try:
        cone=obtener_conexion()
        if not cone:
             return
        cursor = cone.cursor()
        cursor.execute("SELECT * FROM mascota")
        datos=cursor.fetchall()
        return datos
    except Exception as e:
             print("Error al listar mascotas:",e)
    finally:
         if cone:
              cone.close()         

def buscarMascota(chip):
    try:
        cone=obtener_conexion()
        if not cone:
             return
        cursor = cone.cursor()
        cursor.execute("SELECT * FROM mascota WHERE chip = %s",(chip,))
        dato=cursor.fetchone()
        return dato
    except Exception as e:
             print("Error al buscar mascota:",e)
    finally:
         if cone:
              cone.close()  

def actualizarMascota(mascota):

    try:
      cone=obtener_conexion()
      if not cone:
            return
      cursor =cone.cursor()

      if isinstance(mascota,Perro):
            atributo = mascota.getRaza()
      elif isinstance(mascota,Gato):
            atributo=mascota.getColor()
      else:
          raise Exception("Tipo de mascota incorrecta!")
      sql="UPDATE mascota SET nombre=%s, edad=%s, indicador=%s WHERE chip=%s"
      cursor.execute(sql,(mascota.getNombre(),
                            mascota.getEdad(),
                            atributo,
                            mascota.getChip()))
      cone.commit()
      return True
    except Exception as e:
        print("Error al actualizar mascota:",e)
    finally:
         if cone:
              cone.close()

def eliminarMascotas(chip):
    try:
        cone=obtener_conexion()
        if not cone:
             return
        cursor = cone.cursor()
        cursor.execute("DELETE FROM mascota WHERE chip=%s",(chip,))
        cone.commit()
        return True
    except Exception as e:
             print("Error al eliminar mascotas:",e)
    finally:
         if cone:
              cone.close()  

