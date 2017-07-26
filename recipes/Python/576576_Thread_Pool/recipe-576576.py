from threading import Thread
from Queue import Queue
from time import sleep

from tools import propertx # from http://code.activestate.com/recipes/502243/

class Pool(object):
    def __init__(self, Psize=20, Qsize=20):
        self.workers = []
        self.jobs = Queue(Qsize)
        self.size=Psize
        self.accept=True
    @propertx
    def size():
        def set(self, newSize):
            for i in xrange(newSize-len(self.workers)):
                new = Worker(self)
                self.workers.append(new)
                new.start()
            for i in xrange(len(self.workers)-newSize):
                self.jobs.put((None, None, None, None))
        def get(self):
            return len(self.workers)
        return get, set
    def add(self, job, callback=None, *args, **kw):
        if self.accept:
            self.jobs.put((job, args, kw, callback))
    def join(self):
        self.accept=False
        while True:
            for w in self.workers:
                if w.isAlive() :
                    self.jobs.put((None, None, None, None))
                    break
            else:
                break
    @property
    def qsize(self): return self.jobs.qsize()

class Worker(Thread):
    def __init__(self, pool):
        Thread.__init__(self)
        self.pool = pool
        self.cmd=''
    def run(self):
        get=self.pool.jobs.get
        while True:
            cmd, args, kw, callback = get()
            if cmd:
                self.cmd=cmd.__name__
                if callback:
                    callback(cmd(*args, **kw))
                else:
                    cmd(*args, **kw)
                self.cmd=''
            else:
                self.pool.workers.remove(self)
                break

if __name__=='__main__':

    def easyJob(*arg, **kw):
        n=arg[0]
        print '\tSleep\t\t', n
        sleep(n)
        return 'Slept\t%d' % n
    def longJob(*arg, **kw):
        print "\tStart\t\t\t", arg, kw
        n=arg[0]*3
        sleep(n)
        return "Job done in %d" % n
    def badJob(*a, **k):
        print '\n !!! OOOPS !!!\n'
        a=1/0
    def show(*arg, **kw):
        print 'callback : %s' % arg[0]

    pool = Pool(5, 50)
    print "\n\t\t... let's add some jobs ...\n"
    for j in range(5):
        if j==1: pool.add(badJob)
        for i in range(5,0,-1):
            pool.add(longJob, show, i)
            pool.add(easyJob, show, i)
    print '''
        \t\t... and now, we're waiting for the %i workers to get the %i jobs done ...
    ''' % (pool.size, pool.qsize)
    sleep(15)
    print "\n\t\t... ok, that may take a while, let's get some reinforcement ...\n"
    sleep(5)
    pool.size=50
    print '\n\t\t... Joining ...\n'
    pool.join()
    print '\n\t\t... Ok ...\n'
