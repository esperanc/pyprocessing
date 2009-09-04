from pyprocessing import *

noFill();
bezier(85, 20, 10, 10, 90, 90, 15, 80);
fill(255);
steps = 10;
for i in range(steps+1):
  t = i / float(steps);
  x = bezierPoint(85, 10, 90, 15, t);
  y = bezierPoint(20, 10, 90, 80, t);
  ellipse(x, y, 5, 5);

run()
