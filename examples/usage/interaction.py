from pyprocessing import *

size(200,200)

def draw():
    # scribble a line with the mouse
    if mouse.pressed:
        line (pmouse.x, pmouse.y, mouse.x, mouse.y)
    # typing 'C' clears the screen
    if key.pressed and key.char in 'cC':
        background(200)

run()
