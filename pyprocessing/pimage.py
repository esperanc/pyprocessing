import pyglet
from pyglet.gl import *
from globs import *
from constants import *
import config
import ctypes
import math
from colors import _getColor,color,blue


try:
    import numpy
    npy = True
    numpy.seterr(divide='ignore')
except:
    npy = False


# exports

__all__=['PImage', 'loadImage', 'image', 'get', 'setScreen', 'save', 'createImage', 'loadPixels', 'updatePixels','screenFilter','blend']

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
            # Creates an ImageData from width, height and type
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
        ERODE, DILATE and BLUR. This method requires numpy."""
        if not npy: raise ImportError, "Numpy is required"
        if mode == GRAY:
            #Gray value = (77*(n>>16&0xff) + 151*(n>>8&0xff) + 28*(n&0xff)) >> 8
            #Where n is the ARGB color of the pixel
            lum1 = numpy.multiply(numpy.bitwise_and(numpy.right_shift(self.pixels,16),0xff),77)
            lum2 = numpy.multiply(numpy.bitwise_and(numpy.right_shift(self.pixels,8),0xff),151)
            lum3 = numpy.multiply(numpy.bitwise_and(self.pixels,0xff),28)
            lum = numpy.right_shift(numpy.add(numpy.add(lum1,lum2),lum3),8)
            self.pixels = numpy.bitwise_and(self.pixels,0xff000000)
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(lum,16))
            self.pixels = numpy.bitwise_or(self.pixels,numpy.left_shift(lum,8))
            self.pixels = numpy.bitwise_or(self.pixels,lum)
        elif mode == INVERT:
            #This is the same as applying an exclusive or with the maximum value
            self.pixels = numpy.bitwise_xor(self.pixels,0xffffff)
        elif mode == BLUR:
            if not args: args = [3]
            #Makes the image square by adding zeros.
            #This avoids the convolution (via fourier transform multiplication)
            #from jumping to another extreme of the image when a border is reached
            if self.width > self.height:
                dif = self.width - self.height
                updif = numpy.zeros(self.width*dif/2,dtype=numpy.uint32)
                downdif = numpy.zeros(self.width*(dif-dif/2),dtype=numpy.uint32)
                self.pixels = numpy.concatenate((updif,self.pixels,downdif))
                size = self.width
            elif self.width < self.height:
                dif = self.height - self.width
                leftdif = numpy.zeros(self.height*dif/2,dtype=numpy.uint32)
                rightdif = numpy.zeros(self.height*(dif-dif/2),dtype=numpy.uint32)
                self.pixels = self.pixels.reshape(self.height,self.width)
                self.pixels = numpy.transpose(self.pixels)
                self.pixels = self.pixels.reshape(self.width*self.height)
                self.pixels = numpy.concatenate((leftdif,self.pixels,rightdif))
                self.pixels = self.pixels.reshape(self.height,self.height)
                self.pixels = numpy.transpose(self.pixels)
                self.pixels = self.pixels.reshape(self.height*self.height)
                size = self.height
            else: size = self.height
            #Creates a gaussian kernel of the image's size
            _createKernel2d(args[0],size)
            #Divides the image's R, G and B channels, reshapes them
            #to square matrixes and applies two dimensional fourier transforms
            red = numpy.bitwise_and(numpy.right_shift(self.pixels,16),0xff)
            red = numpy.reshape(red,(size,size))
            red = numpy.fft.fft2(red)
            green = numpy.bitwise_and(numpy.right_shift(self.pixels,8),0xff)
            green = numpy.reshape(green,(size,size))
            green = numpy.fft.fft2(green)
            blue = numpy.bitwise_and(self.pixels,0xff)                    
            blue = numpy.reshape(blue,(size,size))
            blue = numpy.fft.fft2(blue)
            #Does a element-wise multiplication of each channel matrix
            #and the fourier transform of the kernel matrix
            kernel = numpy.fft.fft2(weights)
            red = numpy.multiply(red,kernel)
            green = numpy.multiply(green,kernel)
            blue = numpy.multiply(blue,kernel)
            #Reshapes them back to arrays and converts to unsigned integers
            red = numpy.reshape(numpy.fft.ifft2(red).real,size*size)
            green = numpy.reshape(numpy.fft.ifft2(green).real,size*size)
            blue = numpy.reshape(numpy.fft.ifft2(blue).real,size*size)
            red = red.astype(numpy.uint32)
            green = green.astype(numpy.uint32)
            blue = blue.astype(numpy.uint32)
            self.pixels = numpy.bitwise_or(numpy.left_shift(green,8),blue)
            self.pixels = numpy.bitwise_or(numpy.left_shift(red,16),self.pixels)
            #Crops out the zeros added
            if self.width > self.height:
                self.pixels = self.pixels[self.width*dif/2:size*size-self.width*(dif-dif/2)]
            elif self.width < self.height:
                self.pixels = numpy.reshape(self.pixels,(size,size))
                self.pixels = numpy.transpose(self.pixels)
                self.pixels = numpy.reshape(self.pixels,size*size)
                self.pixels = self.pixels[self.height*dif/2:size*size-self.height*(dif-dif/2)]
                self.pixels = numpy.reshape(self.pixels,(self.width,self.height))
                self.pixels = numpy.transpose(self.pixels)
                self.pixels = numpy.reshape(self.pixels,self.height*self.width)
        elif mode == OPAQUE:
            #This is the same as applying an bitwise or with the maximum value
            self.pixels = numpy.bitwise_or(self.pixels,0xff000000)
        elif mode == THRESHOLD:
            #Maximum = max((n & 0xff0000) >> 16, max((n & 0xff00)>>8, (n & 0xff)))
            #Broken down to Maximum = max(aux,aux2)
            #The pixel will be white if its maximum is greater than the threshold
            #value, and black if not. This was implemented via a boolean matrix
            #multiplication.
            if not args: args = [0.5]
            thresh = args[0]*255
            aux = numpy.right_shift(numpy.bitwise_and(self.pixels,0xff00),8)
            aux = numpy.maximum(aux,numpy.bitwise_and(self.pixels,0xff))
            aux2 = numpy.right_shift(numpy.bitwise_and(self.pixels,0xff0000),16)
            boolmatrix = numpy.greater_equal(numpy.maximum(aux,aux2),thresh)
            self.pixels.fill(0xffffff)
            self.pixels = numpy.multiply(self.pixels,boolmatrix)
        elif mode == POSTERIZE:
            #New channel = ((channel*level)>>8)*255/(level-1)
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
            #Checks the pixels directly above, under and to the left and right
            #of each pixel of the image. If it has a greater luminosity, then
            #the center pixel receives its color
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
            #Checks the pixels directly above, under and to the left and right
            #of each pixel of the image. If it has a lesser luminosity, then
            #the center pixel receives its color
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
        self.updatePixels()

    def mask(self,image):
        """Uses the image passed as parameter as alpha mask."""
        if npy:
            aux1 = numpy.bitwise_and(self.pixels,0xffffff)
            aux2 = numpy.bitwise_and(image.pixels,0xff000000)
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
def screenFilter(mode,*args):
    """Applies a filter to the current drawing canvas.
    This method requires numpy."""
    if not npy: raise ImportError, "Numpy is required"
    new = createImage(width,height,'RGBA')
    loadPixels()
    new.pixels = numpy.array(screen.pixels)
    new.filter(mode,*args)
    new.updatePixels()
    image(new,0,0)
    
    
def mix(a, b, f): 
    return a + (((b - a) * f) >> 8);
    
def _mix(a, b, f):
    #Used for the blend function (mixes colors according to their alpha values)
    c = numpy.multiply(numpy.subtract(b,a),f)
    return numpy.add(numpy.right_shift(c,8),a)

def _high(a, b):
    #Used for the blend function (returns the matrix with the maximum bitwise values)
    c = numpy.multiply(a.__le__(b),b)
    d = numpy.multiply(a.__gt__(b),a)
    return numpy.add(c,d)

def _low(a, b):
    #Used for the blend function (returns the matrix with the minimum bitwise values)
    c = numpy.multiply(a.__ge__(b),b)
    d = numpy.multiply(a.__lt__(b),a)
    return numpy.add(c,d)

def _peg(a):
    #Used for the blend function (returns the matrix with constrained values)
    b = numpy.multiply(a.__ge__(0),a)
    c = numpy.multiply(b.__le__(255),b)
    d = numpy.multiply(b.__gt__(255),255)
    return numpy.add(c,d)

def _sub(a,b):
    #Used for the blend function (mimics an unsigned subtraction with signed arrays)
    aux = a
    aux1 = numpy.multiply(aux.__ge__(b),b)
    aux2 = numpy.multiply(b.__gt__(aux),aux)
    b = numpy.add(aux1,aux2)
    return numpy.subtract(aux,b)

def blend(source, x, y, swidth, sheight, dx, dy, dwidth, dheight, mode):
    """Blends a region of pixels from one image into another."""
    if not npy: raise ImportError, "Numpy is required"
    loadPixels()
    a = screen.pixels.reshape((height,width))
    a = a[dy:dy+dheight,dx:dx+dwidth]
    a = a.reshape(a.shape[1]*a.shape[0])
    b = source.pixels.reshape((source.height,source.width))
    b = b[y:y+sheight,x:x+swidth]
    b = b.reshape(b.shape[1]*b.shape[0])
    f = numpy.right_shift(numpy.bitwise_and(b,0xff000000),24)
    a.dtype="int32"
    b.dtype="int32"
    #BLEND Mode
    if mode == 0:
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = _mix(numpy.bitwise_and(a,0xff0000),numpy.bitwise_and(b,0xff0000),f)
        red = numpy.bitwise_and(red,0xff0000)
        green = _mix(numpy.bitwise_and(a,0xff00),numpy.bitwise_and(b,0xff00),f)
        green = numpy.bitwise_and(green,0xff00)
        blue = _mix(numpy.bitwise_and(a,0xff),numpy.bitwise_and(b,0xff),f)
    #ADD Mode
    elif mode == 1:
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = numpy.bitwise_and(b,0xff0000)
        red = numpy.right_shift(numpy.multiply(red,f),8)
        red = numpy.add(red,numpy.bitwise_and(a,0xff0000))
        red = _low(red,0xff0000)
        red = numpy.bitwise_and(red,0xff0000)
        green = numpy.bitwise_and(b,0xff00)
        green = numpy.right_shift(numpy.multiply(green,f),8)
        green = numpy.add(green,numpy.bitwise_and(a,0xff00))
        green = _low(green,0xff00)
        green = numpy.bitwise_and(green,0xff00)
        blue = numpy.bitwise_and(b,0xff)
        blue = numpy.right_shift(numpy.multiply(blue,f),8)
        blue = numpy.add(blue,numpy.bitwise_and(a,0xff))
        blue = _low(blue,0xff)
    #SUBTRACT Mode
    elif mode == 2:
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = numpy.right_shift(numpy.bitwise_and(b,0xff0000),8)
        red = numpy.multiply(red,f)
        red = _sub(numpy.bitwise_and(a,0xff0000),red)
        red = numpy.bitwise_and(_high(red,0xff00),0xff0000)
        green = numpy.right_shift(numpy.bitwise_and(b,0xff00),8)
        green = numpy.multiply(green,f)
        green = _sub(numpy.bitwise_and(a,0xff00),green)
        green = numpy.bitwise_and(_high(green,0xff),0xff00)
        blue = numpy.multiply(numpy.bitwise_and(b,0xff),f)
        blue = numpy.right_shift(blue,8)
        blue = _sub(numpy.bitwise_and(a,0xff),blue)
    #DARKEST Mode
    elif mode == 3:
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = numpy.right_shift(numpy.bitwise_and(b,0xff0000),8)
        red = numpy.multiply(red,f)
        red = _low(numpy.bitwise_and(a,0xff0000),red)
        red = numpy.bitwise_and(_mix(numpy.bitwise_and(a,0xff0000),red,f),0xff0000)
        green = numpy.right_shift(numpy.bitwise_and(b,0xff00),8)
        green = numpy.multiply(green,f)
        green = _low(numpy.bitwise_and(a,0xff00),green)
        green = numpy.bitwise_and(_mix(numpy.bitwise_and(a,0xff00),green,f),0xff00)
        blue = numpy.multiply(numpy.bitwise_and(b,0xff),f)
        blue = numpy.right_shift(blue,8)
        blue = _low(numpy.bitwise_and(a,0xff),blue)
        blue = _mix(numpy.bitwise_and(a,0xff),blue,f)
    #LIGHTEST Mode
    elif mode == 4:
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = numpy.right_shift(numpy.bitwise_and(b,0xff0000),8)
        red = numpy.multiply(red,f)
        red = _high(numpy.bitwise_and(a,0xff0000),red)
        red = numpy.bitwise_and(red,0xff0000)
        green = numpy.right_shift(numpy.bitwise_and(b,0xff00),8)
        green = numpy.multiply(green,f)
        green = _high(numpy.bitwise_and(a,0xff00),green)
        green = numpy.bitwise_and(green,0xff00)
        blue = numpy.right_shift(numpy.bitwise_and(b,0xff),8)
        blue = numpy.multiply(blue,f)
        blue = _high(numpy.bitwise_and(a,0xff),blue)
    #Setup for modes 5:14
    if mode in range(5,14):
        ar = numpy.right_shift(numpy.bitwise_and(a,0xff0000),16)
        ag = numpy.right_shift(numpy.bitwise_and(a,0xff00),8)    
        ab = numpy.bitwise_and(a,0xff)        
        br = numpy.right_shift(numpy.bitwise_and(b,0xff0000),16)
        bg = numpy.right_shift(numpy.bitwise_and(b,0xff00),8)    
        bb = numpy.bitwise_and(b,0xff)
    #DIFFERENCE Mode
    if mode == 5:
        cr = numpy.absolute(numpy.subtract(ar,br))
        cg = numpy.absolute(numpy.subtract(ag,bg))
        cb = numpy.absolute(numpy.subtract(ab,bb))
    #EXCLUSION Mode
    elif mode == 6:
        cr = numpy.right_shift(numpy.multiply(ar,br),7)
        cr = _sub(numpy.add(ar,br),cr)        
        cg = numpy.right_shift(numpy.multiply(ag,bg),7)
        cg = _sub(numpy.add(ag,bg),cg)        
        cb = numpy.right_shift(numpy.multiply(ab,bb),7)
        cb = _sub(numpy.add(ab,bb),cb)
    #MULTIPLY Mode
    elif mode == 7:
        cr = numpy.right_shift(numpy.multiply(ar,br),8)  
        cg = numpy.right_shift(numpy.multiply(ag,bg),8)     
        cb = numpy.right_shift(numpy.multiply(ab,bb),8)
    #SCREEN Mode
    elif mode == 8:
        cr = numpy.subtract(255,ar) 
        cr = numpy.multiply(cr,numpy.subtract(255,br))
        cr = numpy.subtract(255,numpy.right_shift(cr,8))
        cg = numpy.subtract(255,ag) 
        cg = numpy.multiply(cr,numpy.subtract(255,bg))
        cg = numpy.subtract(255,numpy.right_shift(cg,8))
        cb = numpy.subtract(255,ab) 
        cb = numpy.multiply(cr,numpy.subtract(255,bb))
        cb = numpy.subtract(255,numpy.right_shift(cb,8))
    #OVERLAY Mode
    elif mode == 9:
        cr1 = numpy.right_shift(numpy.multiply(ar,br),7)
        cr1 = numpy.multiply(ar.__lt__(128),cr1)
        cr2 = numpy.subtract(255,ar) 
        cr2 = numpy.multiply(cr2,numpy.subtract(255,br))
        cr2 = numpy.subtract(255,numpy.right_shift(cr2,7))
        cr2 = numpy.multiply(ar.__ge__(128),cr2)
        cr = numpy.add(cr1,cr2)
        cg1 = numpy.right_shift(numpy.multiply(ag,bg),7)
        cg1 = numpy.multiply(ag.__lt__(128),cg1)
        cg2 = numpy.subtract(255,ag) 
        cg2 = numpy.multiply(cg2,numpy.subtract(255,bg))
        cg2 = numpy.subtract(255,numpy.right_shift(cg2,7))
        cg2 = numpy.multiply(ag.__ge__(128),cg2)
        cg = numpy.add(cg1,cg2)
        cb1 = numpy.right_shift(numpy.multiply(ab,bb),7)
        cb1 = numpy.multiply(ab.__lt__(128),cb1)
        cb2 = numpy.subtract(255,ab) 
        cb2 = numpy.multiply(cb2,numpy.subtract(255,bb))
        cb2 = numpy.subtract(255,numpy.right_shift(cb2,7))
        cb2 = numpy.multiply(ab.__ge__(128),cb2)
        cb = numpy.add(cb1,cb2)
    #HARD LIGHT Mode
    elif mode == 10:
        cr1 = numpy.right_shift(numpy.multiply(ar,br),7)
        cr1 = numpy.multiply(br.__lt__(128),cr1)
        cr2 = numpy.subtract(255,ar) 
        cr2 = numpy.multiply(cr2,numpy.subtract(255,br))
        cr2 = numpy.subtract(255,numpy.right_shift(cr2,7))
        cr2 = numpy.multiply(br.__ge__(128),cr2)
        cr = numpy.add(cr1,cr2)
        cg1 = numpy.right_shift(numpy.multiply(ag,bg),7)
        cg1 = numpy.multiply(bg.__lt__(128),cg1)
        cg2 = numpy.subtract(255,ag) 
        cg2 = numpy.multiply(cg2,numpy.subtract(255,bg))
        cg2 = numpy.subtract(255,numpy.right_shift(cg2,7))
        cg2 = numpy.multiply(bg.__ge__(128),cg2)
        cg = numpy.add(cg1,cg2)
        cb1 = numpy.right_shift(numpy.multiply(ab,bb),7)
        cb1 = numpy.multiply(bb.__lt__(128),cb1)
        cb2 = numpy.subtract(255,ab) 
        cb2 = numpy.multiply(cb2,numpy.subtract(255,bb))
        cb2 = numpy.subtract(255,numpy.right_shift(cb2,7))
        cb2 = numpy.multiply(bb.__ge__(128),cb2)
        cb = numpy.add(cb1,cb2)
    #SOFT LIGHT Mode
    elif mode == 11:
        cr1 = numpy.multiply(numpy.multiply(ar,ar),br)
        cr1 = numpy.right_shift(cr1,15)
        cr2 = numpy.right_shift(numpy.multiply(ar,ar),8)
        cr3 = numpy.right_shift(numpy.multiply(ar,br),7)
        cr = numpy.add(cr3,numpy.subtract(cr2,cr1))
        cg1 = numpy.multiply(numpy.multiply(ag,ag),bg)
        cg1 = numpy.right_shift(cg1,15)
        cg2 = numpy.right_shift(numpy.multiply(ag,ag),8)
        cg3 = numpy.right_shift(numpy.multiply(ag,bg),7)
        cg = numpy.add(cg3,numpy.subtract(cg2,cg1))
        cb1 = numpy.multiply(numpy.multiply(ab,ab),bb)
        cb1 = numpy.right_shift(cb1,15)
        cb2 = numpy.right_shift(numpy.multiply(ab,ab),8)
        cb3 = numpy.right_shift(numpy.multiply(ab,bb),7)
        cb = numpy.add(cb3,numpy.subtract(cb2,cb1))        
    #DODGE Mode
    elif mode == 12:
        cr1 = numpy.multiply(br.__eq__(255),255)
        cr2 = numpy.left_shift(ar,8)
        cr2 = _peg(numpy.divide(cr2,numpy.subtract(255,br)))
        cr = numpy.add(cr1,numpy.multiply(cr2,br.__ne__(255)))
        cg1 = numpy.multiply(bg.__eq__(255),255)
        cg2 = numpy.left_shift(ag,8)
        cg2 = _peg(numpy.divide(cg2,numpy.subtract(255,bg)))
        cg = numpy.add(cg1,numpy.multiply(cg2,bg.__ne__(255)))
        cb1 = numpy.multiply(bb.__eq__(255),255)
        cb2 = numpy.left_shift(ab,8)
        cb2 = _peg(numpy.divide(cb2,numpy.subtract(255,bb)))
        cb = numpy.add(cb1,numpy.multiply(cb2,bb.__ne__(255)))
    #BURN Mode
    elif mode == 13:
        cr = numpy.left_shift(numpy.subtract(255,ar),8)
        cr = numpy.subtract(255,_peg(numpy.divide(cr,br)))
        cr = numpy.multiply(cr,br.__gt__(0))
        cg = numpy.left_shift(numpy.subtract(255,ag),8)
        cg = numpy.subtract(255,_peg(numpy.divide(cg,bg)))
        cg = numpy.multiply(cg,bg.__gt__(0))
        cb = numpy.left_shift(numpy.subtract(255,ab),8)
        cb = numpy.subtract(255,_peg(numpy.divide(cb,bb)))
        cb = numpy.multiply(cb,bb.__gt__(0))
    #Final blend for modes 5:14
    if mode in range(5,14):
        alpha = numpy.right_shift(numpy.bitwise_and(a,0xff000000),24)
        alpha = numpy.left_shift(_low(numpy.add(alpha,f),0xff),24)
        red = numpy.right_shift(numpy.multiply(numpy.subtract(cr,ar),f),8)
        red = numpy.left_shift(_peg(numpy.add(ar,red)),16)
        green = numpy.right_shift(numpy.multiply(numpy.subtract(cg,ag),f),8)
        green = numpy.left_shift(_peg(numpy.add(ag,green)),8)
        blue = numpy.right_shift(numpy.multiply(numpy.subtract(cb,ab),f),8)
        blue = _peg(numpy.add(ab,blue))
    final = numpy.bitwise_or(numpy.bitwise_or(alpha,red),green)
    final = numpy.bitwise_or(final,blue)
    new = createImage(swidth,sheight,'RGBA')
    new.pixels = numpy.array(final,dtype='uint32')
    new.updatePixels()
    image(new,dx,dy)

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
    

weights = []    
    
def createKernel(sigma):
    #Creates a one dimensional gaussian kernel array of variable size
    global kernel_size, weights
    norm = 1.0/(math.sqrt(2.0*math.pi)*sigma)
    kernel_size = int(math.ceil(6*sigma-1))
    for i in range(-kernel_size/2,kernel_size/2+1):
        w = norm * math.exp(-(i*i)/(2.0*sigma*sigma))
        weights.append(w)
     
def _createKernel2d(sigma,size):
    #Creates a two dimensional gaussian kernel of determined size
    global weights
    weights = numpy.empty([size,size])
    norm = 1.0/(math.pi*2.0*sigma*sigma)
    for j in range(-size/2,size/2 + 1):
        for i in range(-size/2,size/2 + 1):
            w = norm * math.exp(-(i*i+j*j)/(2.0*sigma*sigma))
            weights[i,j] = w
    n = 1/numpy.sum(weights)
    weights = numpy.multiply(weights,n)
