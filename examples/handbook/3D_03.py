from pyprocessing import *

# Draw a cylinder centered on the y-axis, going down from y=0 to y=height.
# The radius at the top can be different from the radius at the bottom,
# and the number of sides drawn is variable.

def setup() :
  size(400, 400);

def draw():
  background(0);
  lights();
  translate(width / 2, height / 2);
  rotateY(mouse.x * PI / width);
  rotateZ(mouse.y * -PI / height);
  noStroke();
  fill(255, 255, 255);
  translate(0, -40, 0);
  drawCylinder(10, 180, 200, 16); # Draw a mix between a cylinder and a cone
  #drawCylinder(70, 70, 120, 16); # Draw a cylinder
  #drawCylinder(0, 180, 200, 4); # Draw a pyramid

def drawCylinder(topRadius, bottomRadius, tall, sides):
  angle = 0;
  angleIncrement = TWO_PI / sides;
  beginShape(QUAD_STRIP);
  for i in range(sides+1):
    #normal(cos(angle),sin(angle),0)
    vertex(topRadius*cos(angle), 0, topRadius*sin(angle));
    vertex(bottomRadius*cos(angle), tall, bottomRadius*sin(angle));
    angle += angleIncrement;
  endShape();
  
  # If it is not a cone, draw the circular top cap
  if (topRadius != 0):
    angle = 0;
    beginShape(TRIANGLE_FAN);
    
    # Center point
    vertex(0, 0, 0);
    for i in range(sides+1):
      vertex(topRadius * cos(angle), 0, topRadius * sin(angle));
      angle += angleIncrement;
    endShape();

  # If it is not a cone, draw the circular bottom cap
  if (bottomRadius != 0):
    angle = 0;
    beginShape(TRIANGLE_FAN);

    # Center point
    vertex(0, tall, 0);
    for i in range(sides+1):
      vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle));
      angle += angleIncrement;
    
    endShape();

run()
