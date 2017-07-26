import threading,Queue

class QueueMinder(object):
    
    def __init__(self, msgQueue, inCallback=None, interval=1.0, doStart=False):
        object.__init__(self)
        self.msgQueue = msgQueue
        if not inCallback: self.inCallback=self.gotMessage
        else: self.inCallback=inCallback
        self.interval = interval
        self.progressTimer = None
        if doStart:
            self.startTimer()

    def startTimer(self):
        self.progressTimer = threading.Timer(self.interval, self._progressCheck)
        self.progressTimer.start()

    def stopTimer(self):
        if self.progressTimer: self.progressTimer.cancel()
        self.progressTimer=None

    def gotMessage(self,msg):
        print 'gotMessage(): msg=%s'%msg

    def _progressCheck(self):
        try:
            while 1:
                msg = self.msgQueue.get(False)
                if msg: self.inCallback(msg)
        except Queue.Empty:
            self.startTimer()

from qt import *
class QtQueueMinder(QueueMinder, QObject):
    
    def __init__(self, msgQueue, inCallback=None, freq=500):
         QObject.__init__(self)
        # the interval is in milliseconds
        QueueMinder.__init__(self, msgQueue, inCallback, freq)

    def startTimer(self):
        if not self.progressTimer:
            self.progressTimer = QTimer()
            self.connect(self.progressTimer, SIGNAL("timeout()"), self._progressCheck)
            self.progressTimer.start(self.interval)

    def stopTimer(self):
        if self.progressTimer: self.progressTimer.stop()
        self.progressTimer=None

from Foundation import NSTimer
class MacQueueMinder(QueueMinder):
    def runTimer(target, selector, interval):
        return NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(interval,target,selector,None,True)
    runTimer = staticmethod(runTimer)
    
    def __init__(self, msgQueue, inCallback=None, freq=0.5):
        # the interval is in seconds
        QueueMinder.__init__(self, msgQueue, inCallback, freq)
        return self

    def startTimer(self):
        self.progressTimer = MacQueueMinder.runTimer(self, 'progressCheck:', self.interval)
        self.progressTimer.retain()

    def stopTimer(self):
        if self.progressTimer:
            self.progressTimer.invalidate()
            self.progressTimer.autorelease()
            self.progressTimer = None

    def progressCheck_(self,timer=None):
        try:
            while 1:
                msg = self.msgQueue.get(False)
                if msg: self.inCallback(msg)
        except Queue.Empty:
	    pass

if __name__=='__main__':

    theQueue = Queue.Queue()

    class MyThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.qm =None
            self.itsAllGood = True
            self.start()

        def run(self):
            self.qm=QueueMinder(theQueue)
            self.qm.startTimer()
            while self.itsAllGood:
                pass

    tt = MyThread()
    theQueue.put('How yall doin')
    theQueue.put('Everybody say hey')
    theQueue.put('Everybody say ho')
    tt.itsAllGood = False
