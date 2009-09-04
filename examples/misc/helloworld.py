from pyprocessing import *

size(300,300,caption="Hello")

textFont(createFont("Times", 36, bold=True, italic=True))
textAlign(CENTER)
text("Hello world", screen.width/2, screen.height/2)

run()

