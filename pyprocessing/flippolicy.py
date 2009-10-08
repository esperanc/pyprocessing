"""
This module contains several window classes derived from pyglet's
window classes. They implement variations on the standard way
of handling the flip method. These are necessary because of the
implementation-dependent way used by OpenGL to flip between the back and
the front buffer. 

In most cases where a modern graphics board is supported
by a recent driver, flipping works by copying the back to the front buffer,
which is necessary whenever the screen is not completely redrawn from
scratch between one frame and the next. If this is the case in your installation,
the regular PyprocessingWindow, which is merely a pyglet.window.Window under 
another name, should be used and will give you the best performance.

Some drivers, however, do not implement flip by copying, but merely makes the 
video controller address the other video memory buffer. This is what is called
flipping by swapping. In such cases, programs which rely on a stable frame
buffer will not work as expected. I spent a long time looking for portable
ways of enforcing a copy flip, but it seems that there is no reliable way of
doing that. 

One way of coping with the problem is to use single buffering, so that drawing
is actually performed on the front buffer. This is not a good idea in
general, because the drawing may result in flickering and other visual
visual artifacts. Nevertheless, I found that the Intel 945 express chipset
works fairly well in this mode under MS Windows. Other driver/board/OS 
combinations might also work well in this mode. If this is the case, 
instancing a SingleBufferWindow will solve the problem.

Another way of providing a stable drawing buffer is to draw to a separate
off-screen buffer. The most efficient way of doing this is to use a Frame
Buffer Object, or FBO. The idea then is to copy the FBO to the back buffer
just before the flip. The FBOWindow implements just this.

Unfortunately the FBO extension is not common in old hardware. In this case,
another type of buffer might be used to store a copy of the back buffer. The 
idea is to copy the back buffer to such an auxiliary buffer, flip and then 
copy it back. The simplest, but probably not the most efficient way of doing
this is to use the accumulation buffer, which can be copied from/to with a
single glAccum instruction. The AccumWindow implements this policy.

The default flipping policy is governed by appropriate calls to the
hint() function just before calling size(). You might wish to change the default
by editting the config variable in the globs submodule.
"""

import pyglet
from pyglet.gl import *
from fbo import FBO

__all__=['PyprocessingWindow','FBOWindow','SingleBufferWindow','AccumWindow']


class PyprocessingWindow (pyglet.window.Window):
    """This is just a wrapper for the pyglet window class. If any 
    window method or attribute should be messed with for all of pyprocessing's
    window classes, it's best to do it here."""
    pass

class FBOWindow(PyprocessingWindow):
    """This is a pyglet window where drawing in fact occurs inside an FBO.
    The flip method is overridden so that instead of merely swapping the
    back and front buffers, the FBO is first blitted onto the back buffer.
    The idea is to provide a stable drawing canvas which is not erased or
    corrupted by the flip."""
    
    def __init__(self, *args, **keyargs):
        """Constructor"""
        # construct the base class
        super(FBOWindow, self).__init__(*args, **keyargs)
        # construct the fbo and attach it
        self.fbo = FBO(self.width, self.height)
        self.fbo.attach()
        
    def flip(self):
        """Override the flip method."""
        # cease using the FBO and start using the regular frame buffer
        self.fbo.detach()
        # save the OpenGL state
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glViewport(0,0,self.width,self.height)
        # Draws a quad with the fbo as a texture
        glDisable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glEnable(GL_TEXTURE_2D)
        glColor3f(1,1,1)
        glBindTexture(GL_TEXTURE_2D, self.fbo.img)
        glBegin(GL_QUADS)
        for v,t in [((-1,-1,0),(0,0)),
                ((-1,1,0),(0,1)),
                ((1,1,0),(1,1)),
                ((1,-1,0),(1,0))]: 
           glTexCoord2f(*t)
           glVertex3f(*v)
        glEnd()
        # restore the state
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPopAttrib()

        # do the actual flip
        super (FBOWindow, self).flip()
        # reattach the fbo for further drawing
        self.fbo.attach()
        
    def on_resize(self,w,h):
        super (FBOWindow, self).on_resize(w,h)
        self.fbo.detach()
        self.fbo = FBO(w,h)
        self.fbo.attach()

class SingleBufferWindow(PyprocessingWindow):
    """This is a pyglet window with a single buffer config."""
    
    def __init__(self, *args, **keyargs):
        """Constructor"""
        # construct the base class
        if 'config' in keyargs:
            config = keyargs['config']
        else:
            config = Config(depth_size=24)
        config.double_buffer = False
        keyargs['config'] = config
        super(SingleBufferWindow, self).__init__(*args, **keyargs)
         
        
class AccumWindow(PyprocessingWindow):
    """This is a pyglet window for which an accumulation buffer is defined.
    The flip method is overridden so that instead of merely swapping the
    back and front buffers, a copy of the back buffer is blitted onto the accum
    buffer, and after the flip the accum buffer is copied back.
    The idea is to provide a stable drawing canvas which is not erased or
    corrupted by the flip."""
    
    def __init__(self, *args, **keyargs):
        """Constructor"""
        # construct the base class
        if 'config' in keyargs:
            config = keyargs['config']
        else:
            config = Config(double_buffer=True,depth_size=24)
        config.accum_alpha_size = 8
        config.accum_red_size = 8
        config.accum_green_size = 8
        config.accum_blue_size = 8
        keyargs['config'] = config
        super(AccumWindow, self).__init__(*args, **keyargs)
        
    def flip(self):
        """Override the flip method."""
        # copy from the the back buffer to the accumulation buffer
        glAccum(GL_LOAD, 1.0)
        # do the actual flip
        super (AccumWindow, self).flip()
        # copy the accum buffer to the back buffer
        glAccum(GL_RETURN, 1)

