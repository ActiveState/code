"""
author : C. Jatniel Prinsloo
licence :

Useful for python sessions that have a long startup time
because of external dependancies
[In my case that would be pygame and pymunk]
I've got a slow computer so it takes a while to reload this is the solution
I came up with

import this before any other of your project imports

import reloading # The modules in your project folder get cleared
import project_module1
...

reloading.py
"""

import sys,__main__
project_path=sys.path[0]
for name,mod in sys.modules.items():
    if (
        hasattr(mod,'__path__')
        and mod.__path__[0].startswith(project_path)
        and mod is not __main__):
            del sys.modules[name]
