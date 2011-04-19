from pyprocessing import *

def setup():
    size(640, 360);
    noStroke();
    fill(204);

def draw():
    background(0);
    lights();
    if (mouse.pressed):
        fov = PI/3.0; 
        cameraZ = (height/2.0) / tan(fov / 2.0);
        perspective(fov, float(width)/float(height), cameraZ/10.0, cameraZ*10.0); 
    else:
        ortho(-width/2, width/2, -height/2, height/2, -height, height); 

    translate(width/2, height/2, 0);
    rotateX(-PI/6); 
    rotateY(PI/3); 
    box(160); 
  

run()
