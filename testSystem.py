#!/usr/bin/python

import sys
import os
import random
import getopt

import System
import Analysis

def usage ():
    print "Usage: \nprovaGSched-random [-help] [-verbose] [-seed value] [-cores value]"
    print "          [-cores value] [-util value] [-policy value]"
    print " abreviated form: [h o: v s: c: u: p:]"   

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

    nPartsMin = 4
    nPartsMax = 8
    nTaskMin = 1
    nTaskMax = 1

    System.generateSystem(mCores, nPartsMin, nPartsMax, globalUtil, nTaskMin, nTaskMax)
    #System.showSystem()

    tlist = System.allTaskList()
    print tlist

    plist = System.allPartList()
    #print plist
    taskParams = sorted(tlist, key=lambda params: params[2])

    wcrt = Analysis.WCRT(taskParams)

    print "Tiempo de respuesta: ", wcrt
        
main (sys.argv)