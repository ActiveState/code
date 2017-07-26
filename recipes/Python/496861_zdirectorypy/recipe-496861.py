'''Support module for working with directories.

This module provides several functions for
copying and pasting directories and files.'''

__version__ = 1.3

################################################################################

import os

class File:

    'File(path) -> new file'

    def __init__(self, path):
        'Initializes a new file object.'
        self.__name = os.path.basename(path)
        self.__data = file(path, 'rb', 0).read()

    def paste(self, path):
        'Creates a new file at path.'
        file(os.path.join(path, self.__name), 'wb', 0).write(self.__data)

class Directory:

    'Directory(path) -> new directory'

    def __init__(self, path):
        'Initializes a new directory object.'
        self.__name = os.path.basename(path)
        self.__data = list()
        for name in os.listdir(path):
            path_name = os.path.join(path, name)
            if os.path.isdir(path_name):
                self.__data.append(Directory(path_name))
            elif os.path.isfile(path_name):
                self.__data.append(File(path_name))

    def paste(self, path):
        'Creates a new directory at path.'
        if self.__name:
            path = os.path.join(path, self.__name)
            os.mkdir(path)
        for item in self.__data:
            item.paste(path)

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
