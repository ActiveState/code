'''Support module for GUI programming.

This module provides access to the Delegate class
that was inspired by the C# programming language.'''

__version__ = 1.1

################################################################################

class Delegate:

    'Delegate(target, *args, **kwargs) -> new delegate'
    
    def __init__(self, target, *args, **kwargs):
        'x.__init__(...) initializes x'
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        
    def __call__(self, *args, **kwargs):
        'x.__call__(*args, **kwargs) <==> x(*args, **kwargs)'
        if args or kwargs:
            return self.__target(*args, **kwargs)
        else:
            return self.__target(*self.__args, **self.__kwargs)
        
    def args(self, *args):
        'Sets args called on target.'
        self.__args = args
        return self
        
    def kwargs(self, **kwargs):
        'Sets kwargs called on target.'
        self.__kwargs = kwargs
        return self

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
