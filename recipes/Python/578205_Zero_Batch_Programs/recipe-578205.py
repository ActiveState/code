# ==============================================================================
# zero.py
# ==============================================================================

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
        sys.stdout.write('Usage: %s <directory>' % os.path.basename(sys.argv[0]))

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
    if size:
        data = open(path, 'wb')
        todo = size
        if todo >= 2 ** 20:
            buff = '\x00' * 2 ** 20
            while todo >= 2 ** 20:
                data.write(buff)
                todo = size - data.tell()
        data.write('\x00' * todo)
        data.close()

if __name__ == '__main__':
    main(zero)

# ==============================================================================
# upper.py
# ==============================================================================

import zero

def upper(path):
    root, ext = zero.os.path.splitext(path)
    upper = ext.upper()
    if ext != upper:
        zero.os.rename(path, root + upper)

if __name__ == '__main__':
    zero.main(upper)

# ==============================================================================
# untar.py
# ==============================================================================

import zero
import tarfile

if __name__ == '__main__':
    zero.main(lambda path: tarfile.open(path).extractall(
        zero.os.path.dirname(path)))

# ==============================================================================
# remove.py
# ==============================================================================

import zero

if __name__ == '__main__':
    zero.main(zero.os.remove)

# ==============================================================================
# one.py
# ==============================================================================

import zero

def one(path):
    size = zero.os.path.getsize(path)
    if size:
        data = open(path, 'wb')
        todo = size
        if todo >= 2 ** 20:
            buff = '\xFF' * 2 ** 20
            while todo >= 2 ** 20:
                data.write(buff)
                todo = size - data.tell()
        data.write('\xFF' * todo)
        data.close()

if __name__ == '__main__':
    zero.main(one)

# ==============================================================================
# lower.py
# ==============================================================================

import zero

def lower(path):
    root, ext = zero.os.path.splitext(path)
    lower = ext.lower()
    if ext != lower:
        zero.os.rename(path, root + lower)

if __name__ == '__main__':
    zero.main(lower)

# ==============================================================================
# random.py
# ==============================================================================

import zero

def kaos(path):
    size = zero.os.path.getsize(path)
    if size:
        data = open(path, 'wb')
        todo = size
        while todo:
            data.write(zero.os.urandom(min(todo, 2 ** 20)))
            todo = size - data.tell()
        data.close()

if __name__ == '__main__':
    zero.main(kaos)

# ==============================================================================
# name.py
# ==============================================================================

import zero
import random

STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def ident(path):
    d, b = zero.os.path.split(path)
    zero.os.rename(path, zero.os.path.join(d, ''.join(random.sample(
        STRING, len(STRING))) + zero.os.path.splitext(b)[1]))

if __name__ == '__main__':
    zero.main(ident)

# ==============================================================================
# newlines.py
# ==============================================================================

import zero

TABLE = ''.join(map(chr, range(256)))
DELETECHARS = ''.join(c for c in TABLE if len(repr(c)) != 6)

def convert(path):
    if not file(path, 'rb').read(2 ** 20).translate(TABLE, DELETECHARS):
        data = file(path, 'r').read()
        file(path, 'w').write(data)

if __name__ == '__main__':
    zero.main(convert)

# ==============================================================================
# extension.py
# ==============================================================================

import zero

def bias(path):
    root, ext = zero.os.path.splitext(path)
    if not ext[1:]:
        zero.os.rename(path, root + '.txt')

if __name__ == '__main__':
    zero.main(bias)
