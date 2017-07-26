###############################################################################
ext.py
###############################################################################

import zero

def main():
    mode = None
    if len(zero.sys.argv) > 1:
        arg = zero.sys.argv.pop(1).upper()
        if arg == 'L':
            mode = ext_lower
        elif arg == 'U':
            mode = ext_upper
        else:
            zero.sys.argv = zero.sys.argv[:1]
    zero.main(mode)

def ext_lower(path):
    head, root, ext = parts(path)
    if ext != ext.lower():
        zero.os.rename(path, zero.os.path.join(head, root + '.' + ext.lower()))

def ext_upper(path):
    head, root, ext = parts(path)
    if ext != ext.upper():
        zero.os.rename(path, zero.os.path.join(head, root + '.' + ext.upper()))

def parts(path):
    head, tail = zero.os.path.split(path)
    split = tail.rsplit('.', 1)
    return head, split[0], split[1] if len(split) > 1 else ''

if __name__ == '__main__':
    main()

###############################################################################
zero.py
###############################################################################

import os
import sys

ERROR = False

def main(function):
    try:
        arguments = sys.argv[1:]
        assert arguments
        for path in arguments:
            assert os.path.isdir(path)
        for path in arguments:
            engine(path, function)
    except:
        sys.stdout.write(os.path.basename(sys.argv[0]) + ' <directory>')

def engine(path, function):
    global ERROR
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            try:
                function(path)
            except:
                sys.stderr.write('%sError: %s' % (ERROR and '\n' or '', path))
                ERROR = True

def zero(path):
    size = os.path.getsize(path)
    file(path, 'wb').write('\0' * size)

if __name__ == '__main__':
    main(zero)
