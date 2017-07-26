'''Support module for syncronizing threads.

This module allows access to the Sync class which can
allow automatic sycronization across several threads.'''

__version__ = 1.1

################################################################################

import thread

class Sync:

    'Sync(threads) -> new syncronizer object'

    def __init__(self, threads):
        'x.__init__(...) initializes x'
        self.__threads = threads
        self.__count = 0
        self.__main = thread.allocate_lock()
        self.__exit = thread.allocate_lock()
        self.__exit.acquire()

    def sync(self):
        'Automatically syncronizes threads.'
        self.__main.acquire()
        self.__count += 1
        if self.__count < self.__threads:
            self.__main.release()
        else:
            self.__exit.release()
        self.__exit.acquire()
        self.__count -= 1
        if self.__count > 0:
            self.__exit.release()
        else:
            self.__main.release()

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
