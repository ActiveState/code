#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
Using re.match, re.search, and re.group in if ... elif ... elif ... else ...
'''

__author__ = 'Peter Kleiweg'
__version__ = '1.4'
__date__ = '2005/11/16'

import re

class RE:
    '''
    Using re.match, re.search, and re.group in if ... elif ... elif ... else ...
    This is NOT thread safe

    Instance data:

        _pattern : pattern compiled by __init__()

    Global data:

        _match : match object saved by last match() or search()

    Example:

        rePat1 = RE(pattern1)
        rePat2 = RE(pattern2)
        for line in lines:
            if rePat1.search(line):
                grp1 = RE.group(1)
                grpA = RE.group('A')
            elif rePat2.search(line):
                grp2 = RE.group(2)
                grpB = RE.group('B')
    '''

    def __init__(self, pattern, flags=0):
        'do and save re.compile(pattern, flags)'
        self._pattern = re.compile(pattern, flags)

    def match(self, string, flags=0):
        'do, save, and return pattern.match(string, flags)'
        RE._match = self._pattern.match(string, flags)
        return RE._match

    def search(self, string, flags=0):
        'do, save, and return pattern.search(string, flags)'
        RE._match = self._pattern.search(string, flags)
        return RE._match

    def group(grp=0):
        'return match_object.group(grp)'
        return RE._match.group(grp)
    group = staticmethod(group)


class SR:
    '''
    Save and return value in bitwise or test
    This is thread safe

    Instance data:

        _ : value saved by __or__()

    Example:

        rePat1 = re.compile(pattern1)
        rePat2 = re.compile(pattern2)
        m = SR()
        for line in lines:
            if m|rePat1.search(line):
                grp1 = m.group(1)
                grpA = m.group('A')
            elif m|rePat2.search(line):
                grp2 = m.group(2)
                grpB = m.group('B')
    '''

    def __or__(self, value):
        'save value as _ and return value'
        self._ = value
        return value

    def group(self, grp=0):
        'return _.group(grp)'
        return self._.group(grp)



if __name__ == '__main__':

    lines = []
    lines.append(' 1     one   ')
    lines.append(' two   2     ')
    lines.append(' three three ')
    lines.append(' 4     4     ')

    reIntStr = RE(r'^\s*(?P<Int>\d+)\s+(?P<Str>\S.*?)\s*$')
    reStrInt = RE(r'^\s*(?P<Str>\S.*?)\s+(?P<Int>\d+)\s*$')
    for line in lines:
        print '>>>', line
        if reIntStr.search(line):
            print 'Int:', RE.group('Int')
            print 'Str:', RE.group('Str')
            print
        elif reStrInt.search(line):
            print 'Str:', RE.group('Str')
            print 'Int:', RE.group('Int')
            print
        else:
            print '*** UNMATCHED ***'
            print

    print "The same as above, now in a thread safe manner\n"

    reIntStr = re.compile(r'^\s*(?P<Int>\d+)\s+(?P<Str>\S.*?)\s*$')
    reStrInt = re.compile(r'^\s*(?P<Str>\S.*?)\s+(?P<Int>\d+)\s*$')
    m = SR()
    for line in lines:
        print '>>>', line
        if m|reIntStr.search(line):
            print 'Int:', m.group('Int')
            print 'Str:', m.group('Str')
            print
        elif m|reStrInt.search(line):
            print 'Str:', m.group('Str')
            print 'Int:', m.group('Int')
            print
        else:
            print '*** UNMATCHED ***'
            print
