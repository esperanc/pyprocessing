from pyprocessing import *

noFill()
camera(0,0,0,0,0,-1,0,1,0);
ortho(0,width,0,height,-100,100)
translate(50,50,0)
rotateX(-PI/6);
rotateY(PI/3);
box(45)

run()
