from pyprocessing import *
import math
import OpenGL.GL as gl

def setup():
    size(200,200)
    noLoop()

def draw(): 
    # clear the whole screen
    background(200)
    lights()
    noStroke()
    background(200)
    pushMatrix()
    fill(255,255,0)
    translate(130,130)
    rotate(PI/6,1,1,0)
    box(50)
    popMatrix()
    fill(255,0,255)
    translate(60, 50)
    sphere(50)
    
    
run()
