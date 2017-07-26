#idle_queue.py

import Queue

#Global queue, import it from anywhere, you get the same object instance.
idle_loop = Queue.Queue()

def idle_add(func, *args, **kwargs):
    def idle():
        func(*args, **kwargs)
        return False
    idle_loop.put(idle)


#weak_ref.py

import weakref


class _BoundMethodWeakref:
    def __init__(self, func):
        self.func_name = func.__name__
        self.wref = weakref.ref(func.__self__) #__self__ returns the class

    def __call__(self):
        func_cls = self.wref()
        if func_cls is None: #lost reference
            return None
        else:
            func = getattr(func_cls, self.func_name)
            return func

def weak_ref(callback):
    if hasattr(callback, '__self__') and callback.__self__ is not None: #is a bound method?
        return _BoundMethodWeakref(callback)
    else:
        return weakref.ref(callback)


#event.py

import threading
#import logging
#logger = logging.getLogger(__name__)

import idle_queue
from weak_ref import weak_ref


class Event:
    def __init__(self, name):
        self.name = name
        self.callbacks = []
        self.lock = threading.Lock()

    def connect(self, callback):
        with self.lock:
            callback = weak_ref(callback)
            self.callbacks.append(callback)

    def disconnect(self, callback):
        with self.lock:
            for index, weakref_callback in enumerate(self.callbacks):
                if callback == weakref_callback():
                    del self.callbacks[index]
                    break

    def emit(self, *args, **kwargs):
        with self.lock:
            #logger.debug("Event emitted: {}".format(self.name))
            for weakref_callback in self.callbacks[:]:
                callback = weakref_callback()
                if callback is not None:
                    idle_queue.idle_add(callback, *args, **kwargs)
                else: #lost reference
                    self.callbacks.remove(weakref_callback)
            #if not self.callbacks:
                #logger.debug("No signals assosiated to: {}".format(self.name))


#events.py

import Event


class _Events:
    #add some signals, example:
    #do_something = Event('do something') #args: my_arg1, my_arg_list2, my_arg_str3
    quit_app = Event('quit app') #args: some_arg

events = _Events()

if __name__ == "__main__":
    def quit(some_arg):
        print some_arg
        sys.exit(0)

    events.quit_app.connect(quit) #connect the callback/slot
    #events.quit_app.disconnect(quit) #disconnect
    something = "goodbye"
    events.quit_app.emit(something) #emit the signal
    
    #this should go in your main thread loop if your are using a gui.
    #example: http://code.activestate.com/recipes/578299-pyqt-pyside-thread-safe-global-queue-main-loop-int/
    callback = idle_loop.get()
    callback() #dispatch the event
