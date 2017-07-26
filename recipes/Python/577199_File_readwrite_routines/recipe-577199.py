import os

__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577199-file-readwrite-routines/'

def read_file(fn, **kw):
    assert os.path.isfile(fn), 'File not found: "%s"' % fn
    binmode = kw.get('binmode', 0)
    if binmode:
        open_mode='rb'
    else:
        open_mode='r'
    f = open(fn, open_mode)
    if binmode:
        rc = f.read()
        assert len(rc) == os.path.getsize(fn)
    else:
        rc = map(lambda x: x.splitlines()[0], f)
    f.close()
    return rc

def write_file(fn, data, **kw):
    binmode = kw.get('binmode', 0)
    if binmode:
        open_mode='wb'
    else:
        open_mode='w'
    f = open(fn, open_mode)
    if binmode:
        f.write(data)
    else:
        for v in data:
            f.write(v + '\n')
    f.close()


def indent_lines(fn_src, fn_dest):
    '''
    Sample 1: indent all lines of source file
    '''
    lines = read_file(fn_src)
    lines = map(lambda x: '    '+x, lines)
    write_file(fn_dest, lines)

def win2unix(fn_src, fn_dest):
    '''
    Sample 2: replace windows line endings (0D 0A) with unix EOL (0A)
    '''
    filedata = read_file(fn_src, binmode=1)
    filedata = filedata.replace('\x0d\x0a', '\x0a')
    write_file(fn_dest, filedata, binmode=1)
