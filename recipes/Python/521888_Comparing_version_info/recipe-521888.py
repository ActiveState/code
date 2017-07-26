# (C) Alexander Belchenko, 2007

"""This module provide useful class for manipulating
with version info in the form:

    major.minor.release.build

Main operations is comparing between different versions


Examples:

>>> v1 = VersionInfo('1')
>>> print v1
1.0
>>> print `v1`
VersionInfo('1.0.0.0')
>>> print '%(major)d.%(minor)d.%(release)d.%(build)d' % v1
1.0.0.0

>>> v2 = VersionInfo((2, 0))
>>> print v2
2.0

>>> v2 == '2.0.0.0'
True
>>> v1 == v2
False
>>> v1 < v2
True

>>> v3 = VersionInfo([2,0,3,4])
>>> print v3
2.0.3.4
>>> v3.major
2
>>> v3.minor
0
>>> v3.release
3
>>> v3.build
4

>>> v3 > v2
True

>>> v4 = VersionInfo('3.34')
>>> v5 = VersionInfo('3.3')
>>> v4 > v5
True

>>> v1 > '0.9'
True
>>> v2 >= '2.0'
True
>>> v3 > (2,0,2,5)
True
>>> v3 > (2,0,3,1)
True
>>> v4 > '2.0'
True

>>> '0.9' < v1 < '1.1'
True
>>> ('0.9' < v5 < '1.1') or v5 == '3.3'
True
"""


class VersionInfo(object):
    """Version info container and comparator"""

    __slots__ = ['major', 'minor', 'release', 'build']

    def __init__(self, v):
        if isinstance(v, basestring):
            # convert string to list
            v = [int(i) for i in v.split('.')]
        else:
            v = list(v)
        # build from sequence
        size = len(v)
        if size > 4:
            raise ValueError('Incorrect version info format. '
                             'Accepted max 4 numbers')
        if size < 4:
            v += [0] * (4-size)

        for ix, name in enumerate(self.__slots__):
            num = int(v[ix])
            setattr(self, name, num)

    def __getitem__(self, name):
        return getattr(self, name)

    def __repr__(self):
        return ("VersionInfo('%(major)d.%(minor)d.%(release)d.%(build)d')"
                % self)

    def __str__(self):
        if self.build > 0:
            fmt = '%(major)d.%(minor)d.%(release)d.%(build)d'
        elif self.release > 0:
            fmt = '%(major)d.%(minor)d.%(release)d'
        else:
            fmt = '%(major)d.%(minor)d'
        return fmt % self

    def __cmp__(self, other):
        """Called for objects comparison.
        Return a negative integer if self < other,
        zero if self == other,
        a positive integer if self > other.
        """
        if not isinstance(other, VersionInfo):
            other = VersionInfo(other)
        res = 0
        for name in self.__slots__:
            res = getattr(self, name) - getattr(other, name)
            if res != 0:
                break
        return res


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    print '*' * 70
    print 'T E S T'
    print '*' * 70
    _test()
