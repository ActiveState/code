import threading
import time

class ThM(object):
    """ThM (ThreadManager)
    Handles very simple thread operations:
        Creating single-shot threads -> ThM.run(...)
        Creating 'looping per interval' threads -> ThM.run(...) with loop set to True
        Stopping looping threads based on name -> ThM.stop_loop(...)
        Joining all threads into the calling thread ThM.joinall()
        Removing stopped threads from 'running_threads' - > ThM.free_dead()

     
    The class has been designed for very simple operations, mainly
    for programs that need "workers" that mindlessly loop over a function.

    NOTE: Locks,Events,Semaphores etc. have not been taken into consideration
    and may cause unexpected behaviour if used!
     """
    running_threads = []

    @classmethod
    def run(cls,targetfunc,thname,loop,interval,arglist=[]):
        """Statrs a new thread and appends it to the running_threads list
        along with the specified values.
        Loop and interval needs to be specified even if you dont
        want it to loop over. This is to avoid lot of keyword arguments
        and possible confusion.
        Example of starting a looping thread:
            ThM.run(function,"MyThreadName",True,0.5,[1,2,"StringArguemnt"])

        To stop it, use:
            ThM.stop_loop("MyThreadName")
        Note, a stopped thread cannot be started again!

        Example of a single-shot thread:
            ThM.run(function,"ThreadName",False,0.5,[1,2,"StringArgument"])
            """

        th = threading.Thread(target=cls._thread_runner_,args=(targetfunc,thname,interval,arglist))
        th.setDaemon(True)
        cls.running_threads.append([th,thname,loop])
        th.start()

    @classmethod
    def free_dead(cls):
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for th in cls.running_threads[:]:
            if th[0].isAlive() == False:
                cls.running_threads.remove(th)

    @classmethod
    def stop_loop(cls,threadname):
        """Stops a looping function that was started with ThM.run(...)"""
        for i,thlis in enumerate(cls.running_threads):
            if thlis[1] == threadname:
                cls.running_threads[i][2] = False
                break
    
    @classmethod
    def joinall(cls):
        """Joins all the threads together into the calling thread."""
        for th in cls.running_threads[:]:
            while th[0].isAlive():
                time.sleep(0.1)
            th[0].join()
         #   print "Thread:",th[1],"joined","isalive:",th[0].isAlive() --- Debug stuff

    @classmethod
    def get_all_params(cls):
        """Returns parameters from the running_threads list for external manipulation"""
        for thli in cls.running_threads:
            yield(thli[0],thli[1],thli[2])


    #This method is only intended for threads started with ThM !
    @classmethod
    def _thread_runner_(cls,targetfunc,thname,interval,arglist):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        indx=0
        for thread in cls.running_threads[:]:
            if thname == thread[1]:
                break
            indx+=1
        targetfunc(*arglist)
        while cls.running_threads[indx][2] == True:
            targetfunc(*arglist)
            if interval != 0:
                time.sleep(interval)
