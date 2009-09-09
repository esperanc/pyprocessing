#************************
# Lights
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from colors import _getColor

__all__=['directionalLight', 'pointLight', 'ambientLight', 'spotLight',
         'lightFalloff', 'lightSpecular', 'lights', 'noLights']

def _lightsOn():
    """Turns on the lighting if not set earlier."""
    if attrib.lights: return
    glEnable(GL_LIGHTING)
    attrib.lights = True
    for i in range(attrib.lightCount): glDisable (GL_LIGHT0+i)
    attrib.lightCount = 0

def directionalLight(v1,v2,v3,nx,ny,nz):
    """Adds a directional light (diffuse/specular) with the given color and direction."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 4)(*attrib.lightSpecular))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(-nx,-ny,-nz,0))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(0,0,-1))
    glLightf(n, GL_SPOT_EXPONENT, 0)
    glLightf(n, GL_SPOT_CUTOFF, 180)
    constant, linear, quadratic = 1, 0, 0
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def pointLight(v1,v2,v3,x,y,z):
    """Adds a point light (diffuse/specular) with the given color and position."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 4)(*attrib.lightSpecular))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,1))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(0,0,-1))
    glLightf(n, GL_SPOT_EXPONENT, 0)
    glLightf(n, GL_SPOT_CUTOFF, 180)
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def ambientLight(v1,v2,v3,x=0,y=0,z=0):
    """Adds an ambient light."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,0))
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)

def spotLight(v1, v2, v3, x, y, z, nx, ny, nz, angle, concentration):
    """Adds a spot light source."""
    _lightsOn()
    color = _getColor(v1,v2,v3)
    n = GL_LIGHT0 + attrib.lightCount
    attrib.lightCount += 1
    glLightfv(n, GL_DIFFUSE, (ctypes.c_float * 4)(*color))
    glLightfv(n, GL_AMBIENT, (ctypes.c_float * 3)(0,0,0))  
    glLightfv(n, GL_SPECULAR, (ctypes.c_float * 3)(0,0,0))
    glLightfv(n, GL_POSITION, (ctypes.c_float * 4)(x,y,z,1))
    glLightfv(n, GL_SPOT_DIRECTION, (ctypes.c_float * 3)(nx,ny,nz))
    glLightf(n, GL_SPOT_EXPONENT, concentration)
    glLightf(n, GL_SPOT_CUTOFF, math.degrees(angle))
    constant, linear, quadratic = attrib.lightFalloff
    glLightf(n, GL_LINEAR_ATTENUATION, linear)
    glLightf(n, GL_QUADRATIC_ATTENUATION, quadratic)
    glLightf(n, GL_CONSTANT_ATTENUATION, constant)
    glEnable(n)


def lightSpecular (v1,v2,v3):
    """Sets the specular coefficients for light sources defined afterwards."""
    attrib.lightSpecular = _getColor(v1,v2,v3)

def lightFalloff(constant, linear, quadratic):
    """Sets the attenuation coefficients for light sources defined afterwards."""
    attrib.lightFalloff = (constant, linear, quadratic)
    
def lights():
    """Turns on the illumination model."""
    _lightsOn()
    lightSpecular(0,0,0)
    directionalLight(128, 128, 128, 0, 0, -1)
    ambientLight(128, 128, 128)
    
def noLights():
    """Turns off the illumination model."""
    glDisable(GL_LIGHTING)
    for i in range(attrib.lightCount): glDisable (GL_LIGHT0+i)
    attrib.lights = False
    attrib.lightCount = 0
    attrib.lightFalloff = (1,0,0)
    attrib.lightSpecular = (0,0,0,1)

