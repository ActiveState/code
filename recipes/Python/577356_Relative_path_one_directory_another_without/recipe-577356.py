# -*- coding: Windows-1251 -*-
'''
Relative path from one directory to another without explicit string functions (unix only)

Function deal with Unix paths (root: "/"), Windows systems are not supported (root: "C:\").
'''
__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577356'

import os

if os.name == 'nt':
    raise ValueError, 'dos/windows paths unsupported in this version'

def relative_path(base, target):

    def split_path(path):
        res = list()
        while 1:
            path, basename = os.path.split(path) 
            if path == os.sep and basename == '':
                # root reached
                break
            res.insert(0, basename)
            if path == '':
                break
        return res

    # check for absolute paths
    if not base.startswith(os.sep):
        raise ValueError, 'base must be absolute: %s' % base
    if not target.startswith(os.sep):
        raise ValueError, 'target must be absolute: %s' % target

    base_parts = split_path(base)
    target_parts = split_path(target)

    while len(base_parts) > 0 and \
          len(target_parts) > 0 and \
          base_parts[0] == target_parts[0]:
        base_parts.pop(0)
        target_parts.pop(0)

    rel_parts = ['..'] * len(base_parts)
    rel_parts.extend(target_parts)

    return os.path.join(*rel_parts)

if __name__ == '__main__':
    base = os.sep + os.path.join('a', 'b', 'c', 'd')
    target = os.sep + os.path.join('a', 'b', 'c1', 'd2')
    print 'base  :', base
    print 'target:', target
    print 'relative base->target:', relative_path(base, target)
