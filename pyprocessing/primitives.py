#************************
#  PRIMITIVE DRAWING
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from attribs import *
from colors import _getColor
import config
from pimage import *

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
    if len(color) == 1 and isinstance(color[0],PImage):
        image(color[0],0,0)
    else:
        color = _getColor(*color)
        glClearColor (*color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
def ellipse(x,y,width,height):
    """Draws an ellipse with center at (x,y) and size (width,height)"""
    if shape.quadric == None:
        shape.quadric = gl.gluNewQuadric()
    if shape.ellipseFillDL==None:
        # Create display lists for ellipse in case none was created before
        shape.ellipseFillDL = glGenLists (1)
        glNewList(shape.ellipseFillDL, GL_COMPILE)
        gluDisk(shape.quadric,0,0.5,shape.ellipseDetail,1)
        glEndList();
        shape.ellipseStrokeDL = glGenLists (1)
        glNewList(shape.ellipseStrokeDL, GL_COMPILE)
        gluDisk(shape.quadric,0.5,0.5,shape.ellipseDetail,1)
        glEndList();        
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
        glCallList(shape.ellipseFillDL)
        _smoothFixHackEnd()
    glPushAttrib(GL_POLYGON_BIT)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLineWidth (attrib.strokeWeight)
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        glCallList(shape.ellipseStrokeDL)
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
    npts = max(5,int(abs(sweep)))
    if shape.quadric == None:
        shape.quadric = gl.gluNewQuadric()
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
        if attrib.strokeJoin == MITER:
            glBegin(GL_LINES)
            glVertex2f(x-attrib.strokeWeight,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width+attrib.strokeWeight,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y+height)
            glVertex2f(x+width+attrib.strokeWeight,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x-attrib.strokeWeight,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x-attrib.strokeWeight/2.0,y+height)
            glVertex2f(x-attrib.strokeWeight/2.0,y)
        elif attrib.strokeJoin == BEVEL:
            w,f,s = attrib.strokeWeight,attrib.fillColor,attrib.strokeColor
            noStroke()
            fill(s)
            triangle(x,y,x,y-w,x-w,y)
            triangle(x+width,y,x+width+w,y,x+width,y-w)
            triangle(x+width,y+height,x+width+w,y+height,x+width,y+height+w)
            triangle(x,y+height,x-w,y+height,x,y+height+w)
            attrib.strokeColor = s
            attrib.fillColor = f
            attrib.strokeWeight = w
            glBegin(GL_LINES)
            glVertex2f(x,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y+height)
            glVertex2f(x+width,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x-attrib.strokeWeight/2.0,y+height)
            glVertex2f(x-attrib.strokeWeight/2.0,y) 
        else:
            w,f,s = attrib.strokeWeight,attrib.fillColor,attrib.strokeColor
            e = attrib.ellipseMode
            noStroke()
            fill(s)
            attrib.ellipseMode = CENTER
            arc(x,y+height,w*2,w*2,PI/2,PI)
            arc(x+width,y+height,w*2,w*2,0,PI/2)
            arc(x,y,w*2,w*2,PI,3*PI/2)
            arc(x+width,y,w*2,w*2,3*PI/2,2*PI)
            attrib.ellipseMode = e
            attrib.strokeColor = s
            attrib.fillColor = f
            attrib.strokeWeight = w
            glBegin(GL_LINES)
            glVertex2f(x,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width,y-attrib.strokeWeight/2.0)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y)
            glVertex2f(x+width+attrib.strokeWeight/2.0,y+height)
            glVertex2f(x+width,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x,y+height+attrib.strokeWeight/2.0)
            glVertex2f(x-attrib.strokeWeight/2.0,y+height)
            glVertex2f(x-attrib.strokeWeight/2.0,y) 
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
        glPointSize (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        glBegin(GL_POINTS)
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
        if len(p1)==2:
            if attrib.strokeCap == ROUND:
                if p2[0] == p1[0]: angle = 0
                else:
                    m = float(p2[1]-p1[1])/(p2[0]-p1[0])
                    angle = math.atan(m)-PI/2
                if p2[0]<p1[0]: angle = angle+PI
                w,f,s = attrib.strokeWeight,attrib.fillColor,attrib.strokeColor
                e = attrib.ellipseMode
                noStroke()
                fill(s)
                attrib.ellipseMode = CENTER
                arc(p1[0],p1[1],w,w,angle,angle-PI)
                arc(p2[0],p2[1],w,w,angle,angle+PI)
                attrib.ellipseMode = e
                attrib.fillColor = f
                attrib.strokeWeight = w
                attrib.strokeColor = s
                glBegin(GL_LINES)
                glVertex2f(*p1)
                glVertex2f(*p2)
            elif attrib.strokeCap == PROJECT:
                if p2[0] == p1[0]:
                    x = 0
                    y = attrib.strokeWeight/2.0
                else:
                    m = float(p2[1]-p1[1])/(p2[0]-p1[0])
                    x = attrib.strokeWeight/(2*math.sqrt(1+m**2))
                    if p2[0]<p1[0]: x = -x
                    y = x*m
                glBegin(GL_LINES)
                glVertex2f(p1[0]-x,p1[1]-y)
                glVertex2f(p2[0]+x,p2[1]+y)
            else:
                glBegin(GL_LINES)
                glVertex2f(*p1)
                glVertex2f(*p2)
        else:
            glBegin(GL_LINES)
            glVertex3f(*p1)
            glVertex3f(*p2)
        glEnd()

def box(*args):
    """Draws a box centered on the origin. Arguments:
    (size) or 
    (sizex, sizey, sizez)"""
    
    def cubeFillList ():
        "Creates a vertex list for drawing a unit cube in filled mode."
        v = []
        for x in -1.0,1.0: 
            for y in -1.0,1.0:
                for z in -1.0,1.0:
                    v+=[(x,y,z)]
        p,n = [],[] 
        for f in (0,1,3,2),(5,4,6,7),(5,1,0,4),(2,3,7,6),(2,6,4,0),(1,5,7,3):
            for fv in f: p+=v[fv]
        for fn in (-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1):
            n += fn*4
        return pyglet.graphics.vertex_list(24,('v3f', p),('n3f', n))

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

        if shape.cubeFillVL == None: shape.cubeFillVL = cubeFillList()
        # Assumes current matrix mode is ModelView
        glPushMatrix()
        glScalef(dx,dy,dz)
        shape.cubeFillVL.draw(pyglet.gl.GL_QUADS)
        glPopMatrix()
        
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
    if shape.quadric == None:
        shape.quadric = gl.gluNewQuadric()
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
