# Copyright (c) 2010 Clovis Fabricio Costa - All rights reserved
# Distribution allowed under MIT license

"""
This module can give you an infinite arsenal of python functions and classes!

Save this as activestate.py
Then you can run:

>>> from activestate.recipe194373 import mreplace
>>> print mreplace('ectave steta racipas rock!', ('a', 'e'), ('e', 'a'))
active state recipes rock!

"""

import sys
import imp
import re
import urllib2

if __name__ == '__main__':
    raise ImportError("This module can't be executed directly - it should be imported")

class RecipeImporter(object):
    _regex = re.compile('%s\.recipe(\d+)' % re.escape(__name__))
    url = 'http://code.activestate.com/recipes/%s/download/1/'
    
    def find_module(self, name, pathlist):
        if name == __name__:
            return self
        base, sep, part = name.partition('.')
        if part.startswith('recipe'):
            return self

    def _create_module(self, modulename):
        mod = imp.new_module(modulename)
        mod.__file__ = "<(%s)>" % (modulename,)
        mod.__loader__ = self
        sys.modules[modulename] = mod
        return mod

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = self._get_module(fullname)
        return mod

    def _get_module(self, fullname):
        if fullname == __name__:
            mod = self._create_module(fullname)
            mod.__path__ = []
        else:
            m = self._regex.match(fullname)
            if m:
                try:
                    code = urllib2.urlopen(self.url % m.groups()).read()
                except (urllib2.HTTPError, urllib2.URLError) as e:
                    raise ImportError("Can't load recipe %s: %s" %
                        (m.group(1), e))
                mod = self._create_module(fullname)
                exec code in mod.__dict__
            else:
                raise ImportError("Don't know how to import %r" % (fullname,))
        return mod

sys.meta_path.append(RecipeImporter())
__path__ = []
