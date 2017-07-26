# Author: Miguel Martinez Lopez
#
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))


"""
I provide in this module the function "tk_call_async".

"tk_call_async" executes the function "computation" asyncronously with the provided "args" and "kwargs" without blocking the tkinter event loop.
If "callback" is provided, it will be called with the result when the computation is finnished. 
If an exception is raised during computation, instead errback will be called.
"Polling" will be the frequency to poll to check for results.
There is two methods to execute the task: using multiprocessing or using threads.
"""

import traceback
import threading

# Python 3 support
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

MULTIPROCESSING = 0
THREADS = 1

def tk_call_async(window, computation, args=(), kwargs={}, callback=None, errback=None, polling=500, method=MULTIPROCESSING):
    if method == MULTIPROCESSING:
        # I use threads because on windows creating a new python process freezes a little the event loop.
        future_result= Queue()

        worker = threading.Thread(target=_request_result_using_multiprocessing, args=(computation, args, kwargs, future_result))
        worker.daemon = True
        worker.start()
    elif method == THREADS:
        future_result = _request_result_using_threads(computation, args=args, kwargs=kwargs)
    else:
        raise ValueError("Not valid method")

    
    if callback is not None or errback is not None:
        _after_completion(window, future_result, callback, errback, polling)
        
    return future_result

def _request_result_using_multiprocessing(func, args, kwargs, future_result):
    import multiprocessing

    queue= multiprocessing.Queue()

    worker = multiprocessing.Process(target=_compute_result, args=(func, args, kwargs, queue))
    worker.daemon = True
    worker.start()

    return future_result.put(queue.get())

def _request_result_using_threads(func, args, kwargs):
    future_result= Queue()

    worker = threading.Thread(target=_compute_result, args=(func, args, kwargs, future_result))
    worker.daemon = True
    worker.start()

    return future_result


def _after_completion(window, future_result, callback, errback, polling):
    def check():
        try:
            result = future_result.get(block=False)
        except:
            window.after(polling, check)
        else:
            if isinstance(result, Exception):
                if errback is not None:
                    errback(result)
            else:
                if callback is not None:
                    callback(result)
                
    window.after(0, check)

def _compute_result(func, func_args, func_kwargs, future_result):
    try: 
        _result = func(*func_args, **func_kwargs)
    except Exception as errmsg:
        _result = Exception(traceback.format_exc())

    future_result.put(_result)


# Multiprocessing uses pickle on windows.
# A pickable function should be in top module or imported from another module.
# This is requirement is not mandatory on Linux because python uses behind the scenes the fork operating system call.
# But on Windows it uses named pipes and pickle.


def _example_calculation(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return _example_calculation(n-1)+_example_calculation(n-2)

if __name__ == "__main__":
    try:
        from Tkinter import Tk, Frame, Entry, Label, Button, IntVar, StringVar, LEFT
        import tkMessageBox as messagebox
    except ImportError:
        from tkinter import Tk, Frame, Entry, Label, Button, IntVar, StringVar, LEFT
        from tkinter import messagebox

    disabled = False

    def calculate_fibonacci():
        global disabled
        if disabled:
            messagebox.showinfo("warning", "It's still calculating...")
            return

        def callback(result):
            global disabled
            disabled = False
            result_var.set(result)

        disabled = True
        tk_call_async(root, _example_calculation, args=(n.get(),), callback=callback, method =MULTIPROCESSING)

    root = Tk()
    
    n = IntVar(value=35)
    row = Frame(root)
    row.pack()
    Entry(row, textvariable=n).pack(side=LEFT)
    Button(row, text="Calculate fibonnaci", command =calculate_fibonacci).pack(side=LEFT)
    Button(row, text="It's responsive", command= lambda: messagebox.showinfo("info", "it's responsive")).pack(side=LEFT)
    
    result_var = StringVar()
    Label(root, textvariable=result_var).pack()
    
    root.mainloop()
