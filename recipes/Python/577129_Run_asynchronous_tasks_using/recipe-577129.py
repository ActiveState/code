#!/usr/bin/python
"""
Run asynchronous tasks in gobject using coroutines. Terminology used:

  * Job: A coroutine that yield tasks.
  * Task: A function which returns a callable whose only parameter 
    (task_return) is called with the result of the task.
    
Tasks themselves must be asynchronous (they are run in the main thread 
of the events loop), so you will probably use functions like gobject.idle_add/
timeout_add/io_add_watch to implement them. If you are unable to write your 
task in a asynchronous way (or you just can't, i.e. an IO operation), you can 
always use a generic threaded_task (see example below).
"""
import gobject

def start_job(generator):
    """Start a job (a coroutine that yield generic tasks)."""
    def _task_return(result):
        """Function to be sent to tasks to be used as task_return."""
        def _advance_generator():
            try:
                new_task = generator.send(result)
            except StopIteration:
                return
            new_task(_task_return)
        # make sure the generator is advanced in the main thread
        gobject.idle_add(_advance_generator)            
    _task_return(None)
    return generator

# 2 task examples: sleep_task, threaded_task

def sleep_task(secs):
    """Suspend job for the given number of seconds and return elapsed time."""
    def _task(task_return):
        start_time = time.time()
        def _on_timeout():
            task_return(time.time() - start_time)
        gobject.timeout_add(int(secs * 1000), _on_timeout)
    return _task
  
import threading
gobject.threads_init()  

def threaded_task(function, *args, **kwargs):
    """Run function(*args, **kwargs) inside a thread and return the result."""
    def _task(task_return):
        def _thread():
            result = function(*args, **kwargs)
            gobject.idle_add(task_return, result)
        thread = threading.Thread(target=_thread, args=())
        thread.setDaemon(True)
        thread.start()
    return _task

# Example of usage

import sys
import time
import random
import urllib2

def myjob(url):
    def download(url):
        return urllib2.urlopen(url).read()
    elapsed = yield sleep_task(random.uniform(0.0, 3.0))
    sys.stderr.write("[slept_for:%0.2f]" % elapsed)
    sys.stderr.write("[start_download:%s]" % url)
    html = yield threaded_task(download, url)
    sys.stderr.write("[done:%s:%d]" % (url, len(html)))      

def basso_continuo():
    sys.stderr.write(".")
    return True

urls = ["http://www.google.com", "http://python.com", "http://www.pygtk.org"]
jobs = [start_job(myjob(url)) for url in urls]

# See how easily can we raise a exception in the job couroutine:
# gobject.timeout_add(1000, lambda: jobs[0].throw(JobStopped))      

gobject.timeout_add(100, basso_continuo)
loop = gobject.MainLoop()
loop.run()
