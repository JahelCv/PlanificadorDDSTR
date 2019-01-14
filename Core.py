class Core:
      
    def __init__(self, cid): # parametros: Id, PartList,  Util, UtilEfectiva, Nperdidas
		self.cid = cid
		self.partList =[]
		self.util = 0
		self.utilEfectiva = 0
		self.nPerdidas= 0
       
    def coreId(self):      # devuelve el Id
		return Id

    def coreAddPartition(self, pid, u):
		self.partList.append(pid)
		self.util += u

    def coreUtilEfective(self, u):   #pone la u efctiva
		self.utilEfectiva=u
            
    def coreParts(self):    # devuelve la lista de parts
        return self.partList

    def coreUtil(self):           #devuelve la util
		return self.util

    def coreUtilEfectiva(self):	
		return self.utilEfectiva
        
    def show(self):
		return "Core("+self.cid + ", " + str(self.util) + ", " + str(self.partList)+ ")"



