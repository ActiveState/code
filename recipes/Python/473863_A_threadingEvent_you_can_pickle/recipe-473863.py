import threading
import copy

class SerializableEvent(object):
    "A threading.Event that can be serialized."
    def __init__(self):
        self.evt = threading.Event()

    def set(self):
        return self.evt.set()

    def clear(self):
        return self.evt.clear()

    def isSet(self):
        return self.evt.isSet()

    def wait(self, timeout=0):
        return self.evt.wait(timeout)

    def __getstate__(self):
        d = copy.copy(self.__dict__)
        if self.evt.isSet():
            d['evt'] = True
        else:
            d['evt'] = False
        return d

    def __setstate__(self, d):
        self.evt = threading.Event()
        if d['evt']:
            self.evt.set()
