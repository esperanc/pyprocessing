from pyprocessing import *


def setup():	
  global i1,i2,i3,i4,i5,i6
  size(200,300)
  frameRate(30)
  i1 = loadImage("images/arch.jpg")
  i2 = loadImage("images/arch.jpg")
  i3 = loadImage("images/arch.jpg")
  i4 = loadImage("images/arch.jpg")
  i5 = loadImage("images/arch.jpg")
  i6 = loadImage("images/arch.jpg")
  i1.filter(GRAY)
  i2.filter(THRESHOLD,0.4)
  i3.filter(POSTERIZE,5)
  i4.filter(DILATE)
  i5.filter(INVERT)
  i6.filter(OPAQUE)
  
  

def draw():
  global i1,i2,i3,i4,i5,i6
  image(i1,0,0)
  image(i2,100,0)
  image(i3,0,100)
  image(i4,100,100)
  image(i5,0,200)  
  image(i6,100,200)



run()
