from pyprocessing import *

def setup() :
    global bg
    size(200,200)
    frameRate(30)
    bg = loadImage("images/doll.jpg")

def draw():
    global bg, a
    background(bg)
    a = (a + 1)%(width+32);
    stroke(226, 204, 0);
    line(0, a, width, a-26);
    line(0, a-6, width, a-32);
  
  
a = 0
run()
