##Module: Utils
import sys
import os
import heapq
from heapq import heappush, heappop

import Tasks
import Utils
import Tracer
from CPU import CPU

readyQueue = []   # this is a heap
releaseQueue = [] # this is a heap
#blockedTasks = [] # this is a list

policies = ["RM", "DM", "EDF", "EDFNP"]

tasksIds = []
tasks = {}
cpusRunning = []
cpu =[]
nTaskActiv = {}

clock = 0
mCores = 0
INFINITE = 99999999
schedAlg = ""
hyper = 0

        
def schedInit(ncores, policy):
    global clock, tasksIds, tasks, mCores, schedAlg
    clock = 0
    tasksIds = []
    tasks = {}
    mCores = ncores
    schedAlg = policy

def scheAddPartition(pid):
    global tasksIds
    #part = Model.partById(pid)
    #tsks = part.partTaskList()
    tsks = Partitions.partTaskList(pid)
    for i in range(len(tsks)):
        tasksIds.append(tsks[i])

def scheAddTask(taskId):
    global tasksIds
    tasksIds.append(taskId)

def nTaskActivation(tid):
	if (nTaskActiv.has_key(tid)):
	    nTaskActiv[tid] = nTaskActiv[tid] + 1
	else:
		nTaskActiv[tid] = 1

def showTasks():
    return tasksIds

def initializeSched():
    global tasksIds, releaseQueue, cpu, schedAlg, hyper
    
    tperiods = []
    tList = []
    utotal = 0.0
    for i in range(len(tasksIds)):
        (tid, tper, tdead, twcet, tutil) = Tasks.taskGetParams(tasksIds[i])
        utotal +=  float(twcet) / float(tper)
        elem = (tasksIds[i], tper, tdead, twcet)
        tList.append(elem)
        tperiods.append(tper)
    
    hyper = Utils.HyperPeriod(tperiods)
    
    if ((schedAlg == "RM") or (schedAlg == "DM") or (schedAlg == "EDF")):
        tList = sorted(tList, key=lambda elm: elm[2])
    
    for i in range(len(tList)):
        (tid, period, relDead, wcet) = tList[i]
        releaseAt = 0
        nActiv = 0
        absDead = relDead

        while (releaseAt <= hyper):
            prio = i + 1    #asigna la prioridad de la tarea en funcion de la ordenacio
            
            heappush(releaseQueue, ((releaseAt, prio), (tid, period, relDead, absDead, wcet, 0, nActiv)))
            releaseAt = releaseAt + period
            absDead = releaseAt + relDead
            nActiv += 1
    #print releaseQueue
    for i in range(mCores):
        cpu.append(())
        cpu[i] = CPU("CPU"+str(i))
        pstate = cpu[i].cpuIdle(0)
    return hyper


def fillRQueue(clock):
    global readyQueue, releaseQueue
    updated = False
    nitems = len(releaseQueue)
    if ( nitems > 0):
        # print " #### NITEMS:", nitems, ", CLOCK:",clock,", PUSHED TO READYQUEUE: ####" 
        (releaseAt, prio) = releaseQueue[0][0]
        #print "Primer element - ReleaseAt: ", releaseAt, " - Prio: ", prio
        # ESTA MAL!!! -> while (clock  <= releaseAt):
        while (releaseAt  <= clock):
            #(tid, period, relDead, absDead, wcet, texec, nActiv) = releaseQueue[0][1]
            ((releaseAt,prio),(tid, period, relDead, absDead, wcet, texec, nActiv)) = heappop(releaseQueue)
            #t = heappop(releaseQueue)
            # print "~~ HEAPPOP: ((",releaseAt,prio,"),(",tid, period, relDead, absDead, wcet, texec, nActiv,"))"

            if ((schedAlg == "RM") or (schedAlg == "DM")):
                heappush(readyQueue, ((prio), (tid, period, relDead, absDead, wcet, 0, nActiv + 1)))
            elif (schedAlg == "EDF"):
                # print "~~ INGRESAMOS ASI -> ((",absDead, prio,"), (",tid, period, relDead, absDead, wcet, 0, nActiv + 1,"))"
                heappush(readyQueue, ((absDead, prio), (tid, period, relDead, absDead, wcet, 0, nActiv + 1)))

            updated = True
            nitems -= 1
            if (nitems > 0):
               (releaseAt, prio) = releaseQueue[0][0]
            else:
                releaseAt = clock + INFINITE
    # print "#### FIN FILL READY QUEUE ####"
    return updated


def selectIdleCPU():
    global cpu
    lcpu = []
    for i in range(mCores):
        value = (cpu[i].cpuPrio(), i)
        lcpu.append(value)
    lcpu.sort()
    if (lcpu[0][0] == 0):  #cpu is idle
        return lcpu[0][1]
    #elif (lcpu[-1][0] > p):  #cpu has a lower priority
    #    return lcpu[-1][1]
    else:                    #no available cpu for prio p
        return -1
        
    
