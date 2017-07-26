# junk.py

def classmethod(method):
    '''Impulate py2.2 classmethod function. -> class method'''
    return lambda self, *args, **dict: method(self.__class__, *args, **dict)

class Foo:
    def bar(klass):
        print 'In', klass, 'bar()'
    bar = classmethod(bar)

Foo().bar()

output = '''
In junk.Foo bar()
'''
