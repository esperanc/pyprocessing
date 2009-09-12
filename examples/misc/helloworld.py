from pyprocessing import *

size(300,300,caption="Hello")

textFont(createFont("Times", 36, bold=True, italic=True))
textAlign(CENTER)
text("Hello world", canvas.width/2, canvas.height/2)

run()

