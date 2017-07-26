#!/usr/bin/python

# Helpers

def _addMethod(fldName, clsName, verb, methodMaker, dict):
    """Make a get or set method and add it to dict."""
    compiledName = _getCompiledName(fldName, clsName)
    methodName = _getMethodName(fldName, verb)
    dict[methodName] = methodMaker(compiledName)
    
def _getCompiledName(fldName, clsName):
    """Return mangled fldName if necessary, else no change."""
    # If fldName starts with 2 underscores and does *not* end with 2 underscores...
    if fldName[:2] == '__' and fldName[-2:] != '__':
        return "_%s%s" % (clsName, fldName)
    else:
        return fldName

def _getMethodName(fldName, verb):
    """'_salary', 'get'  => 'getSalary'"""
    s = fldName.lstrip('_') # Remove leading underscores
    return verb + s.capitalize()

def _makeGetter(compiledName):
    """Return a method that gets compiledName's value."""
    return lambda self: self.__dict__[compiledName]

def _makeSetter(compiledName):
    """Return a method that sets compiledName's value."""    
    return lambda self, value: setattr(self, compiledName, value)

class Accessors(type):
    """Adds accessor methods to a class."""
    def __new__(cls, clsName, bases, dict):
        for fldName in dict.get('_READ', []) + dict.get('_READ_WRITE', []):
            _addMethod(fldName, clsName, 'get', _makeGetter, dict)
        for fldName in dict.get('_WRITE', []) + dict.get('_READ_WRITE', []):
            _addMethod(fldName, clsName, 'set', _makeSetter, dict)
        return type.__new__(cls, clsName, bases, dict)

if __name__ == "__main__":
    
    class Employee:
        __metaclass__ = Accessors
        _READ_WRITE = ['name', 'salary', 'title', 'bonus']
        def __init__(self, name, salary, title, bonus=0):
            self.name = name
            self.salary = salary
            self.title = title
            self.bonus = bonus
    b = Employee('Joe Test', 40000, 'Developer')
    print 'Name:', b.getName()
    print 'Salary:', b.getSalary()
    print 'Title:', b.getTitle()
    print 'Bonus:', b.getBonus()
    b.setBonus(5000)
    print 'Bonus:', b.getBonus()

    class ReadOnly:
        __metaclass__ = Accessors
        _READ = ['__data']
        def __init__(self, data):
            self.__data = data
    ro = ReadOnly('test12345')
    print 'Read-only data:', ro.getData()

    class WriteOnly:
        __metaclass__ = Accessors
        _WRITE = ['_data']
        def __init__(self, data):
            self._data = data
    wo = WriteOnly('test67890')
    print 'Write-only data:', wo._data    
    wo.setData('xzy123')
    print 'Write-only data:', wo._data


    
