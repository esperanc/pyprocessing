from pyprocessing import *
from random import random
import sys
import os

nballs = 100
balls = []


"""This script is aimed at users who don't know which Flip Policy is
best suited for their hardware setup. It will automatically display a
simple pyprocessing example and give the user options to say if the
graphics are displayed correctly: if not, then the setup will change
the Flip Policy automatically and run itself again."""




def setup():
    global policy
    if '-nodouble' not in sys.argv:
        hint(DOUBLE_FLIP_POLICY)
        policy = DOUBLE_FLIP_POLICY
    size(400,400)
    smooth()
    noStroke()
    colorMode(HSB,1.0)
    ellipseMode(CENTER)
    for i in range(nballs):
        x = int(random()*width)
        y = int(random()*height)
        vel = random()*4+2
        ang = random()*TWO_PI
        dx = vel*cos(ang)
        dy = vel*sin(ang)
        r = random()*20+4
        c = color(random(),random()*0.5+0.5,random()*0.5+0.5)
        balls.append([x,y,dx,dy,r,c])
    colorMode(RGB,256)

def draw():
    fill(255,50)
    rect(0,0,width,height-100)
    for i,(x,y,dx,dy,r,c) in enumerate(balls):
        fill(c)        
        x += dx
        newx = constrain(x,r,width-r)
        if newx != x: dx,x = -dx,newx
        y += dy
        newy = constrain(y,r,height-r-100)
        if newy != y: dy,y = -dy,newy
        balls[i][0:4] = x,y,dx,dy
        ellipse(x,y,r,r)
    fill(10,200,10)
    rect(0,height-100,width/2,100)	
    fill(200,10,10)
    rect(width/2,height-100,width/2,100)
    fill(0)
    text("Yes, this config is ok",width/30,height-50)
    text("I'm seeing glitches",5*width/9,height-50)
    text("%3d"%frame.rate,0,20)
        
def mouseClicked():
    global contents, policy
    if (height - 100 < mouse.y < height):
        for i in range(len(contents)-1,-1,-1):
            if contents[i].find("flip") != -1 or contents[i] == "": 
                del contents[i]
        if (mouse.x > width/2):
            if fbo.FBO.supported(): policy = FBO_FLIP_POLICY 
	    else: policy = BACKUP_FLIP_POLICY
            f = open(os.path.expanduser("~/.pyprocessing/userconfig.txt"),"w")
            contents.append("flipPolicy:"+policy)
            contents = '\n'.join(contents)
            f.write(contents)
            f.close()
	    os.system('python %s -nodouble'%sys.argv[0])
            sys.exit()
        else:
            if '-nodouble' in sys.argv: sys.exit()
            f = open(os.path.expanduser("~/.pyprocessing/userconfig.txt"),"w")
            contents.append("flipPolicy:"+policy)
            contents = '\n'.join(contents)
            f.write(contents)
            f.close()
            sys.exit()

try:
    f = open(os.path.expanduser("~/.pyprocessing/userconfig.txt"),"r")
    contents = f.read()
    f.close()
    contents = contents.split('\n')
except IOError:
    try:
        os.mkdir(os.path.expanduser("~/.pyprocessing"))
    except OSError: None
    contents = []






run()








