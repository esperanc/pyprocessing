#************************
#  PRIMITIVE DRAWING
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from colors import _getColor

__all__=['_smoothFixHackBegin', '_smoothFixHackEnd',
         'background', 'ellipse', 'arc', 'rect', 'quad',
         'triangle', 'point', 'line', 'box', 'sphere']
         
def _smoothFixHackBegin():
    """Try to cope with OpenGL's faulty antialiasing of polygons by turning
    off smooth rendering temporarily."""
    if config.smoothFixHack:
        config.smoothTurnedOn = attrib.smooth
        if config.smoothTurnedOn: noSmooth()

def _smoothFixHackEnd():
    """Restore the smooth setting if it was temporarily turned off."""
    if config.smoothFixHack and config.smoothTurnedOn: smooth()
    
def background(*color):
    """Clears the screen with color. 
    Color may be an (r,g,b) tuple or a single gray value. If depth testing is
    turned on, also clears the depth buffer."""
    color = _getColor(*color)
    glClearColor (*color)
    if attrib.depthTest:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    else:
        glClear(GL_COLOR_BUFFER_BIT)

def ellipse(x,y,width,height):
    """Draws an ellipse with lower left corner at (x,y) and size (width,height)"""
    if attrib.ellipseMode==CENTER:
        x -= width/2
        y -= height/2
    elif attrib.ellipseMode==RADIUS:
        x -= width
        y -= height
        width *= 2
        height *= 2
    elif attrib.ellipseMode==CORNERS:
        width = width-x
        height = height-y
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glTranslatef(x,y,0)
    glScalef(width,height,1)
    glTranslatef(0.5,0.5,0)
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        gluDisk(shape.quadric,0,0.5,360,1)
        _smoothFixHackEnd()
    glPushAttrib(GL_POLYGON_BIT)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLineWidth (attrib.strokeWeight)
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        gluDisk(shape.quadric,0.5,0.5,360,1)
    glPopAttrib()    
    glPopMatrix()

def arc(x,y,width,height, start, stop):
    """Draws an ellipse arc with lower left corner at (x,y) and size (width,height)"""
    if attrib.ellipseMode==CENTER:
        x -= width/2
        y -= height/2
    elif attrib.ellipseMode==RADIUS:
        x -= width
        y -= height
        width *= 2
        height *= 2
    elif attrib.ellipseMode==CORNERS:
        width = width-x
        height = height-y
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    if config.coordInversionHack:
        glTranslatef(0,y*2+height,0)
        glScalef(1,-1,1)
    glTranslatef(x,y,0)
    glScalef(width,height,1)
    glTranslatef(0.5,0.5,0)
    if stop<start: start,stop=stop,start
    sweep = math.degrees(stop-start)
    start = math.degrees(start)+90
    npts = min(5,sweep)
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        gluPartialDisk(shape.quadric,0,0.5,npts,1,start,sweep)
        _smoothFixHackEnd()
    glPushAttrib(GL_POLYGON_BIT)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLineWidth (attrib.strokeWeight)
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        gluPartialDisk(shape.quadric,0.5,0.5,npts,1,start,sweep)
    glPopAttrib()    
    glPopMatrix()
        
def rect(x,y,width,height):
    """Draws a rectangle with lower left corner at (x,y) and size (width,height)"""
    if attrib.rectMode==CENTER:
        x -= width/2
        y -= height/2
    elif attrib.rectMode==RADIUS:
        x -= width
        y -= height
        width *= 2
        height *= 2
    elif attrib.rectMode==CORNERS:
        width = width-x
        height = height-y
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        glBegin(GL_POLYGON)
        glVertex2f(x,y)
        glVertex2f(x+width,y)
        glVertex2f(x+width,y+height)
        glVertex2f(x,y+height)
        glEnd()
        _smoothFixHackEnd()
    if attrib.strokeColor != None:
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x,y)
        glVertex2f(x+width,y)
        glVertex2f(x+width,y+height)
        glVertex2f(x,y+height)
        glEnd()

def quad(x0,y0,x1,y1,x2,y2,x3,y3):
    """Draws a 2D quadrilateral with the given coordinates"""
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        glBegin(GL_POLYGON)
        glVertex2f(x0,y0)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glVertex2f(x3,y3)
        glEnd()
        _smoothFixHackBegin()
    if attrib.strokeColor != None:
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0,y0)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glVertex2f(x3,y3)
        glEnd()
        
def triangle(x0,y0,x1,y1,x2,y2):
    """Draws a 2D triangle with the given coordinates"""
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        glBegin(GL_POLYGON)
        glVertex2f(x0,y0)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glEnd()
    if attrib.strokeColor != None:
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0,y0)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glEnd()

def point(x,y,z=0.0):
    """Draws a point at the given coordinates."""
    if attrib.strokeColor != None:
        glBegin(GL_POINTS)
        glColor4f(*attrib.strokeColor)
        glVertex3f(x,y,z)
        glEnd()
        
def line(*coords):
    """Draws a line segment in 2D or 3D. Arguments should be one of:
    (x1,y1,z1),(x2,y2,z2)
    (x1,y1),(x2,y2)
    x1,y1,z1,x2,y2,z2
    x1,y1,x2,y2
    """
    n = len(coords)
    if n==2:
        p1,p2 = coords
    else:
        p1,p2 = coords[:n/2],coords[n/2:]
    assert (len(p1)==len(p2))
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        glLineWidth(attrib.strokeWeight)
        glBegin(GL_LINES)
        if len(p1)==2:
            glVertex2f(*p1)
            glVertex2f(*p2)
        else:
            glVertex3f(*p1)
            glVertex3f(*p2)
        glEnd()

def box(*args):
    """Draws a box centered on the origin. Arguments:
    (size) or 
    (sizex, sizey, sizez)"""
    n = len(args)
    assert(n==1 or n==3)
    if n==1:
        dx=dy=dz=args[0]/2.0
    else:
        dx,dy,dz=args[0]/2.0,args[1]/2.0,args[2]/2.0
    v = []
    for x in [-dx,dx]: 
        for y in [-dy,dy]:
            for z in [-dz,dz]:
                v+=[(x,y,z)]
    faces = [(0,1,3,2),(5,4,6,7),(5,1,0,4),(2,3,7,6),(2,6,4,0),(1,5,7,3)]
    normals = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
    glPushAttrib(GL_POLYGON_BIT)
    if attrib.fillColor!=None:
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1,1)
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        glBegin(GL_QUADS)
        for f,n in zip(faces,normals):
            glNormal3f(*n)
            for i in f:
                glVertex3f(*v[i])
        glEnd()
        _smoothFixHackEnd()
        glDisable(GL_POLYGON_OFFSET_FILL)
    if attrib.strokeColor!=None:
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        glBegin(GL_LINES)
        for i in (0,1,2,3,4,5,6,7, 2,6,3,7,1,5,0,4, 1,3,0,2,4,6,5,7):
            glVertex3f(*v[i])
        glEnd()
    glPopAttrib()

def sphere(radius):
    """Draws a sphere centered at the origin with the given radius."""
    glPushAttrib(GL_POLYGON_BIT)
    if attrib.fillColor!=None:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1,1)
        glColor4f(*attrib.fillColor)
        _smoothFixHackBegin()
        gluSphere(shape.quadric, radius, shape.sphereDetail[0], shape.sphereDetail[1])
        _smoothFixHackEnd()
        glDisable(GL_POLYGON_OFFSET_FILL)
    if attrib.strokeColor!=None:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        gluSphere(shape.quadric, radius, shape.sphereDetail[0], shape.sphereDetail[1])
    glPopAttrib()
