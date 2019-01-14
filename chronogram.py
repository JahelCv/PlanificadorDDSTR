##Module: svgchrono

#import svgchrono
import GraphicPanel
    
def chronoInit(nlines, width, fname):
 #   svgchrono.chronoInit(nlines, width, fname)
    GraphicPanel.chronoInit(nlines, width, fname)

def chronoAddLine(nline, tag):
 #   svgchrono.chronoAddLine(nline, tag)
    GraphicPanel.chronoAddLine(nline, tag)   

def chronoAddExec(nline, start, end, task):
 #   svgchrono.chronoAddExec(nline, start, end, task)
    GraphicPanel.chronoAddExec(nline, start, end, task) 
    
def chronoClose():
 #   svgchrono.chronoClose()
    GraphicPanel.chronoClose() 
