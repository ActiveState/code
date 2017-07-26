## make dictproxy object via ctypes.pythonapi and type()  
Originally published: 2008-10-26 11:00:16  
Last updated: 2008-10-26 19:35:13  
Author: Ikkei Shimomura  
  
Python internal has type 'dictproxy'.

You can get the dictproxy type object in Python.

from types import DictProxyType

any new-style classes has a __dict__ attribute, it's the dictproxy object.
but, the type constructor disallow you to make the instance.

DictProxyType({}) # TypeError

This recipe explains how to make dictproxy object via Python API ... and type() more easy way
