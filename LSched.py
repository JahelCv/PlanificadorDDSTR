##Module: Utils
import sys
import os
import heapq
from heapq import heappush, heappop

import Tasks
import Utils
import Tracer
from CPU import CPU

INFINITE = 99999999
policies = ["RM", "DM", "EDF"]

class LSched:

    def __init__(self, id):
        self.id = id
        self.readyQueue = []   # this is a heap
        self.releaseQueue = [] # this is a heap
        self.tasksIds = []
        self.tasks = {}
        self.cpu =[]
        self.nTaskActiv = {}
        self.clock = 0
        self.mCores = 0
        self.schedAlg = ""
        self.hyper = 0

    def getId(self):
        return self.id

            
    def schedInit(self, ncores, policy):
        self.clock = 0
        self.tasksIds = []
        self.tasks = {}
        self.mCores = ncores
        self.schedAlg = policy

    def scheAddPartition(self, pid):
        tsks = Partitions.partTaskList(pid)
        for i in range(len(tsks)):
            self.tasksIds.append(tsks[i])

    def scheAddTask(self, taskId):
        self.tasksIds.append(taskId)

    def nTaskActivation(tid):
    	if (nTaskActiv.has_key(tid)):
    	    nTaskActiv[tid] = nTaskActiv[tid] + 1
    	else:
    		nTaskActiv[tid] = 1

    def showTasks(self):
        return tasksIds

    def initializeSched(self):        
        tperiods = []
        tList = []
        utotal = 0.0
        for i in range(len(self.tasksIds)):
            (tid, tper, tdead, twcet, tutil) = Tasks.taskGetParams(self.tasksIds[i])
            utotal +=  float(twcet) / float(tper)
            elem = (self.TasksIds[i], tper, tdead, twcet)
            tList.append(elem)
            tperiods.append(tper)
        
        self.hyper = Utils.HyperPeriod(tperiods)
        
        if ((self.schedAlg == "RM") or (self.schedAlg == "DM") or (self.schedAlg == "EDF")):
            tList = sorted(tList, key=lambda elm: elm[2])
        
        for i in range(len(tList)):
            (tid, period, relDead, wcet) = tList[i]
            releaseAt = 0
            nActiv = 0
            absDead = relDead

            while (releaseAt <= self.hyper):
                prio = i + 1    #asigna la prioridad de la tarea en funcion de la ordenacio
                
                heappush(self.releaseQueue, ((releaseAt, prio), (tid, period, relDead, absDead, wcet, 0, nActiv)))
                releaseAt = releaseAt + period
                absDead = releaseAt + relDead
                nActiv += 1
        #print releaseQueue
        for i in range(mCores):
            self.cpu.append(())
            self.cpu[i] = CPU("CPU"+str(i))
            pstate = self.cpu[i].cpuIdle(0)
        return self.hyper


    def fillRQueue(self, clock):
        # global readyQueue, releaseQueue
        updated = False
        nitems = len(self.releaseQueue)
        if ( nitems > 0):
            # print " #### NITEMS:", nitems, ", CLOCK:",clock,", PUSHED TO READYQUEUE: ####" 
            (releaseAt, prio) = self.releaseQueue[0][0]
            #print "Primer element - ReleaseAt: ", releaseAt, " - Prio: ", prio
            # ESTA MAL!!! -> while (clock  <= releaseAt):
            while (releaseAt  <= clock):
                #(tid, period, relDead, absDead, wcet, texec, nActiv) = releaseQueue[0][1]
                ((releaseAt,prio),(tid, period, relDead, absDead, wcet, texec, nActiv)) = heappop(self.releaseQueue)
                #t = heappop(releaseQueue)
                # print "~~ HEAPPOP: ((",releaseAt,prio,"),(",tid, period, relDead, absDead, wcet, texec, nActiv,"))"

                if ((self.schedAlg == "RM") or (self.schedAlg == "DM")):
                    heappush(self.readyQueue, ((prio), (tid, period, relDead, absDead, wcet, 0, nActiv + 1)))
                elif (self.schedAlg == "EDF"):
                    # print "~~ INGRESAMOS ASI -> ((",absDead, prio,"), (",tid, period, relDead, absDead, wcet, 0, nActiv + 1,"))"
                    heappush(self.readyQueue, ((absDead, prio), (tid, period, relDead, absDead, wcet, 0, nActiv + 1)))

                updated = True
                nitems -= 1
                if (nitems > 0):
                   (releaseAt, prio) = self.releaseQueue[0][0]
                else:
                    releaseAt = clock + INFINITE
        # print "#### FIN FILL READY QUEUE ####"
        return updated


    def selectIdleCPU(self):
        # global cpu
        lcpu = []
        for i in range(mCores):
            value = (self.cpu[i].cpuPrio(), i)
            lcpu.append(value)
        lcpu.sort()
        if (lcpu[0][0] == 0):  #cpu is idle
            return lcpu[0][1]
        #elif (lcpu[-1][0] > p):  #cpu has a lower priority
        #    return lcpu[-1][1]
        else:                    #no available cpu for prio p
            return -1
            
        
    def selectCPU(self, p):
        # global cpu
        lcpu = []
        for i in range(mCores):
            value = (self.cpu[i].cpuPrio(), i)
            lcpu.append(value)
        lcpu.sort()
        if (lcpu[0][0] == 0):  #cpu is idle
            return lcpu[0][1]
        elif (lcpu[-1][0] > p):  #cpu has a lower priority
            return lcpu[-1][1]
        else:                    #no available cpu for prio p
            return -1

    def selectCPUEDF(self, absDeadEDF, prioEDF):
        # global cpu
        selectedCPU = -1
        absDeadMax = absDeadEDF
        prioEDFMax = prioEDF
        for ncore in range(mCores):
            (CPUid, CPUtaskId, CPUtaskPrio, CPUtaskPeriod, CPUtaskRelDead, CPUtaskAbsDead, CPUtaskWCET, CPUtaskTexec, CPUtaskNjob) = self.cpu[ncore].cpuInfo()
            if (CPUtaskId == "Idle"):
                selectedCPU = ncore
                break
            elif (absDeadMax < CPUtaskAbsDead) or ((absDeadMax == CPUtaskAbsDead) and (prioEDFMax < CPUtaskPrio)):
                absDeadMax = CPUtaskAbsDead
                prioEDFMax = CPUtaskPrio
                selectedCPU = ncore
        return selectedCPU;
        
    def schedHyperperiod(self):
    	return self.hyper

    def showCPUS(self):
        # global cpu
        for i in range(mCores):
            self.cpu[i].cpuInfo()
            
    def schedRun(self, ticks):
        #prepare data structures
        # global tasks, cpu, readyQueue, releaseQueue

        clock = 0
        niter = 0
        verbose = True

        cTaskId = []
        pTaskId = []
        
        self.hyper = initializeSched()

        if (verbose): print "******** Clock: ", clock, "***************"

        while (True):
            # add tasks in blocked to ready if release time
            updated = fillRQueue(clock)
            
            print "#### Despres de fillRQueue(clock), la readyQueue lleva: ####"
            for i in range(len(self.readyQueue)):     
                print self.readyQueue[i]
            # DESCOMENTAR raw_input('#### Press enter to continue: ####')
            # print "--------------------------------------------------------------"  
            
            if ((self.schedAlg == "RM") or (self.schedAlg == "DM")):
                while (len(self.readyQueue) > 0):
                    prio = readyQueue[0][0]
                    ncore = selectCPU(prio)
                    if (ncore >= 0):
                        ((prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(self.readyQueue) 
                        prevState = self.cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
                        (prio, pcTaskId, (pper, prDead, pwcet), (pabsDead, ptexec, pnActiv)) = prevState
                        if (pcTaskId != "Idle"):
                            heappush(self.readyQueue, ((prio), (pcTaskId, pper, prDead, pabsDead, pwcet, ptexec, pnActiv)))
                    else:
                        break

            elif (self.schedAlg == "EDF"):
                while (len(self.readyQueue) > 0):
                    (absDead, prio) = self.readyQueue[0][0]
                    ncore = selectCPUEDF(absDead, prio)
                    if (ncore >= 0):
                        ((absDead, prio), (cTaskId, period, relDead, absDead, wcet, texec, nActiv)) = heappop(self.readyQueue) 
                        prevState = self.cpu[ncore].cpuAlloc(clock, cTaskId, prio, period, relDead, absDead, wcet, texec, nActiv)
                        (prio, pcTaskId, (pper, prDead, pwcet), (pabsDead, ptexec, pnActiv)) = prevState
                        if (pcTaskId != "Idle"):
                            heappush(self.readyQueue, ((pabsDead, prio), (pcTaskId, pper, prDead, pabsDead, pwcet, ptexec, pnActiv)))
                    else:
                        break
            # Look for next significant next event
            if (len(self.releaseQueue) > 0):
                nxtRelease = self.releaseQueue[0][0][0]
            else:
                nxtRelease = INFINITE + clock

            strrem = "nxtRelease: ", nxtRelease
            nxtEvent = nxtRelease - clock
            
            for i in range(mCores):
                rem = self.cpu[i].cpuRemainTicks()
                strrem +=  "   ["+str(i)+ "] rem: ",  rem, ", "
                if (rem < nxtEvent):
                   nxtEvent = rem
            if (nxtEvent > self.hyper):
                nxtEvent = self.hyper - clock
            if (verbose): showCPUS()
            clock = clock + nxtEvent
            if (verbose): print "******** Clock: ", clock, "***************", nxtEvent
            
            for i in range(mCores):
                rem = self.cpu[i].cpuRunTicks(nxtEvent)
                if (rem == 0):
                    self.cpu[i].cpuIdle(clock)

            if (verbose): showCPUS()    
            if (verbose): print "-------------------------"    
            niter += 1
            #until 
            if (clock >= self.hyper):
            	break
            
        print "Hyperperiodo = ", self.hyper, " Clock: ", clock, "No Iter: ", niter, "Policy: ", self.schedAlg
        self.cpu[i].cpuAlloc(clock,  "Idle", 0, 0, 0,0, 0, 0, 0)
        #for i in range(mCores):
        #    cpu[i].cpuInfo()
        ans = ""
        for i in range(mCores):
            ans += self.cpu[i].cpuShow()
        return ans

    def schedChrono(self, ncore):
        chrono = self.cpu[ncore].cpuChrono()
        return chrono




