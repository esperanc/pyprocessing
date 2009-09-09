from constants import *
import pyglet,os

__all__ = ['mouse', 'pmouse', 'attrib', 'frame', 'key', 'screen', 'shape', 
           'config', 'callback']

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

class frame:
    """Frame rate and the like."""
    loop=True
    rate=10 # estimated frame rate
    targetRate = 60 # the target frame rate
    count=0 # number of frames displayed since the application started
    
class shape:
    """Attributes for shapes."""
    quadric = gl.gluNewQuadric()
    tess = gl.gluNewTess()
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
    smoothTurnedOn = False # tells whether smooth was on before the hack
    
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
