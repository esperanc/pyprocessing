"""
Holds system wide configuration options.
"""

from constants import *
import os
from ConfigParser import *


"""Loads the user configuration preferences from the config.txt file situated
on the user's home path. If the file doesn't exist, it is then created with
default values for the main preferences, including DOUBLE_FLIP_POLICY as
flip policy setup. The config file can be changed manually by the user,
noting that the right parameter orders must be followed accordingly. The
order of the parameters is FlipPolicy, Multisample, coordInversionhack,
halfPixelShiftHck and smoothFixHack."""

try:
    f = open(os.path.expanduser("~/pyprocessing/config.txt"),"r")
except:
    try:
        f = open(os.path.expanduser("~/pyprocessing/config.txt"),"w")
    except:
        os.mkdir(os.path.expanduser("~/pyprocessing"))
        f = open(os.path.expanduser("~/pyprocessing/config.txt"),"w")
    f = open(os.path.expanduser("~/pyprocessing/config.txt"),"w")
    f.write(DOUBLE_FLIP_POLICY+"\nTrue\nTrue\nFalse\nFalse")
    f.close()
    f = open(os.path.expanduser("~/pyprocessing/config.txt"),"r")
contents = f.read()
contents = contents.split("\n")


if False and contents[0] not in (DOUBLE_FLIP_POLICY,SINGLE_FLIP_POLICY, FBO_FLIP_POLICY, ACCUM_FLIP_POLICY, BACKUP_FLIP_POLICY):
    f.close()
    f = open(os.path.expanduser("~/pyprocessing/config.txt"),"w")
    f.write(BACKUP_FLIP_POLICY)
    f.close()
    f = open(os.path.expanduser("~/pyprocessing/config.txt"),"r")
    contents = f.read()
f.close()


flipPolicy = contents[0]
multisample = eval(contents[1])
coordInversionHack = eval(contents[2])
halfPixelShiftHack = eval(contents[3])
smoothFixHack = eval(contents[4])





"""Uncommenting the preferences at this part of the script will make the
preferences be globally applied, with a higher priority than the preferences
imported from the config.txt file"""

# Whether or not to try to obtain an OpenGL context supporting multisampling.
# This usually produces nicer results but is unsupported in older hardware.
# Even if this is set to false, however, pyprocessing will fallback to 
# a non-multisampled config if it is not supported.
#multisample = True

# Whether or not to invert the y axis. This is required for strict conformity
# with Processing. Beyond altering the modelview matrix, this also implies that
# the drawing of some primitives such as arc or text be modified.
#coordInversionHack = True 

# Since OpenGL actually addresses lines between pixels, in some cases 
# shifting the drawing by half a pixel makes lines sharper. 
#halfPixelShiftHack = False # off by default

# try to get around the artifacts when drawing filled polygons in smooth mode
#smoothFixHack = False # off by default 
smoothTurnedOn = False # Used internally to tell whether smooth was on

# flipping policy: uncomment only one of the assignments below
# flipPolicy = DOUBLE_FLIP_POLICY # this is the default and should work for modern boards/drivers
# flipPolicy = SINGLE_FLIP_POLICY # use this for Intel 945 under Windows or other cheap boards
# flipPolicy = FBO_FLIP_POLICY # use this for modern boards/drivers where flip uses swap and not copy
# flipPolicy = ACCUM_FLIP_POLICY # use this for cheap boards where 'SINGLE' produces too much flickering
# flipPolicy = BACKUP_FLIP_POLICY # use this for cheap boards where 'ACCUM' isn't working correctly







