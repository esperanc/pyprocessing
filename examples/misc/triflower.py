"""
Adapted from the TriFlower sketch of Ira Greenberg
"""

#
# Triangle Flower 
# by Ira Greenberg. 
# 
# Using rotate() and triangle() functions generate a pretty 
# flower. Uncomment the line "// rotate(rot+=radians(spin));"
# in the triBlur() function for a nice variation.
#

from pyprocessing import *

p = [None]*3
shift = 1.0
fade = 0
fillCol = 0
rot = 0
spin = 0

def setup():
  size(200, 200);
  background(0);
  smooth();
  global fade,spin
  fade = 255.0/(width/2.0/shift);
  spin = 360.0/(width/2.0/shift);
  p[0] = PVector (-width/2, height/2)
  p[1] = PVector (width/2, height/2)
  p[2] = PVector (0, -height/2)
  noStroke()
  translate(width/2, height/2)
  triBlur()

def triBlur():
  global fillCol,rot
  fill(fillCol)
  fillCol+=fade
  rotate(spin)
  # another interesting variation: uncomment the line below 
  # rot+=radians(spin); rotate(rot)
  p[0].x+=shift; p[0].y-=shift; p[1].x-=shift; p[1].y-=shift; p[2].y+=shift; 
  triangle (p[0].x, p[0].y, p[1].x, p[1].y, p[2].x, p[2].y)
  if p[0].x<0:
    # recursive call
    triBlur()

run()
