##Module: Utils
import sys
import os
from heapq import heappush, heappop

import Partitions
import Tasks
import Utils
import Tracer
from CPU import CPU

readyQueue = []   # this is a heap
releaseQueue = []
blockedTasks = [] # this is a list

policies = ["RM", "EDF", "EDFNP"]

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
        (tper, tdead, twcet, tutil) = Tasks.taskGetParams(tasksIds[i])
        utotal +=  float(twcet) / float(tper)
        elem = (tasksIds[i], tper, tdead, twcet)
        tList.append(elem)
        tperiods.append(tper)
    
    hyper = Utils.HyperPeriod(tperiods)
    
    if ((schedAlg == "RM") or (schedAlg == "DM")):
        tList = sorted(tList, key=lambda elm: elm[2])
    
    for i in range(len(tList)):
        (tid, period, relDead, wcet) = tList[i]
        releaseAt = 0
        nActiv = 0
        absDead = relDead

        while (releaseAt <= hyper):
            if (schedAlg == "RM"):
                prio = i + 1
            else:
                prio = absDead
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
        (releaseAt, prio) = releaseQueue[0][0]
        while (clock  == releaseAt):
            (tid, period, relDead, absDead, wcet, texec, nActiv) = releaseQueue[0][1]
            t = heappop(releaseQueue)
            heappush(readyQueue, ((prio), (tid, period, relDead, absDead, wcet, 0, nActiv + 1)))
            updated = True
            nitems -= 1
            if (nitems > 0):
               (releaseAt, prio) = releaseQueue[0][0]
            else:
                releaseAt = clock + INFINITE
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
    
def schedHyperperiod():
	return hyper

def showCPUS():
    global cpu
    for i in range(mCores):
        cpu[i].cpuInfo()
        
def schedRun(ticks):
    #prepare data structures
    global tasks, cpu, readyQueue, releaseQueue

    cTaskId = []
    pTaskId = []
    
    hyper = initializeSched()

    clock = 0
    niter = 0
    verbose = False
    
    if (verbose): print "******** Clock: ", clock, "***************"

    while (True):
        #add tasks in blocked to ready if release time
        updated = fillRQueue(clock)
        
        if (schedAlg == "EDFNP"):
            while ((selectIdleCPU() >= 0) and (len(readyQueue) > 0)):
                ncore = selectIdleCPU()
                ((prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(readyQueue) 
                prevState = cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
        else:
            while (len(readyQueue) > 0):
                prio = readyQueue[0][0]
                ncore = selectCPU(prio)
                if (ncore >= 0):
                    ((prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(readyQueue) 
                    prevState = cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
                    (prio, pcTaskId, (pper, prDead, pwcet), (pabsDead, ptexec, pnActiv)) = prevState
                    if (pcTaskId != "Idle"):
                        heappush(readyQueue, ((prio), (pcTaskId, pper, prDead, pabsDead, pwcet, ptexec, pnActiv)))
                else:
                    break

        
# Loof for next significant next event
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
        
    print "Hyperperiodo = ", hyper, " Clock: ", clock, "No Iter: ", niter, "Policy: ", schedAlg
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




