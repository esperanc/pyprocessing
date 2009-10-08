#!/usr/bin/env python
# coding:utf-8

from distutils.core import setup

long_description = '''
This Python package provides an environment for graphics applications that 
closely resembles that of the Processing system.

The project mission is to implement Processing's friendly graphics 
functions and interaction model in Python. Not all of Processing is ported, 
though, since Python itself already provides alternatives for many features 
of Processing.

The pyprocessing backend is built upon OpenGL and Pyglet, 
which provide the actual graphics rendering. Since these are multiplatform, 
so is pyprocessing.
'''

# MAKE SURE THE VERSION BELOW IS THE SAME AS THAT IN CONSTANTS.PY!

setup(name='pyprocessing',
      version='0.1.1',
      description='A Processing-like environment for Python',
      long_description=long_description,
      author='Claudio Esperança',
      author_email='claudio.esperanca@gmail.com',
      url='http://code.google.com/p/pyprocessing/',
      license='BSD',
      packages=['pyprocessing'],
     )

