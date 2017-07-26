#!/usr/bin/env python

"""worker.py: Executes inline code across multiple execution contexts.

The inline code to be executed is contained in a generator, which contains a
`yield` statement to signal each context change. A decorator added to the
generator function wraps the returned generator in the executor when the
generator function is called. Calling the returned executor iterates the
generator to completion, handling the context switching at each `yield`. The
executor and generator can communicate values through the `yield` statements
and `send()` method of the generator.

An example is provided of an executor which executes alternate iterations of a
generator asynchronously (in a `Thread`) and synchronously (in an event loop).

References:
http://code.activestate.com/recipes/576952/ [inline asynchronous code]
"""

import threading
from sys import exc_info
from traceback import print_exc
from functools import partial, wraps
from Queue import Queue, Empty

if __name__ == '__main__':
    import optparse
    from time import sleep

__version__ = '$Revision: 2539 $'.split()[1]

__usage__ = 'usage: %prog [options]'


def execute(exec_factory, *exargs, **exkeys):
    """Wrap a returned generator in an executor.

    The returned executor can then be called to iterate the generator to
    completion. The executor should also implement the signature of the
    returned generator.

    The `exec_factory` argument is a callable (such as a class or function)
    which takes a generator as its first argument and returns a callable
    executor.

    Generator functions decorated with `execute` can be passed arguments in
    three different places:
    * in the decorator (`exargs` and `exkeys`); these arguments are passed to
        `exec_factory` when the executor is instantiated;
    * in the call to the wrapped generator function; these arguments are
        passed unchanged when instantiating the generator; and
    * in the call to the executor returned by the wrapped generator function.
    """
    def exec_wrapper(generator):
        @wraps(generator)
        def work_factory(*genargs, **genkeys):
            work_iter = generator(*genargs, **genkeys)
            return exec_factory(work_iter, *exargs, **exkeys)
        return work_factory
    return exec_wrapper


class Executor:
    """A skeletal base class for executors.

    Delegates to the enclosed generator so as not to change the signature.
    Subclasses must implement the `_execute()` method.
    """
    def __init__(self, generator, exc_handler=print_exc):
        """Construct an executor.

        If `exc_handler` is not `None` and any method of the generator raises
        an exception other than `StopIteration`, `exc_handler` will be called;
        otherwise, exceptions (including `StopIteration`) are reraised to the
        caller. Thus, an implementation of Executor can call the exception
        handler by calling `self.throw(*sys.exc_info())`; the exception will
        be handled by the generator, handled by the exception handler (if
        any), or thrown back to the caller.
        """
        self.__generator = generator
        self.__executing = False
        self.__exc_handler = exc_handler
        self.__throw = generator.throw
        self.__send = generator.send
        self.__next = generator.next
        self.__close = generator.close

    def __iter__(self): return self

    def __call_gen(self, method, *args, **keys):
        """If the generator exits, discard it and call `_handle_exit()`."""
        if not self.stopped():
            try:
                return method(*args, **keys)
            except StopIteration:
                return self._handle_exit(True)
            except:
                return self._handle_exit(False)
        elif self.__exc_handler is None: raise StopIteration()
        else: return None

    def __call__(self, *args, **keys):
        """Start the executor. May only be called once per executor.

        Returns the excutor, as a convenience for chained calls.

        Subclasses should not override this method, but should implement the
        `_execute()` method to iterate the generator to completion, changing
        contexts as appropriate at each `yield` statement.

        If the `exc_handler` key is present, it will be removed and will
        override the default exception handler.
        """
        if not self.__executing:
            self.__executing = True
            exc_handler = keys.pop('exc_handler', None)
            if exc_handler is not None: self.__exc_handler = exc_handler
            try:
                self._execute(*args, **keys)
            except:
                self.throw(*exc_info())
        else:
            raise ValueError("executor already executing." if self.__generator else "executor already complete.")
        return self

    def _execute(self):
        """Start the executor.

        Subclasses must implement the `_execute()` method to iterate the
        generator to completion, changing contexts as appropriate at each
        `yield` statement.
        """
        raise NotImplementedError, "_execute() must be implemented in subclass"

    def _handle_exit(self, isStop=False):
        """Handle a generator exit.

        Discards the generator, so that generator exit can be checked by
        calling `stopped()`, rather than wrapping every call to the generator
        in a `try...except` clause. Calls `exc_handler` if the generator
        raises an exception other than `StopIteration`; reraises exceptions
        (including `StopIteration`) if `exc_handler` is None.

        `isStop` is `True` if the generator raised `StopIteration`.
        """
        self.__generator = None
        if not self.__exc_handler: raise
        elif not isStop: self.__exc_handler()
        return None

    def stopped(self):
        """Check whether the generator has exited."""
        return self.__generator is None

    def throw(self, *args, **keys):
        """If the generator exits, discard it and call `_handle_exit()`."""
        return self.__call_gen(self.__throw, *args, **keys)

    def close(self):
        """If the generator exits, discard it and call `_handle_exit()`."""
        return self.__call_gen(self.__close)

    def next(self):
        """If the generator exits, discard it and call `_handle_exit()`."""
        return self.__call_gen(self.__next)

    def send(self, value):
        """If the generator exits, discard it and call `_handle_exit()`."""
        return self.__call_gen(self.__send, value)


