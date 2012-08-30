from math import sqrt
import types

__all__ = ['PVector']


class PVectorMeta(type):
    """PVector's metaclass, used to enable class calls."""
    def add(cls, v1, v2):
        return v1 + v2
    def sub(cls, v1, v2):
        return v1 - v2
    def mult(cls, v1, v2):
        return v1 * v2
    def div(cls, v1, v2):
        return v1 / v2

class overload(object):
    """Class used to implement the PVetor overload mechanism."""
    def __init__(self, method):
        self.method = method
    def __get__(self, instance, cls):
        if instance is None:
            clsmethod = getattr(cls.__class__, self.method.__name__)
            return types.MethodType(clsmethod, cls, cls.__class__)
        return types.MethodType(self.method, instance, cls)

class PVector(list):
    """A vector class that mimics Processing's PVector class."""

    __metaclass__ = PVectorMeta
    def __init__(self, *args):
        """Constructor"""
        list.__init__(self)
        if len(args)==0: self.extend([0,0,0])
        elif len(args)==3: self.extend(args)
        elif len(args)==2: self.extend([args[0],args[1],0.0])
        elif len(args)==1: self.extend(args[0])
    
    def set(self,*args):
        """Assignment."""
        self = PVector(*args)
    
    def get(self):
        """Returns a copy."""
        return PVector(*self)
    
    def __add__(self, v2):
        """Returns a PVector which is a sum of this vector with vector v2.
        Notice that this overrides the common meaning of the + operator for
        lists."""
        return PVector ([self [i]+v2[i] for i in range(3)])
    
    def __iadd__(self, v2):
        """Must also override the += operator"""
        self [:] = [self [i]+v2[i] for i in range(3)]
        
    @overload
    def add(self,v2):
        """Adds vector v2 to this vector."""
        self [:] = self + v2

    def __sub__(self, v2):
        """Returns the difference between this vector and vector v2."""
        return PVector ([self [i]-v2[i] for i in range(3)])
        
    @overload
    def sub(self,v2):
        """Subtracts vector v2 from this vector."""
        self [:] = self - v2

    def __mul__(self, v2):
        """Returns the product between this vector and a scalar or a vector."""
        if isinstance (v2, list):
            return PVector ([self [i]*v2[i] for i in range(3)])
        else: 
            return PVector ([self [i]*v2 for i in range(3)])

    @overload
    def mult (self, v2):
        """Multiplies this vector by v2 (a vector or a scalar)"""
        self [:] = self*v2

    def __div__(self, v2):
        """Returns the quotient between this vector and a scalar or a vector."""
        if isinstance (v2, list):
            return PVector ([self [i]/v2[i] for i in range(3)])
        else: 
            return PVector ([self [i]/v2 for i in range(3)])

    @overload
    def div (self, v2):
        """Divides this vector by v2 (a vector or a scalar)"""
        self [:] = self/v2
     
    def dot (self,v2):
        """Dot product between two vectors."""
        return self[0]*v2[0]+self[1]*v2[1]+self[2]*v2[2]
 
    def mag (self):
        """Magnitude of the vector."""
        return sqrt(self.dot(self))
               
    def cross(self,v2):
        """Cross product between two vectors."""
        v1=self
        return PVector(v1[1] * v2[2] - v2[1] * v1[2],
                v1[2] * v2[0] - v2[2] * v1[0],
                v1[0] * v2[1] - v2[0] * v1[1])
    
    def normalize(self):
        """Makes this a unit vector."""
        self [:] = self/self.mag()
        
    # Getters and setters
    def __getx(self): return self [0]

    def __setx(self, x): self [0] = x
    
    def __gety(self): return self [1]

    def __sety(self, y): self [1] = y
    
    def __getz(self): return self [2]

    def __setz(self, z): self [2] = z
    
    # x, y, z fields implemented through properties
    x = property(__getx,__setx)
    y = property(__gety,__sety)
    z = property(__getz,__setz)

#test program
if __name__=="__main__":
    def computeNormal(p0,p1,p2):
        """Computes a normal for triangle p0-p1-p2."""
        return (PVector(p1)-PVector(p0)).cross(PVector(p2)-PVector(p1))
    a = PVector(1,2,3).cross(PVector(2,1,1))
    print a
    print a.x, a.y, a.z
    b = a.get()
    a.x = 0
    print a,b
    a.add(b)
    print a+b,a,a-b,a.mag()
    a.normalize()
    print a, a.mag()
    print computeNormal((0,0,0),(0,1,0),(1,0,0))
