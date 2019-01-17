#!/usr/bin/python

import sys
import os
import random
import getopt

from heapq import heappush, heappop

import System
import Analysis

import chronogram
import Cores
import Tasks
import GSched
import LSched
import Utils
import BinPacking


def usage ():
    print "Usage: \nprovaGSched-random [-help] [-verbose] [-seed value] [-cores value]"
    print "          [-cores value] [-util value] [-policy value]"
    print " abreviated form: [h o: v s: c: u: p:]"
    print ""
    print "--- IMPORTANT NOTE ---"
    print ""   
    print "    * If you want global policy, define only one policy value. ex. -p \"RM\" "
    print "    * If you want local policy, define n policy values as cores values. "
    print "      Splitted by \",\". ex. -c 4 -p \"RM,RM,EDF,DM\""
    print ""

def getOpts(argv):
    seed = None
    cores = None
    util = None
    output = None
    verbose = False
    psched = ["RM"]
    binpacking = "FF"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:vs:c:u:p:", ["help", "output=", "seed=", "cores=", "util=", "policy:", "binpacking:"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-s", "--seed"):
            seed = a
        elif o in ("-c", "--cores"):
            cores = a
        elif o in ("-u", "--util"):
            util = a
        elif o in ("-p", "--policy"):
            psched = a.split(",")
        elif o in ("-b", "--binpacking"):
            binpacking = a
        else:
            assert False, "unhandled option"
    # ...
    return  (verbose, output, seed, cores, util, psched, binpacking)
    
#-------------------------#
#          MAIN           #
#-------------------------#
def main (argv):

    globalUtil = 0.8
    mCores = 1
    semilla = random.randint(0, sys.maxint)
    random.seed(semilla)                       
    
    (verbose, fout, semilla, cores, util, sched, bp) = getOpts(argv)
    
    if (util != None):
        globalUtil = float(util)
    if (semilla != None):
        random.seed(semilla)
    if (cores != None):
        mCores = int(cores)

    nTaskMin = 4
    nTaskMax = 8

    ##System.generateSystem(mCores, nPartsMin, nPartsMax, globalUtil, nTaskMin, nTaskMax)

    System.generateSystem(mCores, globalUtil, nTaskMin, nTaskMax)
    #System.showSystem()

    tlist = System.allTaskList()
    print "Lista de tareas", tlist

    if len(sched) == 1:
        if (sched[0].strip() == ""):
            return 
        #wcrt = Analysis.WCRT(taskParamsList)
        util = Analysis.utilization(tlist)
        print "Utilizacion = ", util

        wcrt = Analysis.schedulabilityTest(sched[0], 1, tlist)
        print "Tiempo de respuesta: ", wcrt

        GSched.schedInit(mCores, sched[0])

        for tid in (Tasks.allTaskIds()):
            GSched.scheAddTask(tid)

        print "Tasks: "
        GSched.showTasks()
        GSched.schedRun(100)
        
        hyper = GSched.schedHyperperiod()
        
        chronogram.chronoInit(mCores, hyper, "chrono")
        
        for i in range(mCores):
            chronogram.chronoAddLine(i, "C"+str(i))
        
        for c in range(mCores):
            chrono = GSched.schedChrono(c)
            for e in range(len(chrono)):
                (tsk, start, end) = chrono[e]
                chronogram.chronoAddExec(c, start, end, tsk)
        chronogram.chronoClose()
    else:
        if len(sched) != mCores:
            print ""
            print "--- ERROR ---"
            print ""
            print " Different number of cores and policies"
            print ""

        lsched = []
        for c in range(mCores):
            lsched.append(())
            lsched[c] = LSched("LCPU" + str(c))

        #wcrt = Analysis.WCRT(taskParamsList)
        #util = Analysis.utilization(tlist)
        #print "Utilizacion = ", util

        #wcrt = Analysis.schedulabilityTest(sched[0], 1, tlist)
        #print "Tiempo de respuesta: ", wcrt

        # Calcular hyperperiodo global
        tperiods = []
        for i in range(len(tasksIds)):
            (tid, tper, tdead, twcet, tutil) = Tasks.taskGetParams(tasksIds[i])
            tperiods.append(tper)

        hyper = Utils.HyperPeriod(tperiods)


        # Bin packing
        BinPacking.initBin(bp, mCores)
        for (pid, util) in (tList):
            ok = BinPacking.binAdd(pid, util)
            if (not ok):
                print "Fallo la particion no cabe", pid, util
                break

        #(Bins, Pesos) = BinPacking.binGetAll() # (Bins, Pesos)
        for c in range(mCores): 
            lsched[c].schedInit(mCores, sched[c])
            # Cal afegir les tasques
            (taskBinIds, taskpesos) = BinPacking.binGetbyIndex(c)
            for btask in range(taskBinIds):
                lsched[c].scheAddTask(btask)
            print "Core ", c, " - Tasks: "
            lsched[c].showTasks()
            lsched[c].schedRun(hyper)
        
        chronogram.chronoInit(mCores, hyper, "chrono")
        
        for i in range(mCores):
            chronogram.chronoAddLine(i, "C"+str(i))
        
        for c in range(mCores):
            chrono = lsched[c].schedChrono(0)
            for e in range(len(chrono)):
                (tsk, start, end) = chrono[e]
                chronogram.chronoAddExec(c, start, end, tsk)
        chronogram.chronoClose()



main (sys.argv)