from pyprocessing import *

balls = [(20,20,2.5,3,10),(100,50,-3.5,-3,15)]

def setup():
    size(150,150)
    ellipseMode(CENTER)
    noStroke()

def draw():
    fill(200,50)
    rect(0,0,150,150)
    fill(0)
    for i in range(len(balls)):
        x,y,dx,dy,r = balls[i]
        x += dx
        if constrain(x,r,150-r) != x: dx = -dx
        y += dy
        if constrain(y,r,150-r) != y: dy = -dy
        balls[i] = x,y,dx,dy,r
        ellipse(x,y,r,r)

run()
