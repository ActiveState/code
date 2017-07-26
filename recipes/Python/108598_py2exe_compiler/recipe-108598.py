from distutils.core import setup
import sys, os, py2exe

name = sys.argv[1]
sys.argv[1] = 'py2exe'
sys.path.append(os.path.dirname(os.path.abspath(name)))

setup(name=name[:-3], scripts=[name])
