#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
'''An attempt to implement a check on Chicago Manual of Style page ranges.

http://www.chicagomanualofstyle.org/ch09/ch09_sec064.html
9.64 Abbreviating, or condensing, inclusive numbers
'''

import codecs
from glob import glob
import re

def proper_range(fir, sec):
    '''
    >>> valid = [(3, 10), (71, 72), (96, 117), (100, 104), (1100, 1113), (101, 8), (1103, 4), (321, 28), (212, 302), (1496, 1504), (498, 532)]
    >>> all([proper_range(*pair) for pair in valid])
    True

    >>> invalid = [(71, 2), (1103, 2), (321, 20), (321, 328)]
    >>> any([proper_range(*pair) for pair in invalid])
    False

    '''
    
    if fir < 100:
        if sec < fir:
            #print "** fir < 100 and didn't use all digits" 
            return False # (12, 3)
        else:
            return True # (12, 13)

    if fir % 100 == 0:
        if fir > sec:
            #print "** fir multiple of 100 and didn't use all digits" 
            return False # (100, 4)
        else:
            return True # (100, 104)

    if len(str(fir)) == len(str(sec)) and int(str(fir)[0]) == int(str(sec)[0]):
        if len(str(fir)) > 3:
            if all(a != b for a,b in zip(str(fir), str(sec))[1:]): 
                return True # (1496, 1504)
            else:
                #print "** not all least significant digits changed in 4+ digit number"
                return False # (1496, 1506)
        else:
            if fir < sec:
                #print "** used more digits than needed" # (389, 391)
                return False
            else:
                return True # (498, 532)

    if int(str(fir)[-len(str(sec)):]) > sec:
        #print "** first is larger than second" 
        return False #(1103, 102)

    #print "** defaulting to true"
    return True

files = sorted(glob('[!~]*.mdn'))
pages_pattern = re.compile(r'\[(\d+-\d+)\]')
for file_name in files:
    source = codecs.open(file_name, "r", "UTF-8", "replace")
    for line in source:
        matches = pages_pattern.findall(line)
        if matches:
            for page_range in matches:
                fir, sec = page_range.split('-')
                if not proper_range(int(fir), int(sec)):
                    print file_name, page_range
                    
