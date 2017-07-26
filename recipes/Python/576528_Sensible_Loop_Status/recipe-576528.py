'''
    import logging
    from LoopStatus import LoopStatus

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s L%(lineno)d %(message)s',
        datefmt='%H:%M:%S',
        )

    status = LoopStatus()
    ...
    if status():
        logging.info('%dnth occurence',status.Value)
'''

import signal

class LoopStatus(object):

    def __init__(self,base=2,seconds=5*60,target=1):
        self.i = 0
        self.base = base
        self.target = target
        self.nonzero = True
        self.timesup = False
        self.interval = seconds
        if 0 < seconds:
            self.reset_timer()
            signal.signal(signal.SIGALRM,self.trap_alarm)

    def trap_alarm(self,*args,**kwargs):
        self.timesup = True

    def reset_timer(self,interval=None):
        if interval is None:
            interval = self.interval
        if 0 < interval:
            self.timesup = False
            signal.alarm(interval)

    def __call__(self):
        self.i += 1
        self.nonzero = self.timesup or (self.target <= self.i)
        if self:
            self.target *= self.base
            self.reset_timer()
        return self.nonzero

    @property
    def Value(self):
        return self.i

    def __nonzero__(self):
        return self.nonzero

    def __str__(self):
        return str(self.Value)
