from pyprocessing import *

x = 0

def setup():
  size(200, 200);
  noLoop();

def draw():
  background(204);
  line(x, 0, x, height); 

def mousePressed():
  global x
  x += 1;
  redraw();

run()

