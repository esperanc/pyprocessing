

# Introduction #

**Target Audience:** Beginner, Intermediate and Expert Users

<br />
# Topics #
## Animations ##
```

"""
   Adapted from "Chronosynclastic Curlicue Clock"
    http://studio.sketchpad.cc/sp/pad/view/ro.9PXzsGOaaeT-z/rev.41

    Originally created by Fergus Ray Murray using ProcessingJS
"""

from pyprocessing import *


STEP_SIZE=28 # Each seed value gives a different fractal.
DDDF=0.000000005 # dddf controls how much the fractal changes with each frame.
START_TIME=3600*hour()+60*minute()+second() # How many seconds since midnight?

def setup():
  size (600, 600)
  colorMode (HSB, 360)
  background (0)
  frameRate(15)

def draw(): 
  # We need to reset most of the variables every frame.
  strokeWeight(2)
 
  fill(0, 6)
  stroke(255)
  rect(0, 0, width, height)
  # Hours
  ddf=TWO_PI*(START_TIME+millis()/1000.0)/86400.0 
  curlicue (ddf*1440, 9, 32.0, 0, 30) # seconds (1 rev/minute) 
  curlicue (ddf*24, 60, 16.0, 80, 75) # minutes (1 rev/hour) 
  curlicue (ddf, 360, 8.0, 150, 90)  # hours (1 rev/24 hours) 

 
def curlicue(ddf,curlLength,stepSize,baseHue,hueRange):  
  f=0.0
  df=0.0
  x=width/2
  y=height/2
  strokeWeight (stepSize/2)

  for i in range(0,curlLength,1): 
    stroke (baseHue+(float(i)/curlLength)*hueRange, 360, 360, 60)
    f+=df
    df+=ddf
    x+=stepSize*sin(f)
    y-=stepSize*cos(f)
    point(x, y)
    point(width-x, height-y)

run()
```
## Generative Art ##
### Motion ###
> Work In Progress
<br />

### Noise Function ###
```
from pyprocessing import *

RADIUS = 100.0
CENTX = 250
CENTY = 150
START_NOISE = 0.0
NOISE_STEP = 0.0

eyeRootx= 0.0
eyeRooty= 0.0 
eyeXnoise= 0.0
eyeYnoise = 0.0
eyeDistRootX= 0.0 
eyeDistRootY= 0.0 
eyeDistXnoise= 0.0 
eyeDistYnoise = 0.0

def setup():
  size(500,300)
  background(255)
  strokeWeight(5)
  smooth()
  frameRate(12)
  
  stroke(0, 30)
  noFill()
  ellipse(CENTX,CENTY,RADIUS*2,RADIUS*2)
  
  STARTNOISE = noise(10)
  NOISESTEP = 0.1
 
  eyeRootx = (width/2) - 50
  eyeRooty = height/2
  eyeXnoise = noise(10)
  eyeYnoise = noise(10)
  eyeDistRootX = 30
  eyeDistRootY = 0
  eyeDistXnoise = noise(10)
  eyeDistYnoise = noise(10) 
  
  strokeWeight(1)



def draw():
   global START_NOISE, NOISE_STEP, eyeXnoise, eyeYnoise

   stepStep = 0.01  
   fill(255, noise(10))
   noStroke()
   rect(0,0,width,height)
   fill(20, 50, 70, noise(50))
   rect(0,0,width,height)
  
   START_NOISE += 0.01
   NOISE_STEP += stepStep
   
   if (NOISE_STEP > 5):
      stepStep *= -1
   elif(NOISE_STEP < -5):
      stepStep *= -1
      ##end if

   x =0.0
   y =0.0
   noiseval = START_NOISE
  
   fill(255, 150)
   stroke(20, 50, 70)
   beginShape()
   vertex((width/2)-20, height)
  
   for ang in range(90, 430,15):    
      noiseval += NOISE_STEP
      radVariance = 40 * customNoise(noiseval)
    
      thisRadius = RADIUS + radVariance
      rad = radians(ang)
      x = CENTX + (thisRadius * cos(rad))
      y = CENTY + (thisRadius * sin(rad))
    
      curveVertex(x,y)
      ##end for...
  
   curveVertex((width/2)+20, height)
   curveVertex((width/2)+20, height)
   vertex((width/2)-20, height)
   endShape()
   
  
   eyeXnoise += 0.01
   eyeYnoise += 0.01
  
   eye1x = eyeRootx + (noise(eyeXnoise) * 40) - 20
   eye1y = eyeRooty + (noise(eyeYnoise) * 20) - 10
   eyeDistX = eyeDistRootX + (noise(eyeXnoise) * 20) - 100
   eyeDistY = eyeDistRootY + (noise(eyeYnoise) * 40) - 200
   stroke(0)
   fill(255)
   ellipse(eye1x+200, eye1y+100, 20, 20)
   ellipse(eye1x+eyeDistX, eye1y+eyeDistY, 20, 20)
   fill(0)
   ellipse(eye1x+200, eye1y+100, 5, 5)
   ellipse(eye1x+eyeDistX, eye1y+eyeDistY, 5, 5)
   ##end def draw()
  

def customNoise(value):   # returns value -1 to +1
   retValue = sin(value)
   count = int((value % 10))
   for i in range(0, count, 1):
     retValue *= sin(value)
   
   return retValue 

 
run()

```


### Shapes ###
Work in Progress
<br />
## Simulations ##