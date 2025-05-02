import csv
from typing import Dict, Any, List
from datetime import  datetime, timedelta
import uuid
from exceptiones import IdInexistente

def mostrar_menu():
     print("-----------------------------")
     print("----------TO-DO LIST---------")
     print("-----------------------------")
     print("1. Agregar tarea")
     print("2. Ver tareas")
     print("3. Buscar tarea")
     print("4. Filtrar por prioridad")
     print("5. Mostrar vencidas")
     print("6. Marcar como completada")
     print("7. Eliminar tarea")
     print("8. OPCIÓN ADICIONAL:Exportar completados como txt")
     print("9. Guardar y salir")
     

def solicitar_opción() -> str:
     
     while True:
          valor = input("Ingrese el número de opción\n")
          if valor.isdigit() and 1<=int(valor)<=9: 
               return valor
          
          print("❗El valor ingresado no es válido. Por favor vuelva a intentar")

              
     

def listar_tareas(tareas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
     
     #ordena las tareas con fecha de vencimiento la más antigua a la más reciente
     tareas.sort(key= lambda tarea: tarea["fecha_vencimiento"])
     
     for tarea in tareas:
          #asignar valores a una variable
          id_tarea = tarea["id"] 
          titulo = tarea["titulo"] 
          fecha_venc = tarea["fecha_vencimiento"] 
          prioridad = tarea["prioridad"] 
          if tarea["completada"] == True:
               completada = "✘"
          else:
               completada = " "

          #mostrar detalle de la tarea en la consola
          print(f"ID: {id_tarea} | [{completada}] {titulo} | 🕒 {fecha_venc} | Prioridad: {prioridad}")


def agregar_tareas(tareas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

     id_tarea = str(uuid.uuid4())
     titulo = input("Definir título de la tarea\n")
     desc = input("Definir descripción\n")

     #Validar el ingreso de la fecha de vencimiento
     while True:
          try: 
               fecha_venc = input("Definir fecha de vencimiento en formato 'YYYY-MM-DD'\n")
               fecha = datetime.strptime(fecha_venc,"%Y-%m-%d").date()
               break
          except ValueError:
               print("❗El valor ingresado no tiene el formato correto, vuelva a ingresar el valor")

     #Validar el ingreso de la prioridad
     while True:
          prioridad = input("Definir prioridad 'Alta', 'Media' o 'Baja' \n").capitalize()
          if prioridad not in ["Alta", "Media", "Baja"]:
               print("❗El valor ingresado no es correcto, vuelva a ingresar el valor")
          else:
               break


     completada = False

     #crear diccionario

     tarea = {
          "id" : id_tarea,
          "titulo": titulo, 
          "descripcion" : desc , 
          "fecha_vencimiento": fecha, 
          "prioridad" : prioridad, 
          "completada" : completada
          }
     
     #añadirlo a la lista
     tareas.append(tarea)



     

def buscar_tareas(tareas: List[Dict[str, Any]]):
     #incializar lista de resultados
     resultados = []

     #obtener input
     palabra_clave = input("Ingrese palabra clave\n").lower()

     #Filtrar las tareas y guardarlos en la lista "resultados"
     resultados = list(filter(lambda tarea: tarea["titulo"].lower().find(palabra_clave) > -1 or tarea["descripcion"].find(palabra_clave) > -1,tareas))
     
     #Imprimir solo si hay resultados
     if len(resultados) == 0:
          print("❕No se encontraron resultados")
          
     else:
          listar_tareas(resultados)
          

def filtrar_por_prioridad(tareas: List[Dict[str, Any]]):
     #incializar lista de resultados
     resultados = []
     #Ingresar prioridad
     while True:
          prioridad_a_buscar = input("Ingrese prioridad: Alta, Media o Baja\n").capitalize()
          print(prioridad_a_buscar)
          if prioridad_a_buscar not in ["Alta", "Media", "Baja"]:
               print("❗El valor ingresado no es correcto, vuelva a ingresar el valor")
          else:
               break


     #Filtrar las tareas y guardarlos en la lista "resultados"
     resultados = list(filter(lambda tarea: tarea["prioridad"] == prioridad_a_buscar,tareas))
 
     #Imprimir solo si hay resultados
     if len(resultados) == 0:
          print("❕No se encontraron resultados")
          
     else:
          listar_tareas(resultados)

def mostrar_vencidas(tareas: List[Dict[str, Any]]):

     #incializar lista de resultados
     resultados = []

     #Filtrar vencidas   
     resultados = list(filter(lambda tarea: tarea["fecha_vencimiento"] <= datetime.today().date(), tareas))
     
     #Imprimir solo si hay resultados
     if len(resultados) == 0:
          print("❕No se encontraron resultados")
          
     else:
          listar_tareas(resultados)
          


def marcar_como_completada(tareas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
     id_a_buscar = input("Indicar el id de la tarea\n")

     encontrado = False

     try:
          for tarea in tareas:
               if tarea["id"] == id_a_buscar:
                    encontrado = True
                    tarea["completada"] = True
                    break
          
          if encontrado == False:
               #Si no encuenta el id en la lista de tareas, mandará una excepción
               raise IdInexistente("❗El id no existe. Regresarás al menú")
          
          print(f"✨Tarea : {tarea["titulo"]} fue marcada como completada")
     except IdInexistente as e:
          print(e)
     

def eliminar_tarea(tareas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
     id_a_buscar = input("Indicar el id de la tarea\n")

     encontrado = False

     try:
          for tarea in tareas:
               if tarea["id"] == id_a_buscar:
                    tarea_a_eliminar = tarea
                    encontrado = True
                    tareas.remove(tarea_a_eliminar)
                    break
          
          if encontrado == False:
               #Si no encuenta el id en la lista de tareas, mandará una excepción
               raise IdInexistente("❗El id no existe. Regresarás al menú")
          else:
               print(f"✨Tarea : {tarea["titulo"]} fue eliminada")
     except IdInexistente as e:
          print(e)


def guardar_salir(tareas: List[Dict[str, Any]]):

     try:
     #genera un archivo llamado lista_de_tareas.csv en el cual guardará todas las tareas ingresadas
          with open('data/lista_de_tareas.csv', 'w') as archivo:
               cabeceras = list(tareas[0].keys())

               #inicializa el writer
               writer = csv.DictWriter(archivo, fieldnames = cabeceras)
               

               #escribe la cabecera
               writer.writeheader()

               #escribe los datos
               for tarea in tareas:
                    writer.writerow(tarea)

                    

          print("💾✨ Archivo lista_de_tareas.csv generado exitosamente en la carpeta 'data'")
     
     except csv.Error:
          print("❗Error en la lectura del archivo csv")


def cargar_tareas(tareas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    
     try:
          with open('data/lista_de_tareas.csv', 'r') as archivo:
               reader = csv.DictReader(archivo)

               #inicializa el reader
               for row in reader:
                    tarea = {}
                    
                    tarea = {
                    "id" : row["id"],
                    "titulo": row["titulo"], 
                    "descripcion" : row["descripcion"] , 
                    "fecha_vencimiento":  datetime.strptime(row["fecha_vencimiento"],"%Y-%m-%d").date(), 
                    "prioridad" : row["prioridad"], 
                    "completada" : bool( 1 if row["completada"] == 'True' else 0 )
                    }
               
                    #añadirlo a la lista
                    tareas.append(tarea)

          print("🗨️  Data cargadada y lista para usar")
          
          return tareas
     
     except csv.Error:
          print("❗Error en la lectura del archivo csv")

               

     

def generar_txt(tareas: List[Dict[str, Any]]):


     tareas_completadas = list(filter(lambda tarea: tarea["completada"] == True, tareas))

     try:
          #crear o abrir archivo txt
          with open('data/lista_de_tareas_completadas.txt', 'w') as archivo:

               #writer
               writer  = csv.writer(archivo)

               #recorrer lista de tareas
               for tarea in tareas_completadas:
                    id_tarea = tarea["id"] 
                    titulo = tarea["titulo"] 
                    descripcion = tarea["descripcion"] 
                    fecha_venc = tarea["fecha_vencimiento"].strftime("%Y-%m-%d")
                    prioridad = tarea["prioridad"] 
                    completada = "X"

                    #generar detalle
                    detalle = f"ID: {id_tarea} | [{completada}]  {titulo} | {descripcion} | {fecha_venc} |  Prioridad:  {prioridad}"
                          
                    
                    #escribir en el txt
                    writer.writerow([detalle])

          print("💾✨ Archivo lista_de_tareas_completadas.txt generado exitosamente en la carpeta 'data'")           

     except csv.Error:
          print("❗Error en la lectura del archivo csv")


def generar_recordatorios(tareas: List[Dict[str, Any]]):

 
     print("📌Sistema de recodatorios📌")

     resultados = []
     
     fecha_actual = datetime.today().date()

     #Filtrar las tareas vencidas
     vencidas = list(filter(lambda tarea: tarea["completada"] == False and tarea["fecha_vencimiento"] <= fecha_actual, tareas))
     
     #Filtrar las tareas que vencen mañana
     por_vencer = list(filter(lambda tarea: tarea["completada"] == False and tarea["fecha_vencimiento"] == fecha_actual + timedelta(days=1) , tareas))
     
     #Unir tareas
     resultados = vencidas + por_vencer

     #Imprimir solo si hay resultados
     if len(resultados) == 0:
          print("No hay tareas vencidas o por vencer próximamente")
          
     else:
          print("Tareas vencidas o que vencerán mañana:")
          listar_tareas(resultados)

     