from pyprocessing import *

background(56, 90, 94);
smooth();
x = 0;
strokeWeight(12);
for i in range(51,256,51):
  stroke(242, 204, 47, i);
  line(x, 20, x+20, 80);
  x += 20;

run()
