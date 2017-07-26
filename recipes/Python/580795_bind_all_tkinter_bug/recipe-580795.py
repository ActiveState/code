from __future__ import print_function

import sys
import collections
import functools

_handlers = collections.defaultdict(list)

def _run_handlers(list_of_handlers, event):
    exc_info = None
    for func in list_of_handlers:
        try:
            func(event)
        except SystemExit:
            exc_info = sys.exc_info()
        except:
            import traceback
            print("Error in global_binding._run_handlers:", file=sys.stderr)
            traceback.print_exc()
            exc_info = sys.exc_info()

    if exc_info is not None:
        raise exc_info[0], exc_info[1], exc_info[2]


def global_bind(w, event, func, add=None):
    root = w.nametowidget(".")
    
    handlers_of_event = _handlers[event]
    if len(handlers_of_event) == 0:
        root.bind_all(event, functools.partial(_run_handlers, handlers_of_event))
    
    if add == "+":
        handlers_of_event.append(func)
    else:
        handlers_of_event[:] = [func]

    return func

def global_unbind(w, event, func):
    handlers_of_event = _handlers[event]
    handlers_of_event.remove(func)
    
    if len(handlers_of_event) == 0:
        w.unbind_all(event)
        
if __name__ == "__main__":
    try:
        from Tkinter import Tk, Frame
    except ImportError:
        from tkinter import Tk, Frame
        
    root = Tk()
    f = Frame(root, width= 300, height=300)
    f.pack()
    
    def callback1(event):
        print("callback1")
        
    def callback2(event):
        print("callback2")
    
    def callback3(event):
        print("callback3")
        
    global_bind(root, "<1>", callback1, add="+")
    global_bind(f, "<1>", callback2, add="+")
    global_bind(f, "<1>", callback3, add="+")
    
    global_unbind(f, "<1>", callback1)
    
    root.mainloop()
