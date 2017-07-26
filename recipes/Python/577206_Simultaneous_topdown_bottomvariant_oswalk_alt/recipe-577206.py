#!/usr/bin/env python


def cleanpycs(root, exclude='CVS .svn .git .hg .bzr'.split()):
    '''Deletes .pyc files and empty directories under this directory.

    Directories in ``exclude`` are not traversed.
    '''
    from os.path import join, normpath
    from os import listdir, remove, rmdir
    exclude = frozenset(exclude)
    for dir, subdirs, files, top in walk2(root):
        if top:
            for f in files:
                if f.endswith('.pyc'):
                    remove(join(dir,f))
            subdirs[:] = [d for d in subdirs if d not in exclude]
        elif not listdir(dir):
            rmdir(dir)


def walk2(top, onerror=None, followlinks=False):
    '''Simultaneous topdown and bottomup version of os.walk.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 4-tuple::

        dirpath, dirnames, filenames, top

    The triples (``dirpath``, ``dirnames``, ``filenames``) are the same yielded
    by os.walk, however each such triple is yielded twice, once before the
    subtree rooted at ``dirpath`` is visited (``top=True``) and once after
    (``top=False``).

    As with os.walk with ``topdown=True``, the caller can modify the dirnames
    list in-place when ``top=True`` (e.g., via del or slice assignment),
    and walk will only recurse into the subdirectories whose names remain in
    dirnames. Modifying dirnames when ``top=False``is ineffective, since
    the directories in dirnames have already been generated.
    '''
    from os import listdir, error
    from os.path import join, isdir, islink
    try:
        names = listdir(top)
    except error, err:
        if onerror is not None:
            onerror(err)
        return
    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
    yield top, dirs, nondirs, True
    for name in dirs:
        path = join(top, name)
        if followlinks or not islink(path):
            for x in walk2(path, onerror, followlinks):
                yield x
    yield top, dirs, nondirs, False


if __name__ == '__main__':
    import sys
    cleanpycs(sys.argv[1] if len(sys.argv) > 1 else '.')
