## Long processing computation in Tkinter or long-running task

Originally published: 2017-02-04 07:42:55
Last updated: 2017-02-06 18:30:18
Author: Miguel Martínez López

I provide in this module the function "tk_call_async": It executes a function asynchronously.\n\n    tk_call_async(window, computation, args=(), kwargs={}, callback=None, polling=100, method=MULTIPROCESSING)\n\n"tk_call_async" executes the function "computation" asynchronously with the provided "args" and "kwargs" without blocking the tkinter event loop.\n\nIf "callback" is provided, it will be called with the result when the computation is finished.\n\nIf an exception happens doing the computation, the errback function is called with the exception if this is provided.\n\n"Polling" will be the frequency to poll to check for results.\n\nThere is two methods to execute the task: using multiprocessing or using threads.