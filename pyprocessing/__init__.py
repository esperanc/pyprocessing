#coding: utf-8
# ----------------------------------------------------------------------------
# pyprocessing
# Copyright (c) 2009 Claudio Esperança
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyprocessing nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
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
    
import sys,math,ctypes,os,time,webbrowser
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
from flippolicy import *
import config

# We infringe good Python practice here by polluting the
# __builtin__ namespace with global symbols width and height,
# which are the two most commonly used "global" variables
# in Processing. This is done in two places: the size() function
# and the on_resize() callback. 

import __builtin__

__builtin__.width = __builtin__.height = 0

starttime = time.time()

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
    mouse.x, mouse.y = x, height - y
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
    mouse.x, mouse.y = x, height - y
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
    if key.modifiers == 1:
        key.char = key.char.upper()
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
    mouse.x, mouse.y = x, height - y
    mouse.pressed = True
    callback.mouseDragged()

def on_mouse_motion(x, y, dx, dy):
    """Called when mouse is moved with no buttons pressed."""
    pmouse.x,pmouse.y = mouse.x,mouse.y
    mouse.x, mouse.y = x, height - y
    mouse.button = None
    mouse.pressed = False
    callback.mouseMoved()
    
def on_resize(w, h):
    """Called whenever the window is resized."""
    # beware of the margin!
    mx, my = canvas.margin
    if max(mx,my)>0 and w == width+mx and h == height+my: 
        # This window has the same size as specified by
        # size(). keep the margin!
        pass
    else:
        # get rid of the margin
        canvas.margin = mx,my = 0,0
        __builtin__.width = w
        __builtin__.height = h
    # Remember window size if fullscreen
    if canvas.window.fullscreen:
        __builtin__.width,__builtin__.height=screen.width,screen.height
    # Set up a reasonable perspective view
    glViewport(mx/2, my/2, width, height)
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
        raise ValueError, "Wrong number of arguments"
        
def noCursor():
    """Hides the cursor."""
    canvas.window.set_mouse_visible(False)
    
def link(url, target = None):
    """Links to a webpage using the default browser."""
    webbrowser.open(url)
    
def delay(t):
    """Stops the program for t milliseconds."""
    time.sleep(t/1000.0)

def day():
    """Returns the current day as a value from 1 - 31"""
    return int(time.strftime("%d",time.gmtime()))

def hour():
    """Returns the current hour as a value from 0 - 24"""
    gmt = int(time.strftime("%H",time.gmtime()))
    timezone = time.timezone/60/60
    if gmt < timezone: gmt+=24
    if gmt-timezone > 23: return (gmt-timezone)%24
    return gmt-timezone

def millis():
    """Returns the number of milliseconds since starting
    the application."""
    return (time.time() - starttime)*1000

def minute():
    """Returns the current minute as a value from 0 - 59"""
    return int(time.strftime("%M",time.gmtime()))

def month():
    """Returns the current month as a value from 1 - 12"""
    return int(time.strftime("%m",time.gmtime()))

def second():
    """Returns the current second as a value from 0 - 61"""
    return int(time.strftime("%S",time.gmtime()))

def year():
    """Returns the current year (2005, 2006, etc)"""
    return int(time.strftime("%Y",time.gmtime()))

def loop():
    """Enables the periodical refresh of the screen."""
    frame.loop = True
    pyglet.clock.unschedule(__draw)
    pyglet.clock.schedule_interval(__draw,1.0/frame.targetRate)
    
def noLoop():
    """Disables the periodical refresh of the screen."""
    frame.loop = False
    pyglet.clock.unschedule(__draw)
    
def redraw():
    """Signals that the 'draw()' callback should be called."""
    pyglet.clock.schedule_once(__draw,0)
    
def frameRate(rate):
    """Sets the frame rate."""        
    frame.targetRate = rate
    if frame.loop: loop()    
        
def popStyle():
    """Restores the prior drawing settings."""
    glPopAttrib(GL_ALL_ATTRIB_BITS)

def pushStyle():
    """Saves the current drawing settings."""
    glPushAttrib(GL_ALL_ATTRIB_BITS)

