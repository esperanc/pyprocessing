from pyprocessing import *

def setup():
  size(200, 100, resizable=True)

def draw():
  lights()
  # First camera
  glViewport (0,0,width/2,height)
  background (200)
  glMatrixMode (GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt (-3, 0, 100, 0, 0, 0, 0, 1, 0)
  glMatrixMode (GL_PROJECTION)
  gluPerspective (60,float(height)
  box(45)
  

run()
