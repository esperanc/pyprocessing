#************************
#  TRANSFORMATIONS STUFF 
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from math import *
import config

__all__=['pushMatrix', 'popMatrix', 'resetMatrix', 'applyMatrix', 'getMatrix',
         'printMatrix', 'getProjection', 'printProjection',
         'translate', 'rotate', 'rotateX', 'rotateY', 'rotateZ',
         'scale', 'camera', 'perspective', 'ortho',
         'screenXYZ', 'screenX', 'screenY', 'screenZ',
         'modelXYZ','modelX', 'modelY', 'modelZ', 'shearX', 'shearY']
         
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
    """Applies matrix."""
    # notice that processing uses a transposed matrix
    glMultMatrixf((ctypes.c_float * 16)(n00, n04, n08, n12,
                n01, n05, n09, n13,
                n02, n06, n10, n14,
                n03, n07, n11, n15))

def shearX(angle):
    """Shears a shape around the x-axis the amount specified by the angle
    parameter"""
    # notice that processing uses a transposed matrix
    glMultMatrixf((ctypes.c_float * 16)(1, 0, 0, 0,
                angle, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1))

def shearY(angle):
    """	Shears a shape around the y-axis the amount specified by the angle
    parameter."""
    # notice that processing uses a transposed matrix
    glMultMatrixf((ctypes.c_float * 16)(1, angle, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1))

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
        if config.halfPixelShiftHack:
            # Add a half-pixel shift in order to obtain sharper lines
            glTranslatef(0.5,0.5,0)
        gluLookAt (width/2.0, height/2.0, (height/2.0) / tan(PI*60.0 / 360.0), 
                   width/2.0, height/2.0, 0, 0, 1, 0)
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
        cameraZ = height/2.0 / math.tan(math.pi*60/360)
        gluPerspective(60, width*1.0/height, cameraZ/100.0, cameraZ*10.0)
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
    ortho(0, width, 0, height, -10, 10)."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if len(args)==0:
        left, right = 0, width
        bottom, top =  0, height
        near, far = -height*2, height*2 # a saner default than Processing's
    else:
        assert(len(args)==6)
        left, right, bottom, top, near, far = args
    # invert the y axis
    if config.coordInversionHack: bottom, top = top, bottom
    glOrtho(left, right, bottom, top, near, far)
    glMatrixMode(GL_MODELVIEW)
    
def screenXYZ (ox,oy,oz):
    """Returns the projected space coordinates of object coordinates ox,oy,oz"""
    # variables for calling gluUnProject
    viewport = (ctypes.c_int*4)()
    projmatrix = (ctypes.c_double*16)()
    mviewmatrix = (ctypes.c_double*16)()
    sx,sy,sz = (ctypes.c_double)(),(ctypes.c_double)(),(ctypes.c_double)()
    # get current transformation state
    glGetIntegerv(GL_VIEWPORT, viewport)
    glGetDoublev(GL_MODELVIEW_MATRIX, mviewmatrix)
    glGetDoublev(GL_PROJECTION_MATRIX, projmatrix)
    # call gluUnProject
    gluProject(ox,oy,oz,
               mviewmatrix,projmatrix,viewport,
               ctypes.byref(sx),ctypes.byref(sy),ctypes.byref(sz))
    if config.coordInversionHack: 
        return sx.value, height-sy.value, sz.value
    else:
        return sx.value, sy.value, sz.value
    
def screenX (ox,oy,oz):
    """Returns the x coordinate of screenXYZ(ox,oy,oz)"""
    return screenXYZ(ox,oy,oz)[0]

def screenY (ox,oy,oz):
    """Returns the y coordinate of screenXYZ(ox,oy,oz)"""
    return screenXYZ(ox,oy,oz)[1]
    
def screenZ (ox,oy,oz):
    """Returns the Z coordinate of screenXYZ(ox,oy,oz)"""
    return screenXYZ(ox,oy,oz)[2]

# As far as I can understand, modelX, modelY and modelZ are synonyms of 
# screenX, screenY and screenZ
modelX, modelY, modelZ, modelXYZ = screenX, screenY, screenZ, screenXYZ