def size(nx=100,ny=100,fullscreen=False,resizable=False,caption="pyprocessing",
         multisample=config.multisample):
    """Inits graphics screen with nx x ny pixels.
    Caption is the window title."""
    # Set up canvas
    global canvas,screen
    if canvas.window != None:
        # get rid of window created on an earlier call to size
        canvas.window.close()
        canvas.window = None
    
    # Create a window. 
    #
    # Note 1: It is created initially with visible=False so
    # that the default window may be silently destroyed and recreated.
    # After the run() function is called, the window is made visible.
    # 
    # Note 2: A margin is defined for small windows. Apparently, 
    # Pyglet under MS Windows does not cope well with windows with height 
    # smaller than 120 pixels.
    #
    if fullscreen: 
        sizex,sizey = None,None
        canvas.margin = (0,0)
    else:
        sizex = max(120,int(nx))
        sizey = max(120,int(ny))
        canvas.margin = (sizex-nx, sizey-ny)
    if multisample: 
        canvas.config = Config(sample_buffers=1,samples=4,depth_size=24,double_buffer=True,alpha_size=8)
    else: 
        canvas.config = Config(depth_size=24,double_buffer=True,apha_size=8) # a sane default, hopefully
        
    # select the proper window class depending on the flippolicy
    windowClass = { DOUBLE_FLIP_POLICY:PyprocessingWindow,
                    SINGLE_FLIP_POLICY:SingleBufferWindow,
                    FBO_FLIP_POLICY:FBOWindow,
                    ACCUM_FLIP_POLICY:AccumWindow,
                    BACKUP_FLIP_POLICY:BackupWindow}[config.flipPolicy]
    #
    # If single buffering is used, the window must be mapped onto 
    # the screen immediately (visible = True).
    #
    isVisible = config.flipPolicy in (SINGLE_FLIP_POLICY,ACCUM_FLIP_POLICY,BACKUP_FLIP_POLICY)
    try:
        # Try and create a window with the requested config
        canvas.window = windowClass(sizex, sizey, resizable=resizable,
                        fullscreen=fullscreen,
                        config=canvas.config, caption=caption, visible = isVisible)
        #glEnable(GL_BLEND) 
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

    except pyglet.window.NoSuchConfigException, msg:
        # Fall back to a minimalistic config for older hardware
        display = pyglet.window.get_platform().get_default_display()
        screen = display.get_screens()[0]
        canvas.config = None
        for template_config in [
            Config(depth_size=24, double_buffer = True),
            Config(depth_size=16, double_buffer = True)]:
            try:
                canvas.config = screen.get_best_config(template_config)
                break
            except pyglet.window.NoSuchConfigException:
                pass
        if canvas.config == None: 
            raise pyglet.window.NoSuchConfigException,\
            "Sorry, but it seems your hardware does not support any usable OpenGL config"
        canvas.window = windowClass(sizex, sizey, resizable=resizable, caption=caption, 
                                    fullscreen=fullscreen, config = canvas.config,
                                    visible = isVisible)
        # turn on the fix that prevents polygon antialiasing
        config.smoothFixHack = True

    canvas.window.clear()
    # set the width and height global variables
    __builtin__.width = nx
    __builtin__.height = ny
    
    # get the screen dimensions
    screen.width = canvas.window.screen.width
    screen.height = canvas.window.screen.height
    
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
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (ctypes.c_float * 4)  (0,0,0,1))
    specular(0)
    ambient(0.2*255)
    shininess(10)
    # set up colors
    fill(255)
    stroke(0)
    # clear canvas with medium gray
    background(200)
    # force a resize call
    on_resize(sizex,sizey)
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
        __draw()
        
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
if canvas.window == None: size(100,100)

#test program
if __name__=="__main__":
    def draw():
        background(200)
        smooth()
        textFont (createFont ("Times", size=24))
        fill (0)
        text("Python Processing", 10, 42)
        fill (255)
        stroke(0)
        rect(width/2,height/2,50,50)
        if mouse.pressed:
            if mouse.button == LEFT:
                fill(255,0,0,100)
                noStroke()
                ellipse(mouse.x,mouse.y, 60, 60)
            elif mouse.button == RIGHT:
                fill(0,128,255,100)
                noStroke()
                rect (mouse.x, mouse.y, 60, 60)
            else: save("test.png")
    size(300,300)
    ellipseMode(CENTER)
    rectMode (CENTER)
    run()
