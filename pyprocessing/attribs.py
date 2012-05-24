#************************
#  ATTRIBUTES
#************************          

from globs import *
from constants import *
from pyglet.gl import *
from colors import _getColor
import config

__all__=['stroke', 'noStroke', 'strokeWeight', 'fill', 'noFill', 'tint', 'noTint',
         'smooth', 'noSmooth', 'ellipseMode', 'rectMode', 'imageMode', 'hint',
         'texture', 'textureMode', 'strokeJoin', 'strokeCap']
         
def stroke(*color):
    """Sets color as color for drawing lines and shape borders."""
    attrib.strokeColor = _getColor(*color)

def noStroke():
    """Omits line drawings"""
    attrib.strokeColor = None
      
def strokeWeight (weight):
    """Sets line width for drawing outline objects"""
    if weight<=0: weight=0.001
    attrib.strokeWeight = weight

def strokeCap(mode):
    attrib.strokeCap = mode

def strokeJoin(mode):
    attrib.strokeJoin = mode
    
def fill(*color):
    """Sets color as color for drawing filled shapes."""
    attrib.fillColor = _getColor(*color)

def tint(*color):
    """Sets color as a tint for drawing images."""
    attrib.tintColor = _getColor(*color)
    
def noTint():
    """Undefines tint for drawing images."""
    attrib.tintColor = None

def noFill():
    """Omits filled drawings"""
    attrib.fillColor = None

def texture(filename):
    attrib.texture = filename
    
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

def textureMode(mode):
    """Alters the meaning of the arguments of the ellipse function"""
    attrib.textureMode = mode

def ellipseMode(mode):
    """Alters the meaning of the arguments of the ellipse function"""
    attrib.ellipseMode = mode
    
def rectMode(mode):
    """Alters the meaning of the arguments of the rectangle function"""
    attrib.rectMode = mode
    
def imageMode(mode):
    """Alters the meaning of the arguments of the image function"""
    attrib.imageMode = mode
    
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
        FBO_FLIP_POLICY, ACCUM_FLIP_POLICY,BACKUP_FLIP_POLICY):
        config.flipPolicy=hintconst
    else:
        raise ValueError,"Unknown hint"

