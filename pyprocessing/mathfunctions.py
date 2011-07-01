#=====================
# SOME MATH FUNCTIONS (not in python's math)
#=====================

import math



def binary(*args):
    """Converts a char or int to a string containing the equivalent binary notation."""
    if isinstance(args[0],str): number = bin(ord(args[0]))[2:]
    else: number = bin(args[0])[2:]
    if len(args) == 1: return number
    st = len(number) - args[1]
    return number[st:]
    
def hex(*args):
    """Converts a char or int to a string containing the equivalent hexadecimal notation."""
    if isinstance(args[0],str): number = "%X"%ord(args[0])
    else: number = "%X"%args[0]
    if len(args) == 1: return number
    return number[(len(number)-args[1]):]
    
def unbinary(value):
    """Converts a string representation of a binary number to its equivalent integer value."""
    return int(value,2)

def unhex(value):
    """Converts a string representation of a hexadecimal number to its equivalent integer value."""
    return int(value,16)

def byte(value):
    """Converts a char or int to its byte representation."""
    if isinstance(value,str) and len(value) == 1: return ord(value)
    elif isinstance(value,int):
        if value > 127: return byte(value-256)
        if value < -128: return byte(256+value)
        return value

def constrain (value, minv, maxv):
    """Returns the constrained value so that it falls between minv and maxv."""
    return min(max(value,minv),maxv)

def dist(*args):
    """Calculates the Euclidean distance between two points. Arguments are of the form
    dist(x1,y1,x2,y2)
    dist(x1,y1,z1,x2,y2,z2)"""
    if len(args)==4:
        return math.sqrt(sum([(a-b)**2 for a,b in zip(args[:2],args[2:])]))
    else:
        assert(len(args)==6)
        return math.sqrt(sum([(a-b)**2 for a,b in zip(args[:3],args[3:])]))

def map(value,low1,high1,low2,high2):
    """Re-maps a number from one range to another.
    CAUTION: this function overwrites Python's map builtin.
    """
    return float(value-low1)/(high1-low1)*(high2-low2)+low2

def norm(value,low,high):
    """Normalizes a number from another range into a value between 0 and 1.
    Identical to map(value, low, high, 0, 1)."""
    return float(value-low)/(high-low)

def mag(*args):
    """Calculates the magnitude (or length) of a vector. Arguments are of the form
    mag(x,y)
    mag(x,y,z)
    """
    return math.sqrt(sum([a*a for a in args]))

def lerp(value1,value2,amt):
    """Calculates a number between two numbers at a specific increment. 
    The amt parameter is the amount to interpolate between the two values
    where 0.0 equal to the first point, 0.1 is very near the first point, 
    0.5 is half-way in between, etc"""
    return value1+amt*(value2-value1)
    
def sq(value): 
    """Returns the square of value."""
    return value*value

# test program
if __name__=='__main__':
    print dist(1,1,1,2,2,2)
    print constrain(0.1,0,1),constrain(-0.1,0,1),constrain(10,0,1)
    print map(25,0,100,100,300)
    print norm(25,0,100)
    print mag(1,1,1)
    
