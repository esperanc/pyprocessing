from pyprocessing import *

noStroke()
colorMode(HSB, 100)
for i in range(100):
    for j in range(100):
        stroke(i, j, 100)
        point(i, j)

run()
