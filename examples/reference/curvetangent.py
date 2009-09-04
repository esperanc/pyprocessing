from pyprocessing import *
from math import atan2, cos, sin

noFill()
curve(5, 26, 73, 24, 73, 61, 15, 65)
steps = 6;
for i in range(steps+1):
  t = i / float(steps);
  x = curvePoint(5, 73, 73, 15, t);
  y = curvePoint(26, 24, 61, 65, t);
  #ellipse(x, y, 5, 5);
  tx = curveTangent(5, 73, 73, 15, t);
  ty = curveTangent(26, 24, 61, 65, t);
  a = atan2(ty, tx);
  a -= PI/2.0;
  line(x, y, cos(a)*8 + x, sin(a)*8 + y);

run()
