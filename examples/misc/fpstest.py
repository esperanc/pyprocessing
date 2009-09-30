from pyprocessing import *
from random import random

# Choose the total number of bouncing balls
nballs = 100
balls = []

def setup():
    hint('DOUBLE_FLIP_POLICY')
    size(400,400)
    smooth()
    noStroke()
    colorMode(HSB,1.0)
    ellipseMode(CENTER)
    # generate n balls with random positions, sizes, speeds and colors
    for i in range(nballs):
        # position
        x = int(random()*width)
        y = int(random()*height)
        # speed
        vel = random()*4+2
        ang = random()*TWO_PI
        dx = vel*cos(ang)
        dy = vel*sin(ang)
        # radius
        r = random()*20+4
        # color
        c = color(random(),random()*0.5+0.5,random()*0.5+0.5)
        balls.append([x,y,dx,dy,r,c])
    colorMode(RGB,256)

def draw():
    # fade the last frame by drawing background in transparent color
    fill(255,50)
    rect(0,0,width,height)
    # draw/bounce balls
    for i,(x,y,dx,dy,r,c) in enumerate(balls):
        fill(c)        
        x += dx
        newx = constrain(x,r,width-r)
        if newx != x: dx,x = -dx,newx
        y += dy
        newy = constrain(y,r,height-r)
        if newy != y: dy,y = -dy,newy
        balls[i][0:4] = x,y,dx,dy
        ellipse(x,y,r,r)
    fill(0)
    text("%3d"%frame.rate,0,20)
        
run()
