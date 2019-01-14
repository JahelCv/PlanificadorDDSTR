class CPU:

    NoCPUs = 0; 
  
    def __init__(self, id):  # 
		self.id = id
		self.status = 0
		self.cTask = "Idle"
		self.prio = 0
		self.clk = 0
		self.period = 0
		self.relDead = 0
		self.wcet = 0
		self.absDead = 0
		self.texec = 0
		self.njob = 0		
		self.totalticks = 0
		self.event = []
		self.event.append(("B", "Idle", 0, 0))	
		CPU.NoCPUs += 1

    def cpuId(self):
        return self.id

    def cpuCurrentTask(self):
        return self.cTask

    def cpuAlloc(self, clk, tid, prio,  period, rdead, adead, wcet, texec, njob):
        previousState = (self.prio, self.cTask, (self.period, self.relDead, self.wcet), (self.absDead, self.texec, self.njob))
        self.event.append(("E", self.cTask, clk, self.njob))
        self.cTask = tid 
        self.status = 1
        self.prio = prio
        self.period = period
        self.relDead = rdead
        self.wcet = wcet
        self.absDead = adead
        self.texec = texec
        self.njob = njob		
        self.event.append(("B", tid, clk, njob))
        return previousState

    def cpuIdle(self, clk):
        previousState = (self.prio, self.cTask, (self.period, self.relDead, self.wcet), (self.absDead, self.texec, self.njob))
        self.event.append(("E", self.cTask, clk, self.njob))
        self.status = 0
        self.cTask = "Idle"
        self.prio = 0
        self.clk = 0
        self.period = 0
        self.relDead = 0
        self.wcet = 0
        self.absDead = 0
        self.texec = 0
        self.njob = 0		
        self.event.append(("B", "Idle", clk, 0))	
        return previousState

    def cpuTaskAbort(self, clk):
        previousState = (self.prio, self.cTask, (self.period, self.relDead, self.wcet), (self.absDead, self.texec, self.njob))
        self.event.append(("EA", self.cTask, clk, self.njob))
        self.status = 0
        self.cTask = "Idle"
        self.prio = 0
        self.clk = 0
        self.period = 0
        self.relDead = 0
        self.wcet = 0
        self.absDead = 0
        self.texec = 0
        self.njob = 0		
        self.event.append(("B", "Idle", clk, 0))	
        return previousState


    def cpuPrio(self):
        return self.prio

    def cpuIsIdle(self):
        return (self.cTask == "Idle")

    def cpuContext(self):
        return (self.prio, self.cTask, (self.period, self.relDead, self.wcet), (self.absDead, self.texec, self.njob))
               
    def cpuRunTicks(self, nticks):
        if ((self.cTask != "Idle") and (self.status == 1)): 
            self.texec = self.texec + nticks
            self.totalticks += nticks
            if (self.wcet == self.texec):
            	self.status = 0
            return self.wcet -  self.texec
        else:
            return 99999999

    def cpuRemainTicks(self):
        if ((self.cTask != "Idle") and (self.status == 1)):
            return self.wcet - self.texec # wcet - texec
        else:
        	return 999999999
    
    def cpuInfo(self):
        return (self.id, self.cTask, self.prio, self.period, self.relDead, self.absDead, self.wcet, self.texec, self.njob)

    def cpuShow(self):
		#print "CPU( " +str(self.id)
		ans = ""
		nact = {}
		acct = {}
		for i in range(len(self.event)):
		    (com, tsk, clk, nj) = self.event[i]
		    if (tsk != "Idle"):
		        if (com == "B"):
		            ans += "["+self.id+", "+ tsk+", " + str(clk) + ", " 
		            c1 = clk
		        elif (com == "E"):
		            ans += str(clk) + ", " + str(clk-c1) + ", ("+str(nj)+ ")]\n"
		            if (nact.has_key(tsk)):
		                nact[tsk] += 1
		                acct[tsk] += clk-c1
		            else:
		                nact[tsk] = 1
		                acct[tsk] = clk-c1
		for key in sorted(nact.keys()):
		    rel = acct[key] / nact[key]
		    #print "No Activations of: ", key , ":", nact[key], " Total ticks:", acct[key], "(", rel, ")"
		return ans

    def cpuChrono(self):
		nact = {}
		acct = {}
		chrono = []
		value = (0,0,0)
		for i in range(len(self.event)):
		    (com, tsk, clk, nj) = self.event[i]
		    if (tsk != "Idle"):
		        if (com == "B"):
		            tsk = self.id
		            start = clk
		        elif (com == "E"):
		            chrono.append((tsk, start, clk))
		return chrono