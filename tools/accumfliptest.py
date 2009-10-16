"""
This is a simple application intended to test the accumulation buffer flip
policy of pyprocessing. If everything works as intended, you should see
a rotating square...
"""

def usage():
    print "Usage:", sys.argv[0], "--accum | --fbo | --single | --double"
    print "where --accum tests the accumulation flip policy (default),"
    print "      --fbo tests the frame buffer object flip policy,"
    print "      --single tests the single buffer flip policy"
    print "      --double tests the double buffer flip policy"

import pyglet,sys
from pyglet.gl import *
from flippolicy import *
fps_display = pyglet.clock.ClockDisplay(color=(1, 1, 1, 1),)

if len(sys.argv)==1 or sys.argv[1]=="--accum":
    win = AccumWindow(200,200)
elif sys.argv[1]=="--double":
    win = PyprocessingWindow(200,200)
elif sys.argv[1]=="--fbo":
    win = FBOWindow(200,200)
elif sys.argv[1]=="--single":
    win = SingleBufferWindow(200,200)
else:
    print "Unrecognized argument:",sys.argv[1]
    usage()
    sys.exit(-1)
    
ang = 0

@win.event
def on_draw():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor4f(0,0,0,0.05)
    glRectf(-1,-1,1,1)
    global ang
    ang += 1
    glRotatef(ang,0,0,1)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    pt = [(-0.5,-0.5,0),(0.5,-0.5,0),(0.5,0.5,0),(-0.5,0.5,0)]
    glColor4f(1,1,1,0.5)
    glBegin(GL_QUADS)
    for p in pt: glVertex3f(*p)
    glEnd()
    glColor4f(0,1,1,0.8)
    glPointSize(10)
    glBegin(GL_POINTS)
    for p in pt: glVertex3f(*p)
    glEnd()
    
def dummy(t): pass

pyglet.clock.schedule_interval(dummy,1.0/30)
pyglet.app.run()
