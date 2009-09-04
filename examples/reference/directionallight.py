from pyprocessing import *

hint(ENABLE_DEPTH_TEST)

size(100, 100);
background(0);
noStroke();
directionalLight(51, 102, 126, -1, 0, 0);
translate(20, 50, 0);
sphere(30);

run()
