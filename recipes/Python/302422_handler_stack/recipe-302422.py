class Handler (object):
    """The base class for all the handlers"""

    def __init__(self):
        self.data = {}
        self.nextHandler = None

    def __add__(self, newHandler):
        """Used to append handlers to each other"""
        if not isinstance(newHandler, Handler):
            raise TypeError('Handler.__add__() expects Handler')
        if self.nextHandler:
            self.nextHandler + newHandler
        else:
            self.nextHandler = newHandler
            while newHandler:
                newHandler.data = self.data
                newHandler = newHandler.nextHandler
        return self

    def useHook(self, fileName):
        """Wrapper around the hook method"""
        if self.nextHandler:
            if not self.nextHandler.useHook(fileName):
                return False
        else:
            self.data.clear( )
        return self.hook(fileName)

    def hook(self, fileName):
        """Default hook method to be overridden in subclasses"""
        return True

# Subclasses of Handler
import os, time
class Filter (Handler):
    def hook(self, fileName):
        if fileName[-3:] == '.py':
            return True
        else:
            return False
class Processor (Handler):
    def hook(self, fileName):
        modtime = os.path.getmtime(fileName)
        if (time.time()- modtime) < 24*60*60:
            self.data['state']='changed'
            self.data['modtime']=time.ctime(modtime)
        else:
            self.data['state']='unchanged'
        return True
class Logger (Handler):
    def hook(self, fileName):
        print fileName,
        for key in self.data.keys():
            print '%s=%s' % (key, self.data[key]),
        print
        return True

# Script that shows the use of a handler stack
if '__main__'==__name__:
    import sys
    a=Logger( )
    b=Processor( )
    c=Filter( )
    d=a+b+c
    for dirPath, dirNames, fileNames in os.walk(sys.argv[1]):
        for fileName in fileNames:
            d.useHook(os.path.join(dirPath, fileName))
