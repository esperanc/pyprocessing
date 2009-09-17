"""
Adapted from 
/** 
 * Synthesis 1: Form and Code
 * Riley Waves by Casey Reas (www.processing.org)
 * p. 151
 * 
 * Step 3, values are modified to create a new pattern. 
*/
"""

from pyprocessing import *

size(1200, 280);
background(255);
smooth();
noStroke();
#fill(0);
angle = PI;
angle2 = PI;
magnitude = 3;

for i in range(-magnitude,height+magnitude,12):

  angle2 = angle;
  
  fill(0);
  beginShape(TRIANGLE_STRIP);
  for x in range(0,width+1,8):
    y = i + (sin(angle)* magnitude);
    angle += PI/24.0;
    y2 = i+4 + (sin(angle+PI/12)* magnitude);
    vertex(x, y);
    vertex(x, y2);
  endShape();

run()
