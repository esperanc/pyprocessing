from pyprocessing import *

size(200, 200);
background(100);
smooth();
noStroke();

diameter = 150;
angs = [30, 10, 45, 35, 60, 38, 75, 67];
lastAng = 0;

for a in angs:
  fill(a * 3.0);
  arc(canvas.width/2, canvas.height/2, diameter, diameter, lastAng, 
      lastAng+radians(a))
  lastAng += radians(a)
    
run()
