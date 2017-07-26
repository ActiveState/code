import sys
def set(**kw):
    assert len(kw)==1
    
    a = sys._getframe(1)
    a.f_locals.update(kw)
    return kw.values()[0]

#
# sample
#

A=range(10)

while set(x=A.pop()):
    print x
