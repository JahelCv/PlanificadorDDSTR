###Module System
import random
import Utils


import Tasks


def generateSystem(mCores, utilTotal, nTaskMin, nTaskMax):

# define nCores
    nTareas = random.randint(nTaskMin, nTaskMax)

    
#crea las particiones
    taskParams = []
    if (nTareas > 1):
        utilsTareas = Utils.UUniFast(nTareas, utilTotal)
    else:
        utilsTareas = []
        utilsTareas.append(utilTotal)
    
    for t in range(nTareas):
        tid =  "T"+str(t)
        ut = utilsTareas[t]
        (per, wcet) = Utils.PeriodWCET(ut)
        #crea las tareas con una particion ficticia
        Tasks.defineTask2(tid, ut, per, per, wcet, "P0")


def allTaskList():   
    return Tasks.allTaskParams()

def showSystem():
    for tid in (allTaskList()):
        print tid
