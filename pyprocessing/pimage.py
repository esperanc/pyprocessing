import pyglet
from pyglet.gl import *
from globs import *
from constants import *
import config
import ctypes
from colors import _getColor, color,alpha



try:
    import numpy
    npy = True
except:
    npy = False


# exports

__all__=['PImage', 'loadImage', 'image', 'get', 'setScreen', 'save', 'createImage', 'loadPixels', 'updatePixels']

# the PImage class

class PImage (object):
    """This basically wraps pyglet's AbstractImage with a Processing-like syntax."""
    img = None # this is the actual AbstractImage
    
    
    def __init__(self, *args):
        """Either creates a new image from scratch or wraps an AbstractImage.
        Arguments are of the form
        PImage()
        PImage(width,height)
        PImage(width,height,format)
        PImage(img)
        """
        
        if len(args)==1 and isinstance(args[0],pyglet.image.AbstractImage): 
            # Wraps an AbstractImage
            self.img = args[0]
        elif len(args) in (2,3):
            # Creates an ImageData from width,height and type
            if len(args)==2: 
                # default 
                w,h = args
                format = ARGB
            else:
                w,h,format = args
            data = create_string_buffer(w*h*len(format))
            self.img = pyglet.image.ImageData(w,h,format,data.raw)
        else:
            assert(len(args)==0)
        # Do an initial loading of the pixels[] array
        self.loadPixels()
        self.updatePixels()
    
    def loadPixels(self):
        """Gets the pixel data as an array of integers."""
        n = self.width*self.height
        self.buf = self.img.get_image_data().get_data('BGRA',-self.width*4)
        if npy:
            self.pixels = numpy.fromstring(self.buf,dtype=ctypes.c_uint)
        else:
            self.pixels = ctypes.cast(self.buf,ctypes.POINTER(ctypes.c_uint))
        
    def filter(self,mode,*args):
        """Applies a filter to the image.
        The existant filters are: GRAY, INVERT, OPAQUE, THRESHOLD, POSTERIZE,
        ERODE and DILATE. This method requires numpy."""
        if mode == GRAY:
            if not npy: raise ImportError, "Numpy is required"
            lum1 = numpy.multiply(numpy.bitwise_and(numpy.right_shift(self.pixels,16),0xff),77)
            lum2 = numpy.multiply(numpy.bitwise_and(numpy.right_shift(self.pixels,8),0xff),151)
            lum3 = numpy.multiply(numpy.bitwise_and(self.pixels,0xff),28)
            lum = numpy.right_shift(numpy.add(numpy.add(lum1,lum2),lum3),8)
            self.pixels = numpy.bitwise_and(self.pixels,0xff000000)
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(lum,16))
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(lum,8))
            self.pixels = numpy.bitwise_or(self.pixels,lum)
        elif mode == INVERT:
            if not npy: raise ImportError, "Numpy is required"
            self.pixels = numpy.bitwise_xor(self.pixels,0xffffff)
        elif mode == OPAQUE:
            if not npy: raise ImportError, "Numpy is required"
            self.pixels = numpy.bitwise_or(self.pixels,0xff000000)
        elif mode == THRESHOLD:
            if not npy: raise ImportError, "Numpy is required"
            if not args: args = [0.5]
            thresh = args[0]*255
            aux = numpy.right_shift(numpy.bitwise_and(self.pixels,0xff00),8)
            aux = numpy.maximum(aux,numpy.bitwise_and(self.pixels,0xff))
            aux2 = numpy.right_shift(numpy.bitwise_and(self.pixels,0xff0000),16)
            boolmatrix = numpy.greater_equal(numpy.maximum(aux,aux2),thresh)
            self.pixels.fill(0xffffff)
            self.pixels = numpy.multiply(self.pixels,boolmatrix)
        elif mode == POSTERIZE:
            if not npy: raise ImportError, "Numpy is required"
            if not args: args = [8]
            levels1 = args[0] - 1
            rlevel = numpy.bitwise_and(numpy.right_shift(self.pixels,16),0xff)
            glevel = numpy.bitwise_and(numpy.right_shift(self.pixels,8),0xff)
            blevel = numpy.bitwise_and(self.pixels,0xff)
            rlevel = numpy.right_shift(numpy.multiply(rlevel,args[0]),8)
            rlevel = numpy.divide(numpy.multiply(rlevel,255),levels1)
            glevel = numpy.right_shift(numpy.multiply(glevel,args[0]),8)
            glevel = numpy.divide(numpy.multiply(glevel,255),levels1)
            blevel = numpy.right_shift(numpy.multiply(blevel,args[0]),8)
            blevel = numpy.divide(numpy.multiply(blevel,255),levels1)
            self.pixels = numpy.bitwise_and(self.pixels,0xff000000)
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(rlevel,16))
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(glevel,8))
            self.pixels = numpy.bitwise_or(self.pixels,blevel)
        elif mode == ERODE:
            if not npy: raise ImportError, "Numpy is required"
            out = numpy.empty(self.width*self.height)
            colorOrig = numpy.array(self.pixels)
            colOut = numpy.array(self.pixels)
            colLeft = numpy.roll(colorOrig,1)
            colRight = numpy.roll(colorOrig,-1)
            colUp = numpy.roll(colorOrig,self.width)
            colDown = numpy.roll(colorOrig,-self.width)
            currLum1 = numpy.bitwise_and(numpy.right_shift(colorOrig,16),0xff)
            currLum1 = numpy.multiply(currLum1,77)
            currLum2 = numpy.bitwise_and(numpy.right_shift(colorOrig,8),0xff)
            currLum2 = numpy.multiply(currLum2,151)
            currLum3 = numpy.multiply(numpy.bitwise_and(colorOrig,0xff),28)
            currLum = numpy.add(numpy.add(currLum1,currLum2),currLum3)
            lumLeft1 = numpy.bitwise_and(numpy.right_shift(colLeft,16),0xff)
            lumLeft1 = numpy.multiply(lumLeft1,77)
            lumLeft2 = numpy.bitwise_and(numpy.right_shift(colLeft,8),0xff)
            lumLeft2 = numpy.multiply(lumLeft2,151)
            lumLeft3 = numpy.multiply(numpy.bitwise_and(colLeft,0xff),28)
            lumLeft = numpy.add(numpy.add(lumLeft1,lumLeft2),lumLeft3)
            lumRight1 = numpy.bitwise_and(numpy.right_shift(colRight,16),0xff)
            lumRight1 = numpy.multiply(lumRight1,77)
            lumRight2 = numpy.bitwise_and(numpy.right_shift(colRight,8),0xff)
            lumRight2 = numpy.multiply(lumRight2,151)
            lumRight3 = numpy.multiply(numpy.bitwise_and(colRight,0xff),28)
            lumRight = numpy.add(numpy.add(lumRight1,lumRight2),lumRight3)  
            lumDown1 = numpy.bitwise_and(numpy.right_shift(colDown,16),0xff)
            lumDown1 = numpy.multiply(lumDown1,77)
            lumDown2 = numpy.bitwise_and(numpy.right_shift(colDown,8),0xff)
            lumDown2 = numpy.multiply(lumDown2,151)
            lumDown3 = numpy.multiply(numpy.bitwise_and(colDown,0xff),28)
            lumDown = numpy.add(numpy.add(lumDown1,lumDown2),lumDown3)  
            lumUp1 = numpy.bitwise_and(numpy.right_shift(colUp,16),0xff)
            lumUp1 = numpy.multiply(lumUp1,77)
            lumUp2 = numpy.bitwise_and(numpy.right_shift(colUp,8),0xff)
            lumUp2 = numpy.multiply(lumUp2,151)
            lumUp3 = numpy.multiply(numpy.bitwise_and(colUp,0xff),28)
            lumUp = numpy.add(numpy.add(lumUp1,lumUp2),lumUp3)  
            numpy.putmask(colOut,lumLeft>currLum,colLeft)
            numpy.putmask(currLum,lumLeft>currLum,lumLeft)
            numpy.putmask(colOut,lumRight>currLum,colRight)
            numpy.putmask(currLum,lumRight>currLum,lumRight)
            numpy.putmask(colOut,lumUp>currLum,colUp)
            numpy.putmask(currLum,lumUp>currLum,lumUp)
            numpy.putmask(colOut,lumDown>currLum,colDown)
            numpy.putmask(currLum,lumDown>currLum,lumDown)
            self.pixels = colOut
        elif mode == DILATE:
            if not npy: raise ImportError, "Numpy is required"
            out = numpy.empty(self.width*self.height)
            colorOrig = numpy.array(self.pixels)
            colOut = numpy.array(self.pixels)
            colLeft = numpy.roll(colorOrig,1)
            colRight = numpy.roll(colorOrig,-1)
            colUp = numpy.roll(colorOrig,self.width)
            colDown = numpy.roll(colorOrig,-self.width)
            currLum1 = numpy.bitwise_and(numpy.right_shift(colorOrig,16),0xff)
            currLum1 = numpy.multiply(currLum1,77)
            currLum2 = numpy.bitwise_and(numpy.right_shift(colorOrig,8),0xff)
            currLum2 = numpy.multiply(currLum2,151)
            currLum3 = numpy.multiply(numpy.bitwise_and(colorOrig,0xff),28)
            currLum = numpy.add(numpy.add(currLum1,currLum2),currLum3)
            lumLeft1 = numpy.bitwise_and(numpy.right_shift(colLeft,16),0xff)
            lumLeft1 = numpy.multiply(lumLeft1,77)
            lumLeft2 = numpy.bitwise_and(numpy.right_shift(colLeft,8),0xff)
            lumLeft2 = numpy.multiply(lumLeft2,151)
            lumLeft3 = numpy.multiply(numpy.bitwise_and(colLeft,0xff),28)
            lumLeft = numpy.add(numpy.add(lumLeft1,lumLeft2),lumLeft3)
            lumRight1 = numpy.bitwise_and(numpy.right_shift(colRight,16),0xff)
            lumRight1 = numpy.multiply(lumRight1,77)
            lumRight2 = numpy.bitwise_and(numpy.right_shift(colRight,8),0xff)
            lumRight2 = numpy.multiply(lumRight2,151)
            lumRight3 = numpy.multiply(numpy.bitwise_and(colRight,0xff),28)
            lumRight = numpy.add(numpy.add(lumRight1,lumRight2),lumRight3)  
            lumDown1 = numpy.bitwise_and(numpy.right_shift(colDown,16),0xff)
            lumDown1 = numpy.multiply(lumDown1,77)
            lumDown2 = numpy.bitwise_and(numpy.right_shift(colDown,8),0xff)
            lumDown2 = numpy.multiply(lumDown2,151)
            lumDown3 = numpy.multiply(numpy.bitwise_and(colDown,0xff),28)
            lumDown = numpy.add(numpy.add(lumDown1,lumDown2),lumDown3)  
            lumUp1 = numpy.bitwise_and(numpy.right_shift(colUp,16),0xff)
            lumUp1 = numpy.multiply(lumUp1,77)
            lumUp2 = numpy.bitwise_and(numpy.right_shift(colUp,8),0xff)
            lumUp2 = numpy.multiply(lumUp2,151)
            lumUp3 = numpy.multiply(numpy.bitwise_and(colUp,0xff),28)
            lumUp = numpy.add(numpy.add(lumUp1,lumUp2),lumUp3)  
            numpy.putmask(colOut,lumLeft<currLum,colLeft)
            numpy.putmask(currLum,lumLeft<currLum,lumLeft)
            numpy.putmask(colOut,lumRight<currLum,colRight)
            numpy.putmask(currLum,lumRight<currLum,lumRight)
            numpy.putmask(colOut,lumUp<currLum,colUp)
            numpy.putmask(currLum,lumUp<currLum,lumUp)
            numpy.putmask(colOut,lumDown<currLum,colDown)
            numpy.putmask(currLum,lumDown<currLum,lumDown)
            self.pixels = colOut


    def mask(self,image):
        """Uses the image passed as parameter as alpha mask."""
        if npy:
            aux1 = numpy.bitwise_and(self.pixels,0xffffff)
            aux2 = numpy.bitwise_and(image.pixels,0xff000000)
            aux2 = numpy.left_shift(aux,24)
            self.pixels = numpy.bitwise_or(aux1,aux2)
            return
        for i in range(self.width):
            for j in range(self.height):
                n = self.get(i,j)
                m = image.get(i,j)
                new = ((m & 0xff000000) << 24) | (n & 0xffffff)
                self.set(i,j,new)

    def updatePixels(self):
        """Saves the pixel data."""
        if npy: self.buf = self.pixels.tostring()
        self.img.get_image_data().set_data('BGRA',-self.width*4,self.buf)
        
    def set(self, x, y, color):
        """Sets the pixel at x,y with the given color."""
        self.pixels [y*self.width+x] = color
        self.updatePixels()
        
    def get(self, *args):
        """Returns a copy, a part or a pixel of this image.
        Arguments are of the form:
        get()
        get(x,y)
        get(x,y,width,height)
        """
        if len(args) in (0,4):
            # the result is an image
            if len(args) == 0:
                x,y,width,height = 0,0,self.width,self.height
            else:
                x,y,width,height = args
            assert(x>=0 and x<self.width and y>=0 and y<self.height and
                   width>0 and height>0 and x+width<=self.width and 
                   y+height<=self.height)
            if width != self.width or height != self.height:
                source = self.img.get_region(x,self.height-y-height,width,height)
            else:
                source = self.img
            result = PImage(width,height,self.img.format)
