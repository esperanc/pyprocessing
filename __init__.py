#coding: utf-8
"""
A Processing-like environment for doing graphics with Python.

Other than Python, the only requirement is pyglet, which in turn
requires OpenGL.
"""

import pyglet,sys,math,ctypes,os
from math import *
from pyglet.gl import *
from pvector import PVector

#************************
#  CONSTANTS
#************************

#keycodes
F1 = 65470
F2 = 65471
F3 = 65472
F4 = 65473
F5 = 65474
F6 = 65475
F7 = 65476
F8 = 65477
F9 = 65478
F10 = 65479
F11 = 65480
F12 = 65481
F13 = 65482
F14 = 65483
F15 = 65484
F16 = 65485
LSHIFT = SHIFT = 65505
RSHIFT = 65506
LCTRL = CTRL = 65507
RCTRL = 65508
CAPSLOCK = 65509
LMETA = META = 65511
RMETA = 65512
LALT = ALT = 65513
RALT = 65514
LWINDOWS = WINDOWS = 65515
RWINDOWS = 65516
LCOMMAND = COMMAND = 65517
RCOMMAND = 65518
LOPTION = 65488
ROPTION = 65489
BACKSPACE = 65288
TAB = 65289
LINEFEED = 65290
CLEAR = 65291
RETURN = 65293
ENTER = 65293
PAUSE = 65299
SCROLLLOCK = 65300
SYSREQ = 65301
ESCAPE = 65307
HOME = 65360
LEFT = 65361
UP = 65362
RIGHT = 65363
DOWN = 65364
PAGEUP = 65365
PAGEDOWN = 65366
END = 65367
BEGIN = 65368
DELETE = 65535
SELECT = 65376
PRINT = 65377
EXECUTE = 65378
INSERT = 65379
UNDO = 65381
REDO = 65382
MENU = 65383
FIND = 65384
CANCEL = 65385
HELP = 65386
BREAK = 65387

CODED = '\0'

#rectmode/ellipsemode/mousebutton
CORNER = 1
CORNERS = 2
CENTER = 3
RADIUS = 4

#textalign
TOP = 7
BOTTOM = 8
BASELINE = 9

# this maps Processing constants to strings used by pyglet's text
# rendering subsystem
textAlignConst = {LEFT:'left', RIGHT:'right',
                  CENTER:'center', TOP:'top',
                  BOTTOM:'bottom', BASELINE:'baseline'}

# colorMode
RGB=0
HSB=1

# math
PI = math.pi
TWO_PI = PI*2
HALF_PI = PI/2

# hints
ENABLE_DEPTH_TEST=1
DISABLE_DEPTH_TEST=2

# shapes 
POINTS = GL_POINTS
LINES = GL_LINES
TRIANGLES = GL_TRIANGLES
TRIANGLE_FAN = GL_TRIANGLE_FAN
TRIANGLE_STRIP = GL_TRIANGLE_STRIP
QUADS = GL_QUADS 
QUAD_STRIP = GL_QUAD_STRIP
CLOSE = 1

#blend modes
BLEND, ADD, SUBTRACT, DARKEST, LIGHTEST, DIFFERENCE, EXCLUSION, \
MULTIPLY, SCREEN, OVERLAY, HARD_LIGHT, SOFT_LIGHT, DODGE, BURN = range(14)

#************************
#  GLOBALS
#************************
class mouse:
    """Stores mouse state"""
    pressed = False # Tells if any mouse button is pressed
    x = 0 # x coordinate of mouse
    y = 0 # y coordinate of mouse
    button = None # state of mouse buttons

class pmouse:
    """Store previous position of mouse"""
    pressed = False # Tells if any mouse button is pressed
    x = 0 # x coordinate of mouse
    y = 0 # y coordinate of mouse
    savex = 0 # saved x from the previous frame
    savey = 0 # saved y from the previous frame
    button = None # state of mouse buttons
    
class key:
    """Stores keyboard state"""
    char = ""
    code = 0
    modifiers = None
    pressed = False

class screen:
    """Stores screen attributes"""
    window = None 
    width = 300
    height = 300
    
class attrib:
    """Drawing attributes"""
    strokeColor = (0,0,0,1)
    fillColor = (1,1,1,1)
    strokeWeight = 1
    font = {}
    location = pyglet.resource.FileLocation(os.path.dirname(__file__))
    frameRate = 30
    loop=True
    rectMode = CORNER
    ellipseMode = CENTER
    textAlign = (LEFT,BASELINE)
    # color attribs
    colorMode = RGB
    colorRange = (255.0,255.0,255.0,255.0)
    # light attribs
    lights = False
    lightCount = 0
    lightSpecular = (0,0,0,1)
    lightFalloff = (1, 0, 0) # constant, linear, quadratic
    # depth testing
    depthTest = True

class shape:
    """Attributes for shapes."""
    quadric = gluNewQuadric()
    tess = gluNewTess()
    type = None
    sphereDetail = (20,10)
    bezierDetail = 20
    curveDetail = 20
    tension = 0.5
    bezierBlend = []
    vtx = []
    nrm = []

class config:
    """Configuration variables for the library."""
    # whether or not to invert the y axis. This requires fixing the drawing of 
    # some primitives such as arc or text
    coordInversionHack = True 
    # try to get around the artifacts when drawing filled polygons in smooth mode
    smoothFixHack = True 
    
