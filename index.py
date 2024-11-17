import math
from tabulate import tabulate
import os
import bisect

import ProcessControlBlock as PCB

# Variables globales
memory_size = 0  # Tamaño de la memoria en KB
os_size = 0  # Tamaño del SO en KB
frame_size = 0  # Tamaño de cada frame en KB
num_frames_max = 0  # Número de frames maximo por proceso
frames = []  # Lista de frames (0 = libre, 's' = asignado al SO, 'u' = asignado al usuario)
processesControlBlock = []

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enterMemoryData():
    global memory_size, os_size, frame_size, num_frames_max, frames, processesControlBlock
    memory_size = int(input("Ingrese el tamaño de la memoria real en KB: "))
    os_size = int(input("Ingrese el tamaño del SO en KB: "))
    frame_size = int(input("Ingrese el tamaño de cada frame en KB: "))
    num_frames_max = int(input("Ingrese la cantidad de frames a asignar a todos los procesos: "))
    
    # Inicializar los frames (0 = libre, 's' = asignado al SO, 'u' = asignado al usuario)
    frames_os = math.ceil(os_size / frame_size)
    frames_user = (memory_size - os_size) // frame_size
    frames = ['s'] * frames_os + ['0'] * frames_user
    print(f"Memoria configurada con {memory_size} KB, tamaño de frame {frame_size} KB.")

def showFrameTable():
    # Use tabulate to display the frame table
    headers = ["Frame", "Estado", "Asignado a"]
    
    rows = []
    for i, frame in enumerate(frames):
        estado = "Ocupado" if frame != '0' else "Libre"
        asignado_a = "SO" if frame == 's' else ("Usuario" if frame == 'u' else "N/A")
        rows.append([i, estado, asignado_a])

    print("\nTabla de Frames:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def searchProcess(pid):
    #processesControlBlock is sorted
    left = 0
    right = len(processesControlBlock) - 1

    while left <= right:
        mid = (left + right) // 2

        # Compare the PID with the middle element
        if processesControlBlock[mid].pid == pid:
            return mid
        elif processesControlBlock[mid].pid < pid:
            left = mid + 1
        else:
            right = mid - 1

    return -1

def insertSorted(list, new_object):
    # Extract the key for sorting (id in this case)
    keys = [element.pid for element in list]
    # Find the position to insert using bisect
    position = bisect.bisect_left(keys, new_object.pid)
    # Insert the object at the correct position
    list.insert(position, new_object)

def addProcess():
    notAvailableId = True

    while(notAvailableId):
        pid = int(input("\nIngrese el identificador del proceso (entero): "))

        if(searchProcess(pid) != -1):
            print("Este indetificador ya existe, ingrese uno nuevo")
        else:
            notAvailableId = False

    size = int(input("Ingrese el tamaño del proceso en KB: "))

    processCB = PCB.ProcessControlBlock(pid,size,frame_size)

    insertSorted(processesControlBlock,processCB)

    processCB.addToMemory(frames,num_frames_max)

def showPageTable():
    notValidId = True

    while(notValidId):
        pid = int(input("\nIngrese el identificador del proceso (entero): "))

        index = searchProcess(pid)
        if(index == -1):
            print("Este indetificador no existe, vuelva a intentarlo")
        else:
            notValidId = False
    
    processControlBlock = processesControlBlock[index]

    #Use tabulate to display the page Use tabulate to display the frame table
    headers = ["Pagina", "Frame", "Bit Validez"]
    
    rows = []
    for i, pag in enumerate(processControlBlock.pageTable):
        numPage = i
        numFrame = pag[0] if pag[0] != -1 else "N/A"
        vBit = pag[1]
        rows.append([numPage, numFrame, vBit])

    print("\nTabla de Frames:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    

def showMenu():
    while True:
        print("\n----- MENÚ DE ADMINISTRACIÓN DE MEMORIA -----")
        print("1) Ingresar datos de memoria")
        print("2) Mostrar tabla de frames")
        print("3) Ingresar un proceso")
        print("4) Eliminar un proceso")
        print("5) Mostrar tabla de páginas")
        print("6) Simular acceso a páginas con LRU")
        print("7) Mostrar dirección física de una dirección lógica")
        print("0) Salir")
        
        opt = input("Seleccione una opción: ")
        
        if opt == '1':
            enterMemoryData()
            pass
        elif opt == '2':
            showFrameTable()
            pass
        elif opt == '3':
            addProcess()
            pass
        elif opt == '4':
            # Eliminar un proceso
            pass
        elif opt == '5':
            showPageTable()
            pass
        elif opt == '6':
            # Llamar a la función para simular el acceso a páginas con LRU
            pass
        elif opt == '7':
            # Llamar a la función para mostrar la dirección física
            pass
        elif opt == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def main() -> int:
    showMenu()

main()
