"""
Defines a decorator, synchronous, that allows calls to methods
of a class to be synchronized using an instance based lock.
tlockname must refer to an instance variable that is some
kind of lock with methods acquire and release.  For thread safety this
would normally be a threading.RLock.

"""

from functools import wraps

def synchronous( tlockname ):
    """A decorator to place an instance based lock around a method """

    def _synched(func):
        @wraps(func)
        def _synchronizer(self,*args, **kwargs):
            tlock = self.__getattribute__( tlockname)
            tlock.acquire()
            try:
                return func(self, *args, **kwargs)
            finally:
                tlock.release()
        return _synchronizer
    return _synched

#-----------------------------------------------------------------
# Usage Examples:

if __name__ == "__main__":
    import threading

    class MyClass(object):
        mm = 0
        def __init__(self):
            self.mylock = threading.RLock()
            self.myList = []
            self.n = 0

        @synchronous('mylock')
        def addToMyList(self, item):
            self.n = self.n+1
            self.__class__.mm = self.mm+1
            time.sleep(0.01)
            self.myList.append(str(self.n)+str(self.mm)+item)
            self.n = self.n-1
            self.__class__.mm = self.mm-1

        @synchronous('mylock')
        def popListItem(self):
            return self.myList.pop(0)

#Within any instance of MyClass, the methods addToMyList and
#popListItem cannot be invoked at the same time (via different threads).

    class Class2(object):
        classlock = threading.RLock()
        mm = 0

        def __init__(self):
            self.myList = []
            self.n = 0

        @synchronous('classlock')
        def addToMyList(self, item):
            self.n = self.n+1
            self.__class__.mm = self.mm+1
            time.sleep(0.01)
            self.myList.append(str(self.n)+str(self.mm)+item)
            self.n = self.n-1
            self.__class__.mm = self.mm-1

        @synchronous('classlock')
        def popListItem(self):
            return self.myList.pop(0)

# In the above example all instances use the same class based lock.

# The decorator may be used to synchronize methods of an existing class
# by subclassing the class, with the __init__ method creating the lock
# and the methods that are to be synchronized redeclared, as in the following.

    #Existing unsynchronized class---
    class SomeBase(object):
        mm = 0

        def __init__(self, arg1):
            self.arg1 = arg1
            self.myList = []
            self.n = 0

        def addToMyList(self, item):
            self.n = self.n+1
            self.__class__.mm = self.mm+1
            time.sleep(0.01)
            self.myList.append(str(self.n)+str(self.mm)+item)
            self.n = self.n-1
            self.__class__.mm = self.mm-1

        def popListItem(self):
            return self.myList.pop(0)

    #Derived synchronous class---
    class SafeSomeBase(SomeBase):
        def __init__(self, arg1):
            SomeBase.__init__(self,arg1)
            self.instlock = threading.RLock()

        addToMyList = synchronous('instlock')(SomeBase.addToMyList)
        popListItem = synchronous('instlock')(SomeBase.popListItem)


    plock = threading.RLock()

    import time
    def threadProc( name, baseobj ):
        popped=[]
        tsleep = .05 + ((ord(name[0])+ord(name[3]))%11)*.01
        for j in range(5):
            baseobj.addToMyList( name+str(j) )
            time.sleep(tsleep)
            try:
                popped.append(baseobj.popListItem())
            except Exception, ex:
                print ex
            time.sleep(.13);

        time.sleep(1.0)
        plock.acquire()
        print name, popped
        plock.release()

    def synchTest(thrdnames, synchlist):
        threads=[]
        ix = 0
        for n in thrdnames:
           synched = synchlist[ix]
           ix = (ix+1) % len(synchlist)
           thrd = threading.Thread(target=threadProc, name = n, args=(n, synched))
           threads.append( thrd)

        for thread in threads:
            thread.start()

#        for av in range(22):
#            lcpy = []
#            lcpy.extend(synched.myList)
#            print lcpy
#            time.sleep(.056)
            
        for thread in threads:
            thread.join()

        ok = raw_input("Next? ")

    thrdnames = "Karl Nora Jean Lena Bart Dawn Owen Dave".split()
    synched = [MyClass(), MyClass()]
    synchTest(thrdnames, synched)

    synched = [Class2(), Class2()]
    synchTest(thrdnames, synched)
    
    synched = [SafeSomeBase('alph'),SafeSomeBase('beta')]
    synchTest(thrdnames, synched)
    
    synched = [SomeBase('alph'), SomeBase('beta')]
    synchTest(thrdnames, synched)
