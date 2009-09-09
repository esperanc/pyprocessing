from pyprocessing import *

line(20, 20, 80, 80);
# Saves a PNG file named "diagonal.png"
save("diagonal.png");
# Saves a PNG file named "cross.png"
line(80, 20, 20, 80);
save("cross.png");

run()
