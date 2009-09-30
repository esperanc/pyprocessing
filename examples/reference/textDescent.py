from pyprocessing import *

font = createFont("Helvetica"); 
textFont(font);

textSize(32); 
descent = textDescent();
text("dp", 0, 70);
line(0, 70+descent, 100, 70+descent); 

textSize(64);
descent = textDescent();
text("dp", 35, 70);
line(35, 70+descent, 100, 70+descent);

run()
