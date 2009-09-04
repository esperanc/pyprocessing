from pyprocessing import *


# Run this program to learn how each of these functions
# relate to the others 

def draw(): pass # Empty draw() needed to keep the program running

def keyPressed():
  print "pressed ", ord(key.char), " ", key.code;

def keyTyped():
  print "typed ", ord(key.char), " ", key.code;

def keyReleased() :
  print "released ", ord(key.char), " ", key.code;


run()