class callback:
    """Call back functions."""
    
    @staticmethod
    def dummy(*args):
        """A callback function that does nothing."""
        pass
        
    """All of these are imported from the user space
    by the 'run' function or else fall back to dummy"""
    draw = mousePressed = mouseReleased = mouseClicked = mouseDragged = \
           mouseMoved = keyPressed = keyReleased = keyTyped = exit = \
           screenResized = dummy
        
#************************
#  COLORS
#************************

def hsb_to_rgb (h,s,v,a):
    """Simple hsv to rgb conversion. Assumes components specified in range 0.0-1.0."""
    tmp = color[0]*5.9999
    hi = int (tmp)
    f = tmp-hi
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)
    if hi==0:
        r,g,b = v,t,p
    elif hi==1:
        r,g,b = q,v,p
    elif hi==2:
        r,g,b = p,v,t
    elif hi==3:
        r,g,b = p,q,v
    elif hi==4:
        r,g,b = t,p,v
    else:
        r,g,b = v,p,q
    return r,g,b,a

def rgb_to_hsb(r,g,b,a): 
    """Simple hsv to rgb conversion. Assumes components specified in range 0.0-1.0."""
    maxval = max(r,g,b)
    minval = min(r,g,b)
    if maxval==minval:
        h = 0.0
    elif maxval==r:
        h = ((60 * (g-b)/(maxval-minval) + 360) % 360) / 360.0
    elif maxval==g:
        h = (60 * (b-r)/(maxval-minval) + 120) / 360.0
    else:
        h = (60 * (r-g)/(maxval-minval) + 240) / 360.0
    if maxval==0.0:
        s = 0.0
    else:
        s = (maxval-minval)/maxval
    v = maxval
    return (h,s,v,a)
    
def _getColor(*color):
    """Analyzes the color arguments and returns a proper 4-float tuple or None"""
        
    if len(color) == 1 and type(color[0])==tuple: 
        # a tuple, i.e., a value of type color, was passed rather than in-line values:
        # no transformation takes place
        assert (len(color[0]) == 4)
        return color[0]
    if len(color) == 1:
        # one value: None or a gray code
        if color[0] == None: return None
        color = (color[0],color[0],color[0],attrib.colorRange[3])
    elif len(color) == 2:
        # two values: Gray and Alpha
        color = (color[0],color[0],color[0],color[1])
    elif len(color) == 3:
        # three values: RGB
        color = (color[0],color[1],color[2],attrib.colorRange[3])
    else:
        assert(len(color)==4)
    color = tuple(float(x)/r for x,r in zip(color,attrib.colorRange))
    if attrib.colorMode==HSB: color = hsb_to_rgb(*color)
    return color

# the color data type is merely a 4-tuple as computed by _getColor
color = _getColor

def red(color):
    """Red component of the color."""
    return color[0]*attrib.colorRange[0]

def green(color):
    """Green component of the color."""
    return color[1]*attrib.colorRange[1]
    
def blue(color):
    """Blue component of the color."""
    return color[2]*attrib.colorRange[2]

def alpha(color):
    """Alpha component of the color."""
    return color[3]*attrib.colorRange[3]

def hue(color):
    """Hue component of the color."""
    color = rgb_to_hsb(*color)
    return color[0]*attrib.colorRange[0]

def saturation(color):
    """Saturation component of the color."""
    color = rgb_to_hsb(*color)
    return color[1]*attrib.colorRange[1]

def brightness(color):
    """Brightness component of the color."""
    color = rgb_to_hsb(*color)
    return color[2]*attrib.colorRange[2]

def lerpColor(c1,c2,amt):
    """Returns the linear interpolation between two colors c1 and c2.
    amt is a value between 0.0 and 1.0."""
    amtb = 1.0 - amt
    return tuple([amtb*x+amt*y for x,y in zip(c1,c2)])
    
def colorMode(mode,*args):
    """Sets the color system used for specifying colors and the 
    component ranges"""
    attrib.colorMode = mode
    if len(args)==1:
        attrib.colorRange = args*4
    elif len(args)==3:
        attrib.colorRange = (args[0],args[1],args[2],attrib.colorRange[3])
    else:
        assert(len(args)==4)
        attrib.colorRange = args

from colorblend import blendColor

#************************
#  ATTRIBUTES
#************************          
def stroke(*color):
    """Sets color as color for drawing lines and shape borders."""
    attrib.strokeColor = _getColor(*color)

def noStroke():
    """Omits line drawings"""
    attrib.strokeColor = None
      
def strokeWeight (weight):
    """Sets line width for drawing outline objects"""
    attrib.strokeWeight = weight
    
def fill(*color):
    """Sets color as color for drawing filled shapes."""
    attrib.fillColor = _getColor(*color)

def noFill():
    """Omits filled drawings"""
    attrib.fillColor = None
    
def smooth():
    """Sets state so that lines are rendered antialiased."""
    attrib.smooth = True
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

def noSmooth():
    """Sets state so that lines are rendered quickly."""
    attrib.smooth = False
    glDisable(GL_BLEND)
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_POINT_SMOOTH)
    glDisable(GL_POLYGON_SMOOTH)

