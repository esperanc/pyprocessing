#************************
#  TRANSFORMATIONS STUFF 
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from math import *

__all__=['pushMatrix', 'popMatrix', 'applyMatrix', 'getMatrix',
         'printMatrix', 'getProjection', 'printProjection',
         'translate', 'rotate', 'rotateX', 'rotateY', 'rotateZ',
         'scale', 'camera', 'perspective', 'ortho']
         
def pushMatrix(): 
    """Saves current transformation"""
    glPushMatrix()
    
def popMatrix():
    """Restores previous transformation"""
    glPopMatrix()
    
def resetMatrix():
    """Loads an identity matrix"""
    glLoadIdentity()
    
def applyMatrix(n00, n01, n02, n03,
                n04, n05, n06, n07,
                n08, n09, n10, n11,
                n12, n13, n14, n15):
    """Loads an identity matrix"""
    # notice that processing uses a transposed matrix
    glMultMatrixf((ctypes.c_float * 16)(n00, n04, n08, n12,
                n01, n05, n09, n13,
                n02, n06, n10, n14,
                n03, n07, n11, n15))

def getMatrix():
    """Returns the MODELVIEW matrix as a tuple."""
    matrix = (ctypes.c_double*16)()
    glGetDoublev (GL_MODELVIEW_MATRIX, matrix)
    return tuple([matrix [i] for i in range(16)])

def getProjection():
    """Returns the PROJECTION matrix as a tuple."""
    matrix = (ctypes.c_double*16)()
    glGetDoublev (GL_PROJECTION_MATRIX, matrix)
    return tuple([matrix [i] for i in range(16)])
    
def printMatrix():
    """Prints the MODELVIEW matrix."""
    print getMatrix()

def printProjection():
    """Prints the PROJECTION matrix."""
    print getProjection()

def translate(x,y,z=0):
    """Translation transformation"""
    glTranslatef(x,y,z)

def rotate(*args):
    """Rotation transformation. Angles in radians"""
    if len(args) == 1: glRotatef(math.degrees(args[0]), 0,0,1)
    else: glRotatef(math.degrees(args[0]),args[1],args[2],args[3])

rotateZ = rotate

def rotateX(angle):
    """Rotation around the X axis"""
    rotate (angle, 1, 0, 0)

def rotateY(angle):
    """Rotation around the Y axis"""
    rotate (angle, 0, 1, 0)
    
def scale(*args):
    """Scale transformation"""
    if len(args) == 1: glScalef(args[0],args[0],args[0])
    elif len(args)==2: glScalef(args[0],args[1],1)
    else: glScalef(*args)

def camera (*args):
    """Args should either be empty or be of the form 
    (eyex,eyey,eyez,centerx, centery, centerz, upx, upy, upz).
    Creates a viewing transformation given the camera position
    (eyex,eyey,eyez), the center of the scene (centerx, centery, centerz) and
    a vector to be used as the up direction (upx, upy, upz). If no args
    are passed, the standard camera is created."""
    glLoadIdentity()
    if len(args)==0:
        # default camera
        gluLookAt (screen.width/2.0, screen.height/2.0, (screen.height/2.0) / tan(PI*60.0 / 360.0), 
                   screen.width/2.0, screen.height/2.0, 0, 0, 1, 0)
    else:
        assert (len(args)==9)
        gluLookAt (*args)

def perspective(*args):
    """Args should either be empty or be of the form 
    (fov,aspect,znear,zfar). Loads a perspective projection matrix, where
    fov is the field-of-view angle (in radians) for vertical direction, aspect
    is the ratio of width to height, znear is the z-position of nearest clipping 
    plane and zfar is the z-position of nearest farthest plane. If no args are
    passed, the standard projection is created, i.e, equivalent to 
    perspective(PI/3.0, width/height, cameraZ/10.0, cameraZ*10.0)
    where cameraZ is ((height/2.0) / tan(PI*60.0/360.0))."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if len(args)==0:
        cameraZ = screen.height/2.0 / math.tan(math.pi*60/360)
        gluPerspective(60, screen.width*1.0/screen.height, cameraZ/100.0, cameraZ*10.0)
    else:
        assert(len(args)==4)
        fov,aspect,znear,zfar = args
        gluPerspective(degrees(fov),aspect,znear,zfar)
    # invert the y axis
    if config.coordInversionHack: glScalef(1,-1,1)
    glMatrixMode(GL_MODELVIEW)

def ortho(*args):
    """Args should either be empty or be of the form 
    (left, right, bottom, top, near, far). Loads an orthogonal projection matrix.
    The clipping volume in this case is an axes-aligned parallelepiped, where 
    left and right are the minimum and maximum x values, top and bottom are 
    the minimum and maximum y values, and near and far are the minimum and 
    maximum z values. If no parameters are given, the default is used: 
    ortho(0, screen.width, 0, screen.height, -10, 10)."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if len(args)==0:
        left, right = 0, screen.width
        bottom, top =  0, screen.height
        near, far = -screen.height*2, screen.height*2 # a saner default than processing's
    else:
        assert(len(args)==6)
        left, right, bottom, top, near, far = args
    # invert the y axis
    if config.coordInversionHack: bottom, top = top, bottom
    glOrtho(left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW)    
