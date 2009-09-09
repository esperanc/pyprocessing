#************************
#  MATERIAL PROPERTIES
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from colors import _getColor

__all__=['emissive', 'shininess', 'specular', 'ambient']

def emissive(*args):
    """Emission material Properties"""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_EMISSION, (ctypes.c_float * 4)(*color)) 
        
def shininess(shine):
    """Specular reflection material properties."""
    glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, shine)
    
def specular(*args):
    """Specular reflection material properties."""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_SPECULAR, (ctypes.c_float * 4)(*color))
    
def ambient(*args):
    """Ambient reflection material properties."""
    color = _getColor(*args)
    glMaterialfv (GL_FRONT_AND_BACK, GL_AMBIENT, (ctypes.c_float * 4)(*color))    

