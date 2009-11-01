"""
Holds system wide configuration options.
"""

from constants import *

# Whether or not to try to obtain an OpenGL context supporting multisampling.
# This usually produces nicer results but is unsupported in older hardware.
# Even if this is set to false, however, pyprocessing will fallback to 
# a non-multisampled config if it is not supported.
multisample = True

# Whether or not to invert the y axis. This is required for strict conformity
# with Processing. Beyond altering the modelview matrix, this also implies that
# the drawing of some primitives such as arc or text be modified.
coordInversionHack = True 

# Since OpenGL actually addresses lines between pixels, in some cases 
# shifting the drawing by half a pixel makes lines sharper. 
halfPixelShiftHack = False # off by default

# try to get around the artifacts when drawing filled polygons in smooth mode
smoothFixHack = False # off by default 
smoothTurnedOn = False # Used internally to tell whether smooth was on

# flipping policy: uncomment only one of the assignments below
flipPolicy = DOUBLE_FLIP_POLICY # this is the default and should work for modern boards/drivers
# flipPolicy = SINGLE_FLIP_POLICY # use this for Intel 945 under Windows or other cheap boards
# flipPolicy = FBO_FLIP_POLICY # use this for modern boards/drivers where flip uses swap and not copy
# flipPolicy = ACCUM_FLIP_POLICY # use this for cheap boards where 'SINGLE' produces too much flickering

