#!/usr/bin/python

import sys
import os

import Tasks

#-------------------------#
#          MAIN           #
#-------------------------#
def main (argv):

    for i in range(10):
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
            print (partId, " Exists")

    alltsk = Tasks.allTasks()
    for tid in (alltsk):
        print (Tasks.taskShow(tid))
        
main (sys.argv)