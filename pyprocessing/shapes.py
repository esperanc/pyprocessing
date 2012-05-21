#coding: utf-8

#************************
#  SHAPE STUFF 
#************************

import ctypes
from pyglet.gl import *
from globs import *
from constants import *
from pvector import *
from primitives import _smoothFixHackBegin,_smoothFixHackEnd
from math import *

__all__=['beginShape', 'vertex', 'normal', 'bezierVertex', 'endShape',
         'bezierDetail', 'bezierPoint', 'bezierTangent', 'bezierSample',
         'bezier', 'curveTightness', 'curve', 'curveVertex', 'curvePoint', 'curveDetail',
         'curveTangent','sphereDetail']
         
def beginShape(type=None):
    """Begins the drawing of a shape."""
    shape.type = type
    shape.vtx = []  # vertices drawn with vertex or sampled by curveVertex
    shape.bez = []  # bezier vertices drawn with bezierVertex
    shape.crv = []  # contents of the last three curveVertex calls
    shape.nrm = []  # pairs (vtxindex,normal) 

def vertex(x,y,z=0.0,u=0.0,v=0.0):
    """Adds a new vertex to the shape"""
    if attrib.texture: shape.vtx += [(x,y,z,u,v)]
    else: shape.vtx += [(x,y,z)]

def normal(x,y,z):
    """Sets the next vertex's normal"""
    shape.nrm += [(len(shape.vtx),(x,y,z))]
    
def bezierVertex(*coords):
    """Generates a cubic bezier arc. Arguments are of the form
    (cx1, cy1, cx2, cy2, x, y) or
    (cx1, cy1, cz1, cx2, cy2, cz2, x, y, z), i.e. coordinates
    for 3 control points in 2D or 3D. The first control point of the
    arc is the last point of the previous arc or the last vertex.
    """
    assert (len(coords) in (6,9))
    assert (len(shape.vtx)>0)
    # remember the index where the bezier control points will be stored
    shape.bez.append(len(shape.vtx)) 
    if len(coords) == 6:
        shape.vtx += [coords[:2]+(0,),coords[2:4]+(0,),coords[4:6]+(0,)]
    else:
        shape.vtx += [coords[:3],coords[3:6],coords[6:9]]