class ThreadExecutor(Executor):
    """Executes alternate iterations asynchonously and synchronously.

    Asynchronous iterations are executed in a separate thread; synchronous
    iterations are executed through a callable, which usually queues into an
    event queue.
    """
    def __init__(self, generator, synchronizer, exc_handler=print_exc):
        """Construct a threaded executor.

        `synchronizer` is a callable which executes a callable passed to it in
        the synchronous context, usually by queueing the passed callable in an
        event dispatch queue.
        """
        self.__synchronizer = synchronizer
        Executor.__init__(self, generator, exc_handler)

    def _execute(self):
        """Check for exit, iterate once in a separate thread, and call `__finish()`."""
        if not self.stopped():
            try:
                threading.Thread(target=lambda:(self.next(), self.__finish())).start()
            except:
                self.throw(*exc_info())

    def __finish(self):
        """Check for exit, iterate once in the synchronous context, and call `self()`."""
        if not self.stopped():
            try:
                self.__synchronizer(lambda:(self.next(), self._execute()))
            except:
                self.throw(*exc_info())


class GeneratorWrapper(Executor):
    """An executor which turns a generator into a callable."""
    def __init__(self, generator, iterate_once=False, exc_handler=None):
        """If `iterate_once` is `True`, the generator is iterated once (by
        calling `next()`) immediately after construction, in order to be able
        to pass the parameters of the first `__call__()` to the generator by
        calling `send()`. Any yielded value is discarded. Note that if the
        first `__call__()` passes no arguments or a single `None`, the first
        iteration will succeed, and the generator need not be iterated once to
        initialize it.

        Note also that the default exception handler for a wrapper is `None`,
        so that exceptions are raised to the caller of `__call__()`.
        """
        Executor.__init__(self, generator, exc_handler)
        if iterate_once: generator.next()

    def __call__(self, *args, **keys):
        """Iterate the generator.

        Packages the parameters in the most reasonable fashion, calls
        `next()` or `send()`, and returns the yielded value.

        Overrides `__call__()` rather than `_execute()`, because it doesn't
        iterate to completion.
        """
        if not keys:
            if not args:
                return self.next()
            elif len(args) == 1:
                return self.send(args[0])
            else:
                return self.send(args)
        else:
            if not args:
                return self.send(keys)
            else:
                return self.send((args, keys))


class QueuedGeneratorWrapper:
    """Call `task_done()` on a `Queue` when the generator terminates."""
    def __init__(self, generator, queue):
        self.__generator = generator
        self.__queue = queue

    def __call_gen(self, method, *args, **keys):
        if self.__generator is not None:
            try:
                return method(*args, **keys)
            except:
                self.__generator = None
                self.__queue.task_done()
                raise
        else: raise StopIteration()

    def __getattr__(self, attr):
        """Delegate to the generator."""
        if self.__generator is None:
            raise AttributeError("no generator in QueuedGeneratorWrapper")
        else:
            attr = getattr(self.__generator, attr)
            return partial(QueuedGeneratorWrapper.__call_gen, self, attr) if callable(attr) else attr


