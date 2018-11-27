##Module: chronogram

import svgwrite

separation = 50
offset = 20
inc = 20
heigth = 10
tNum = 0
taskId = {}
fout = "chronogram.svg"

xmax = 0
ymax = 0
lines = 0
labels = []
taskIds = {}

palette = [ "blue", "darkorange", "darkgreen", "darkred", "blueviolet", "brown", "magenta", "indigo", 
 "navy", "olive", "olivedrab", "orange", "violet", "peru",
 "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue",    
"crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", 
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

    
def chronoInit(nlines, width, fname):
    global xmax, ymax, lines, dwg

    lines = nlines
    xmax = width
    ymax = lines * separation
    fout = fname+".svg"
    for i in range(lines):
        labels.append("")
    dwg = svgwrite.Drawing(fout, profile='tiny')
    dwg.add(dwg.rect((offset, offset), size=(xmax, ymax), fill='snow'))
    
    xpos = 0
    while (xpos <= xmax):
        dwg.add(dwg.line((offset + xpos, offset), (offset + xpos, offset + ymax), stroke='grey', stroke_width=1).dasharray([3,6]))
        dwg.add(dwg.line((offset + xpos + inc/2, offset), (offset + xpos + inc/2, offset + ymax), stroke='gray').dasharray([1,5]))
        dwg.add(dwg.text(str(xpos), insert=(offset + xpos-3, 6+offset + ymax), font_size="6px"))
        xpos += inc
    

def chronoAddLine(nline, tag):
    global dwg
    labels[nline] = tag
    lpos = nline + 1
    dwg.add(dwg.text(labels[nline], insert=(0, lpos * separation)))
    dwg.add(dwg.line((offset, lpos * separation), (offset+ xmax, lpos * separation), stroke='black'))


def chronoAddExec(nline, start, end, task):
    global dwg, tNum
    if (taskIds.has_key(task)):
        ntsk = taskIds[task]
    else:
        taskIds[task] = tNum % len(palette)
        ntsk = tNum
        tNum += 1
    lpos = nline + 1
    dwg.add(dwg.rect((start + offset, (lpos * separation)-heigth), size=(end-start, heigth), fill=palette[ntsk]))


    
def chronoClose():
    xpos = offset 
    ypos = ymax + 20
    part = -1
    for (tsk, idx)  in sorted(taskIds.items(), key=lambda params: params[0]):
        prt = tsk[1:3]
        if (prt != part):
            ypos = ypos + 15
            xpos = offset
            part = prt
            dwg.add(dwg.text("P"+str(prt)+":", insert=(xpos, ypos+7), font_size="6px"))
            xpos = xpos + 20
        dwg.add(dwg.text(tsk, insert=(xpos, ypos+7), font_size="6px"))
        dwg.add(dwg.rect((xpos + 15, ypos), size=(10, heigth), fill=palette[idx]))
        xpos = xpos + offset + 20

    dwg.save()