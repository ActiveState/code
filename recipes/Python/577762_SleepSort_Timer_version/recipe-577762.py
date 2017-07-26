from __future__ import print_function
from threading import Timer

l = [8, 2, 4, 6, 7, 1]

for n in l:
    Timer(n, lambda x: print(x), [n]).start()
