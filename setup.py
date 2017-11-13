# -*- coding: utf-8 -*-

# A simple setup script to create an executable running wxPython. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# wxapp.py is a very simple 'Hello, world' type wxPython application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

opts = {'packages': ['wx.lib.pubsub', 'scipy', 'matplotlib'],
        'include_files': ['./locale/', './properties/']
        }

executables = [
    Executable('tava.py', base=base)
]

setup(name='hello',
      version='0.001',
      description='Sample cx_Freeze wxPython script',
      options={'build_exe': opts},
      executables=executables
      )
