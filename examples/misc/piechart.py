from pyprocessing import *

size(200, 200);
background(100);
noStroke();

diameter = 150;
angs = [30, 10, 45, 35, 60, 38, 75, 67];
lastAng = 0;
smooth()
for a in angs:
  fill(a * 3.0);
  arc(width/2, height/2, diameter, diameter, lastAng, 
      lastAng+radians(a))
  lastAng += radians(a)

run()
