# obtaining the name of a function/method
# Christian Tismer
# March 2001

# the following function might be implemented in the
# sys module, when generators are introduced.
# For now, let's emulate it. The way is quite inefficient
# since it uses an exception, but it works.

import sys

def _getframe(level=0):
    try:
        1/0
    except:
        import sys
        tb = sys.exc_info()[-1]
    frame = tb.tb_frame
    while level >= 0:
        frame = frame.f_back
        level = level - 1
    return frame

sys._getframe = _getframe
del _getframe

# we now assume that we have sys._getframe

def funcname():
    return sys._getframe(1).f_code.co_name

class Log:

    def __init__(self):
        self.previous = None

    def methodA(self):
        self.previous = funcname()

    def methodB(self):
        self.previous = funcname()

myinstance = Log()
myinstance.methodA()
print myinstance.previous
myinstance.methodB()
print myinstance.previous

printout="""
methodA
methodB
"""
# that's all folks
