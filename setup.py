from distutils.core import setup
import py2exe
setup(console=['cheetaGUI.py'])




"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app

from setuptools import setup
import image
import networkx
import lib2to3
import PIL
from PIL import Image
from PIL import _imaging

APP = ['cheetaGUI.py']
DATA_FILES = ['wowmonkey.jpg','Jane']
OPTIONS = {'argv_emulation': True,
       # 'iconfile': 'cooltext.icon'
           }


# 
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

"""
