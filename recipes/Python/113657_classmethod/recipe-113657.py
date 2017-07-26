def classmethod(method):
    return lambda self, *args, **dict: method(self.__class__, *args, **dict)

class Singleton:
    count = 0
    def __init__(klass):
        klass.count += 1
        print klass, klass.count
    __init__ = classmethod(__init__)

    def __getattr__(klass, name):
        return getattr(klass, name)
    __getattr__ = classmethod(__getattr__)
    
    def __setattr__(klass, name, value):
        setattr(klass, name, value)
    __setattr__ = classmethod(__setattr__)

c = Singleton()
d = Singleton()
c.test = 'In d?'
print 'c.test', c.test
print 'd.test', d.test

output = '''
junk.Singleton 1
junk.Singleton 2
c.test In d?
d.test In d?
'''