#            print source._current_pitch
#            print result.img._current_pitch
#            buf = source.get_data ('BGRA',result.img._current_pitch)
#            result.img.set_data ('BGRA', result.img._current_pitch, buf)
            result.img.get_texture().blit_into (source,0,0,0)
            return result
        else:
            # result is a pixel
            x,y = args
            assert(x>=0 and x<self.width and y>=0 and y<self.height)
            return self.pixels[y*self.width+x]
    
    def save(self,filename):
        """Saves this image as a file of the proper format."""
        self.img.save(filename)
    
    def __getWidth(self):
        """Getter for the width property."""
        return self.img.width
    
    width = property(__getWidth)

    def __getHeight(self):
        """Getter for the height property."""
        return self.img.height
    
    height = property(__getHeight)

# Image functions

def loadPixels():
    """Loads the data for the display window into the pixels array."""
    current = get()
    if npy:
        screen.pixels = numpy.array(current.pixels)
        return
    screen.pixels = (c_long*(width*height)) ()
    for i in range(width*height): screen.pixels[i] = current.pixels[i]

def updatePixels():
    """Updates the display window with the data in the pixels array."""
    new = createImage(width,height,'RGBA')
    color = _getColor((200))
    glClearColor (*color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if npy:
        new.pixels = numpy.array(screen.pixels)
        new.updatePixels()
    else: 
        for i in range(width*height): new.pixels[i] = screen.pixels[i]
    image(new,0,0)

def createImage(width, height, format):
    """Returns an empty PImage object."""
    return PImage(width, height, format)

def loadImage(filename,extension=None):
    """Loads an image from a file. Returns a PImage. Currently the extension
    argument is ignored."""
    return PImage(pyglet.image.load(filename))

def image(img, x, y, width=None, height=None):
    """Draws img at position x,y eventually scaled so that it has 
    the given width and height. """
    sprite = pyglet.sprite.Sprite(img.img)
    sprite.x = x
    sprite.y = y
    if attrib.imageMode == CORNERS:
        width = width-x
        height = height-y
    elif attrib.imageMode == CENTER:
        if width != None:
            sprite.x -= width/2
            sprite.y -= height/2
        else:
            sprite.x -= img.width/2
            sprite.y -= img.height/2
    if attrib.tintColor != None:
        r,g,b,a = attrib.tintColor
        sprite.color = (int(r*255),int(g*255),int(b*255))
        sprite.opacity = int(a*255)
    glPushMatrix()
    if width != None: 
        scalex = width*1.0/img.width
        scaley = height*1.0/img.height
        sprite.x /= scalex
        sprite.y /= scaley
    else:
        scalex,scaley = 1.0,1.0
    if config.coordInversionHack:
        glTranslatef(0,(sprite.y*2+sprite.height)*scaley,0)
        glScalef(scalex,-scaley,1)
    sprite.draw() 
    glPopMatrix()

def get(*args):
    """Returns a copy, a part or a pixel of the screen.
    Arguments are of the form:
    get()
    get(x,y)
    get(x,y,width,height)
    """
    if len(args) in (0,4):
        # the result is an image
        if len(args) == 0:
            x,y,w,h = 0,0,width,height
        else:
            x,y,w,h = args
        assert(x>=0 and x<width and y>=0 and y<height and
               w>0 and h>0 and x+w<=width and 
               y+h<=height)
        if w != width or h != height:
            return PImage(pyglet.image.get_buffer_manager().get_color_buffer()).get(x,y,w,h)
        else:
            return PImage(pyglet.image.get_buffer_manager().get_color_buffer())
    else:
        x,y = args
        return PImage(pyglet.image.get_buffer_manager().get_color_buffer()).get(x,y)

def setScreen (x,y,data):
    """Sets the position x,y of the screen with data, which can be a color or
    a PImage.
    Important: this function is equivalent to Processing's 'set' function. 
    Python, however, uses the 'set' identifier to refer to the set data type. 
    """
    if isinstance (data,PImage):
        image(data,x,y)
    else:
        glRasterPos2i(x,y)
        buf = (ctypes.c_uint)(data)
        glDrawPixels(1,
                     1,
 	                 GL_BGRA, 
 	                 GL_UNSIGNED_BYTE, 
 	                 byref(buf))
 	                 
def save(filename):
    """Saves the canvas into a file. Note that only .png images are supported by
    pyglet unless PIL is also installed."""
    get().save(filename)
