from pyprocessing import *

size(200,200)

def mouseDragged():
    # scribble a line with the mouse
    line (pmouse.x, pmouse.y, mouse.x, mouse.y)
    
def keyPressed():
    # typing 'C' clears the screen
    if key.char in 'cC':
        background(200)

run()
