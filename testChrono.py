#!/usr/bin/python

import sys
import os

import chronogram
import GraphicPanel


#-------------------------#
#          MAIN           #
#-------------------------#
def main (argv):

    
    mCores = 4
    hyper = 10000
    
    #chronogram.chronoInit(mCores, hyper, "chrono")
    GraphicPanel.chronoInit(mCores, hyper, "chrono")

#Pone una linea por cada core con su nombre: C0, C1, C2, .....    
    for i in range(mCores):
        #chronogram.chronoAddLine(i, "C"+str(i))
        GraphicPanel.chronoAddLine(i, "C"+str(i))

#ejemplo de lo que pondre en cada core: cada uno de los tiempos en los se ejecuta una tarea 
# conendra el nombre de la tarea el instante de inicio y instante de terminacion


#core 0
    listaEjecuciones = (("T1", 0, 10), ("T2", 10, 20), ("T1", 20, 30), ("T2", 100, 105), ("T1", 160, 200))
    
    for le in listaEjecuciones:
        (tsk, start, end) = le
        #chronogram.chronoAddExec(0, start, end, tsk)
        GraphicPanel.chronoAddExec(0, start, end, tsk)
            
#core 1

    listaEjecuciones = (("T3", 0, 50), ("T4", 60, 80), ("T5", 110, 190), ("T3", 200, 205), ("T5", 250, 290))
    
    for le in listaEjecuciones:
        (tsk, start, end) = le
        #chronogram.chronoAddExec(1, start, end, tsk)
        GraphicPanel.chronoAddExec(1, start, end, tsk)

#core 2
    listaEjecuciones = (("T6", 0, 10), ("T7", 10, 20), ("T6", 40, 70), ("T7", 100, 155), ("T6", 160, 240))
    
    for le in listaEjecuciones:
        (tsk, start, end) = le
        #chronogram.chronoAddExec(2, start, end, tsk)
        GraphicPanel.chronoAddExec(2, start, end, tsk)
            
#core 3

    listaEjecuciones = (("T9", 0, 50), ("T8", 60, 80), ("T9", 110, 180), ("T8", 200, 205), ("T10", 250, 290))
    
    for le in listaEjecuciones:
        (tsk, start, end) = le
        #chronogram.chronoAddExec(3, start, end, tsk)
        GraphicPanel.chronoAddExec(3, start, end, tsk)


#cierra el chronograma y escribe el fichero con el grafico
    #chronogram.chronoClose()
    GraphicPanel.chronoClose()
        
main (sys.argv)