import time
import threading
import sys

# TODO: Maybe Interval should be a multiply of Precision.

class Job:
    Interval = 0
    Elapsed = 0
    JobFunction = None
    Force = False

class JobController(threading.Thread):
    
    def __init__(self,precision=1.0):
        threading.Thread.__init__(self)
        self.__StopIt = False
        self.__Jobs = {}
        self.__JobCounter = 0
        self.__Precision = precision
        self.__JobsLock = threading.Lock()
        
    def run(self):
        
        while(1):
            jobfuncs = []

            if self.__StopIt == True:
                return
            
            self.__JobsLock.acquire()
            try:
                for key,val in self.__Jobs.items():
                    val.Elapsed += self.__Precision
                    if val.Elapsed >= val.Interval or val.Force:
                        val.Elapsed = 0
                        val.Force = False
                        
                        # copy to another list for
                        # not acquirirng JobsLock()
                        # while calling the JobsFunction 
                        jobfuncs.append(val.JobFunction)
            finally:
                self.__JobsLock.release()
                
            # now invoke the job functions
            for jobfunc in jobfuncs:
                try:
                    jobfunc()
                # no unhandled exceptions allowed
                except Exception,e:
                    print "JOBERROR:"+str(e)
            time.sleep(self.__Precision)
                    
            
    def JcStart(self):
        self.start()
    
    def JcStop(self):
        self.__StopIt = True
        
    def __AssertBounds(self,val,min,max):
        if (val < min) or (val > max):
            raise AssertionError, "value not in bounds" \
                      "["+str(val)+"]["+str(min)+"]["+str(max)+"]"
        
    def JcAddJob(self,interval,jobfunction):
        
        self.__AssertBounds(interval,self.__Precision,float(sys.maxint))
        
        # create a job object
        ajob = Job()
        ajob.Interval = interval
        ajob.Elapsed = 0
        ajob.JobFunction = jobfunction
        ajob.Force = False
        # append it to jobs dict
        self.__JobCounter += 1

        self.__JobsLock.acquire()
        try:
            self.__Jobs[self.__JobCounter] = ajob
        finally:
            self.__JobsLock.release()
            
        return self.__JobCounter
        
    def JcRemoveJob(self,jobid):
        self.__JobsLock.acquire()
        try:
            del self.__Jobs[jobid]
        finally:
            self.__JobsLock.release()
        
    def JcForceJob(self,jobid):
        self.__JobsLock.acquire()
        try:            
            self.__Jobs[jobid].Force = True
        finally:
            self.__JobsLock.release()
        
    def JcChangeJob(self,jobid,interval,jobfunction):

        self.__AssertBounds(interval,self.__Precision,sys.maxint)
        
        self.__JobsLock.acquire()
        try:  
            self.__Jobs[jobid].Interval = interval
            self.__Jobs[jobid].JobFunction = jobfunction
        finally:
            self.__JobsLock.release()

# EXAMPLE
A simple example is like this:
jc = JobController(60.0) # precision is 60 secs, so main JobController will be invoked
                         # per 60 secs.
jc.JcAddJob(60*30,CheckConnectionJob)
jc.JcAddJob(60*5,CheckStatisticsJob)
jc.start()
jc.JcAddJob(60*5,CheckPingJob)
.
.
