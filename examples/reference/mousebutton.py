from pyprocessing import *
 	
# Click within the image and press
# the left and right mouse buttons to 
# change the value of the rectangle
def draw():
  if (mouse.pressed and (mouse.button == LEFT)):
    fill(0);
  elif (mouse.pressed and (mouse.button == RIGHT)):
    fill(255);
  else:
    fill(126);
  
  rect(25, 25, 50, 50);


run()
