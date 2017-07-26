'''Support module for array and matrix use.

This module provides two classes that emulate one and two
dimentional lists with fixed sizes but mutable internals.'''

__version__ = 1.2

################################################################################

class Array:

    'Array(length[, value]) -> new array'

    def __init__(self, length, value=None):
        'x.__init__(...) initializes x'
        assert type(length) is int and length > 0
        self.__data = [value for index in range(length)]

    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return repr(self.__data)

    def __len__(self):
        'x.__len__() <==> len(x)'
        return len(self.__data)

    def __getitem__(self, index):
        'x.__getitem__(i) <==> x[i]'
        return self.__data[index]

    def __setitem__(self, index, value):
        'x.__setitem__(i, y) <==> x[i]=y'
        self.__data[index] = value

    def __delitem__(self, index):
        'x.__delitem__(i) <==> del x[i]'
        self.__data[index] = None

    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return iter(self.__data)

    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        return value in self.__data

class Matrix:

    'Matrix(rows, columns[, value]) -> new matrix'

    def __init__(self, rows, columns, value=None):
        'x.__init__(...) initializes x'
        assert type(rows) is int and rows > 0
        self.__data = [Array(columns, value) for index in range(rows)]

    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return repr(self.__data)

    def __len__(self):
        'x.__len__() <==> len(x)'
        return len(self.__data)

    def __getitem__(self, index):
        'x.__getitem__(i) <==> x[i]'
        return self.__data[index]

    def __setitem__(self, index, value):
        'x.__setitem__(i, y) <==> x[i]=y'
        self.__data[index] = Array(len(self.__data[index]), value)

    def __delitem__(self, index):
        'x.__delitem__(i) <==> del x[i]'
        self.__data[index] = Array(len(self.__data[index]))

    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return iter(self.__data)

    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        for item in self.__data:
            if value in item:
                return True
        return False

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
