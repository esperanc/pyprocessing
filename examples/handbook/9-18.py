from pyprocessing import *

# Change the saturation and brightness, hue constant
colorMode(HSB);
for i in range(100):
  for j in range(100):
    stroke(132, j*2.5, i*2.5);
    point(i, j)

run()

