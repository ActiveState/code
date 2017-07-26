import re

DIGITS = re.compile(r'[0-9]+')
def compnum(x, y):
    nx = ny = 0
    while True:
        a = DIGITS.search(x, nx)
        b = DIGITS.search(y, ny)
        if None in (a,b):
            return cmp(x[nx:], y[ny:])
        r = (cmp(x[nx:a.start()], y[ny:b.start()]) or
             cmp(int(x[a.start():a.end()]), int(y[b.start():b.end()])))
        if r:
            return r
        nx, ny = a.end(), b.end()


#
#  sample
#

L1 = ["file~%d.txt"%i for i in range(1,15)]
L2 = L1[:]

L1.sort()
L2.sort(compnum)

for i,j in zip(L1, L2):
    print "%15s %15s" % (i,j)
