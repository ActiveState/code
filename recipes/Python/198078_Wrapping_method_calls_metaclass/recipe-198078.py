import re

log = open('log','w')
indent = 0
indStr = '  '

def logmethod(methodname):
    def _method(self,*argl,**argd):
        global indent

        #parse the arguments and create a string representation
        args = []
        for item in argl:
            args.append('%s' % str(item))
        for key,item in argd.items():
            args.append('%s=%s' % (key,str(item)))
        argstr = ','.join(args)   
        print >> log,"%s%s.%s(%s) " % (indStr*indent,str(self),methodname,argstr)
        indent += 1
        # do the actual method call
        returnval = getattr(self,'_H_%s' % methodname)(*argl,**argd)
        indent -= 1
        print >> log,'%s:'% (indStr*indent), str(returnval)
        return returnval

    return _method


class LogTheMethods(type):
    def __new__(cls,classname,bases,classdict):
        logmatch = re.compile(classdict.get('logMatch','.*'))
        
        for attr,item in classdict.items():
            if callable(item) and logmatch.match(attr):
                classdict['_H_%s'%attr] = item    # rebind the method
                classdict[attr] = logmethod(attr) # replace method by wrapper

        return type.__new__(cls,classname,bases,classdict)

class Test(object):
    __metaclass__ = LogTheMethods
    logMatch = '.*'

    def __init__(self):
        self.a = 10

    def meth1(self):pass
    def add(self,a,b):return a+b
    def fac(self,val): # faculty calculation
        if val == 1:
            return 1
        else:
            return val * self.fac(val-1)

if __name__ == '__main__':
    l = Test()
    l.meth1()
    print l.add(1,2)
    print l.fac(10)
