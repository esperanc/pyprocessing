from pyprocessing import *

for i in range(30,width-15):
    for j in range(20,height-25):
        c = color(204-j, 153-i, 0);
        setScreen(i, j, c);


run()

