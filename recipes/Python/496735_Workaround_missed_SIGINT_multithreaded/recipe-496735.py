import threading, time, os, signal, sys, operator

class MyThread(threading.Thread):
    """this is a wrapper for threading.Thread that improves
    the syntax for creating and starting threads.
    """
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()

class Watcher:
    """this class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and the process that contains the
    threads.  See Appendix A of The Little Book of Semaphores.
    http://greenteapress.com/semaphores/

    I have only tested this on Linux.  I would expect it to
    work on the Macintosh and not work on Windows.
    """
    
    def __init__(self):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            print 'KeyBoardInterrupt'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError: pass


def counter(xs, delay=1):
    """print the elements of xs, waiting delay seconds in between"""
    for x in xs:
        print x
        time.sleep(delay)


def main(script, flag='with'):
    """This example runs two threads that print a sequence, sleeping
    one second between each.  If you run it with no command-line args,
    or with the argument 'with', you should be able it interrupt it
    with Control-C.

    If you run it with the command-line argument 'without', and press
    Control-C, you will probably get a traceback from the main thread,
    but the child thread will run to completion, and then print a
    traceback, no matter how many times you try to interrupt.
    """

    if flag == 'with':
        Watcher()
    elif flag != 'without':
        print 'unrecognized flag: ' + flag
        sys.exit()
    
    t = range(1, 10)

    # create a child thread that runs counter
    MyThread(counter, t)

    # run counter in the parent thread
    counter(t)

if __name__ == '__main__':
    main(*sys.argv)
