##Module: BinPacking
import random

politicas = ("FF", "NF", "BF", "WF")
politica = "" 
criterio = ""
NBins = 0
Bins = {}
Pesos = []
nextBin = 0
init = 0
nFallos = 0

def adjust(v, nd):
    return float(float(round(v * 10**nd)) / 10**nd)

def initBin(metodo, nbins):
    global politica,  NBins, Pesos, init, nextBin, nFallos
    if (metodo in politicas):
        politica = metodo;
    else:
        raise Invalid_Param
    if (nbins >0):
        NBins = nbins
    else:
        raise Invalid_Param
    Pesos = [0.0] * NBins
    for i in range(NBins):
        Bins[i] = []
    init = 1
    nextBin = 0
    nFallos = 0

def binAdd(item, peso):      
# "anade un item a una de las lista con un peso de acuerdo al metodo y criterio definido en initBins"
    #print "binAdd", item, peso
    if (politica == "FF"):
        ok = binAddFF(item, peso)
    elif (politica == "NF"):
        ok = binAddNF(item, peso)
    elif (politica == "BF"):
        ok = binAddBF(item, peso)
    elif (politica == "WF"):
        ok = binAddWF(item, peso)
    return ok


def binAddFF(item, peso):
    #print "addFF", item, peso, NBins
    global Pesos, nFallos
    allocated = 0
    i = 0
    while (allocated == 0) and (i < NBins):
        if ((Pesos[i] + peso) <= 1.0):
            b = Bins[i]
            b.append(item)
            Pesos[i] = adjust(Pesos[i] + peso, 2)
            allocated = 1
        i += 1
    if (allocated == 0):
        nFallos += 1
        return False
    else:
        return True

def binAddNF(item, peso):
    #print "addNF", item, peso
    global nextBin, nFallos
    allocated = 0
    i = nextBin
    n = 0
    while (allocated == 0) and (n < NBins):
        if ((Pesos[i] + peso) <= 1.0):
            b = Bins[i]
            b.append(item)
            Pesos[i] = adjust(Pesos[i] + peso, 2)
            allocated = 1
            nextBin = i
        i = (i + 1) % NBins
        n += 1
    if (allocated == 0):
        nFallos += 1
        return False
    else:
        return True

def binAddBF(item, peso):
    #print "addBF", item, peso
    global Pesos, nFallos
    allocated = 0
    pcp = []
    for i in range(len(Pesos)):
        tmp = (Pesos[i], i)
        pcp.append(tmp)
    pcp.sort()
    i = 0
    while (allocated == 0) and (i < NBins):
        tmp = pcp.pop(-1)
        p = tmp[0]
        pos = tmp[1]
        if ((p + peso) <= 1.0):
            b = Bins[pos]
            b.append(item)
            Pesos[pos] = adjust(Pesos[pos] + peso, 2)
            allocated = 1
            nextBin = i
        i += 1
    if (allocated == 0):
        nFallos += 1
        return False
    else:
        return True
    
def binAddWF(item, peso):
    global Pesos, nFallos
    allocated = 0
    pcp = []
    for i in range(len(Pesos)):
        tmp = (Pesos[i], i)
        pcp.append(tmp)
    pcp.sort()
    i = 0
    while (allocated == 0) and (i < NBins):
        tmp = pcp.pop(0)
        p = tmp[0]
        pos = tmp[1]
        if ((p + peso) <= 1.0):
            b = Bins[pos]
            b.append(item)
            Pesos[pos] = adjust(Pesos[pos] + peso, 2)
            allocated = 1
            nextBin = i
        i += 1
    if (allocated == 0):
        nFallos += 1
        return False
    else:
        return True
    

def binGetbyIndex(idx):   
#    "devuelve una lista con una lista de items y su peso (("P1", "P2"), 0,87)"
    return (Bins[idx], Pesos[idx])

def binGetAll():
#    "devuelve todas las listas de cada bin y una lista con los pesos" 
    return (Bins, Pesos)

def binUtil(idx):
#    "devuelve el peso de la lista identificada or idx"
    return 1

def binUtilAll():
#    "devuelve la lista de los pesos"
     return Pesos
   
def binDiscrepancy():
#    "devuelve una lista con las diferencias de peso de los bins. Por ejemplo: si la 0: 40, 1: 50, 2:60  3: 38"
#    "la funcion devolveria (2, 12, 22, 0) la minima es cero y el resto la diferencia respecto a la min"
     p = Pesos
     p.sort()
     min = p[0]
     disc = []
     for i in range(len(p)):
        n = adjust(p[i] - min, 2)
        disc.append(n)
     return disc

def binNFallos():
    return nFallos
    
def show():
    spesos = 0.0
    for i in range(len(Pesos)):
        spesos += Pesos[i]
    out = ""
    for n in range(NBins):
        b = Bins[n]
        p = Pesos[n]
        out += "Core"+str(n)+": "+ str(b)+"  Util: "+str(p)+"\n" 
    out += " Suma Util:"+ str(spesos)+ "\n"
    print out