from pyprocessing import *
 	
def setup():
  size(100, 100);


def draw():
  background(204);
  
  x = mouse.x;
  y = mouse.y;
  z = -100;
  
  # Draw "X" at z = -100
  stroke(255);
  line(x-10, y-10, z, x+10, y+10, z); 
  line(x+10, y-10, z, x-10, y+10, z); 
  
  # Draw line in 2D at same x value
  # Notice the parallax
  stroke(102);
  line(x, 0, 0, x, height, 0);
  
  # Draw 2D line to match the x value
  # element drawn at z = -100 
  stroke(0);
  theX = screenX(x, y, z);
  line(theX, 0, 0, theX, height, 0);

run()
