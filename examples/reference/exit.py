from pyprocessing import *

x = 0

def setup():
  size(200, 200);

def draw():
  background(204);
  global x
  x = (x+1)%canvas.width
  line(x, 0, x, canvas.height); 

def mousePressed():
  exit()

run()

