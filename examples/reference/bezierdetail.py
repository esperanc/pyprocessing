from pyprocessing import *

def setup():
  size(100, 100);
  noFill();
  noLoop()
  
def draw():
  bezierDetail(1);
  bezier(85, 20, 10, 10, 90, 90, 15, 80);
  stroke(126);
  bezierDetail(3);
  bezier(85, 20, 10, 10, 90, 90, 15, 80);
  stroke(255);
  bezierDetail(12);
  bezier(85, 20, 10, 10, 90, 90, 15, 80);

run()