def endShape(close=False):
    """Does the actual drawing of the shape."""
    
    def computeNormal(p0,p1,p2):
        """Computes a normal for triangle p0-p1-p2."""
        return (PVector(p1)-PVector(p0)).cross(PVector(p2)-PVector(p1))
        
    if attrib.texture:
        glEnable(GL_TEXTURE_2D)
        if type(attrib.texture) == str:
            image = pyglet.image.load(attrib.texture)
            texture = image.get_texture()
        else:
            texture = attrib.texture.img.get_texture()
        t = texture.tex_coords
        glBindTexture(GL_TEXTURE_2D,texture.id)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glMatrixMode(GL_TEXTURE);
        glLoadIdentity();
        glTranslatef(0.0,t[7],0.0);
        glMatrixMode(GL_MODELVIEW);
        if attrib.textureMode == IMAGE:
            normx = image.width
            normy = image.height
        elif attrib.textureMode == NORMALIZED:
            normx = normy = 1.0
        if shape.type: glBegin(shape.type)
        else: glBegin(GL_POLYGON)
        for v in shape.vtx:
            glTexCoord2f(v[3]*t[6]/normx,-v[4]*t[7]/normy)
            glVertex3f(*v[:3])
        glEnd()
        attrib.texture = None
    # Draw the interior of the shape    
    elif attrib.fillColor != None:
        glColor4f(*attrib.fillColor)
        # establish an initial normal vector
        if shape.nrm != []:
            inormal, normal = shape.nrm[0]
        else:
            inormal = len(shape.vtx)
            if len(shape.vtx)>=3:
                normal = computeNormal(shape.vtx[0],shape.vtx[1],shape.vtx[2])
            else:
                normal = [0,0,1]
        glNormal3f(*normal)
        # Draw filled shape
        if shape.type==None:
            _smoothFixHackBegin()
            # first create a tesselator object if none was defined yet
            if shape.tess == None: shape.tess = gl.gluNewTess()
            # set up the tesselator callbacks
            gluTessCallback(shape.tess, GLU_TESS_VERTEX, ctypes.cast(glVertex3dv,ctypes.CFUNCTYPE(None)))
            gluTessCallback(shape.tess, GLU_TESS_BEGIN, ctypes.cast(glBegin,ctypes.CFUNCTYPE(None)))
            gluTessCallback(shape.tess, GLU_TESS_END, ctypes.cast(glEnd,ctypes.CFUNCTYPE(None)))
            gluTessBeginPolygon(shape.tess, None)
            gluTessBeginContour(shape.tess)
            i = 0
            n = len(shape.vtx)
            shape.bez += [n]
            b = 0
            a = []
            while i<n:
                if i == shape.bez[b]:
                    for v in bezierSample (shape.vtx[i-1],shape.vtx[i],
                                          shape.vtx[i+1],shape.vtx[i+2]):
                        a += [(ctypes.c_double * 3)(*v)]
                        gluTessVertex(shape.tess, a[-1], a[-1])
                    b += 1
                    i += 3
                else:
                    v = shape.vtx[i]
                    a += [(ctypes.c_double * 3)(*v)]
                    i += 1
                    gluTessVertex(shape.tess, a[-1], a[-1])
            gluTessEndContour (shape.tess)
            gluTessEndPolygon (shape.tess)
            _smoothFixHackEnd()
        else:
            if shape.nrm != []:
                # User supplied normals
                inrm = 0
                inormal,normal = shape.nrm[0]
                glBegin(shape.type)
                glNormal3f(*normal)
                for i,v in enumerate(shape.vtx):
                    if i==inormal: 
                        # load the next normal before proceeding
                        glNormal3f(*normal)
                        inrm+=1
                        if inrm<len(shape.nrm):
                            inormal, normal = shape.nrm[inrm]
                    glVertex3f(*v)
                glEnd()
            else:
                # No normals were specified. Must compute normals on the fly
                glBegin(shape.type)
                for i,v in enumerate(shape.vtx):
                    if i+2 < len(shape.vtx):
                        if shape.type==QUADS and i%4==0 or \
                           shape.type==QUAD_STRIP and i%2==0 or \
                           shape.type==TRIANGLES and i%3==0 or \
                           shape.type==TRIANGLE_FAN and i>1 or \
                           shape.type==TRIANGLE_STRIP and i>1:
                            normal = computeNormal(shape.vtx[i],shape.vtx[i+1],shape.vtx[i+2])
                            glNormal3f (*normal)
                    glVertex3f(*v)
                glEnd()
                
                
                
    # Draw the outline of the shape
    if attrib.strokeColor != None:
        glColor4f(*attrib.strokeColor)
        glPushAttrib(GL_POLYGON_BIT)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glLineWidth (attrib.strokeWeight)
        if shape.type==None:
            if close: glBegin(GL_LINE_LOOP)
            else: glBegin(GL_LINE_STRIP)
            i = 0
            n = len(shape.vtx)
            shape.bez += [n]
            nextbez = shape.bez.pop(0)
            while i<n:
                if i == nextbez:
                    for v in bezierSample (shape.vtx[i-1],shape.vtx[i],
                                          shape.vtx[i+1],shape.vtx[i+2]):
                        glVertex3f(*v)
                    nextbez = shape.bez.pop(0)
                    i += 3
                else:
                    v = shape.vtx[i]
                    i += 1
                    glVertex3f(*v)
            glEnd()
        else:
            glBegin(shape.type)
            for v in shape.vtx: glVertex3f(*v)        
            glEnd()
        glPopAttrib()

def bezierDetail(n=shape.bezierDetail):
    """Establishes the Bézier level of detail, i.e., the number of points
    per Bézier curve segment."""
    shape.bezierDetail = n
    # precompute blending factors
    shape.bezierBlend = []
    for i in range(n+1):
        t = float(i)/n
        u = 1 - t
        shape.bezierBlend.append((u*u*u,3*u*u*t,3*t*t*u,t*t*t))

def bezierPoint (a,b,c,d,t):
    """Given the x or y coordinate of Bézier control points a,b,c,d and
    the value of the t parameter, return the corresponding
    coordinate of the point."""
    u = 1.0 - t
    return a*u*u*u + b*3*u*u*t + c*3*t*t*u + d*t*t*t

def bezierTangent (a,b,c,d,t):
    """Given the x or y coordinate of Bézier control points a,b,c,d and
    the value of the t parameter, return the corresponding
    coordinate of the tangent at that point."""
    u = 1.0 - t
    return -a*3*u*u + b*(9*u*u-6*u) + c*(6*t-9*t*t) + d*3*t*t
    
def bezierSample(*p):
    """Returns a list of points for cubic bezier arc defined by the given
    control points. The number of points is given by shape.bezierDetail."""
    assert (len (p) == 4)
    result = []
    for b in shape.bezierBlend:
        x,y,z = 0,0,0
        for pi,bi in zip(p,b):
           x += pi[0]*bi
           y += pi[1]*bi
           z += pi[2]*bi
        result.append((x,y,z))
    return result

