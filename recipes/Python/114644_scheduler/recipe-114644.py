import time
import threading

class Task( threading.Thread ):
    def __init__( self, action, loopdelay, initdelay ):
        self._action = action
        self._loopdelay = loopdelay
        self._initdelay = initdelay
        self._running = 1
        threading.Thread.__init__( self )

    def __repr__( self ):
        return '%s %s %s' % (
            self._action, self._loopdelay, self._initdelay )

    def run( self ):
        if self._initdelay:
            time.sleep( self._initdelay )
        self._runtime = time.time()
        while self._running:
            start = time.time()
            self._action()
            self._runtime += self._loopdelay
            time.sleep( self._runtime - start )

    def stop( self ):
        self._running = 0
    
class Scheduler:
    def __init__( self ):
        self._tasks = []
        
    def __repr__( self ):
        rep = ''
        for task in self._tasks:
            rep += '%s\n' % `task`
        return rep
        
    def AddTask( self, action, loopdelay, initdelay = 0 ):
        task = Task( action, loopdelay, initdelay )
        self._tasks.append( task )
    
    def StartAllTasks( self ):
        for task in self._tasks:
            task.start()
    
    def StopAllTasks( self ):
        for task in self._tasks:
            print 'Stopping task', task
            task.stop()
            task.join()
            print 'Stopped'

if __name__ == '__main__':

    def timestamp( s ):
        print '%.2f : %s' % ( time.time(), s )
    
    def Task1():
        timestamp( 'Task1' )

    def Task2():
        timestamp( '\tTask2' )

    def Task3():
        timestamp( '\t\tTask3' )
    
    s = Scheduler()

    #           task    loopdelay   initdelay 
    # ---------------------------------------
    s.AddTask(  Task1,  1.0,        0       )
    s.AddTask(  Task2,  0.5,        0.25    )
    s.AddTask(  Task3,  0.1,        0.05    )

    print s
    s.StartAllTasks()
    raw_input()
    s.StopAllTasks()
