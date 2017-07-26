"""
find a unique name based on a prefix for a content in a container
(eg. a file in a directory) adding a digit to the name

Does it in log2(n) + log2(n/2) were n is the number of duplicates
"""


def go_down(name, exists, lower, upper):
    """bisection to find first free slot
    """
    if upper - lower < 2:
        if exists(name + '-%d' % lower):
            return name + '-%d' % upper
        else:
            return name + '-%d' % lower
    else:
        mid = (upper + lower) // 2
        if exists(name + '-%d' % mid):
            return go_down(name, exists, mid, upper)
        else:
            return go_down(name, exists, lower, mid)


def go_up(name, exists, n):
    """find a free slot in log2(n) time
    """
    if exists(name + '-%d' % n):
        return go_up(name, exists, n * 2)
    else:
        # NOTE : 'or 1' for we don't want <name>-0
        return go_down(name, exists, n // 2 or 1, n)


def getname(name, exists):
    """return a unique name, using name as suffix

    exists is a function that will test existence
    """
    if not exists(name):
        return name
    else:
        return  go_up(name, exists, 1)


if __name__ == '__main__':
    # quick test
    import os
    import glob
    import tempfile
    import shutil
    cwd = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    try:
        os.chdir(tmpdir)
        for i in xrange(50):
            name = getname('a', os.path.exists)
            with open(name, 'w') as f:
                f.write(str(i))
        # verify (do not verify 0 as it is a special case)
        assert set(glob.glob('a-*')) == set('a-%d' % i for i in xrange(1, 50))
        # verify content to assert order of allocation was correct
        for i in xrange(1, 50):
            with open('a-%d' % i) as f:
                assert f.read() == str(i)
    finally:
        os.chdir(cwd)
        os.chdir(tmpdir)
        shutil.rmtree(tmpdir)
