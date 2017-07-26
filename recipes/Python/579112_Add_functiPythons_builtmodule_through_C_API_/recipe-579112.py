#!/usr/bin/python
# -*- coding: utf8 -*-

# import mymodule
# ^^^^^^^^^^^^^^^ <- no need to import module
#
# for more info, please see the references - this is just an ugly demo

def bar(d):
    usleep(500000) # there isn't function by this name in std Python
    print d
    print type(d)
    return int(d['a'] + d['b'])
