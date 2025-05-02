import logicas_tareas as lt
from datetime import datetime,date

def iniciar_to_do_list():
     tareas = []
     tareas = lt.cargar_tareas(tareas)

     #mostrar recordatorios
     lt.generar_recordatorios(tareas)

     while True:

          #Mostrar menú principal
          lt.mostrar_menu()
          opcion = lt.solicitar_opción()

          #Validar opción a realizar
          if opcion == "1":
               lt.agregar_tareas(tareas)
          elif opcion == "2":
               lt.listar_tareas(tareas)
          elif opcion == "3":
               lt.buscar_tareas(tareas)
          elif opcion == "4":
               lt.filtrar_por_prioridad(tareas)
          elif opcion == "5":
               lt.mostrar_vencidas(tareas)
          elif opcion == "6":
               lt.marcar_como_completada(tareas)
          elif opcion == "8":
               lt.generar_txt(tareas)
          elif opcion == "7":
               lt.eliminar_tarea(tareas)
          elif opcion == "9":
               lt.guardar_salir(tareas)
               break
          
          


iniciar_to_do_list()


