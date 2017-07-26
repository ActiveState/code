#!/usr/bin/env python

"""
Create a dictionary of ascending (sequential) directories.
"""

def make_pathdict(keys, fspath = None):

    """Quickly create a dictionary of ascending path components.
    
    :param keys: list of dictionary keys (base -> root order)
    :returns: dictionary of keyed paths

    NOTICE: This does not check path-length::key-count, etc.!
            Also, not as robust as os.path in x-platform use.

    >>> fspath = "/and/the/player/asks/anyone/for_tennis.py"
    >>> keys = "base midl root".split()
    >>> ret_dict = make_pathdict(keys, fspath)
    >>> for k in keys: print "{0:<6}{1}".format(k, ret_dict[k])
    base  /and/the/player/asks/anyone
    midl  /and/the/player/asks
    root  /and/the/player
    """
    
    from os import path as os_path

    _cache = {}

    fspath = os_path.abspath(fspath or __file__)


    # divide the path into len(keys) + 1 parts, the root, directories and file

    tokenz = fspath.rsplit(os_path.sep, len(keys))


    # iterate the keys assigning the decreasing-lenght path-portions

    for idx, key in enumerate(keys):
        _cache[key] = os_path.join(*tokenz[:-(idx + 1)])


    return _cache
