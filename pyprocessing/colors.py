#************************
#  COLORS
#************************

from globs import *
from constants import *

__all__=['_getColor','color','red','green','blue','alpha','hue','saturation','brightness',
         'lerpColor', 'colorMode', 'blendColor'] 

def hsb_to_rgb (h,s,v,a):
    """Simple hsv to rgb conversion. Assumes components specified in range 0.0-1.0."""
    tmp = h*5.9999
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
    """Simple rgb to hsb conversion. Assumes components specified in range 0.0-1.0."""
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
        # one value: This is tricky, because it could either convey a 
        # gray code or an argb color.  Processing has the same problem, and we
        # adopt the same solution, i.e., an integer with any high 8 bits set or
        # bigger than the allowed range for the first coordinate is viewed
        # as an argb color. Otherwise, it is regarded as a gray code
        n = color[0]
        if not isinstance(n,float) and (n & 0xff000000 != 0 or n>attrib.colorRange[0]):
            # argb color: just convert to tuple format and return
            color = ((n&0xff0000)>>16)/255.0, ((n&0xff00)>>8)/255.0, \
                    (n&0xff)/255.0, ((n&0xff000000)>>24)/255.0
            return color
        else:
            # a gray value. 
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

def color(*args):
    """This returns a color encoded as an unsigned int."""
    r,g,b,a = _getColor(*args)
    return int(a*255)<<24 | int(r*255)<<16 | int(g*255)<<8 | int(b*255)
    
def red(color):
    """Red component of the color."""
    color = _getColor(color)
    return color[0]*attrib.colorRange[0]

def green(color):
    """Green component of the color."""
    color = _getColor(color)
    return color[1]*attrib.colorRange[1]
    
def blue(color):
    """Blue component of the color."""
    color = _getColor(color)
    return color[2]*attrib.colorRange[2]

def alpha(color):
    """Alpha component of the color."""
    color = _getColor(color)
    return color[3]*attrib.colorRange[3]

def hue(color):
    """Hue component of the color."""
    color = _getColor(color)
    color = rgb_to_hsb(*color)
    return color[0]*attrib.colorRange[0]

def saturation(color):
    """Saturation component of the color."""
    color = _getColor(color)
    color = rgb_to_hsb(*color)
    return color[1]*attrib.colorRange[1]

def brightness(color):
    """Brightness component of the color."""
    color = _getColor(color)
    color = rgb_to_hsb(*color)
    return color[2]*attrib.colorRange[2]

def lerpColor(c1,c2,amt):
    """Returns the linear interpolation between two colors c1 and c2.
    amt is a value between 0.0 and 1.0."""
    c1 = _getColor(c1)
    c2 = _getColor(c2)
    amtb = 1.0 - amt
    r,g,b,a = ([amtb*x+amt*y for x,y in zip(c1,c2)])
    return int(a*255)<<24 | int(r*255)<<16 | int(g*255)<<8 | int(b*255)
    
def colorMode(mode,*args):
    """Sets the color system used for specifying colors and the 
    component ranges"""
    attrib.colorMode = mode
    if len(args)==0:
        pass
    elif len(args)==1:
        attrib.colorRange = args*4
    elif len(args)==3:
        attrib.colorRange = (args[0],args[1],args[2],attrib.colorRange[3])
    else:
        assert(len(args)==4)
        attrib.colorRange = args

# These are helper routines (grabbed from Processing's Pimage.java source)
# They are used to define the various blending mode functions. They
# assume 8-bit integer color coordinates

def low(a, b): return min(a,b)

def high(a, b): return max(a,b)

def peg(a): return min(255,max(a,0))

def mix(a, b, f): return a + (((b - a) * f) >> 8);

# bitwise masks

ALPHA_MASK = 0xff000000
RED_MASK = 0xff0000
GREEN_MASK = 0xff00
BLUE_MASK = 0xff

# conversion from/to int/tuple

def tuplecolor(i): 
    return ((i & RED_MASK)>>16)/255.0,((i & GREEN_MASK)>>8)/255.0,\
           (i & BLUE_MASK)/255.0,((i & ALPHA_MASK)>>24)/255.0

