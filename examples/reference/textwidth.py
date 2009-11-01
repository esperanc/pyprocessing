from pyprocessing import *

font = createFont("Times"); 
textFont(font, 28); 

c = 'T';
cw = textWidth(c);
text(c, 0, 40);
line(cw, 0, cw, 50); 

s = "Tokyo";
sw = textWidth(s);
text(s, 0, 85);
line(sw, 50, sw, 100);

run()
