#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import with_statement
import os
import os.path

class ChangeDirectory(object):
    """
    ChangeDirectory is a context manager that allowing 
    you to temporary change the working directory.

    >>> import tempfile
    >>> td = os.path.realpath(tempfile.mkdtemp())
    >>> currentdirectory = os.getcwd()
    >>> with ChangeDirectory(td) as cd:
    ...     assert cd.current == td
    ...     assert os.getcwd() == td
    ...     assert cd.previous == currentdirectory
    ...     assert os.path.normpath(os.path.join(cd.current, cd.relative)) == cd.previous
    ...
    >>> assert os.getcwd() == currentdirectory
    >>> with ChangeDirectory(td) as cd:
    ...     os.mkdir('foo')
    ...     with ChangeDirectory('foo') as cd2:
    ...         assert cd2.previous == cd.current
    ...         assert cd2.relative == '..'
    ...         assert os.getcwd() == os.path.join(td, 'foo')
    ...     assert os.getcwd() == td
    ...     assert cd.current == td
    ...     os.rmdir('foo')
    ...
    >>> os.rmdir(td)
    >>> with ChangeDirectory('.') as cd:
    ...     assert cd.current == currentdirectory
    ...     assert cd.current == cd.previous
    ...     assert cd.relative == '.'
    """

    def __init__(self, directory):
        self._dir = directory
        self._cwd = os.getcwd()
        self._pwd = self._cwd

    @property
    def current(self):
        return self._cwd
    
    @property
    def previous(self):
        return self._pwd
    
    @property
    def relative(self):
        c = self._cwd.split(os.path.sep)
        p = self._pwd.split(os.path.sep)
        l = min(len(c), len(p))
        i = 0
        while i < l and c[i] == p[i]:
            i += 1
        return os.path.normpath(os.path.join(*(['.'] + (['..'] * (len(c) - i)) + p[i:])))
    
    def __enter__(self):
        self._pwd = self._cwd
        os.chdir(self._dir)
        self._cwd = os.getcwd()
        return self

    def __exit__(self, *args):
        os.chdir(self._pwd)
        self._cwd = self._pwd


if __name__ == '__main__':
    import doctest
    doctest.testmod()
