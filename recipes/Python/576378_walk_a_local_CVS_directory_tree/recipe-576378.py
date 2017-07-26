import os

def cvs_walk(currdir):
    """ walk through a CVS hierarchy

    Modeled after os.walk, this generator returns a topdown list of (currdir, dirs,
    files) tuples based on the CVS hierarchy.

    """
    dirs = []
    files = []
    if os.path.isdir(dir) and os.path.isdir(os.path.join(currdir, 'CVS')):
        for entry in open(os.path.join(currdir, 'CVS', 'Entries')):
            e = entry.split('/')
            if (len(e) > 1):
                if e[0] == 'D':
                    dirs.append(e[1])
                else:
                    files.append(e[1])
    yield (currdir, dirs, files)
    for d in dirs:
        for x in cvs_walk(os.path.join(currdir, d)):
            yield x
#
# use it just like os.path.walk
#

for (a_dir, dirs, files) in cvs_walk(top):
    for file in files:
        print os.path.join(a_dir, file)
