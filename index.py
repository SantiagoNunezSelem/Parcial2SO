import math
from tabulate import tabulate
import os

# Variables globales
memory_size = 0  # Tamaño de la memoria en KB
os_size = 0  # Tamaño del SO en KB
frame_size = 0  # Tamaño de cada frame en KB
num_frames = 0  # Número de frames
frames = []  # Lista de frames (0 = libre, 's' = asignado al SO, 'u' = asignado al usuario)
processes = {}  # Diccionario para almacenar los procesos

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def ingresarDatosMemoria():
    global memory_size, os_size, frame_size, num_frames, frames
    memory_size = int(input("Ingrese el tamaño de la memoria real en KB: "))
    os_size = int(input("Ingrese el tamaño del SO en KB: "))
    frame_size = int(input("Ingrese el tamaño de cada frame en KB: "))
    num_frames = int(input("Ingrese la cantidad de frames a asignar a todos los procesos: "))
    
    # Inicializar los frames (0 = libre, 's' = asignado al SO, 'u' = asignado al usuario)
    frames_os = math.ceil(os_size / frame_size)
    frames_user = (memory_size - os_size) // frame_size
    frames = ['s'] * frames_os + ['0'] * frames_user
    print(f"Memoria configurada con {memory_size} KB, tamaño de frame {frame_size} KB.")

def mostrar_tabla_frames():
    # Usar tabulate para mostrar la tabla
    headers = ["Frame", "Estado", "Asignado a"]
    
    rows = []
    for i, frame in enumerate(frames):
        estado = "Ocupado" if frame != '0' else "Libre"
        asignado_a = "SO" if frame == 's' else ("Usuario" if frame == 'u' else "N/A")
        rows.append([i, estado, asignado_a])

    print("\nTabla de Frames:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def max_frames_libres_contiguos():
    max_free_frames = 0
    free_frames = 0

    for i, frame in enumerate(frames):
        if(frame == '0'):   
            free_frames += 1

        else:
            if(free_frames > max_free_frames):
                max_free_frames = free_frames

            free_frames = 0
    
    return max_free_frames

def hay_frames_libres_contiguos(cant_frames):
    free_frames = 0

    for frame in enumerate(frames):
        if(frame == '0'):   
            free_frames += 1
            if(free_frames >= cant_frames):
                return True


        else:
            free_frames = 0
    
    return False

def ingresar_proceso():
    not_enought_space = True

    while(not_enought_space):
        pid = int(input("\nIngrese el identificador del proceso (entero): "))
        size = int(input("Ingrese el tamaño del proceso en KB: "))
        
        if(not hay_frames_libres_contiguos(size)):
            print("No hay suficiente espacio libre para asignarlo a memoria")
        else:
            not_enought_space = False

    processes[pid] = {'size': size, 'pages': []}
    print(f"Proceso {pid} de tamaño {size} KB ingresado.")

def mostrar_menu():
    while True:
        print("\n----- MENÚ DE ADMINISTRACIÓN DE MEMORIA -----")
        print("1) Ingresar datos de memoria")
        print("2) Mostrar tabla de frames")
        print("3) Ingresar un proceso")
        print("4) Mostrar tabla de páginas")
        print("5) Simular acceso a páginas con LRU")
        print("6) Mostrar dirección física de una dirección lógica")
        print("0) Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ingresarDatosMemoria()
            pass
        elif opcion == '2':
            mostrar_tabla_frames()
            pass
        elif opcion == '3':
            # Llamar a la función para ingresar un proceso
            pass
        elif opcion == '4':
            # Llamar a la función para mostrar la tabla de páginas
            pass
        elif opcion == '5':
            # Llamar a la función para simular el acceso a páginas con LRU
            pass
        elif opcion == '6':
            # Llamar a la función para mostrar la dirección física
            pass
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def main() -> int:
    mostrar_menu()

main()
