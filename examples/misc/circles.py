from pyprocessing import *

size(300,300)
hint(DISABLE_DEPTH_TEST)
smooth()

l = []

def mousePressed():
    l.append ([mouse.x,mouse.y,1])
    
def mouseDragged():
    l.append ([mouse.x,mouse.y,1])
    
def draw():
    fill(0,10)
    noStroke()
    rect(0,0,width,height)
    stroke(255)
    nl = l[:]
    l[:]=[]
    for x,y,w in nl:
        g = 255-w
        if g<0: continue
        stroke(g)
        ellipse(x,y,w,w)
        l.append([x,y,w+2])
        
run()
