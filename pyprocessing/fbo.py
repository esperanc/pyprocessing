import pyglet
from pyglet.gl import *
from ctypes import *

class FBO(object):
    """Basic helper for using OpenGL's Frame Buffer Object (FBO)"""
    
    @staticmethod
    def supported():
        """A static method that tells if FBOs are supported.
        If not sure, call this before creating an FBO instance."""
        
        # Check if the board / driver supports FBO
        if not gl_info.have_extension("GL_EXT_framebuffer_object"):
            return False
        if not gl_info.have_extension("GL_ARB_draw_buffers"):
            return False
        
        return True

    def __init__(self, width=100, height=100):
        """Creates a Frame Buffer Object (FBO)"""
    
        # Must be supported...
        assert (FBO.supported())
        
        self.width = width
        self.height = height
 
        # Setting it up
        self.framebuffer = c_uint(0)
        self.depthbuffer = c_uint(0)
        self.img = c_uint(0)
        
        glGenFramebuffersEXT(1, byref(self.framebuffer))
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.framebuffer)
        
        # Adding a Depth Buffer
        glGenRenderbuffersEXT(1, byref(self.depthbuffer))
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, self.depthbuffer)
        glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_DEPTH_ATTACHMENT_EXT, 
                                     GL_RENDERBUFFER_EXT, self.depthbuffer)
    
        # Adding a Texture To Render To
        glGenTextures(1, byref(self.img))
        glBindTexture(GL_TEXTURE_2D, self.img)
    
        # Black magic (only works with these two lines)
        # (nearest works, as well as linear)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)

        # Add the texture ot the frame buffer as a color buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width, self.height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, 
                     GL_TEXTURE_2D, self.img, 0)
    
        # Check if it worked so far
        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        assert(status == GL_FRAMEBUFFER_COMPLETE_EXT)

    def attach(self):
        """Call this before rendering to the FBO."""

        # First we bind the FBO so we can render to it
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.framebuffer)
	
        # Save the view port and set it to the size of the texture
        glPushAttrib(GL_VIEWPORT_BIT)
        glViewport(0,0,self.width,self.height)

    def detach(self):
        """Call this after rendering to the FBO so that rendering now
        goes to the regular frame buffer."""

        # Restore old view port and set rendering back to default frame buffer
        glPopAttrib()    
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

    def getTexture(self):
        """Returns a pyglet image with the contents of the FBO."""
        self.data = (c_ubyte * (self.width*self.height*4))()
    
        glGetTexImage(GL_TEXTURE_2D, # target, 
 	                  0, # level, 
 	                  GL_RGBA, # format, 
 	                  GL_UNSIGNED_BYTE , # type, 
 	                  self.data) # GLvoid * img
 	              
        return pyglet.image.ImageData (self.width, self.height, 'RGBA', self.data)
 	
    def __del__(self):
        """Deallocates memory. Call this before discarding FBO."""
        glDeleteFramebuffersEXT(1, byref(self.framebuffer))
        glDeleteRenderbuffersEXT(1, byref(self.depthbuffer))
        glDeleteTextures(1,byref(self.img))
        

