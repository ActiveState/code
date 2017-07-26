"""tp.py"""
import threading, Queue, inspect

class Pipe(threading.Thread, Queue.Queue):
        def __init__(self, input=None):
                threading.Thread.__init__(self)
                Queue.Queue.__init__(self)

                fnargs = inspect.getargspec(self.fn)[0]
                if input is None and len(fnargs) != 1:
                        raise TypeError, 'no arguments for fn() if pipe is faucet'
                if input is not None and len(fnargs) != 2:
                        raise TypeError, '1 argument for fn() if pipe has input'
                if input is not None and not isinstance(input, Queue.Queue):
                        raise TypeError, 'queue not provided as input'

                self.input = input

        def fn(self):
                """
                this function gets overridden
                must return something to fill the queue with
                """
                pass

        def run(self):
                """
                runs the overridden fn()
                if fn() returns False, put it on the stack and quit
                so any other pipes will get it and pass it on, quitting
                if fn() returns None, don't put anything
                """
                ret = True 
                while ret is not False:
                        if self.input is None: # it's a faucet
                                ret = self.fn()
                        elif hasattr(self.input, 'get'): # it's a pipe
                                ob = self.input.get()
                                if ob is False:
                                        self.put(ob)
                                        break
                                ret = self.fn(ob)
                        if ret is not None: self.put(ret)