def ellipseMode(mode):
    """Alters the meaning of the arguments of the ellipse function"""
    attrib.ellipseMode = mode
    
def rectMode(mode):
    """Alters the meaning of the arguments of the rectangle function"""
    attrib.rectMode = mode
    
def hint(hintconst):
    """Sets/unsets configuration settings. At present, only depth testing
    can be set or unset using constants DISABLE_DEPTH_TEST and ENABLE_DEPTH_TEST."""
    if hintconst==ENABLE_DEPTH_TEST:
        attrib.depthTest = True
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
    elif hintconst==DISABLE_DEPTH_TEST:
        attrib.depthTest = False
        glDisable(GL_DEPTH_TEST)

#************************
# Lights
#************************

def _lightsOn():
    """Turns on the lighting if not set earlier."""
    if attrib.lights: return
    glEnable(GL_LIGHTING)
    attrib.lights = True
    for i in range(attrib.lightCount): glDisable (GL_LIGHT0+i)
    attrib.lightCount = 0

def directionalLight(v1,v2,v3,nx,ny,nz):
    """Adds a directional light (diffuse/specular) with the given color and direction."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 4)(*attrib.lightSpecular))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(-nx,-ny,-nz,0))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(0,0,-1))
    glLightf(n, GL_SPOT_EXPONENT, 0)
    glLightf(n, GL_SPOT_CUTOFF, 180)
    constant, linear, quadratic = 1, 0, 0
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def pointLight(v1,v2,v3,x,y,z):
    """Adds a point light (diffuse/specular) with the given color and position."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 4)(*attrib.lightSpecular))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,1))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(0,0,-1))
    glLightf(n, GL_SPOT_EXPONENT, 0)
    glLightf(n, GL_SPOT_CUTOFF, 180)
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def ambientLight(v1,v2,v3,x=0,y=0,z=0):
    """Adds an ambient light."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,0))
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def spotLight(v1, v2, v3, x, y, z, nx, ny, nz, angle, concentration):
    """Adds a spot light source."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))  
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,1))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(nx,ny,nz))
    glLightf(n, GL_SPOT_EXPONENT, concentration)
    glLightf(n, GL_SPOT_CUTOFF, math.degrees(angle))
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)


def lightSpecular (v1,v2,v3):
    """Sets the specular coefficients for light sources defined afterwards."""
    attrib.lightSpecular = _getColor(v1,v2,v3)

def lightFalloff(constant, linear, quadratic):
    """Sets the attenuation coefficients for light sources defined afterwards."""
    attrib.lightFalloff = (constant, linear, quadratic)
    
def lights():
    """Turns on the illumination model."""
    _lightsOn()
    lightSpecular(0,0,0)
    directionalLight(128, 128, 128, 0, 0, -1)
    ambientLight(128, 128, 128)
    
def noLights():
    """Turns off the illumination model."""
    glDisable(GL_LIGHTING)
    for i in range(attrib.lightCount): glDisable (GL_LIGHT0+i)
    attrib.lights = False
    attrib.lightCount = 0
    attrib.lightFalloff = (1,0,0)
    attrib.lightSpecular = (0,0,0,1)

#************************
#  MATERIAL PROPERTIES
#************************

def emissive(*args):
    """Emission material Properties"""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_EMISSION, (ctypes.c_float * 4)(*color)) 
        
def shininess(shine):
    """Specular reflection material properties."""
    glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, shine)
    
def specular(*args):
    """Specular reflection material properties."""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_SPECULAR, (ctypes.c_float * 4)(*color))
    
def ambient(*args):
    """Ambient reflection material properties."""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_AMBIENT, (ctypes.c_float * 4)(*color))    

#************************
#  PRIMITIVE DRAWING
#************************

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
        gluDisk(shape.quadric,0,0.5,360,1)
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
        gluPartialDisk(shape.quadric,0,0.5,npts,1,start,sweep)
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
        glBegin(GL_POLYGON)
        glVertex2f(x,y)
        glVertex2f(x+width,y)
        glVertex2f(x+width,y+height)
        glVertex2f(x,y+height)
        glEnd()
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
        glBegin(GL_POLYGON)
        glVertex2f(x0,y0)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glVertex2f(x3,y3)
        glEnd()
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
        if config.smoothFixHack: 
            # Many implementations of Opengl render antialiased polygons
            # incorrectly, thus, we fix it by turning it off temporarily
            issmooth = attrib.smooth
            if issmooth: noSmooth()
            glBegin(GL_QUADS)
            for f,n in zip(faces,normals):
                glNormal3f(*n)
                for i in f:
                    glVertex3f(*v[i])
            glEnd()
            if issmooth: smooth()
        else:
            glBegin(GL_QUADS)
            for f,n in zip(faces,normals):
                glNormal3f(*n)
                for i in f:
                    glVertex3f(*v[i])
            glEnd()
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
        if config.smoothFixHack:
            # Many implementations of Opengl render antialiased polygons
            # incorrectly, thus, we fix it by turning it off temporarily
            issmooth = attrib.smooth
            if issmooth: noSmooth()
            gluSphere(shape.quadric, radius, shape.sphereDetail[0], shape.sphereDetail[1])
            if issmooth: smooth()
        else:
            gluSphere(shape.quadric, radius, shape.sphereDetail[0], shape.sphereDetail[1])
        glDisable(GL_POLYGON_OFFSET_FILL)
    if attrib.strokeColor!=None:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glLineWidth (attrib.strokeWeight)
        glColor4f(*attrib.strokeColor)
        gluSphere(shape.quadric, radius, shape.sphereDetail[0], shape.sphereDetail[1])
    glPopAttrib()
                        
