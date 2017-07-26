import sys
import os

path = os.path.abspath('.') # default is current dir
if len(sys.argv) == 2:
    path = sys.argv[1]
exts = []
for root, dirs, files in os.walk(os.path.expanduser(path)):
    for fn in files:
        bn, ext = os.path.splitext(fn)
        if not ext in exts:
            exts.append(ext)
            if ext:
                print ext
