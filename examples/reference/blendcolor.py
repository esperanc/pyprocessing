from pyprocessing import *

orange = color(204, 102, 0);
blue = color(0, 102, 153);
print orange,blue
orangeblueadd = blendColor(orange, blue, ADD);
background(51);
noStroke();
fill(orange);
rect(14, 20, 20, 60);
fill(orangeblueadd);
rect(40, 20, 20, 60);
fill(blue);
rect(66, 20, 20, 60);

run()
