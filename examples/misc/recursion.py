from pyprocessing import *

def setup() :
  size(200, 200)
  noStroke()
  smooth()
  noLoop()

def draw():
  drawCircle (126, 170, 6)

def drawCircle (x, radius, level):
  fill(126 * level/4.0)
  ellipse(x, 100, radius*2, radius*2)
  if level > 1:
    level = level - 1
    drawCircle(x - radius/2, radius/2, level)
    drawCircle(x + radius/2, radius/2, level)

run()
