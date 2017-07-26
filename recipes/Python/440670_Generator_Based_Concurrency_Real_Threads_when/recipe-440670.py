import nanothreads
import time
import sys

def task_1():
    while True:
        print "Performing work in task_1"
        yield nanothreads.CONTINUE()
        #yielding nanothreads.UNBLOCK will perform 
        #the next iteration in a seperate thread.
        yield nanothreads.UNBLOCK()
        print "Simulating some Blocking IO..."
        time.sleep(10)
        print "Finished Blocking IO."
        yield nanothreads.CONTINUE()

def task_2():
    while True:
        print "Performing work in task_2"
        yield nanothreads.CONTINUE()
        time.sleep(1)


a = nanothreads.install(task_1())
b = nanothreads.install(task_2())
#defer an exit call for 11 seconds, so this test eventually stops.
nanothreads.defer_for(11, sys.exit)
nanothreads.loop()
