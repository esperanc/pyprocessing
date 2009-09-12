from pyprocessing import *

# Move the mouse left and right across the image
# to see the cursor change from a cross to a hand

def draw() :
  if mouse.x < 50:
    cursor(CROSS)
  else:
    cursor(HAND)

run()
