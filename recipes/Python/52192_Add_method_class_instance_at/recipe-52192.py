import string
import new

def __str__(self):
    classStr = ''
    for name, value in self.__class__.__dict__.items( ) + self.__dict__.items( ): 
        classStr += string.ljust( name, 15 ) + '\t' + str( value ) + '\n'
    return classStr

def addStr(anInstance):
    anInstance.__str__ = new.instancemethod(__str__, anInstance, anInstance.__class__)

# Test it

class TestClass:
    classSig = 'My Sig'
    def __init__(self, a = 1, b = 2, c = 3 ):
        self.a = a
        self.b = b
        self.c = c
    
test = TestClass()
addStr( test )
print test
