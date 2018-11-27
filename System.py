###Module System
import random
import Utils


import Tasks
import Partitions
import Cores


def generateSystem(mCores, nPartsMin, nPartsMax, utilTotal, nTaskMin, nTaskMax):

# define nCores
    for m in range(mCores):
        cid = "C"+str(m)
        Cores.defineCore(cid)

    nPartCriticas = random.randint(nPartsMin, nPartsMax)
    utilCriticas = utilTotal

# distribuye la utilizacion global entre las particiones
    utilParts = Utils.UUniFast(nPartCriticas, utilCriticas)
    
#crea las particiones
    taskParams = []
    for i in range(nPartCriticas):
         pid = "P"+str(i)
         Partitions.definePartition(pid, 1, utilParts[i])
    #determina el n. de tareas de la particion    
         if (nTaskMin == nTaskMax):
             nTareas =   nTaskMin
         else:  
             nTareas = random.randint(nTaskMin, nTaskMax)
         #distribuye la utilizacion dela particion entre las tareas
         if (nTareas > 1):
             utilsTareas = Utils.UUniFast(nTareas, utilParts[i])
         else:
             utilsTareas = []
             utilsTareas.append(utilParts[i])
         for t in range(nTareas):
             tid =  "T1"+str(i)+str(t)
             ut = utilsTareas[t]
             (per, wcet) = Utils.PeriodWCET(ut)
             Tasks.defineTask2(tid, ut, per, per, wcet, pid)
#             taskParams.append((tid, params[0], params[0], params[1], 0))
             Partitions.partAddTask(pid, tid, ut)

def allTaskList():
    taskList = []
    for pid in (Partitions.allParts()):
        for tid in (Partitions.partTaskList(pid)):
            (per, dead, wcet, util) = Tasks.taskGetParams(tid)
            u = float(wcet) / float(per)
            elem = (tid, per, dead, wcet, u)
            taskList.append(elem)
    return taskList

def allPartList():
    pList = []
    for pid in (Partitions.allParts()):
        elem = (pid,  Partitions.partUtilEfective(pid))
        pList.append(elem)
    return pList

def showSystem():
    print "N. Cores: "+ str(Cores.coreNumber())
    crsIds = Cores.allCores()
    for cr in (crsIds):
        print Cores.coreShow(cr)

    print "N. Partitions: "+ str(Partitions.partNumber())
    allParts = Partitions.allParts()
    for pid in (allParts):
        print Partitions.partShow(pid)
        tsks = Partitions.partTaskList(pid)
        for tid in (tsks):
            print Tasks.taskShow(tid)   