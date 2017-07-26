## make dictproxy object via ctypes.pythonapi and type()Originally published: 2008-10-26 11:00:16 
Last updated: 2008-10-26 19:35:13 
Author: Ikkei Shimomura 
 
Python internal has type 'dictproxy'.\n\nYou can get the dictproxy type object in Python.\n\nfrom types import DictProxyType\n\nany new-style classes has a __dict__ attribute, it's the dictproxy object.\nbut, the type constructor disallow you to make the instance.\n\nDictProxyType({}) # TypeError\n\nThis recipe explains how to make dictproxy object via Python API ... and type() more easy way\n