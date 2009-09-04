from pyprocessing import *

fillVal = color(126);

def draw():
  fill(fillVal);
  rect(25, 25, 50, 50);

def keyPressed():
  global fillVal
  if (key.char == CODED):
    if (key.code == UP):
      fillVal = 255;
    elif (key.code == DOWN):
      fillVal = 0;
  else:
    fillVal = 126;

run()
