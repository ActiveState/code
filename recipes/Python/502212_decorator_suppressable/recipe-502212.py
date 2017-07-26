import logging

log = logging.getLogger('decorators') # or whatever you want

class UnhandledSuppression(Exception):
    '''
    this is strictly for handling situations where your
    potentially-suppressed function returns a value.
    if the function is suppressed, variable = suppressedFunc(somevars)
    would contain an invalid value, which could screw up your code.
    so this is thrown, intended to be caught and handled
    '''
    pass

def suppressable(fn):
    decoratorobj = _Suppressable(fn)
    def wrapper(*args, **kwargs):
        return decoratorobj(*args, **kwargs)
    return wrapper
    
class _Suppressable(object):
    '''
    useful in tandem with optparse to parse options and
    suppress certain checks based on command-line variables
    '''
    __suppress = False
    def __init__(self, fn):
        self.fn = fn
        
    def __call__(self, *args, **kwargs):
        '''the actual decorator'''
        if _Suppressable.__suppress:
            log.debug('skipping %s' % repr(self.fn.__name__))
            raise UnhandledSuppression
        else: return self.fn(*args, **kwargs)
    @classmethod
    def suppress(cls, expr):
        cls.__suppress = expr

## EXAMPLE
#from optparse import OptionParser

#usage = 'usage: %prog [options]'
#version = '%prog 0.1'
#parser = OptionParser(usage, version=version)

#parser.add_option('-s', '--suppress', action='store_true', dest='suppress', default=False, help='suppress certain checks')

#options, args = parser.parse_args()
#Suppressable.suppress(options.suppress)

#class SomeProcedure(object):
    #def __init__(self):
        #pass
        
    #def run(self):
        #try: self.doCheck1()
        #except: pass
        
        #try:
            #if self.doCheck2() is False:
                #return
        #except: pass
        
        #self.__actuallyRun()
        
    #def __actuallyRun(self):
        #pass
    
    #@suppressable
    #def doCheck1(self):
        #pass
    
    #@suppressable
    #def doCheck2(self):
        #return False
    
#procedure = SomeProcedure()

## skips checks if the user specified supression
#procedure.run()
