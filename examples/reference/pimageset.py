from pyprocessing import *

img = loadImage("images/tower.jpg");
black = color(0, 0, 0);
img.set(30, 20, black); 
img.set(85, 20, black); 
img.set(85, 75, black); 
img.set(30, 75, black); 
image(img, 0, 0);

run()

