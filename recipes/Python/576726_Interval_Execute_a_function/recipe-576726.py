import threading
from time import sleep

def intervalExecute(interval, func, *args, **argd):
    ''' @param interval: execute func(*args, **argd) each interval
        @return: a callable object to enable you terminate the timer.
    '''
    cancelled = threading.Event()
    def threadProc(*args, **argd):
        while True:
            cancelled.wait(interval)
            if cancelled.isSet():
                break
            func(*args, **argd) #: could be a lenthy operation
    th = threading.Thread(target=threadProc, args=args, kwargs=argd)
    th.start()
    def close(block=True, timeout=3):
        ''' @param block: if True, block the caller until the thread 
                          is closed or time out
            @param timout: if blocked, timeout is used
            @return: if block, True -> close successfully; False -> timeout
                     if non block, always return False
        '''
        if not block:
            cancelled.set()
            return False
        else:
            cancelled.set()
            th.join(timeout)
            isClosed = not th.isAlive()
            return isClosed
    return close

if __name__=='__main__':
    # sample usage is as follow....
    
    def testFunc(identifier, txt=''):
        print 'test func entered'
        sleep(2)
        print identifier, txt

    cancellObj = intervalExecute(2.0, testFunc, 1, 'haha')
    help(cancellObj)
    sleep(5.2)
    print cancellObj() #: cancel the intervalExecute timer.
    print 'after calling close'
