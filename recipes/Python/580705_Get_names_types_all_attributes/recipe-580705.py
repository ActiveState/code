from __future__ import print_function

# mod_attrs_and_types.py 
# Purpose: To show the attribute names and types 
# of a Python module, to help with learning about it.
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram
# Web site: https://vasudevram.github.io
# Blog: http://jugad2.blogspot.com
# Product store: https://gumroad.com/vasudevram

import sys

def attrs_and_types(mod_name):

    print('Attributes and their types for module {}:'.format(mod_name))
    print()
    for num, attr in enumerate(dir(eval(mod_name))):
        print("{idx}: {nam:30}  {typ}".format(
            idx=str(num + 1).rjust(4),
            nam=(mod_name + '.' + attr).ljust(30), 
            typ=type(eval(mod_name + '.' + attr))))

attrs_and_types(sys.__name__)
