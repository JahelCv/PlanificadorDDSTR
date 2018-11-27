class Task:

# Task: se modela mediante una serie de atributos
  #    tid: identificador, nombre de la Tarea 
  #    period: periodo de la tarea
  #.   deadLine: plazo 
  #    wcet: tiempo de peor caso
  #.   util: utilizacion
  #    partId: Identificador de la particion
  #    
  # -------------------------------------------------------------------------

#Constructora
    def __init__(self, tid, partId):  # attributos: Id, Period, Deadline, WCET, Util
        self.tid = tid
        self.partId = partId
        self.util = None
        self.period = None
        self.deadLine = None
        self.wcet = None
        self.util = None

#Modificadora
    def taskParams(self, Per, Dead, Wcet, util):  # deadline = period
        self.period = Per
        self.deadLine = Dead
        self.wcet = Wcet
        self.util = util

    def taskUtil(self, util):
        self.util = util

#Observadora
    def taskGetParams(self):
        return (self.period, self.deadLine, self.wcet, self.util)

    def taskId(self):
        return self.tid

    def taskPeriod(self):
        return self.period  

    def taskDeadline(self):
        return self.deadLine

    def taskWCET(self):
        return self.wcet
    
    def taskUtil(self):
        return self.util

    def taskPartition(self):
        return self.partId
        
    def show(self):
        return "Task( " +str(self.tid)+ ", " +str(self.period)+ ", " +str(self.deadLine)+ ", " +str(self.wcet)+ ", " +str(self.util)+ ", " +str(self.partId)+" )"
    