#************************
#  SHAPE STUFF 
#************************

def beginShape(type=None):
    """Begins the drawing of a shape."""
    shape.type = type
    shape.vtx = []  # vertices drawn with vertex or sampled by curveVertex
    shape.bez = []  # bezier vertices drawn with bezierVertex
    shape.crv = []  # contents of the last three curveVertex calls
    shape.nrm = []  # pairs (vtxindex,normal) 

def vertex(x,y,z=0.0):
    """Adds a new vertex to the shape"""
    shape.vtx += [(x,y,z)]

def normal(x,y,z):
    """Sets the next vertex's normal"""
    shape.nrm += [(len(shape.vtx),(x,y,z))]
    
def bezierVertex(*coords):
    """Generates a cubic bezier arc. Arguments are of the form
    (cx1, cy1, cx2, cy2, x, y) or
    (cx1, cy1, cz1, cx2, cy2, cz2, x, y, z), i.e. coordinates
    for 3 control points in 2D or 3D. The first control point of the
    arc is the last point of the previous arc or the last vertex.
    """
    assert (len(coords) in (6,9))
    assert (len(shape.vtx)>0)
    # remember the index where the bezier control points will be stored
    shape.bez.append(len(shape.vtx)) 
    if len(coords) == 6:
        shape.vtx += [coords[:2]+(0,),coords[2:4]+(0,),coords[4:6]+(0,)]
    else:
        shape.vtx += [coords[:3],coords[3:6],coords[6:9]]

def endShape(close=False):
    """Does the actual drawing of the shape."""
    
    def computeNormal(p0,p1,p2):
        """Computes a normal for triangle p0-p1-p2."""
        return (PVector(p1)-PVector(p0)).cross(PVector(p2)-PVector(p1))
    
    # Draw the interior of the shape    
    if attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        # establish an initial normal vector
        if shape.nrm != []:
            inormal, normal = shape.nrm[0]
        else:
            inormal = len(shape.vtx)
            if len(shape.vtx)>=3:
                normal = computeNormal(shape.vtx[0],shape.vtx[1],shape.vtx[2])
            else:
                normal = [0,0,1]
        glNormal3f(*normal)
        # Draw filled shape
        if shape.type==None:
            issmooth = attrib.smooth
            # Many implementations of Opengl render antialiased polygons
            # incorrectly, thus, we fix it by turning it off temporarily
            if config.smoothFixHack: 
                if issmooth: glDisable(GL_POLYGON_SMOOTH)
            gluTessCallback(shape.tess, GLU_TESS_VERTEX, ctypes.cast(glVertex3dv,ctypes.CFUNCTYPE(None)))
            gluTessCallback(shape.tess, GLU_TESS_BEGIN, ctypes.cast(glBegin,ctypes.CFUNCTYPE(None)))
            gluTessCallback(shape.tess, GLU_TESS_END, ctypes.cast(glEnd,ctypes.CFUNCTYPE(None)))
            gluTessBeginPolygon(shape.tess, None)
            gluTessBeginContour(shape.tess)
            i = 0
            n = len(shape.vtx)
            shape.bez += [n]
            b = 0
            a = []
            while i<n:
                if i == shape.bez[b]:
                    for v in bezierSample (shape.vtx[i-1],shape.vtx[i],
                                          shape.vtx[i+1],shape.vtx[i+2]):
                        a += [(ctypes.c_double * 3)(*v)]
                        gluTessVertex(shape.tess, a[-1], a[-1])
                    b += 1
                    i += 3
                else:
                    v = shape.vtx[i]
                    a += [(ctypes.c_double * 3)(*v)]
                    i += 1
                    gluTessVertex(shape.tess, a[-1], a[-1])
            gluTessEndContour (shape.tess)
            gluTessEndPolygon (shape.tess)
            if config.smoothFixHack:
                if issmooth: glEnable(GL_POLYGON_SMOOTH)
        else:
            if shape.nrm != []:
                # User supplied normals
                inrm = 0
                inormal,normal = shape.nrm[0]
                glBegin(shape.type)
                glNormal3f(*normal)
                for i,v in enumerate(shape.vtx):
                    if i==inormal: 
                        # load the next normal before proceeding
                        glNormal3f(*normal)
                        inrm+=1
                        if inrm<len(shape.nrm):
                            inormal, normal = shape.nrm[inrm]
                    glVertex3f(*v)
                glEnd()
            else:
                # No normals were specified. Must compute normals on the fly
                glBegin(shape.type)
                for i,v in enumerate(shape.vtx):
                    if i+2 < len(shape.vtx):
                        if shape.type==QUADS and i%4==0 or \
                           shape.type==QUAD_STRIP and i%2==0 or \
                           shape.type==TRIANGLES and i%3==0 or \
                           shape.type==TRIANGLE_FAN and i>1 or \
                           shape.type==TRIANGLE_STRIP and i>1:
                            normal = computeNormal(shape.vtx[i],shape.vtx[i+1],shape.vtx[i+2])
                            glNormal3f (*normal)
                    glVertex3f(*v)
                glEnd()
    # Draw the outline of the shape
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        glPushAttrib(GL_POLYGON_BIT)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glLineWidth (attrib.strokeWeight)
        if shape.type==None:
            if close: glBegin(GL_LINE_LOOP)
            else: glBegin(GL_LINE_STRIP)
            i = 0
            n = len(shape.vtx)
            shape.bez += [n]
            nextbez = shape.bez.pop(0)
            while i<n:
                if i == nextbez:
                    for v in bezierSample (shape.vtx[i-1],shape.vtx[i],
                                          shape.vtx[i+1],shape.vtx[i+2]):
                        glVertex3f(*v)
                    nextbez = shape.bez.pop(0)
                    i += 3
                else:
                    v = shape.vtx[i]
                    i += 1
                    glVertex3f(*v)
            glEnd()
        else:
            glBegin(shape.type)
            for v in shape.vtx: glVertex3f(*v)        
            glEnd()
        glPopAttrib()

