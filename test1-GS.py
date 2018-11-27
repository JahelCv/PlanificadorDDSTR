#!/usr/bin/python

import sys
import os
import Utils
import random
import getopt
from heapq import heappush, heappop

import chronogram

import Cores
import Partitions
import Tasks

import GSched
import Analysis


def getOpts(argv):
    seed = None
    cores = None
    util = None
    output = None
    verbose = False
    psched = "RM"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:vs:c:u:p:", ["help", "output=", "seed=", "cores=", "util=", "policy:"])
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
            psched = a
        else:
            assert False, "unhandled option"
    # ...
    return  (verbose, output, seed, cores, util, psched)
    
    
#-------------------------#
#          MAIN           #
#-------------------------#
def main (argv):

    globalUtil = 0.8
    mCores = 1

    semilla = random.randint(0, sys.maxint)
    random.seed(semilla)
    
    (verbose, fout, semilla, cores, util, sched) = getOpts(argv)
    
    if (util != None):
    	globalUtil = float(util)
    if (semilla != None):
    	random.seed(semilla)
    if (cores != None):
        mCores = int(cores)
    if (sched != None):
        psched = sched

    print "Cores: ", mCores, "Utilization:", globalUtil, "Politica:", psched
    
    parts = []
    #System.defineSystem(mCores, globalUtil)

    	
    nPartCriticas = 4

    params = ((20, 20, 4, 0.2), (30, 30, 5, 0.2), (50, 50, 8, 0.16), (60, 60, 10, 0.2))


    cid = "C0"
    Cores.defineCore(cid)
    #Model.addCoreModel(cid, c)

    utotal = 0.0
    taskParams = []
    for i in range(nPartCriticas):
        (per, plazo, c, u) = params[i]
        pid = "P"+str(i+1)
        tid = "T"+str(i+1)
        Partitions.definePartition(pid, 1, u)
        Tasks.defineTask(tid, u, per, plazo, c, pid)
        Partitions.partAddTask(pid, tid, u)
        Cores.coreAddPartition(cid, pid, u)


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

    
    res = Analysis.schedulabilityTest(psched, mCores, taskParams)
    print "Analisi: ", res
       
    print "No Partitions: ", Partitions.partNumber()
    print "Utilization: ", utotal
    #System.show()
    
    GSched.schedInit(mCores, psched)
    
    for i in range(nPartCriticas):
        pid = "P"+str(i+1)
        GSched.scheAddPartition(pid)
    
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
        
main (sys.argv)