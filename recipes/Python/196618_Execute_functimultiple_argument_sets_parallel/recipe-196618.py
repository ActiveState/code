import random
import sys
import threading
import time
import types

class Thread( threading.Thread ):
    def  __init__( self, target, args=() ):
         if type( args ) <> types.TupleType:
            args = (args,)
         threading.Thread.__init__( self, target=target, args=args )

class LockedIterator:
    def __init__( self, iterator ):
        self._lock     = threading.Lock()
        self._iterator = iterator

    def __iter__( self ):
        return self

    def next( self ):
        try:
            self._lock.acquire()
            return self._iterator.next()
        finally:
            self._lock.release()

class MultiThread:
    def __init__( self, function, argsVector, maxThreads=5 ):
        self._function     = function
        self._argsIterator = LockedIterator( iter( argsVector ) )
        self._threadPool   = []
        for i in range( maxThreads ):
            self._threadPool.append( Thread( self._tailRecurse ) )

    def _tailRecurse( self ):
        for args in self._argsIterator:
            self._function( args ) 

    def start( self ):
        for thread in self._threadPool:
            time.sleep( 0 ) # necessary to give other threads a chance to run
            thread.start()

    def join( self, timeout=None ):
        for thread in self._threadPool:
            thread.join( timeout )

def recite_n_times_table( n ):
    for i in range( 1, 13 ):
        print "%d * %d = %d" % (n, i, n * i)
        time.sleep( 0.5 + random.random() )

if __name__=="__main__":
   mt = MultiThread( recite_n_times_table, range( 1, 13 ) )
   mt.start()
   mt.join()
   print "Well done kids!" 
