from pyprocessing import *

size(200,200)
poly = []
smooth()
def mousePressed():
    poly [:] = [(mouse.x,mouse.y)]

def mouseDragged():
    poly.append((mouse.x,mouse.y))
    
def draw():
    background(200)
    beginShape()
    for x,y in poly: vertex(x,y)
    endShape(CLOSE)

run()


