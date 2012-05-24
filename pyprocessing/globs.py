from constants import *
import pyglet,os

__all__ = ['mouse', 'pmouse', 'attrib', 'frame', 'key', 'canvas', 'shape', 
           'screen', 'callback']

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

class canvas:
    """Stores the drawing window attributes"""
    window = None 
    # These two symbols were relocated to the __builtin__ namespace
    #width = 100
    #height = 100
    
class screen:
    """Current window properties."""
    co = 2
    pixels = []
    width = None
    height = None
    
class attrib:
    """Drawing attributes"""
    strokeJoin = MITER
    strokeCap = SQUARE
    textureMode = IMAGE
    strokeColor = (0,0,0,1)
    fillColor = (1,1,1,1)
    tintColor = None
    strokeWeight = 1
    font = {}
    location = pyglet.resource.FileLocation(os.path.dirname(__file__))
    rectMode = CORNER
    ellipseMode = CENTER
    imageMode = CORNER
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
    texture = False

class frame:
    """Frame rate and the like."""
    loop=True
    rate=10 # estimated frame rate
    targetRate = 60 # the target frame rate
    count=0 # number of frames displayed since the application started
    
class shape:
    """Attributes for shapes."""
    quadric = None # Stores a gluQuadricObject
    tess = None # Stores a gluTesselatorObject
    ellipseFillDL = None # Stores a display list for a filled ellipse
    ellipseStrokeDL = None # Stores a display list for an outline ellipse
    cubeFillVL = None # Stores a vertex list for drawing a cube with quads
    cubeStrokeVL = None # Stores a vertex list for drawing a cube with line segments
    type = None # stores the type of the shape as passed to function beginShape
    sphereDetail = (20,10)
    bezierDetail = 40
    curveDetail = 20
    ellipseDetail = 100
    tension = 0.5
    bezierBlend = []
    vtx = []
    nrm = []
    

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

