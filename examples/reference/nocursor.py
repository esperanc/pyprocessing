from pyprocessing import *

# Press the mouse to hide the cursor

def draw() :
  if mouse.pressed:
    noCursor()
  else:
    cursor(HAND)

run()