def bezierDetail(n=shape.bezierDetail):
    """Establishes the Bézier level of detail, i.e., the number of points
    per Bézier curve segment."""
    shape.bezierDetail = n
    # precompute blending factors
    shape.bezierBlend = []
    for i in range(n+1):
        t = float(i)/n
        u = 1 - t
        shape.bezierBlend.append((u*u*u,3*u*u*t,3*t*t*u,t*t*t))

def bezierPoint (a,b,c,d,t):
    """Given the x or y coordinate of Bézier control points a,b,c,d and
    the value of the t parameter, return the corresponding
    coordinate of the point."""
    u = 1.0 - t
    return a*u*u*u + b*3*u*u*t + c*3*t*t*u + d*t*t*t

def bezierTangent (a,b,c,d,t):
    """Given the x or y coordinate of Bézier control points a,b,c,d and
    the value of the t parameter, return the corresponding
    coordinate of the tangent at that point."""
    u = 1.0 - t
    return -a*3*u*u + b*(9*u*u-6*u) + c*(6*t-9*t*t) + d*3*t*t
    
def bezierSample(*p):
    """Returns a list of points for cubic bezier arc defined by the given
    control points. The number of points is given by shape.bezierDetail."""
    assert (len (p) == 4)
    result = []
    for b in shape.bezierBlend:
        x,y,z = 0,0,0
        for pi,bi in zip(p,b):
           x += pi[0]*bi
           y += pi[1]*bi
           z += pi[2]*bi
        result.append((x,y,z))
    return result

def bezier(*coords):
    """Draws a cubic Bézier curve for the 4 control points."""
    assert (len (coords) in (8,12))
    if len(coords) == 8:
        ctrlpoints = coords[:2]+(0,)+coords[2:4]+(0,)+coords[4:6]+(0,)+coords[6:]+(0,)
    beginShape()
    vertex (*ctrlpoints[0:3])
    bezierVertex(*ctrlpoints[3:])
    endShape()

class CatmullRomBlend:
    """Cubic Catmull Rom Blending"""
  
    def __init__ (self, tension = 0.5):
        self.tau = tension
        
    def blendFactors (self, u):
        """Given a value for u, returns the blending factors for each
        of the 4 control points."""
        u2 = u*u
        u3 = u2*u
        return [
             -self.tau * u + 2 * self.tau * u2 - self.tau * u3,
             1 + (self.tau-3) * u2 + (2 - self.tau) * u3,
             self.tau * u + (3 - 2*self.tau) * u2 + (self.tau - 2) * u3,
             -self.tau * u2 + self.tau * u3]

    def tangentBlendFactors (self, u):
        """Given a value for u, returns the tangent blending factors for each
        of the 4 control points."""
        u2 = u*u
        return [
             -self.tau + 4 * self.tau * u - 3 * self.tau * u2,
             (2*self.tau-6) * u + (6 - 3*self.tau) * u2,
             self.tau + (6 - 4*self.tau) * u + (3*self.tau - 6) * u2,
             -2*self.tau * u + 3*self.tau * u2]
    
  
    def blendPoint (self, u, p0, p1, p2, p3):
        """Returns the point obtained by blending pi with factor u."""
        result = [0,0,0]
        for b,p in zip (self.blendFactors(u),(p0,p1,p2,p3)):
            for i,x in enumerate(p):
                result[i] += p[i]*b
        return result
        
    def blendTangent(self, u, p0, p1, p2, p3):
        """Returns the curve tangent at the point obtained by blending pi with factor u."""
        result = [0,0,0]
        for b,p in zip (self.tangentBlendFactors(u),(p0,p1,p2,p3)):
            for i,x in enumerate(p):
                result[i] += p[i]*b
        return result
    
def curveTightness (squishy):
    """Uses 'squishy' as the tension factor for the catmull-rom spline."""
    shape.tension = (1-squishy)/2.0
    
def curveVertex(x,y,z=0):
    """Generates a cubic Catmull-Rom curve corresponding to interpolating
    the three last points issued with earlier calls to curveVertex and this one.
    """
    shape.crv.append((x,y,z))
    if len(shape.crv)>4: shape.crv = shape.crv[-4:]
    if len(shape.crv)==4:
        blend = CatmullRomBlend(shape.tension)
        npts = shape.curveDetail
        for i in range(npts+1):
            p = blend.blendPoint(float(i)/npts, *shape.crv)
            vertex(*p)
            
