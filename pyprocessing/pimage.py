import pyglet
from pyglet.gl import *
from globs import *
from constants import *
import config
import ctypes
from colors import _getColor, color,alpha


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
                w,h=args
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
        self.pixels = ctypes.cast(self.buf,ctypes.POINTER(ctypes.c_uint))
        
    def filter(self,mode,*args):
        """Applies a filter to the image.
        The existant filters are: GRAY, INVERT, OPAQUE, THRESHOLD, POSTERIZE,
        ERODE and DILATE."""
        if mode == GRAY:
            for i in range(self.width):
                for j in range(self.height):
                    n = self.get(i,j)
                    rgba = _getColor(n)
                    lum = (77*(n>>16&0xff) + 151*(n>>8&0xff) + 28*(n&0xff)) >> 8
                    new = (n & -16777216) | lum<<16 | lum<<8 | lum
                    self.set(i,j,new)
        elif mode == INVERT:
            for i in range(self.width):
                for j in range(self.height):
                    n = self.get(i,j)
                    n ^= 0xffffff
                    self.set(i,j,n)
        elif mode == OPAQUE:
            for i in range(self.width):
                for j in range(self.height):
                    n = self.get(i,j)
                    rgba = _getColor(n)
                    new = (rgba[0],rgba[1],rgba[2],1)
                    new = color(new)
                    self.set(i,j,new)
        elif mode == THRESHOLD:
            thresh = args[0]*255
            for i in range(self.width):
                for j in range(self.height):
                    n = self.get(i,j)
                    new = max((n & 16711680) >> 16, max((n & 65280)>>8, (n & 255)))
                    if new < thresh: new = (new & -16777216) | 0x000000
                    else: new = (new & -16777216) | 0xffffff
                    self.set(i,j,new)
        elif mode == POSTERIZE:
            levels1 = args[0] - 1
            for i in range(self.width):
                for j in range(self.height):
                    n = self.get(i,j)
                    rlevel = (n >> 16) & 0xff
                    glevel = (n >> 8) & 0xff
                    blevel = n & 0xff
                    rlevel = (((rlevel*args[0])>>8)*255)/levels1
                    blevel = (((blevel*args[0])>>8)*255)/levels1
                    glevel = (((glevel*args[0])>>8)*255)/levels1
                    new = ((0xff000000 & n) | (rlevel << 16) | (glevel << 8) | blevel)
                    self.set(i,j,new)
        elif mode == ERODE:
            currIdx=0
            maxIdx=self.width*self.height
            out = [0]*(maxIdx)
            while (currIdx<maxIdx):
                currRowIdx=currIdx
                maxRowIdx=currIdx+self.width
                while (currIdx<maxRowIdx):
                    colOrig=colOut=self.pixels[currIdx]
                    idxLeft=currIdx-1
                    idxRight=currIdx+1
                    idxUp=currIdx-self.width
                    idxDown=currIdx+self.width
                    if (idxLeft<currRowIdx): idxLeft=currIdx
                    if (idxRight>=maxRowIdx): idxright=currIdx
                    if (idxUp<0): idxUp=0
                    if (idxDown>=maxIdx): idxDown=currIdx
                    colUp=self.pixels[idxUp]
                    colLeft=self.pixels[idxLeft]
                    colDown=self.pixels[idxDown]
                    colRight=self.pixels[idxRight]
                    currLum=77*(colOrig>>16&0xff)+151*(colOrig>>8&0xff)+28*(colOrig&0xff)
                    lumLeft=77*(colLeft>>16&0xff)+151*(colLeft>>8&0xff)+28*(colLeft&0xff)
                    lumRight=77*(colRight>>16&0xff)+151*(colRight>>8&0xff)+28*(colRight&0xff)
                    lumUp=77*(colUp>>16&0xff)+151*(colUp>>8&0xff)+28*(colUp&0xff)
                    lumDown=77*(colDown>>16&0xff)+151*(colDown>>8&0xff)+28*(colDown&0xff)
                    if (lumLeft>currLum):
                        colOut=colLeft
                        currLum=lumLeft
                    if (lumRight>currLum):
                        colOut=colRight
                        currLum=lumRight
                    if (lumUp>currLum):
                        colOut=colUp
                        currLum=lumUp
                    if (lumDown>currLum):
                        colOut=colDown
                        currLum=lumDown
                    out[currIdx]=colOut
                    currIdx+=1
            for i in range(maxIdx): self.pixels[i] = out[i]
        elif mode == DILATE:
            currIdx=0
            maxIdx=self.width*self.height
            out = [0]*(maxIdx)
            while (currIdx<maxIdx):
                currRowIdx=currIdx
                maxRowIdx=currIdx+self.width
                while (currIdx<maxRowIdx):
                    colOrig=colOut=self.pixels[currIdx]
                    idxLeft=currIdx-1
                    idxRight=currIdx+1
                    idxUp=currIdx-self.width
                    idxDown=currIdx+self.width
                    if (idxLeft<currRowIdx): idxLeft=currIdx
                    if (idxRight>=maxRowIdx): idxright=currIdx
                    if (idxUp<0): idxUp=0
                    if (idxDown>=maxIdx): idxDown=currIdx
                    colUp=self.pixels[idxUp]
                    colLeft=self.pixels[idxLeft]
                    colDown=self.pixels[idxDown]
                    colRight=self.pixels[idxRight]
                    currLum=77*(colOrig>>16&0xff)+151*(colOrig>>8&0xff)+28*(colOrig&0xff)
                    lumLeft=77*(colLeft>>16&0xff)+151*(colLeft>>8&0xff)+28*(colLeft&0xff)
                    lumRight=77*(colRight>>16&0xff)+151*(colRight>>8&0xff)+28*(colRight&0xff)
                    lumUp=77*(colUp>>16&0xff)+151*(colUp>>8&0xff)+28*(colUp&0xff)
                    lumDown=77*(colDown>>16&0xff)+151*(colDown>>8&0xff)+28*(colDown&0xff)
                    if (lumLeft<currLum):
                        colOut=colLeft
                        currLum=lumLeft
                    if (lumRight<currLum):
                        colOut=colRight
                        currLum=lumRight
                    if (lumUp<currLum):
                        colOut=colUp
                        currLum=lumUp
                    if (lumDown<currLum):
                        colOut=colDown
                        currLum=lumDown
                    out[currIdx]=colOut
                    currIdx+=1
            for i in range(maxIdx): self.pixels[i] = out[i]

    def mask(self,image):
        """Uses the image passed as parameter as alpha mask."""
        for i in range(self.width):
            for j in range(self.height):
                n = self.get(i,j)
                m = image.get(i,j)
                new = ((m & 0xff) << 24) | (n & 0xffffff)
                self.set(i,j,new)

    def updatePixels(self):
        """Saves the pixel data."""
        self.img.get_image_data().set_data('BGRA',-self.width*4,self.buf)
        
    def set(self, x, y, color):
        """Sets the pixel at x,y with the given color."""
        self.pixels [y*self.width+x] = color
        
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
    screen.pixels = (c_long*(width*height)) ()
    for i in range(width*height): screen.pixels[i] = current.pixels[i]

def updatePixels():
    """Updates the display window with the data in the pixels array."""
    new = createImage(width,height,'RGBA')
    color = _getColor((200))
    glClearColor (*color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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
