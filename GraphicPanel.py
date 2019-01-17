##Module: chronogram

from Tkinter import Tk, Canvas, Frame, BOTH

fct = 2
separation = 60
offset = 60
inc = 20
heigth = 15
tNum = 0
taskId = {}
fout = "chronogram.svg"

xmax = 0
ymax = 0
lines = 0
monocore = None
labels = []
taskIds = {}

palette = [ "blue", "darkorange", "darkgreen", "darkred", "blueviolet", "brown", "magenta",
 "navy", "olivedrab", "orange", "violet", "peru",
 "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", 	
 "cyan", "darkblue", "darkcyan", "darkgoldenrod", 
 "darkkhaki", "darkmagenta", "darkolivegreen", 
"darkorchid",  "darksalmon", "darkseagreen", "darkslateblue", 
"darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", 
 "dodgerblue", "firebrick", "forestgreen", 
"fuchsia",  "gold", "goldenrod", "orangered",
 "green", "greenyellow",  "hotpink", "indianred", "khaki",  "lawngreen", 
 "lightblue", "lightcoral", 
"lightgreen", "lightgrey", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", 
"lightslategrey", "lightsteelblue",  "lime", 
"limegreen",  "maroon", "mediumaquamarine", "mediumblue", 
"mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise",
"mediumvioletred", "midnightblue",
"orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", 
"peachpuff", "pink", "plum", "powderblue", "purple", 
"red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", 
"seagreen", "sienna", "skyblue", "slateblue", 
"slategray", "slategrey", "springgreen", "steelblue", "tan", 
"teal", "thistle", "tomato", "turquoise",  "wheat", 
 "yellow", "yellowgreen"]


color = []
dwg = None
root = None

    
def chronoInit(nlines, width, fname):
    global xmax, ymax, lines, monocore, dwg
    global root

    monocore = (nlines == 1)
    lines = nlines
    xmax = width * fct
    ymax = lines * separation 
    fout = fname+".svg"

    root=Tk()
    dwg = Canvas(root, width=xmax+offset, height=4*ymax+offset)
    root.wm_title("Cronograma")
    dwg.pack()

 #   dwg = svgwrite.Drawing(fout, profile='tiny')

    for i in range(lines):
        labels.append("")

    #dwg.add(dwg.rect((offset, offset), size=(xmax, ymax), fill='snow'))
    dwg.create_rectangle(offset, offset, offset + xmax, offset + ymax, fill="snow")

    xpos = 0
    while (xpos <= xmax):

        #dwg.add(dwg.line((offset + xpos, offset), (offset + xpos, offset + ymax), stroke='grey', stroke_width=1).dasharray([3,6]))
        #dwg.add(dwg.line((offset + xpos + inc/2, offset), (offset + xpos + inc/2, offset + ymax), stroke='gray').dasharray([1,5]))
        #dwg.add(dwg.text(str(xpos), insert=(offset + xpos-3, 6+offset + ymax), font_size="6px"))

        dwg.create_line(offset + xpos, offset, offset + xpos, offset + ymax, fill="grey")
        dwg.create_line(offset + xpos + inc/2, offset, offset + xpos + inc/2, offset + ymax, fill="gray")
        dwg.create_text(offset + xpos-3, 6+offset + ymax, text=str(xpos/2), fill="black", font=("Helvetica", 6))
        
        xpos += inc
    

def chronoAddLine(nline, tag):
    global dwg
    xoff = 30
    labels[nline] = tag
    lpos = nline + 1
    dwg.create_text(xoff, lpos * separation, text=labels[nline], fill="black", font=("Helvetica", 14))
    dwg.create_line(offset, lpos * separation, offset+ xmax, lpos * separation, fill="black")

#    dwg.add(dwg.text(labels[nline], insert=(0, lpos * separation)))
 #   dwg.add(dwg.line((offset, lpos * separation), (offset+ xmax, lpos * separation), stroke='black'))


def chronoAddExec(nline, start, end, task):
    global dwg, tNum
    ntask = int(task[1:])
    if (taskIds.has_key(task)):
        ntsk = taskIds[task]
    else:
        taskIds[task] = tNum % len(palette)
        ntsk = tNum
        tNum += 1

    lpos = nline + 1
 #   dwg.add(dwg.rect((start + offset, (lpos * separation)-heigth), size=(end-start, heigth), fill=palette[ntsk]))
    x0 = (fct*start) + offset
    y0 = (lpos * separation) - heigth 
    if (monocore):
        y0 = y0 + (ntask * heigth)
    x1 = offset + (fct*end)
    y1 = y0 + heigth 
    dwg.create_rectangle(x0, y0, x1, y1, fill=palette[ntsk])


    
def chronoClose():
    global dwg
    xpos = offset 
    ypos = ymax + 55
    part = -1
    for (tsk, idx)  in sorted(taskIds.items(), key=lambda params: params[0]):
        prt = tsk[1:3]
        if (prt != part):
            ypos = ypos + 15
            xpos = offset
            part = prt
            dwg.create_text(xpos, ypos+7, text="P"+str(prt)+":", fill="black", font=("Helvetica", 10))
#           dwg.add(dwg.text("P"+str(prt)+":", insert=(xpos, ypos+7), font_size="6px"))
            xpos = xpos + 40
 #       dwg.add(dwg.text(tsk, insert=(xpos, ypos+7), font_size="6px"))
        dwg.create_text(xpos, ypos+7, text=tsk, fill="black", font=("Helvetica", 10))
        dwg.create_rectangle(xpos + 15, ypos, xpos + 15+10, ypos+heigth, fill=palette[idx])
# dwg.add(dwg.rect((xpos + 15, ypos), size=(10, heigth), fill=palette[idx]))
        xpos = xpos + offset + 20

#    dwg.save()
    root.mainloop()
