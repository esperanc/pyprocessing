from pyprocessing import *

def setup():
  size(100, 100)

def draw():
  noFill();
  background(200);
  if (mouse.pressed):
     camera(0,0,0,0,0,-1,0,1,0)
     ortho(0,width,0,height,-height,height)
  else:
     camera()
     perspective()
  translate(50, 50, 0);
  rotateX(-PI/6);
  rotateY(PI/3);
  box(45);

run()
