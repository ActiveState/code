'''
pmeter.py -- Precise console progress meter with ETA calculation

Some code inherited from CFV sources (cfv.sf.net)

2010-01-11 20:23
'''
import sys
import time
import threading

__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577002-precise-console-progress-meter-with-eta-calculatio/?in=user-57155'

def format_sec(sec):
    sec = int(sec)
    min_, sec = divmod(sec, 60)
    hour, min_ = divmod(min_, 60)
    return '%d:%02d:%02d' % (hour, min_, sec)

class ETA(object):
    '''
    calculate ETA (Estimated Time of Arrival :)
    for some events

    Save few last update points or some seconds.
    Help fight statistics after hibernate :)
    '''
    
    def __init__(self, wanted_size, max_point=20, max_seconds=30):
        self.wanted_size = wanted_size
        self.points = list()
        self.max_point = max_point
        self.max_seconds = max_seconds
        self.points.append([time.clock(), 0])
        self.eta = 'N/A'

    def _cleanup(self):
        if len(self.points) < 2:
            return 0
        else:
            last_point_time = self.points[-1][0]
            while len(self.points) > 2:
                if last_point_time - self.points[0][0] > self.max_seconds and \
                   len(self.points) > self.max_point:
                    self.points.pop(0)
                else:
                    break
            return 1

    def update(self, cursize):
        self.points.append([time.clock(), cursize])
        if not self._cleanup():
            return

        delta_time = self.points[-1][0] - self.points[0][0]
        delta_work = cursize
        speed = float(delta_work) / float(delta_time)
        if speed == 0.0:
            return 

        eta = (float(self.wanted_size) - float(cursize)) / float(speed)
        self.eta = format_sec(eta) 

    def getstatus(self):
        return self.eta


class ProgressMeter(object):
  
    def __init__(self, steps=20, min_update_delta=0.1, outstream=sys.stdout):
        self.wantsteps = steps
        self.prev_message = ''
        self.last_update_time = -100
        self.needrefresh = 1
        self.times = list()
        self.done_char = '#'
        self.left_char = '.'
        self.eta_calculator = None
        self.min_update_delta = max(min_update_delta, 0.04) # max 25 fps on redraw :)
        self.outstream = outstream
        self.work_mutex = threading.Lock()
        self.size = None
        self.label = None
        self.steps = None

    def init(self, label, size, cursize=0):
        self.size = size
        self.label = label
        self.steps = self.wantsteps
        self.needrefresh = 1

        self.eta_calculator = ETA(size)
        self.update(cursize)

        self.last_update_time = -100

    def set_complete(self):
        self.needrefresh = 1
        self.update(self.size)
        print # left progress bar on screen

    def _rawupdate(self, cursize):
        self.eta_calculator.update(cursize)

        donesteps = (cursize * self.steps) / self.size
        stepsleft = self.steps - donesteps
        percent = 100.0 * float(cursize) / float(self.size)
        percent_str = '         %.2f%%' % percent
        percent_str = percent_str[-7:]

        if cursize == self.size:
            percent = 100.0

        eta = self.eta_calculator.getstatus()

        message = '%s:%s %s%s ETA: %s' % (self.label, percent_str, self.done_char*donesteps, self.left_char*stepsleft, eta)
        self.outstream.write('\b'*len(self.prev_message) + message); self.outstream.flush()
        self.prev_message = message

        self.last_update_time = time.clock()

    def update_left(self, left):
        '''
        useful in miltithreaded environment when processing job pool:
            
        Main:
            pm.init(len(joblist))

        In thread.run():
            job = joblist.pop(0)
            pm.update_left(len(joblist))
        '''
        self.update(self.size - left)
    
    def update(self, cursize):
        self.work_mutex.acquire()
        if self.needrefresh:
            self._rawupdate(cursize)
            self.needrefresh = 0
        else:
            delta = time.clock() - self.last_update_time
            if delta < self.min_update_delta:
                pass
            else:
                self._rawupdate(cursize)
        self.work_mutex.release()
    
    def cleanup(self):
        self.work_mutex.acquire()
        if not self.needrefresh:
            self.outstream.write('\r' + ' ' * len(self.prev_message) + '\r')
            self.needrefresh = 1
        self.work_mutex.release()


if __name__ == '__main__':
    progress = ProgressMeter(30, outstream=sys.stderr)
    progress.init('Progress Label', 500)
    for i in range(500+1):
        time.sleep(0.01)
        progress.update(i)
    progress.cleanup()
