from pyprocessing import *
 	
# Drag (click and hold) your mouse across the 
# image to change the value of the rectangle

value = 0;

def draw():
  fill(value);
  rect(25, 25, 50, 50);

def mouseDragged():
  global value
  value = value + 5;
  if (value > 255):
    value = 0;

run()
