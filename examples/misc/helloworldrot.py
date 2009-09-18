from pyprocessing import *

size(300,300)
textFont(createFont("Times New Roman", 36))
textAlign(CENTER,CENTER)
ang = 0

def draw():
    global ang
    background(0,0,0)
    fill (255)
    translate (width/2, height/2)
    rotateZ (ang)
    ang += 0.01
    text("Hello world", 0, 0)

run()

