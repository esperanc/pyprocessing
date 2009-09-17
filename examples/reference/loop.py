from pyprocessing import *

def setup():
    size(200,200)
    noLoop()
    
x = 0

def draw():
    global x
    background(204)
    x = x+0.5
    if x>width: x = 0
    line(x,0,x,height)


def mousePressed(): loop()

def mouseReleased(): noLoop()
        
run()
