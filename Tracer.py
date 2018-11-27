##Module: Utils
import random

Traces = {}
mcores = 0
Activations = {}
last = ""
lastTask = ""
nTicks = {}
totalTicks = 0

def traceInit(ncores, tticks):
    global last, totalTicks

    mcores = ncores
    for i in range(ncores):
        Traces[i] = []
    Activations = {}
    nTicks = {}
    last = ""
    totalTicks = tticks


def traceExecBegin(ncore, time, taskId):
    global last, lastTask

    list = Traces[ncore]
    if (last == "B"):
        list.append((lastTask, "TE", time))

    list.append((taskId, "TB", time)) 
    #print "TB", time, taskId
    Traces[ncore] = list
    lastTask = taskId
    last = "B"
    if (Activations.has_key(taskId)):
        Activations[taskId] = Activations[taskId] + 1
    else:
        Activations[taskId] = 1

def traceExecEnd(ncore, time, taskId):
    global last, lastTask
    #print "TE", time, taskId

    list = Traces[ncore]
    list.append((taskId, "TE", time)) 
    Traces[ncore] = list
    last = "E"

    
def traceShow(ncore):
    global nTicks
    res = ""
    trz = Traces[ncore]
    for i in range(len(trz)):
        if ("TB" in trz[i]):
            (taskId,  id, startTime) = trz[i]
            res += taskId + " [" + str(startTime)
        elif ("TE" in trz[i]):
            (taskId, id, endTime) = trz[i]
            duration = endTime - startTime
            res += ", " + str(endTime) + ", " + str(duration) + "]\n"
            if (nTicks.has_key(taskId)):
                nTicks[taskId] = nTicks[taskId] + duration
            else:
                nTicks[taskId] = duration

    print res
    print Activations
    tticks = 0
    for key, value in sorted(nTicks.items()) :
        print "Task: ", key, "ticks: ", value
        tticks += value 
    print "Total ticks = ", tticks, " of ", totalTicks