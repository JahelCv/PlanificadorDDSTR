#module  Cores:

from Core import Core

NoCores = 0; 
coreDict = {}
coreIds = []

def defineCore(cid):  # attributos: 
    global NoCores
    if (not coreDict.has_key(cid)):
        cr = Core(cid)
        coreDict[cid] = cr
        coreIds.append(cid)
        NoCores += 1
        return True
    else:
        return False

def coreAddPartition(cid, pid, pUtil):
    coreDict[cid].coreAddPartition(pid, pUtil)

def coreUtil(cid):   #pone la u efctiva
    return coreDict[cid].coreUtil()
            
def coreParts(cid):    # devuelve la lista de parts
    return coreDict[cid].coreParts()

def partUtil(cid):
    return coreDict[cid].partUtil()

def partUtilEfective(cid, eUtil):
    coreDict[cid].partUtilEfective(eUtil)

def partUtilGetEfective(cid):
    return coreDict[cid].partUtilEfective()

def allCores():
    return coreIds

def coreNumber():
    global NoCores
    return NoCores

def coreShow(cid):
    return coreDict[cid].show()

def coreShowAll():
    st = ""
    for p in (coreIds):
        st += coreDict[p].show()
    return st
