from pyprocessing import *

noFill();
fov = PI/3.0;
cameraZ = (screen.height/2.0) / tan(fov/2.0);
perspective(fov, float(screen.width)/float(screen.height), 
            cameraZ/10.0, cameraZ*10.0);
translate(50, 50, 0);
rotateX(-PI/6);
rotateY(PI/3);
box(45);

run()