def selectCPU(p):
    global cpu
    lcpu = []
    for i in range(mCores):
        value = (cpu[i].cpuPrio(), i)
        lcpu.append(value)
    lcpu.sort()
    if (lcpu[0][0] == 0):  #cpu is idle
        return lcpu[0][1]
    elif (lcpu[-1][0] > p):  #cpu has a lower priority
        return lcpu[-1][1]
    else:                    #no available cpu for prio p
        return -1

def selectCPUEDF(absDeadEDF, prioEDF):
    global cpu
    selectedCPU = -1
    absDeadMax = absDeadEDF
    prioEDFMax = prioEDF
    for ncore in range(mCores):
        (CPUid, CPUtaskId, CPUtaskPrio, CPUtaskPeriod, CPUtaskRelDead, CPUtaskAbsDead, CPUtaskWCET, CPUtaskTexec, CPUtaskNjob) = cpu[ncore].cpuInfo()
        if (CPUtaskId == "Idle"):
            selectedCPU = ncore
            break
        elif (absDeadMax < CPUtaskAbsDead) or ((absDeadMax == CPUtaskAbsDead) and (prioEDFMax < CPUtaskPrio)):
            absDeadMax = CPUtaskAbsDead
            prioEDFMax = CPUtaskPrio
            selectedCPU = ncore
    return selectedCPU;
    
def schedHyperperiod():
	return hyper

def showCPUS():
    global cpu
    for i in range(mCores):
        cpu[i].cpuInfo()
        
def schedRun(ticks):
    #prepare data structures
    global tasks, cpu, readyQueue, releaseQueue

    clock = 0
    niter = 0
    verbose = False
    cambioscontexto = 0

    cTaskId = []
    pTaskId = []
    
    hyper = initializeSched()

    if (verbose): print "******** Clock: ", clock, "***************"

    while (True):
        # add tasks in blocked to ready if release time
        updated = fillRQueue(clock)
        
        if (verbose):
            print "#### Despres de fillRQueue(clock), la readyQueue lleva: ####"
            for i in range(len(readyQueue)):     
                print readyQueue[i]
        
        if ((schedAlg == "RM") or (schedAlg == "DM")):
            while (len(readyQueue) > 0):
                prio = readyQueue[0][0]
                ncore = selectCPU(prio)
                if (ncore >= 0):
                    cambioscontexto += 1
                    ((prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(readyQueue) 
                    prevState = cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
                    (prio, pcTaskId, (pper, prDead, pwcet), (pabsDead, ptexec, pnActiv)) = prevState
                    if (pcTaskId != "Idle"):
                        heappush(readyQueue, ((prio), (pcTaskId, pper, prDead, pabsDead, pwcet, ptexec, pnActiv)))
                else:
                    break

        elif (schedAlg == "EDF"):
            while (len(readyQueue) > 0):
                (absDead, prio) = readyQueue[0][0]
                ncore = selectCPUEDF(absDead, prio)
                if (ncore >= 0):
                    cambioscontexto += 1
                    ((absDead, prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(readyQueue) 
                    prevState = cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
                    (prio, pcTaskId, (pper, prDead, pwcet), (pabsDead, ptexec, pnActiv)) = prevState
                    if (pcTaskId != "Idle"):
                        heappush(readyQueue, ((pabsDead, prio), (pcTaskId, pper, prDead, pabsDead, pwcet, ptexec, pnActiv)))
                else:
                    break
        # Look for next significant next event
        if (len(releaseQueue) > 0):
            nxtRelease = releaseQueue[0][0][0]
        else:
            nxtRelease = INFINITE + clock

        strrem = "nxtRelease: ", nxtRelease
        nxtEvent = nxtRelease - clock
        
        for i in range(mCores):
            rem = cpu[i].cpuRemainTicks()
            strrem +=  "   ["+str(i)+ "] rem: ",  rem, ", "
            if (rem < nxtEvent):
               nxtEvent = rem
        if (nxtEvent > hyper):
            nxtEvent = hyper - clock
        if (verbose): showCPUS()
        clock = clock + nxtEvent
        if (verbose): print "******** Clock: ", clock, "***************", nxtEvent
        
        for i in range(mCores):
            rem = cpu[i].cpuRunTicks(nxtEvent)
            if (rem == 0):
                cpu[i].cpuIdle(clock)

        if (verbose): showCPUS()    
        if (verbose): print "-------------------------"    
        niter += 1
        #until 
        if (clock >= hyper):
        	break
        
    print ""
    print " ## Hyperperiodo = ", hyper, " Clock: ", clock, "No Iter: ", niter, "Policy: ", schedAlg
    print ""
    print " ## Cambios de contexto = ", cambioscontexto
    print ""
    cpu[i].cpuAlloc(clock,  "Idle", 0, 0, 0,0, 0, 0, 0)
    #for i in range(mCores):
    #    cpu[i].cpuInfo()
    ans = ""
    for i in range(mCores):
        ans += cpu[i].cpuShow()
    return ans

def schedChrono(ncore):
    chrono = cpu[ncore].cpuChrono()
    return chrono