def curve (*coords):
    """Generates a catmull-rom curve given 4 points. Takes either 8 numbers 
    for coordinates of 4 points in 2D or 12 numbers for 4 points in 3D"""
    if len(coords)==8:
        p0,p1,p2,p3 = coords[0:2],coords[2:4],coords[4:6],coords[6:8]
    else:
        assert (len(coords)==12)
        p0,p1,p2,p3 = coords[0:3],coords[3:6],coords[6:9],coords[9:12]
    blend = CatmullRomBlend(shape.tension)
    beginShape()
    npts = shape.curveDetail
    for i in range(npts+1):
        p = blend.blendPoint(float(i)/npts, p0,p1,p2,p3)
        vertex(*p)
    endShape()

def curvePoint (a,b,c,d,t):
    """Evaluates the n'th coordinate of a cubic Catmull-Rom curve at parameter
    t for control points having their n'th coordinate equal to a, b, c and d, respectively.
    """
    blend = CatmullRomBlend(shape.tension)
    return blend.blendPoint(t,(a,),(b,),(c,),(d,)) [0]

def curveTangent (a,b,c,d,t):
    """Evaluates the n'th coordinate of the tangent at the point on a cubic Catmull-Rom 
    curve at parameter t for control points having their n'th coordinate equal to 
    a, b, c and d, respectively.
    """
    blend = CatmullRomBlend(shape.tension)
    return blend.blendTangent(t,(a,),(b,),(c,),(d,)) [0]
    
def curveDetail(npts=shape.curveDetail):
    """Controls the number of samples per curve arc."""
    shape.curveDetail = npts

#************************
#  FONT STUFF 
#************************

def textAlign (align,yalign=BASELINE):
    """Set the text alignment attributes."""
    attrib.textAlign = (align, yalign)
    
def createFont(family = None, size = 16, bold=False, italic=False):
    """Creates a font for subsequent use"""
    return {"font_name":family, "font_size":size, "bold":bold, "italic":italic }
    
def textFont (font):
    """Set font as current font. Should be object created with createFont"""
    attrib.font = font
    
def htmlText(string, x, y, z = 0):
    """Draws the html text at x,y,z"""
    if attrib.fillColor != None:
        r,g,b,a=[int (c*255) for c in attrib.fillColor]        
        label = pyglet.text.HTMLLabel(string, location=attrib.location,
                                      x=x, y=y, width=screen.width,
                                      anchor_x=textAlignConst[attrib.textAlign[0]],
                                      anchor_y=textAlignConst[attrib.textAlign[1]],
                                      multiline=True)
        label.color=(r,g,b,a)
        if config.coordInversionHack:
            glPushMatrix()
            glTranslatef(0,y*2,0)
            glScalef(1,-1,1)
            label.draw()
            glPopMatrix()
        else:
            label.draw()

def text(string, x, y, z = 0):
    """Draws the html text at x,y,z"""
    if attrib.fillColor != None:
        r,g,b,a=[int (c*255) for c in attrib.fillColor]
        label = pyglet.text.Label(string,
                          x=x, y=y, color=(r,g,b,a),
                          anchor_x=textAlignConst[attrib.textAlign[0]],
                          anchor_y=textAlignConst[attrib.textAlign[1]],
                          **attrib.font)
        if config.coordInversionHack:
            glPushMatrix()
            glTranslatef(0,y*2,0)
            glScalef(1,-1,1)
            label.draw()
            glPopMatrix()
        else:
            label.draw()

#************************
#  TRANSFORMATIONS STUFF 
#************************
    
def pushMatrix(): 
    """Saves current transformation"""
    glPushMatrix()
    
def popMatrix():
    """Restores previous transformation"""
    glPopMatrix()
    
def resetMatrix():
    """Loads an identity matrix"""
    glLoadIdentity()
    
def applyMatrix(n00, n01, n02, n03,
                n04, n05, n06, n07,
                n08, n09, n10, n11,
                n12, n13, n14, n15):
    """Loads an identity matrix"""
    # notice that processing uses a transpose matrix
    glMultMatrixf((ctypes.c_float * 16)(n00, n04, n08, n12,
                n01, n05, n09, n13,
                n02, n06, n10, n14,
                n03, n07, n11, n15))

def getMatrix():
    """Returns the MODELVIEW matrix as a tuple."""
    matrix = (ctypes.c_double*16)()
    glGetDoublev (GL_MODELVIEW_MATRIX, matrix)
    return tuple([matrix [i] for i in range(16)])

def getProjection():
    """Returns the PROJECTION matrix as a tuple."""
    matrix = (ctypes.c_double*16)()
    glGetDoublev (GL_PROJECTION_MATRIX, matrix)
    return tuple([matrix [i] for i in range(16)])
    
def printMatrix():
    """Prints the MODELVIEW matrix."""
    print getMatrix()

def printProjection():
    """Prints the PROJECTION matrix."""
    print getProjection()

def translate(x,y,z=0):
    """Translation transformation"""
    glTranslatef(x,y,z)

