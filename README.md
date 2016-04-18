WHAT IS THIS?

The pyprocessing project provides a Python package that creates an environment
for graphics applications that closely resembles that of the Processing system.
Usage is mostly restricted to importing the package and calling run(). 

The project mission is to implement Processing's friendly graphics functions and
interaction model in Python. Not all of Processing is to be ported, though,
since Python itself already provides alternatives for many features of
Processing, such as XML parsing.

The pyprocessing backend is built upon OpenGL and Pyglet, which provide the
actual graphics rendering. Since these are multiplatform, so is pyprocessing.

We hope that, much in the same spirit of the Processing project, pyprocessing
will appeal to people who want to easily program and interact with computer
generated imagery. It is also meant to help teaching computer programming by
making it possible to write compact code with rich visual semantics.

WHAT ARE THE REQUIREMENTS?

In essence, all you need is the pyglet package (see www.pyglet.org) and its 
requirements, i.e., OpenGL and Python (2.5 or 2.6). If you are able to run 
pyglet's sample programs, you are in good shape to run pyprocessing.

HOW TO INSTALL IT?

Put the pyprocessing directory (the one which contains __init__.py, attribs.py,
etc) in any place Python expects to find modules and packages. The simplest
way of achieving this is to run the provided setup.py program:

      python setup.py install
      
This will copy the files to the proper places. You might have to have 
administration privileges to do this, however. In most flavors of Linux, for 
instance, you might have to type:

      sudo python setup.py install

Alternatively, if you are running some flavor of MS-Windows, there is a binary 
installation file which you will find in the pyprocessing site 
(http://code.google.com/p/pyprocessing/downloads).

HOW TO USE IT?

There are several example programs in the examples folder that you may try. 
You may also take a look at the project wiki for simple usage instructions
(http://code.google.com/p/pyprocessing/wiki/UsageInstructions)