def intcolor(r,g,b,a):
    return int(a*255)<<24 | int(r*255)<<16 | int(g*255)<<8 | int(b*255)
    
# blend functions

def blend_blend(a, b):
    """Combines a and b proportionally to b's alpha"""
    f = (b & ALPHA_MASK) >> 24;

    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            mix(a & RED_MASK, b & RED_MASK, f) & RED_MASK |
            mix(a & GREEN_MASK, b & GREEN_MASK, f) & GREEN_MASK |
            mix(a & BLUE_MASK, b & BLUE_MASK, f));

def blend_add_pin(a, b):
    """Adds b to a proportionally to b's alpha"""
    f = (b & ALPHA_MASK) >> 24;

    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            low(((a & RED_MASK) +
                 ((b & RED_MASK) >> 8) * f), RED_MASK) & RED_MASK |
            low(((a & GREEN_MASK) +
                 ((b & GREEN_MASK) >> 8) * f), GREEN_MASK) & GREEN_MASK |
            low((a & BLUE_MASK) +
                (((b & BLUE_MASK) * f) >> 8), BLUE_MASK))

def blend_sub_pin(a, b):
    """ Subtractive blend with clipping"""
    f = (b & ALPHA_MASK) >> 24;

    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            high(((a & RED_MASK) - ((b & RED_MASK) >> 8) * f),
                 GREEN_MASK) & RED_MASK |
            high(((a & GREEN_MASK) - ((b & GREEN_MASK) >> 8) * f),
                 BLUE_MASK) & GREEN_MASK |
            high((a & BLUE_MASK) - (((b & BLUE_MASK) * f) >> 8), 0))

def blend_lightest(a, b):
    """Only returns the blended lightest colour """
    f = (b & ALPHA_MASK) >> 24;
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            high(a & RED_MASK, ((b & RED_MASK) >> 8) * f) & RED_MASK |
            high(a & GREEN_MASK, ((b & GREEN_MASK) >> 8) * f) & GREEN_MASK |
            high(a & BLUE_MASK, ((b & BLUE_MASK) * f) >> 8));

def blend_darkest(a, b):
    """Only returns the blended darkest colour """
    f = (b & ALPHA_MASK) >> 24;
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            mix(a & RED_MASK,
                low(a & RED_MASK,
                    ((b & RED_MASK) >> 8) * f), f) & RED_MASK |
            mix(a & GREEN_MASK,
                low(a & GREEN_MASK,
                    ((b & GREEN_MASK) >> 8) * f), f) & GREEN_MASK |
            mix(a & BLUE_MASK,
                low(a & BLUE_MASK,
                    ((b & BLUE_MASK) * f) >> 8), f));
            
def blend_difference(a, b):
    """ returns the absolute value of the difference of the input colors
    C = |A - B|"""
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    cr = abs(ar-br)
    cg = abs(ag-bg)
    cb = abs(ab-bb)
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_exclusion(a, b):
    """ Cousin of difference, algorithm used here is based on a Lingo version
    found here: http://www.mediamacros.com/item/item-1006687616/
    (Not yet verified to be correct)."""
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    cr = ar + br - ((ar * br) >> 7);
    cg = ag + bg - ((ag * bg) >> 7);
    cb = ab + bb - ((ab * bb) >> 7);
    
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_multiply(a, b):
    """Returns the product of the input colors
    C = A * B """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    cr = (ar * br) >> 8;
    cg = (ag * bg) >> 8;
    cb = (ab * bb) >> 8;
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_screen(a, b):
    """Returns the inverse of the product of the inverses of the input colors
    (the inverse of multiply).  C = 1 - (1-A) * (1-B) """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    cr = 255 - (((255 - ar) * (255 - br)) >> 8);
    cg = 255 - (((255 - ag) * (255 - bg)) >> 8);
    cb = 255 - (((255 - ab) * (255 - bb)) >> 8);
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_overlay(a, b):
    """Returns either multiply or screen for darker or lighter values of A
    (the inverse of hard light)
    C =
       A < 0.5 : 2 * A * B
       A >=0.5 : 1 - (2 * (255-A) * (255-B))
    """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    if (ar < 128): cr=((ar*br)>>7) 
    else: cr = (255-(((255-ar)*(255-br))>>7))
    if (ag < 128): cg=((ag*bg)>>7)
    else: cg = (255-(((255-ag)*(255-bg))>>7))
    if (ab < 128): cb=((ab*bb)>>7)
    else: cb = (255-(((255-ab)*(255-bb))>>7))
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_hard_light(a, b):
    """Returns either multiply or screen for darker or lighter values of B
     (the inverse of overlay)
     C =
       B < 0.5 : 2 * A * B
       B >=0.5 : 1 - (2 * (255-A) * (255-B))
    """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    if (br < 128): cr=((ar*br)>>7) 
    else: cr = (255-(((255-ar)*(255-br))>>7))
    if (bg < 128): cg=((ag*bg)>>7)
    else: cg = (255-(((255-ag)*(255-bg))>>7))
    if (bb < 128): cb=((ab*bb)>>7)
    else: cb = (255-(((255-ab)*(255-bb))>>7))
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );


