"""
Here's something I found useful when developing python programs. It takes advantage of
my convention to initialize properties that I want to use in the constructor.
This script checks this initialization and complains when a variable wasn't defined.

Great for detecting typos early - what I like most is that when you are ready developing
your script, you just throw the whole thing away from your source and you have no
performance penalty.

It heavily depends on the articles of Alex Martinelli: 'Constants in Python' and 
'Determining Current Function Name' here at ASPN. You could beef this up with
typechecking (see the comments of Philip Nunez at Alex' 'Constants...' article).

Dirk Krause, d_krause@pixelpark.com, 11/08/2001
"""



import sys

def caller():
    try:
        raise RuntimeError
    except RuntimeError:
        exc, val, tb = sys.exc_info()
        frame = tb.tb_frame.f_back
        del exc, val, tb
    try:
        return frame.f_back.f_code.co_name
    except AttributeError:  # called from the top
        return None


class ObjectWithCheck:

    def __setattr__(self, name, value):
    
        c = caller()
        if c == '__init__' or hasattr(self, name):
            self.__dict__[name] = value
        else:
            raise TypeError, self.__class__.__name__ + 'error: variable was not declared!'



class myObjWithCheck(ObjectWithCheck):
    def __init__(self):
        self.somevariable = 0


class myObjWithoutCheck:
    def __init__(self):
        self.somevariable = 0


o = myObjWithoutCheck()

o.somevariable = 2
o.somevaiable = 2   #  This line seems ok ...



o = myObjWithCheck()

o.somevariable = 2
o.somevaiable = 2   #  ... this line raises an error!
