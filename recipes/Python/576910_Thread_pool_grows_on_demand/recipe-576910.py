#! /usr/bin/python

import threading
import Queue
import time
import sys

Instance = None

def getInstance():
    global Instance
    if not Instance:
        Instance = ThreadPool()
    return Instance


class ThreadPool:

    def __init__(self,maxWorkers = 10):
        self.tasks = Queue.Queue()
        self.workers = 0
        self.working = 0
        self.maxWorkers = maxWorkers
        self.allKilled = threading.Event()
        self.countLock = threading.RLock()
        self.timers = {}
        self.timersLock = threading.Lock()
        self.timersThreadLock = threading.Lock()
        self.timersEvent = threading.Event()
        
        self.allKilled.set()
        

    def run(self,target,callback = None, *args, **kargs):
        """ starts task.
            target = callable to run with *args and **kargs arguments.
            callback = callable executed when target ends
                       callback sould accept one parameter where target's
                       return value is passed.
                       If callback is None it's ignored.
        """
        self.countLock.acquire()
        if not self.workers:
            self.addWorker()
        self.countLock.release()
        self.tasks.put((target,callback,args,kargs))
        


    def setMaxWorkers(self,num):
        """ Sets the maximum workers to create.
            num = max workers
                  If number passed is lower than active workers 
                  it will kill workers to match that number. 
        """
        self.countLock.acquire()
        self.maxWorkers = num
        if self.workers > self.maxWorkers:
            self.killWorker(self.workers - self.maxWorkers)
        self.countLock.release()


    def addWorker(self,num = 1):
        """ Add workers.
            num = number of workers to create/add.
        """
        for x in xrange(num):
            self.countLock.acquire()
            self.workers += 1
            self.allKilled.clear()
            self.countLock.release()        
            t = threading.Thread(target = self.__workerThread)
            t.setDaemon(True)
            t.start()


    def killWorker(self,num = 1):
        """ Kill workers.
            num = number of workers to kill.
        """
        self.countLock.acquire()
        if num > self.workers:
            num = self.workers
        self.countLock.release()
        for x in xrange(num):
            self.tasks.put("exit")            
            

    def killAllWorkers(self,wait = None):
        """ Kill all active workers.
            wait = seconds to wait until last worker ends
                   if None it waits forever.
        """
        
        self.countLock.acquire()
        self.killWorker(self.workers)
        self.countLock.release()
        self.allKilled.wait(wait)


    def __workerThread(self):
        while True:
            task = self.tasks.get()
            # exit is "special" tasks to kill thread
            if task == "exit":
                break
            
            self.countLock.acquire()
            self.working += 1
            if (self.working >= self.workers) and (self.workers < self.maxWorkers): # create thread on demand
                self.addWorker()
            self.countLock.release()
    
            fun,cb,args,kargs = task
            try:
                ret = fun(*args,**kargs)
                if cb:
                    cb(ret)
            except:
                print "Unexpected error:", sys.exc_info()                
            
            self.countLock.acquire()
            self.working -= 1
            self.countLock.release()                
                
        self.countLock.acquire()
        self.workers -= 1
        if not self.workers:
            self.allKilled.set()
        self.countLock.release()


    def timer(self, cb, period):
        """ Add or remove timers.
            cb = callback function.
            period = period in seconds (float)
                     if period is 0 timer is deleted.
        """ 
            
            
        self.run(self.__timerThread, None, cb, period) 


    def __timerThread(self, cb, period):
        self.timersLock.acquire()
        self.timersEvent.set()
        if not period:
            if cb in self.timers:
                del(self.timers[cb])
            self.timersLock.release()
            return
                
        self.timers[cb] = [period,time.time()]    
        self.timersLock.release()
        
        if not self.timersThreadLock.acquire(0):
            return
            
        while True:
            self.timersLock.acquire()
            if len(self.timers) == 0:
                self.timersThreadLock.release()
                self.timersLock.release()
                break
                
            minWait = 30*24*3600
            now = time.time()
            for k,v in self.timers.items():
                period, last = v
                wait = period - (now - last)
                if wait <=0:
                    self.run(k)
                    wait = period
                    v[1] = now
                if wait < minWait:
                    minWait = wait
            self.timersLock.release()
            self.timersEvent.wait(minWait)
            self.timersEvent.clear()         
            
                
        
                                       