def blend_soft_light(a, b):
    """Returns the inverse multiply plus screen, which simplifies to
    C = 2AB + A^2 - 2A^2B
    """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    cr = ((ar*br)>>7) + ((ar*ar)>>8) - ((ar*ar*br)>>15);
    cg = ((ag*bg)>>7) + ((ag*ag)>>8) - ((ag*ag*bg)>>15);
    cb = ((ab*bb)>>7) + ((ab*ab)>>8) - ((ab*ab*bb)>>15);
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );


def blend_dodge(a, b):
    """Returns the first (underlay) color divided by the inverse of
    the second (overlay) color. C = A / (255-B)
    """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    if (br==255): cr = 255
    else: cr= peg((ar << 8) / (255 - br))
    if (bg==255): cg =255
    else: cg= peg((ag << 8) / (255 - bg))
    if (bb==255): cb = 255 
    else: cb = peg((ab << 8) / (255 - bb))
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

def blend_burn(a, b):
    """Returns the inverse of the inverse of the first (underlay) color
    divided by the second (overlay) color. C = 255 - (255-A) / B
    """
    # setup (this portion will always be the same)
    f = (b & ALPHA_MASK) >> 24;
    ar = (a & RED_MASK) >> 16;
    ag = (a & GREEN_MASK) >> 8;
    ab = (a & BLUE_MASK);
    br = (b & RED_MASK) >> 16;
    bg = (b & GREEN_MASK) >> 8;
    bb = (b & BLUE_MASK);
    # formula:
    if (br==0): cr = 0
    else: cr= 255 - peg(((255 - ar) << 8) / br);
    if (bg==0): cg = 0
    else: cg= 255 - peg(((255 - ag) << 8) / bg);
    if (bb==0): cb = 0 
    else: cb = 255 - peg(((255 - ab) << 8) / bb);
    # alpha blend (this portion will always be the same)
    return (low(((a & ALPHA_MASK) >> 24) + f, 0xff) << 24 |
            (peg(ar + (((cr - ar) * f) >> 8)) << 16) |
            (peg(ag + (((cg - ag) * f) >> 8)) << 8) |
            (peg(ab + (((cb - ab) * f) >> 8)) ) );

# This array maps the blending modes to the proper color blending functions
blendfunc = [blend_blend, blend_add_pin, blend_sub_pin, blend_darkest, blend_lightest,
             blend_difference, blend_exclusion, blend_multiply, blend_screen, blend_overlay, 
             blend_hard_light, blend_soft_light, blend_dodge, blend_burn]

def blendColor(c1, c2, MODE):
    """Implements the blending of two colors. MODE is one of the blend mode
    constants defined in pyprocessing (an integer between 0 and 13). This expects
    colors expressed as integers."""
    return blendfunc[MODE](c1,c2)