def rotate(*args):
    """Rotation transformation. Angles in radians"""
    if len(args) == 1: glRotatef(math.degrees(args[0]), 0,0,1)
    else: glRotatef(math.degrees(args[0]),args[1],args[2],args[3])

rotateZ = rotate

def rotateX(angle):
    """Rotation around the X axis"""
    rotate (angle, 1, 0, 0)

def rotateY(angle):
    """Rotation around the Y axis"""
    rotate (angle, 0, 1, 0)
    
def scale(*args):
    """Scale transformation"""
    if len(args) == 1: glScalef(args[0],args[0],args[0])
    elif len(args)==2: glScalef(args[0],args[1],1)
    else: glScalef(*args)

def camera (*args):
    """Args should either be empty or be of the form 
    (eyex,eyey,eyez,centerx, centery, centerz, upx, upy, upz).
    Creates a viewing transformation given the camera position
    (eyex,eyey,eyez), the center of the scene (centerx, centery, centerz) and
    a vector to be used as the up direction (upx, upy, upz). If no args
    are passed, the standard camera is created."""
    glLoadIdentity()
    if len(args)==0:
        # default camera
        gluLookAt (screen.width/2.0, screen.height/2.0, (screen.height/2.0) / tan(PI*60.0 / 360.0), 
                   screen.width/2.0, screen.height/2.0, 0, 0, 1, 0)
    else:
        assert (len(args)==9)
        gluLookAt (*args)

def perspective(*args):
    """Args should either be empty or be of the form 
    (fov,aspect,znear,zfar). Loads a perspective projection matrix, where
    fov is the field-of-view angle (in radians) for vertical direction, aspect
    is the ratio of width to height, znear is the z-position of nearest clipping 
    plane and zfar is the z-position of nearest farthest plane. If no args are
    passed, the standard projection is created, i.e, equivalent to 
    perspective(PI/3.0, width/height, cameraZ/10.0, cameraZ*10.0)
    where cameraZ is ((height/2.0) / tan(PI*60.0/360.0))."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if len(args)==0:
        cameraZ = screen.height/2.0 / math.tan(math.pi*60/360)
        gluPerspective(60, screen.width*1.0/screen.height, cameraZ/100.0, cameraZ*10.0)
    else:
        assert(len(args)==4)
        fov,aspect,znear,zfar = args
        gluPerspective(degrees(fov),aspect,znear,zfar)
    # invert the y axis
    if config.coordInversionHack: glScalef(1,-1,1)
    glMatrixMode(GL_MODELVIEW)

def ortho(*args):
    """Args should either be empty or be of the form 
    (left, right, bottom, top, near, far). Loads an orthogonal projection matrix.
    The clipping volume in this case is an axes-aligned parallelepiped, where 
    left and right are the minimum and maximum x values, top and bottom are 
    the minimum and maximum y values, and near and far are the minimum and 
    maximum z values. If no parameters are given, the default is used: 
    ortho(0, screen.width, 0, screen.height, -10, 10)."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if len(args)==0:
        left, right = 0, screen.width
        bottom, top =  0, screen.height
        near, far = -screen.height*2, screen.height*2 # a saner default than processing's
    else:
        assert(len(args)==6)
        left, right, bottom, top, near, far = args
    # invert the y axis
    if config.coordInversionHack: bottom, top = top, bottom
    glOrtho(left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW)    
    
#************************
#  CALLBACK FUNCTIONS
#************************

def __draw(*args):
    """Called for every frame."""
    # reset the modelview transformation
    glMatrixMode (GL_MODELVIEW)
    camera()
    # reset the lighting
    noLights()
    # set last frame's mouse position in pmouse
    pmouse.x,pmouse.y = pmouse.savex, pmouse.savey
    callback.draw()
    # save last mouse position
    pmouse.savex,pmouse.savey=mouse.x,mouse.y
    
def on_close():
    """Called when window is closed."""
    pyglet.clock.unschedule(__draw)
    callback.exit()
    
def on_mouse_press(x, y, button, modifiers):
    """Called when a mouse button is pressed."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, screen.height - y
    if button == 4: button = RIGHT
    elif button == 2: button = CENTER
    elif button == 1: button = LEFT
    else: button = None
    mouse.button = button
    mouse.pressed = True
    callback.mousePressed()

def on_mouse_release(x, y, button, modifiers):
    """Called when a mouse button is released."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, screen.height - y
    mouse.pressed = False
    callback.mouseClicked()
    callback.mouseReleased()

def on_key_press(symbol, modifiers):
    """Called when a key is pressed."""
    key.pressed = True
    key.code = symbol
    key.modifiers = modifiers
    if 32 <= symbol <= 127: 
        key.char = chr(symbol)
    else:
        key.char = CODED
    callback.keyPressed()

def on_key_release(symbol, modifiers):
    """Called when a key is released."""
    key.pressed = False
    key.code = symbol
    key.modifiers = modifiers
    if 32 <= symbol <= 127: 
        key.char = chr(symbol)
    else:
        key.char = CODED
    callback.keyReleased()
    if key.char != CODED : callback.keyTyped()

def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """Called when mouse is moved with at least one button pressed."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, screen.height - y
    mouse.pressed = True
    callback.mouseDragged()

def on_mouse_motion(x, y, dx, dy):
    """Called when mouse is moved with no buttons pressed."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, screen.height - y
    mouse.button = None
    mouse.pressed = False
    callback.mouseMoved()
    
