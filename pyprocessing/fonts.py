#************************
#  FONT/TEXT STUFF 
#************************

import pyglet
from pyglet.gl import *
from globs import *
from constants import *
import config

__all__=['textAlign', 'createFont', 'textFont', 'htmlText', 'text',
         'textSize', 'textWidth', 'textAscent', 'textDescent']

def textAlign (align,yalign=BASELINE):
    """Set the text alignment attributes."""
    attrib.textAlign = (align, yalign)
    
def createFont(family = None, size = 16, bold=False, italic=False):
    """Creates a font for subsequent use"""
    return {"font_name":family, "font_size":size, "bold":bold, "italic":italic }

def textSize(size):
    """Changes the size of the current font to 'size' (in pixels)"""
    attrib.font['font_size'] = size
    
def textFont (font, size=None):
    """Set font as current font. Should be object created with createFont"""
    attrib.font = font
    if size!=None: attrib.font['font_size'] = size

def textWidth (data):
    """Returns the estimated width in pixels of the string 'data' rendered 
    in the current font"""
    label = pyglet.text.Label(data,
                          x=0, y=0, 
                          anchor_x=textAlignConst[attrib.textAlign[0]],
                          anchor_y=textAlignConst[attrib.textAlign[1]],
                          **attrib.font)
    return label.content_width

def textAscent ():
    """Returns the ascent of the current font, i.e., the height starting
    from the baseline."""
    fontspec = {'name':attrib.font.get('font_name', None),
                'size':attrib.font.get('font_size', None),
                'italic':attrib.font.get('italic', False),
                'bold':attrib.font.get('bold', False)}
    font = pyglet.font.load(**fontspec)
    return font.ascent

def textDescent ():
    """Returns the descent of the current font, i.e., the vertical size
    below the baseline."""
    fontspec = {'name':attrib.font.get('font_name', None),
                'size':attrib.font.get('font_size', None),
                'italic':attrib.font.get('italic', False),
                'bold':attrib.font.get('bold', False)}
    font = pyglet.font.load(**fontspec)
    return -font.descent

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

def text(string, x, y, *args):
    """Draws text at x,y. Argument list is of the form:
    text(string,x,y)
    text(string,x,y,z)
    text(string,x,y,width,height)
    text(string,x,y,width,height,z)
    """
    # Do nothing if no fill color is defined
    if attrib.fillColor == None: return
    # get color
    r,g,b,a=[int (c*255) for c in attrib.fillColor]
    # Obtain z coordinate
    if len(args) == 1:
        z = args[0]
    elif len(args)== 3:
        z = args[2]
    else:
        z = 0
    # create a label object
    label = pyglet.text.Label(string,
                  x=x, y=y, color=(r,g,b,a),
                  anchor_x=textAlignConst[attrib.textAlign[0]],
                  anchor_y=textAlignConst[attrib.textAlign[1]],
                  **attrib.font)
    # Obtain width and height
    if len(args)>1:
        label.width, label.height = args[0],args[1]
        label.multiline = True
    else:
        # see if the string has newlines
        s = string.split('\n')
        if len(s)>1:
            # Now follows a horribly inadequate way of figuring out
            # a reasonable value for the width property of the label
            w = 0
            for line in s:
                w = max(w,textWidth(line))
            label.width = w
            print w
            label.multiline=True
    
    glPushMatrix()
    glTranslatef(0,0,z)
    if config.coordInversionHack:
        glPushMatrix()
        glTranslatef(0,y*2,0)
        glScalef(1,-1,1)
        label.draw()
        glPopMatrix()
    else:
        label.draw()
    glPopMatrix()
