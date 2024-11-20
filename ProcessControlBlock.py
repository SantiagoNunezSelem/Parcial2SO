import math
from tabulate import tabulate
class ProcessControlBlock:
    def __init__(self,pid,size,frameSize):
        self.pid = pid
        self.size = size
        self.pageTable = [[-1,'i'] for _ in range(math.ceil(size / frameSize))]   #List of lists. First element of the internal list indicates the reference to a frame. Second element is the validation bit. The index of the main list indicates the page

    def __repr__(self):
        return f"ProcessControlBlock(pid={self.pid}, size='{self.size}', pageTable={self.pageTable})"
    
    def addToMemory(self, memory, maxFrames):
        frameNumber = 0
        i = 0

        while i < len(memory) and frameNumber < maxFrames and frameNumber < len(self.pageTable):
            if memory[i] == '0':
                # Free frame in memory
                self.pageTable[frameNumber][0] = i
                self.pageTable[frameNumber][1] = 'v'

                memory[i] = 'u'  # Mark memory as assigned to a user process

                frameNumber += 1
            i += 1


        if(frameNumber == maxFrames):
            print("\n--- Proceso Guardado con Exito ---")
            print(f"Se pudo asignar {frameNumber} frames del proceso (maxima cantidad por proceso:{maxFrames})")
        elif(frameNumber == len(self.pageTable)):
            print("\n--- Proceso Guardado con Exito ---")
            print(f"Se pudo asignar los {frameNumber} frames del proceso")
        else:
            print("\n--- Proceso Creado con Exito ---")
            print("Memoria llena")
            if(len(self.pageTable) < maxFrames):
                print(f"Se pudo asignar {frameNumber} frames del proceso (frames restantes: {len(self.pageTable)-frameNumber})")
                print(f"Cuando se liberen frames se asignaran los {len(self.pageTable)-frameNumber} frames pendientes de forma automatica")
            else:
                print(f"Se pudo asignar {frameNumber} frames del proceso (max frames: {maxFrames})")
                print(f"Cuando se liberen frames se asignaran los {maxFrames-frameNumber} frames pendientes de forma automatica")

    def hasPagesWaiting(self, maxFrames):
        countFrames = self.countFrames()
        
        if(len(self.pageTable) < maxFrames):
            return countFrames < len(self.pageTable)
        else:
            return countFrames < maxFrames
        
    def countFrames(self):
        countFrames = 0

        for page in self.pageTable:
                if(page[1] == 'v'):
                    countFrames += 1
        
        return countFrames
    
    def getPageTableFrames(self):
        tableFrames = []
        for frame in self.pageTable:
            if(frame[1] == 'v'):
                tableFrames.append(frame)
        
        return tableFrames
    
    def getFrameNumbers(self):
        framesNumbers = []
        for frame in self.pageTable:
            if(frame[1] == 'v'):
                framesNumbers.append(frame[0])

        return framesNumbers

    def lru(self, series):
        tableFrames = self.getPageTableFrames()

        if(len(tableFrames) == 0):
            print(f"\nEl proceso con PID:{self.pid} no tiene frames asignados a nignuna pagina dentro de la tabla de paginas")
            print("Elimine procesos para que se puedan asignar frames libres de forma automatica")
            return -1
        frameNumbers = self.getFrameNumbers()
        lastUsed = [page.copy() for page in self.pageTable]
        displayTable = [[f"Frame {frame[0]}"] for frame in tableFrames]
        
        addColumnInLruTable(self,frameNumbers,displayTable)

        for pageNumber in series:
            if(self.pageTable[pageNumber][1] == 'v'):
                # Si la página en la pageTable está relacionada con un frame, agregar como la más recientemente usada
                frameRelated = self.pageTable[pageNumber][0]
                for page in lastUsed:
                    if(page[0] == frameRelated):
                        lastUsed.remove(page)
                        lastUsed.append(page.copy())
                        break
            else:
                # Si la página no está en memoria, eliminar la referencia al frame en la página menos recientemente usada y agregarla la nueva referencia en su lugar 
                for page in lastUsed:
                    if(page[1] == 'v'):
                        # Encontrar la menos usada
                        leastPageUsed = page
                        lastUsed.remove(page)
                        break
                
                frameLeastProcess = leastPageUsed[0]
                addProcess = [frameLeastProcess, 'v']

                lastUsed.append(addProcess)

                # Eliminar el frame de la página en memoria y agregarlo a la nueva página
                for page in self.pageTable:
                    if(page[0] == frameLeastProcess):
                        page[0] = -1
                        page[1] = 'i'

                self.pageTable[pageNumber][0] = frameLeastProcess
                self.pageTable[pageNumber][1] = 'v'
    
            addColumnInLruTable(self,frameNumbers,displayTable)     #Preparar tabla para mostarar en la terminal
        
        displayLruTable(series,displayTable)

def addColumnInLruTable(self,frameNumbers,displayTable):
    count = 0
    for frameNumber in frameNumbers:
        for i,page in enumerate(self.pageTable):
            if page[0] == frameNumber:
                displayTable[count].append(i)
                count += 1
                break

def displayLruTable(series,displayTable):
    headers = [" - "," inicio "]
    for i in range(0,len(series)):
        headers.append(series[i])
    
    print(tabulate(displayTable, headers=headers, tablefmt="grid"))