from pyprocessing import *

noFill();
translate(50, 50, 0);
rotateY(PI/6); 
stroke(153);
box(35);
# Set rotation angles
ct = math.cos(PI/9.0);
st = math.sin(PI/9.0);          
#Matrix for rotation around the Y axis
applyMatrix(  ct, 0.0,  st,  0.0,
             0.0, 1.0, 0.0,  0.0,
             -st, 0.0,  ct,  0.0,
             0.0, 0.0, 0.0,  1.0);  
stroke(255);
box(50);

run()
