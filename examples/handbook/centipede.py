"""
Adapted from 

/**
 * Synthesis 3: Motion and Arrays
 * Centipede by Ariel Malka (www.chronotext.org)
 * p. 372
 */
"""
from pyprocessing import *

node_length = 30
node_size = node_length-1
n_nodes = 70
nodes = []
delay = 20.0
col_head = color(255, 0, 0)
col_body = color(0)

def setup():
  size(600, 600)
  smooth()
  noStroke()

  global x,y
  x = width/2
  y = height/2

  r1 = 10
  r2 = 100
  dr = r2-r1
  D = 0.0
  
  for i in range(n_nodes):
    r = sqrt(r1 * r1 + 2.0 * dr * D);
    d = (r - r1) / dr;

    nodes.append((x - sin(d) * r, y + cos(d) * r))

    D += node_length;


def draw():
  background(204);
  
  # Set the position of the head
  setTarget(mouse.x, mouse.y)
  
  # Draw the head
  fill(col_head)
  ellipse(nodes[0][0], nodes[0][1], node_size, node_size);
  
  # Draw the body
  fill(col_body);
  for x,y in nodes[1:]:
    ellipse(x,y, node_size, node_size)


def setTarget(tx, ty):
  # Motion interpolation for the head
  global x,y
  x += (tx - x) / delay;
  y += (ty - y) / delay;
  nodes[0] = (x,y)
 
  # Constrained motion for the other nodes
  for i in range(1,n_nodes):
    dx = nodes[i - 1][0] - nodes[i][0]
    dy = nodes[i - 1][1] - nodes[i][1]
    length = sqrt(sq(dx) + sq(dy))
    nodes[i] = (nodes[i - 1][0] - (dx/length * node_length),
                nodes[i - 1][1] - (dy/length * node_length))

run()

