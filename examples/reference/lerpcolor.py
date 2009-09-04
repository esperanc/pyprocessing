from pyprocessing import *

stroke(255);
background(51);
frm = color(204, 102, 0);
to = color(0, 102, 153);
interA = lerpColor(frm, to, .33);
interB = lerpColor(frm, to, .66);
fill(frm);
rect(10, 20, 20, 60);
fill(interA);
rect(30, 20, 20, 60);
fill(interB);
rect(50, 20, 20, 60);
fill(to);
rect(70, 20, 20, 60);

run()
