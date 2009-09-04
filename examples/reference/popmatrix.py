from pyprocessing import *

rect(0, 0, 50, 50);  #White rectangle
pushMatrix();
translate(30, 20);
fill(0);  
rect(0, 0, 50, 50);  #Black rectangle
popMatrix();
fill(102);  
rect(15, 10, 50, 50); #Gray rectangle

run()
