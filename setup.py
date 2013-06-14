#!/usr/bin/env python

from distutils.core import setup

setup(name='flikrstor',
      version='0.1',
      description='Encode and decode files as images so they can be stored on flikr',
      author='Brett Lazarus',
      author_email='blazarus488@gmail.com',
      requires=['numpy', 'Image', 'struct'],
      scripts=['cli'],
      py_modules=['filetoimage']
      )