def bezier(*coords):
    """Draws a cubic Bézier curve for the 4 control points."""
    assert (len (coords) in (8,12))
    if len(coords) == 8:
        ctrlpoints = coords[:2]+(0,)+coords[2:4]+(0,)+coords[4:6]+(0,)+coords[6:]+(0,)
    beginShape()
    vertex (*ctrlpoints[0:3])
    bezierVertex(*ctrlpoints[3:])
    endShape()

class CatmullRomBlend:
    """Cubic Catmull Rom Blending"""
  
    def __init__ (self, tension = 0.5):
        self.tau = tension
        
    def blendFactors (self, u):
        """Given a value for u, returns the blending factors for each
        of the 4 control points."""
        u2 = u*u
        u3 = u2*u
        return [
             -self.tau * u + 2 * self.tau * u2 - self.tau * u3,
             1 + (self.tau-3) * u2 + (2 - self.tau) * u3,
             self.tau * u + (3 - 2*self.tau) * u2 + (self.tau - 2) * u3,
             -self.tau * u2 + self.tau * u3]

    def tangentBlendFactors (self, u):
        """Given a value for u, returns the tangent blending factors for each
        of the 4 control points."""
        u2 = u*u
        return [
             -self.tau + 4 * self.tau * u - 3 * self.tau * u2,
             (2*self.tau-6) * u + (6 - 3*self.tau) * u2,
             self.tau + (6 - 4*self.tau) * u + (3*self.tau - 6) * u2,
             -2*self.tau * u + 3*self.tau * u2]
    
  
    def blendPoint (self, u, p0, p1, p2, p3):
        """Returns the point obtained by blending pi with factor u."""
        result = [0,0,0]
        for b,p in zip (self.blendFactors(u),(p0,p1,p2,p3)):
            for i,x in enumerate(p):
                result[i] += p[i]*b
        return result
        
    def blendTangent(self, u, p0, p1, p2, p3):
        """Returns the curve tangent at the point obtained by blending pi with factor u."""
        result = [0,0,0]
        for b,p in zip (self.tangentBlendFactors(u),(p0,p1,p2,p3)):
            for i,x in enumerate(p):
                result[i] += p[i]*b
        return result
    
def curveTightness (squishy):
    """Uses 'squishy' as the tension factor for the catmull-rom spline."""
    shape.tension = (1-squishy)/2.0
    
def curveVertex(x,y,z=0):
    """Generates a cubic Catmull-Rom curve corresponding to interpolating
    the three last points issued with earlier calls to curveVertex and this one.
    """
    shape.crv.append((x,y,z))
    if len(shape.crv)>4: shape.crv = shape.crv[-4:]
    if len(shape.crv)==4:
        blend = CatmullRomBlend(shape.tension)
        npts = shape.curveDetail
        for i in range(npts+1):
            p = blend.blendPoint(float(i)/npts, *shape.crv)
            vertex(*p)
            
def curve (*coords):
    """Generates a catmull-rom curve given 4 points. Takes either 8 numbers 
    for coordinates of 4 points in 2D or 12 numbers for 4 points in 3D"""
    if len(coords)==8:
        p0,p1,p2,p3 = coords[0:2],coords[2:4],coords[4:6],coords[6:8]
    else:
        assert (len(coords)==12)
        p0,p1,p2,p3 = coords[0:3],coords[3:6],coords[6:9],coords[9:12]
    blend = CatmullRomBlend(shape.tension)
    beginShape()
    npts = shape.curveDetail
    for i in range(npts+1):
        p = blend.blendPoint(float(i)/npts, p0,p1,p2,p3)
        vertex(*p)
    endShape()

def curvePoint (a,b,c,d,t):
    """Evaluates the n'th coordinate of a cubic Catmull-Rom curve at parameter
    t for control points having their n'th coordinate equal to a, b, c and d, respectively.
    """
    blend = CatmullRomBlend(shape.tension)
    return blend.blendPoint(t,(a,),(b,),(c,),(d,)) [0]

def curveTangent (a,b,c,d,t):
    """Evaluates the n'th coordinate of the tangent at the point on a cubic Catmull-Rom 
    curve at parameter t for control points having their n'th coordinate equal to 
    a, b, c and d, respectively.
    """
    blend = CatmullRomBlend(shape.tension)
    return blend.blendTangent(t,(a,),(b,),(c,),(d,)) [0]
    
def curveDetail(npts=shape.curveDetail):
    """Controls the number of samples per curve arc."""
    shape.curveDetail = npts

def sphereDetail(*args):
    """Controls the how many segments are used per circle revolution while drawing a
    sphere. The first and second parameters determine the number of segments used    
    longitudinally and latitudinally, respectively. If only one parameter is used, it
    determines the total number of segments used per full circle revolution."""
    if len(args)==1:
        shape.sphereDetail = (args[0], args[0])
    elif len(args)==2:
        shape.sphereDetail = (args[0], args[1])
