#!/usr/bin/python

import sys
import os

import Tasks
import Analysis

#-------------------------#
#          MAIN           #
#-------------------------#
def main (argv):

    print "Test Task"
    if (len(argv) > 1):
        ntareas = int(argv[1])
    else:
        ntareas = 10


    for i in range(ntareas):
        partId = "P0"
        tid = "T"+str(i)
        util = 0.8 + i*0.1
        per = 100 + i
        dead = 100 + 2*i
        wcet = i + 2
        ok = Tasks.defineTask(tid, util, partId)
        if (ok):
            Tasks.taskParams(tid, per, dead, wcet, util)
        else:
            print partId, " Exists"

    alltskId = Tasks.allTaskIds()
    for tid in (alltskId):
        print Tasks.taskShow(tid)

    alltsk = Tasks.allTaskParams()
    for tsk in (alltsk):
        print tsk
    
        
main (sys.argv)