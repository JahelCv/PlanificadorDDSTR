#module  Tasks:

from Task import Task

NoTasks = 0; 
taskDict = {}
taskIds = []

def defineTask(tid, util, partId):  # attributos: Id, Period, Deadline, WCET, Util
    global NoTasks
    if (not taskDict.has_key(tid)):
        tsk = Task(tid, partId)
        taskDict[tid] = tsk
        taskIds.append(tid)
        NoTasks += 1
        return True
    else:
        return False

def defineTask2(tid, util, per, dead, wcet, partId):  # attributos: Id, Period, Deadline, WCET, Util
    global NoTasks
    tsk = Task(tid, partId)
    tsk.taskParams(per, dead, wcet, util)
    taskDict[tid] = tsk
    taskIds.append(tid)
    NoTasks += 1

def taskParams(tid, per, dead, wcet, util):
    taskDict[tid].taskParams(per, dead, wcet, util)

def taskGetParams(tid):
    return taskDict[tid].taskGetParams()

def allTasks():
    return taskDict.keys()

def taskPeriod(tid):
    return taskDict[tid].taskPeriod()

def taskDeadline(tid):
    return taskDict[tid].taskDeadline()

def taskWCET(tid):
    return taskDict[tid].taskWCET()

def taskPartition(tid):
    return taskDict[tid].taskPartition()

def taskUtil(tid):
    return taskDict[tid].taskUtil()
    
def taskNumber():
    len(taskDict)
	
def taskShow(tid):
	return taskDict[tid].show()

def taskShowAll():
    st = ""
    for t in (taskIds):
        st += taskDict[t].show()
    return st


