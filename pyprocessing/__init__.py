#coding: utf-8
"""
A Processing-like environment for doing graphics with Python.

Other than Python, the only requirement is pyglet, which in turn
requires OpenGL.
"""

try:
    import pyglet
except:
    print """The Pyglet package is not present in your Python
    installation. Please visit http://www.pyglet.org."""
    exit(-1)
    
import sys,math,ctypes,os
from math import *
from pyglet.gl import *

# Sub-modules

from pvector import *
from pimage import *
from constants import *
from globs import *
from colors import *
from attribs import *
from lights import *
from materials import *
from primitives import *
from shapes import *                        
from fonts import *
from transformations import *
from mathfunctions import *
    
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
    # increment frame count and draw
    frame.count += 1
    frame.rate = pyglet.clock.get_fps()
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
    mouse.x, mouse.y = x, canvas.height - y
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
    mouse.x, mouse.y = x, canvas.height - y
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
    mouse.x, mouse.y = x, canvas.height - y
    mouse.pressed = True
    callback.mouseDragged()

def on_mouse_motion(x, y, dx, dy):
    """Called when mouse is moved with no buttons pressed."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, canvas.height - y
    mouse.button = None
    mouse.pressed = False
    callback.mouseMoved()
    
def on_resize(width, height):
    """Called whenever the window is resized."""
    canvas.width = width
    canvas.height = height
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

def cursor(*args):
    """Sets up the cursor type. Arguments:
    cursor()
    cursor(MODE)
    cursor(img,x,y)
    """
    canvas.window.set_mouse_visible(True)
    if len(args)==0:
        pass
    elif len(args)==1:
        canvas.cursor = canvas.window.get_system_mouse_cursor(args[0])
        canvas.window.set_mouse_cursor(canvas.cursor)
    elif len(args)==3:
        canvas.cursor = pyglet.window.ImageMouseCursor(args[0].img, args[1], args[2])
        canvas.window.set_mouse_cursor(canvas.cursor)
    else:
        assert (False, "Wrong number of arguments")
        
def noCursor():
    """Hides the cursor."""
    canvas.window.set_mouse_visible(False)
    
def loop():
    """Enables the periodical refresh of the screen."""
    frame.loop = True
    pyglet.clock.unschedule(__draw)
    pyglet.clock.schedule(__draw,1.0/frame.targetRate)
    
def noLoop():
    """Disables the periodical refresh of the screen."""
    frame.loop = False
    pyglet.clock.unschedule(__draw)
    
def frameRate(rate):
    """Sets the frame rate."""        
    frame.targetRate = rate
    if frame.loop: loop()    

def size(nx=canvas.width,ny=canvas.height,fullscreen=False,resizable=False,caption="PyProcessing"):
    """Inits graphics screen with nx x ny pixels.
    Caption is the window title."""
    # Set up canvas
    global canvas
    if canvas.window != None:
        # get rid of window created on an earlier call to size
        canvas.window.close()
        canvas.window = None
    
    # create a window. Obs.: it is created initially with visible=False so
    # that the default window may be silently destroyed and recreated.
    # After the run() function is called, the window is made visible
    if fullscreen: nx,ny = None,None
    try:
        # Try and create a window with double buffer
        canvas.config = Config(depth_size=24, alpha_size=8, double_buffer=True,)
        canvas.window = pyglet.window.Window(nx, ny, resizable=resizable, fullscreen=fullscreen,
                        config=canvas.config, caption=caption, visible = False)
    except pyglet.window.NoSuchConfigException:
        print ("No such conf")
        # Fall back default config
        canvas.window = pyglet.window.Window(nx, ny, resizable=resizable, caption=caption, 
                        fullscreen=fullscreen, visible = False)
    canvas.width = canvas.window.width
    canvas.height = canvas.window.height
    
    # some defaults:
    noSmooth()
    # bezier init
    bezierDetail(30)
    # set frame rate
    frameRate (frame.targetRate)    
    # enable depth buffering by default
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
    # clear canvas with medium gray
    background(200)
    # force a resize call
    on_resize(canvas.width,canvas.height)
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
        
    # Automatically call setup if function was defined in the main program
    if 'setup' in maindir: 
        __main__.setup()
        # Call draw at least once even if setup called noloop
        if 'draw' in maindir: __main__.draw()
        
    # set up other callbacks
    canvas.window.event(on_close)
    canvas.window.event(on_mouse_press)
    canvas.window.event(on_mouse_release)
    canvas.window.event(on_mouse_drag)
    canvas.window.event(on_mouse_motion)
    canvas.window.event(on_resize)
    canvas.window.event(on_key_press)
    canvas.window.event(on_key_release)
    
    # make window visible
    canvas.window.set_visible(True)
    
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

