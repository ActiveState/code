#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
################################################################################
#
# Utility functions for formatting exceptions and stack traces so that they are 
# guaranteed to fit in a single line and contain only chars in specified encoding.
# Very useful for logging and handling dead end exceptions.
#
# Written by Dmitry Dvoinikov <dmitry@targeted.org> (c) 2005
# Distributed under MIT license.
#
# Sample (test.py), line numbers added for clarity:
#
# 1. from exc_string import *                                                                     
# 2: set_exc_string_encoding("ascii")                                                             
# 3: class foo(object):                                                                           
# 4:     def __init__(self):                                                                      
# 5:         raise Exception("z\xffz\n") # note non-ascii char in the middle and newline          
# 6: try:                                                                                         
# 7:     foo()                                                                                    
# 8: except:                                                                                      
# 9:     assert exc_string() == "Exception(\"z?z \") in __init__() (test.py:5) <- ?() (test.py:7)"
#
# The (2 times longer) source code with self-tests is available from:
# http://www.targeted.org/python/recipes/exc_string.py
#
# (c) 2005 Dmitry Dvoinikov <dmitry@targeted.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights to 
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#
################################################################################

__all__ = [ "exc_string", "trace_string", "force_string", 
            "get_exc_string_encoding", "set_exc_string_encoding" ]

###############################################################################

from sys import exc_info
from traceback import extract_stack, extract_tb
from os import path

###############################################################################

exc_string_encoding = "windows-1251"

def get_exc_string_encoding():
    return exc_string_encoding

def set_exc_string_encoding(encoding):
    global exc_string_encoding
    exc_string_encoding = encoding

###############################################################################

force_string_translate_map = " ????????\t ?? ??????????????????" + "".join([ chr(i) for i in range(32, 256) ])

def force_string(v):
    if isinstance(v, str):
        v = v.decode(exc_string_encoding, "replace").encode(exc_string_encoding, "replace")
        return v.translate(force_string_translate_map)
    elif isinstance(v, unicode):
        v = v.encode(exc_string_encoding, "replace")
        return v.translate(force_string_translate_map)
    else:
        try:
            v = str(v)
        except:
            return "unable to convert %s to string, str() failed" % v.__class__.__name__
        else:
            return force_string(v)

###############################################################################

def _reversed(r):
    result = list(r)
    result.reverse()
    return result

def trace_string(tb = None):
    return " <- ".join([ force_string("%s() (%s:%s)" % (m, path.split(f)[1], n))
                         for f, n, m, u in _reversed(tb or extract_stack()[:-1]) ])
                         
###############################################################################

def exc_string():

    try:

        t, v, tb = exc_info()
        if t is None:
            return "no exception"
        if v is not None:
            v = force_string(v)
        else:
            v = force_string(t)
        if hasattr(t, "__name__"):
            t = t.__name__
        else:
            t = type(t).__name__

        return "%s(\"%s\") in %s" % (t, v, trace_string(extract_tb(tb)))

    except:
        return "exc_string() failed to extract exception string"

################################################################################
# EOF
