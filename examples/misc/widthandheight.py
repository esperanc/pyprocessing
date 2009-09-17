from pyprocessing import *

size(200, 200);
background(127);
noStroke();
for i in range(0,height,20):
  fill(0);
  rect(0, i, width, 10);
  fill(255);
  rect(i, 0, 10, height);
    
    
run()
