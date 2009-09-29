#************************
#  ATTRIBUTES
#************************          

from globs import *
from constants import *
from pyglet.gl import *
from colors import _getColor

__all__=['stroke', 'noStroke', 'strokeWeight', 'fill', 'noFill', 
         'smooth', 'noSmooth', 'ellipseMode', 'rectMode', 'hint']
         
def stroke(*color):
    """Sets color as color for drawing lines and shape borders."""
    attrib.strokeColor = _getColor(*color)

def noStroke():
    """Omits line drawings"""
    attrib.strokeColor = None
      
def strokeWeight (weight):
    """Sets line width for drawing outline objects"""
    attrib.strokeWeight = weight
    
def fill(*color):
    """Sets color as color for drawing filled shapes."""
    attrib.fillColor = _getColor(*color)

def noFill():
    """Omits filled drawings"""
    attrib.fillColor = None
    
def smooth():
    """Sets state so that lines are rendered antialiased."""
    attrib.smooth = True
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

def noSmooth():
    """Sets state so that lines are rendered quickly."""
    attrib.smooth = False
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_POINT_SMOOTH)
    glDisable(GL_POLYGON_SMOOTH)

def ellipseMode(mode):
    """Alters the meaning of the arguments of the ellipse function"""
    attrib.ellipseMode = mode
    
def rectMode(mode):
    """Alters the meaning of the arguments of the rectangle function"""
    attrib.rectMode = mode
    
def hint(hintconst):
    """Sets/unsets configuration settings. 
    * Depth testing can be set or unset using constants DISABLE_DEPTH_TEST and 
      ENABLE_DEPTH_TEST (default=ON).
    * Polygon antialiasing can be turned on or off using ENABLE_POLYGON_SMOOTH 
      and DISABLE_POLYGON_SMOOTH (default=OFF).
    * Flip policy can be selected using the constants DOUBLE_FLIP_POLICY, 
      SINGLE_FLIP_POLICY, FBO_FLIP_POLICY and ACCUM_FLIP_POLICY
    """
    if hintconst==ENABLE_DEPTH_TEST:
        attrib.depthTest = True
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
    elif hintconst==DISABLE_DEPTH_TEST:
        attrib.depthTest = False
        glDisable(GL_DEPTH_TEST)
    elif hintconst in (DOUBLE_FLIP_POLICY,SINGLE_FLIP_POLICY,
        FBO_FLIP_POLICY, ACCUM_FLIP_POLICY):
        config.flipPolicy=hintconst
    else:
        raise ValueError,"Unknown hint"