class ExecutionQueue(Queue):
    """A queue of Executors which are dequeued and executed in sequence.

    An instance of this class can be passed to the `@execute` decorator,
    followed by the executor factory and its arguments that will be used to
    execute the decorated generator function.  When the executors returned by
    the decorated generator functions are called, they will be queued for
    execution rather than executing immediately.
    """
    def __init__(self, *qargs, **qkeys):
        """Construct an execution queue.

        `qargs` and `qkeys` are passed to the underlying `Queue` object.
        """
        Queue.__init__(self, *qargs, **qkeys)
        self.__current_exec = None
        self.__exec_mutex = threading.Lock()

    def __call__(self, generator, exec_class, *exargs, **exkeys):
        """Create an executor and return a function which will queue it.

        Wrap the generator in an object which starts the next queued executor
        when it exits.
        """
        executor = exec_class(QueuedGeneratorWrapper(generator, self), *exargs, **exkeys)
        return lambda *args, **keys: self.put_nowait((executor, args, keys))

    def task_done(self):
        """Start up the next task in the queue as each one completes."""
        Queue.task_done(self)
        self.__next(isRunning=True)

    def put(self, item, *args, **kwargs):
        """Queue an executor, along with its arguments.

        Start executing the queue if this is the first entry."""
        Queue.put(self, item, *args, **kwargs)
        self.__next()

    def flush(self):
        """Empty the execution queue and then close the current executor.

        Calls `close()` on all executors in the queue (after calling `next()`
        to initialize them) as well as the running executor. Executors should
        clean up when `close()` is called, and the associated generators must
        catch the resulting `GeneratorExit` exception and clean up.
        """
        self.__exec_mutex.acquire()
        try:
            while True:
                # Empty the execution queue, closing all queued generators
                qexec, args, keys = self.get_nowait()
                qexec.next()
                qexec.close()
        except Empty:
            # Close the current executor; the executor is responsible for cleanup.
            if self.__current_exec is not None:
                self.__current_exec.close()
                self.__current_exec = None
        finally:
            self.__exec_mutex.release()

    def executing(self):
        self.__exec_mutex.acquire()
        try:
            return self.__current_exec is not None
        finally:
            self.__exec_mutex.release()

    def __next(self, isRunning=False):
        """Dequeue and start the next executor.

        `isRunning` is checked against the current execution status before
        dequeuing and starting the next executor."""
        self.__exec_mutex.acquire()
        if isRunning != (self.__current_exec is None):
            try:
                self.__current_exec, args, keys = self.get_nowait()
            except Empty:
                self.__current_exec = None
                return
            finally:
                self.__exec_mutex.release()
            self.__current_exec(*args, **keys)
        else:
            self.__exec_mutex.release()


if __name__ == '__main__':
    optparser = optparse.OptionParser(usage=__usage__, version=__version__)
    optparser.disable_interspersed_args()
    optparser.add_option('--workers', type='int', metavar='N', default=4,
            help='Number of workers to create [%default]')
    optparser.add_option('--loops', type='int', metavar='N', default=2,
            help='Number of times to iterate each worker [%default]')
    optparser.add_option('--looptime', type='float', metavar='SECONDS', default=0.5,
            help='Timeout for event loop [%default sec]')
    optparser.add_option('--worktime', type='float', metavar='SECONDS', default=2.0,
            help='Worker delay to simulate work [%default sec]')
    (options, args) = optparser.parse_args()

    printLock = threading.Lock()
    eventq = Queue()
    execq = ExecutionQueue()

    def printThread(name, action):
        printLock.acquire()
        print "%s loop %s in %s of %d threads" % (name, action,
            threading.currentThread().getName(), threading.activeCount())
        printLock.release()

    def loop(looptime=0.5):
        """A simple event queue loop."""
        while threading.activeCount() > 1 or not eventq.empty():
            try:
                next = eventq.get(timeout=looptime)
                printThread(" Event", "executing event")
                if callable(next): next()
            except Empty:
                printThread(" Event", "running")

    @execute(execq, ThreadExecutor, eventq.put, exc_handler=None)
    def work(wnum, loops=2, worktime=2.0):
        for count in range(loops):
            # Work performed in separate thread
            printThread("Worker %d loop %d" % (wnum+1, count+1), "starting")
            sleep(worktime)
            printThread("Worker %d loop %d" % (wnum+1, count+1), "ending")
            yield True
            # Work performed in event queue
            printThread("Worker %d loop %d" % (wnum+1, count+1), "finishing")
            yield True

    # Create and queue the workers, and then loop the event queue
    for x in range(options.workers):
        work(x, loops=options.loops, worktime=options.worktime)(exc_handler=print_exc)
    loop(looptime=options.looptime)