def on_resize(width, height):
    """Called whenever the window is resized."""
    screen.width = width
    screen.height = height
    # Set up a reasonable perspective view
    glViewport(0, 0, width, height)
    perspective()
    if callback.screenResized != callback.dummy:
        # User will handle the resize
        callback.screenResized()
    return pyglet.event.EVENT_HANDLED

#************************
#  ENVIRONMENT
#************************

def loop():
    """Enables the periodical refresh of the screen."""
    attrib.loop = True
    pyglet.clock.unschedule(__draw)
    pyglet.clock.schedule(__draw,1.0/attrib.frameRate)
    
def noLoop():
    """Disables the periodical refresh of the screen."""
    attrib.loop = False
    pyglet.clock.unschedule(__draw)
    
def frameRate(rate):
    """Sets the frame rate."""        
    attrib.frameRate = rate
    if attrib.loop: loop()    

def size(nx=screen.width,ny=screen.height,fullscreen=False,resizable=False,caption="PyProcessing"):
    """Inits graphics screen with nx x ny pixels.
    Caption is the window title."""
    # Set up screen
    global screen
    if screen.window != None:
        # get rid of window created on an earlier call to size
        screen.window.close()
        screen.window = None
    
    # create a window. Obs.: it is created initially with visible=False so
    # that the default window may be silently destroyed and recreated.
    # After the run() function is called, the window is made visible
    if fullscreen: nx,ny = None,None
    try:
        # Try and create a window with double buffer
        screen.config = Config(depth_size=24, double_buffer=True,)
        screen.window = pyglet.window.Window(nx, ny, resizable=resizable, fullscreen=fullscreen,
                        config=screen.config, caption=caption, visible = False)
    except pyglet.window.NoSuchConfigException:
        print ("No such conf")
        # Fall back default config
        screen.window = pyglet.window.Window(nx, ny, resizable=resizable, caption=caption, 
                        fullscreen=fullscreen, visible = False)
    screen.width = screen.window.width
    screen.height = screen.window.height
    noSmooth()
    # frame per seconds init
    frameRate(60)
    # bezier init
    bezierDetail(30)
    # enable depth testing
    hint(ENABLE_DEPTH_TEST)
    # set up default material and lighting parameters
    glEnable(GL_COLOR_MATERIAL)
    glEnable (GL_NORMALIZE)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (c_float * 4) (0,0,0,1))
    specular(0)
    ambient(0.2*255)
    shininess(1)
    # set up colors
    fill(255)
    stroke(0)
    # clear screen with medium gray
    background(200)
    # force a resize call
    on_resize(screen.width,screen.height)
    # setup the default camera
    camera()


def run():
    """Registers callbacks and starts event loop."""
    import __main__
    
    maindir = dir(__main__)

    # Import callbacks from main program    
    if 'draw' in maindir: callback.draw = staticmethod(__main__.draw)
    if 'mousePressed' in maindir: callback.mousePressed = staticmethod(__main__.mousePressed)
    if 'mouseReleased' in maindir: callback.mouseReleased = staticmethod(__main__.mouseReleased)
    if 'mouseClicked' in maindir: callback.mouseClicked = staticmethod(__main__.mouseClicked)
    if 'mouseDragged' in maindir: callback.mouseDragged = staticmethod(__main__.mouseDragged)
    if 'mouseMoved' in maindir: callback.mouseMoved = staticmethod(__main__.mouseMoved)
    if 'keyPressed' in maindir: callback.keyPressed = staticmethod(__main__.keyPressed)
    if 'keyReleased' in maindir: callback.keyReleased = staticmethod(__main__.keyReleased)
    if 'keyTyped' in maindir: callback.keyTyped = staticmethod(__main__.keyTyped)
    if 'exit' in maindir: callback.exit = staticmethod(__main__.exit)
    if 'screenResized' in maindir: callback.screenResized = staticmethod(__main__.screenResized)
    
    # set frame rate
    frameRate (attrib.frameRate)
    
    # enable depth buffering by default
    hint(ENABLE_DEPTH_TEST)
    
    # Automatically call setup if function was defined in the main program
    if 'setup' in maindir: 
        __main__.setup()
        # Call draw at least once even if setup called noloop
        if 'draw' in maindir: __main__.draw()
        
    # set up other callbacks
    screen.window.event(on_close)
    screen.window.event(on_mouse_press)
    screen.window.event(on_mouse_release)
    screen.window.event(on_mouse_drag)
    screen.window.event(on_mouse_motion)
    screen.window.event(on_resize)
    screen.window.event(on_key_press)
    screen.window.event(on_key_release)
    
    # make window visible
    screen.window.set_visible(True)
    
    # now for the main loop
    pyglet.app.run()

# create a default window
size(100,100)

#test program
if __name__=="__main__":
    def draw():
        background(200)
        smooth()
        textFont (createFont ("Times", size=24))
        fill (0)
        text("Hello World", 10, 42)
        if mouse.button == LEFT:
            fill(255,0,0,100)
            noStroke()
            ellipse(mouse.x,mouse.y,60,60)
        elif mouse.button == RIGHT:
            fill(255)
            text ("Python Processing", mouse.x, mouse.y)
    size(300,300)
    ellipseMode(CENTER)
    run()

