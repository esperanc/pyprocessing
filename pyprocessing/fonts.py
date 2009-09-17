#************************
#  FONT STUFF 
#************************

import pyglet
from pyglet.gl import *
from globs import *
from constants import *

__all__=['textAlign', 'createFont', 'textFont', 'htmlText', 'text']

def textAlign (align,yalign=BASELINE):
    """Set the text alignment attributes."""
    attrib.textAlign = (align, yalign)
    
def createFont(family = None, size = 16, bold=False, italic=False):
    """Creates a font for subsequent use"""
    return {"font_name":family, "font_size":size, "bold":bold, "italic":italic }
    
def textFont (font):
    """Set font as current font. Should be object created with createFont"""
    attrib.font = font
    
def htmlText(string, x, y, z = 0):
    """Draws the html text at x,y,z"""
    if attrib.fillColor != None:
        r,g,b,a=[int (c*255) for c in attrib.fillColor]        
        label = pyglet.text.HTMLLabel(string, location=attrib.location,
                                      x=x, y=y, width=width,
                                      anchor_x=textAlignConst[attrib.textAlign[0]],
                                      anchor_y=textAlignConst[attrib.textAlign[1]],
                                      multiline=True)
        label.color=(r,g,b,a)
        if config.coordInversionHack:
            glPushMatrix()
            glTranslatef(0,y*2,0)
            glScalef(1,-1,1)
            label.draw()
            glPopMatrix()
        else:
            label.draw()

def text(string, x, y, z = 0):
    """Draws the html text at x,y,z"""
    if attrib.fillColor != None:
        r,g,b,a=[int (c*255) for c in attrib.fillColor]
        label = pyglet.text.Label(string,
                          x=x, y=y, color=(r,g,b,a),
                          anchor_x=textAlignConst[attrib.textAlign[0]],
                          anchor_y=textAlignConst[attrib.textAlign[1]],
                          **attrib.font)
        if config.coordInversionHack:
            glPushMatrix()
            glTranslatef(0,y*2,0)
            glScalef(1,-1,1)
            label.draw()
            glPopMatrix()
        else:
            label.draw()

