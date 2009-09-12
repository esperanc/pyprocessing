from pyprocessing import *

def setup():
    size(200,200)
    noStroke()

def draw():
    background(200)
    if mouse.pressed: lightFalloff(1,0,1e-4)
    pointLight(255,255,255,100,100,50)
    nx = 6
    ny = 6
    for i in range(nx):
        for j in range(ny):
            pushMatrix()
            translate((i+0.5)*canvas.width/nx,(j+0.5)*canvas.height/ny)
            sphere(10)
            popMatrix()

run()
