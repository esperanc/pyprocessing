from pyprocessing import *
 	

# Move the mouse quickly to see the difference 
# between the current and previous position 
def draw() : 
  background(204); 
  line(mouse.x, 20, pmouse.x, 80); 

run()
