import math



class ProcessControlBlock:
    def __init__(self,id,size,frameSize):
        self.id = id
        self.size = size
        self.pageTable = [[-1,'i'] for _ in range(math.ceil(size / frameSize))]   #List of lists. First element of the internal list indicates if there is or there is not a referece to a frame. Second element is the validation bit. The index of the main list indicates the page

    
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


        if(frameNumber == maxFrames or frameNumber == len(self.pageTable)):
            print("\n--- Proceso guardado con exito ---")
            print(f"Se pudo asignar {frameNumber} frames del proceso (maxima cantidad por proceso:{maxFrames})")
        else:
            print("\n--- Proceso creado con exito ---")
            print("Memoria llena")
            if(len(self.pageTable) < maxFrames):
                print(f"Se pudo asignar {frameNumber} frames del proceso (frames restantes: {len(self.pageTable)-frameNumber})")
                print(f"Cuando se liberen frames se asignaran los {len(self.pageTable)-frameNumber} frames pendientes de forma automatica")
            else:
                print(f"Se pudo asignar {frameNumber} frames del proceso (max frames: {maxFrames})")
                print(f"Cuando se liberen frames se asignaran los {maxFrames-frameNumber} frames pendientes de forma automatica")                

