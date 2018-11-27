##Module: Tracer
import random

periods = [20 ,25 ,40 ,50 ,100 ,125 ,200 ,250 ,500 ,1000]

def adjust(v, nd):
	return float(float(round(v * 10**nd)) / 10**nd)
	
def UUniFastDiscard(n, u, nsets):
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(nextSumU)

        # If no task utilization exceeds 1:
        if not [ut for ut in utilizations if ut > 1]:
            sets.append(utilizations)

    return sets

def unsorted(list):
    ulist = []
    while (len(list) > 0):
        idx = random.randint(0,100) % len(list)
        ulist.append(list[idx])
        del list[idx]
    return ulist
    
def UUniFast1(nelem, u):
    n = nelem
    if (n == 1):
        return [u]
    ur = u / float(n)
    values = []
    for i in range(n):
        values.append(ur)

    for i in range(n*4):
        pos = n-1
        val = (random.random() * 0.25)
        delta = values[pos] * val
        values[pos] = adjust(values[pos] - delta , 3)
        pos = random.randint(0,100) % (n-1)
        values[pos] = adjust(values[pos] + delta, 3)
        values.sort()
    
    return unsorted(values)

def UUniFast(nelem, u):
    n = nelem
    values = UUniFastX(n, u)

    for i in range(n):
        pos = n-1
        val = (random.random() * 0.25)
        delta = values[pos] * val
        values[pos] = adjust(values[pos] - delta , 3)
        pos = random.randint(0,100) % (n-1)
        values[pos] = adjust(values[pos] + delta, 3)
        values.sort()
    for i in range(n):
        pos = 0
        val = (random.random() * 0.25)
        delta = values[pos] * val
        values[pos] = adjust(values[pos] + delta , 3)
        pos = (random.randint(0,100) % (n-1) ) + 1
        values[pos] = adjust(values[pos] - delta, 3)
        values.sort()
    if (values[n-1] > 0.82):
    	delta = values[n-1] - 0.819
    	values[0] = values[0] + delta
    	values[n-1] = values[n-1] - delta
    return unsorted(values)
    
def UUniFastX(n, u):
    if (n == 1):
        return (u)
    values = UUniFastDiscard(n, u, 1)
    utils = values[0]
    for i in range(len(utils)):
        utils[i] = adjust(utils[i], 4)
    return utils   
    
def PeriodWCET (u):    #Determina el periodo y wcet que se ajusten a u. Periodo tiene que ser un elemento de periods
    per = random.choice(periods)
    wcet = int(u * per)
    if (wcet == 0):
    	wcet = 1
    return [per, wcet] 

def lcm(x,y):
    if x > y:
        greater = x
    else:
       greater = y
    while(True):
        if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
        greater += 1
    return lcm

def HyperPeriod(pers):    # determina el hiperperiodo de la lista de periodos 
    hypPer = pers.pop()
    while len(pers) > 0:
        hypPer = lcm(hypPer,pers[len(pers)-1])
        k = pers.pop()
    return hypPer
