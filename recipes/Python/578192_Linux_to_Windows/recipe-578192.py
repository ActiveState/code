import os
import sys
import tarfile

ERROR = False
TABLE = ''.join(map(chr, range(256)))
DELETECHARS = ''.join(c for c in TABLE if len(repr(c)) != 6)

def main():
    try:
        arguments = sys.argv[1:]
        assert arguments
        for path in arguments:
            assert os.path.isdir(path)
        for function in (untar, bias, convert):
            for path in arguments:
                engine(path, function)
    except:
        sys.stdout.write(
            'Usage: %s <directory>' % os.path.basename(sys.argv[0]))

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

def untar(path):
    try: tarfile.open(path).extractall(os.path.dirname(path))
    except: pass

def bias(path):
    root, ext = os.path.splitext(path)
    if not ext[1:]:
        os.rename(path, root + '.txt')

def convert(path):
    if not file(path, 'rb').read(2 ** 20).translate(TABLE, DELETECHARS):
        data = file(path, 'r').read()
        file(path, 'w').write(data)

if __name__ == '__main__':
    main()
