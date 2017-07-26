"""Path utility to:

* split a path entirely
* join it
* return true commonprefix on paths

    >>> import os
    >>> path = os.getcwd()
    >>> join(split(path)) == path
    True

    >>> p1, p2, p3 = (os.path.join(*'abc'), os.path.join(*'abd'),
    ...               os.path.join(*'ab'))
    >>> commonprefix(p1, p2, p3) == p3
    True
    >>> p1, p2 = os.path.join(*'xyz'), os.path.join(*'abd')
    >>> commonprefix(p1, p2)
    ''
"""
import os.path

def isplit(path):
    "Generator splitting a path"
    dirname, basename = os.path.split(path)
    if path == dirname:
        # stop recursivity
        yield path
    elif dirname:
        # continue recursivity
        for i in isplit(dirname):
            yield i
    if basename:
        # return tail
        yield basename

def join(iterable):
    """Join iterable's items as a path string

    >>> join(('a', 'b')) == os.path.join('a', 'b')
    True
    """
    items = tuple(iterable)
    if not items:
        return ''
    return os.path.join(*items)
    
def split(path):
    """Return the folder list of the given path

    >>> split(os.path.join('a', 'b'))
    ('a', 'b')
    """
    return tuple(isplit(path))

def commonprefix(*paths):
    """Return the common prefix path of the given paths

    >>> commonprefix(os.path.join('a', 'c'), os.path.join('a', 'b'))
    'a'
    """
    paths = map(split, paths)
    if not paths: return ''
    p1 = min(paths)
    p2 = max(paths)
    for i, c in enumerate(p1):
        if c != p2[i]:
            return join(p1[:i])
    return join(p1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
