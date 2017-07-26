'''
    High level inotify wrapper
'''

from os import listdir
from os.path import join as opj, normpath, isdir
from threading import Thread, RLock
from Queue import Queue
from time import sleep

from inotify import Inotify, FLAGS, mask_str

globals().update(FLAGS)
ALL = ACCESS|MODIFY|ATTRIB|WRITE|CLOSE|OPEN|CREATE|DELETE

class Event(object):
    def __init__(self, wd, watcher, mask, cookie, name):
        self.wd=wd
        self.watcher=watcher
        self.mask=mask
        self.cookie=cookie
        self.name=name
    @property
    def watch(self):
        return self.watcher.watches[self.wd]
    @property
    def path(self):
        path=self.watch.path
        return opj(path, self.name) if self.name else path
    def __str__(self):
        return '%s -> %s' % (mask_str(self.mask), self.path)

class Watch(object):
    def __init__(self, wd, watcher, mask, path, callback, auto, _parent=None):
        self.wd=wd
        self.watcher=watcher
        self.mask=mask
        self.path=normpath(path)
        self.callback=callback
        self.auto=auto
        self._parent=_parent
        if isdir(self.path) and self.auto:
            for name in listdir(self.path):
                path =  opj(self.path, name)
                if isdir(path):
                    self.watcher.add(
                        path, mask, callback, auto=True, _parent=self)
    def __str__(self):
        return 'Watch %i %s %s -> %s' % (
            self.wd, self.path, mask_str(self.mask), self.callback.__name__)

def default(event):
    if event.mask not in (ISDIR|OPEN, ISDIR|CLOSE): print event

class Watcher(object):
    def __init__(self):
        self.inotify=Inotify()
        self.watches={}
        self.queue=Queue()
        self.lock=RLock()
        for t in (self._push, self._pull):
            t=Thread(target=t)
            t.setDaemon(True)
            t.start()
    def _push(self):
        while True:
            for wd, mask, cookie, name in self.inotify.read():
                self.queue.put(Event(wd, self, mask, cookie, name))
    def _pull(self):
        while True:
            event = self.queue.get()
            mask=event.mask
            self.lock.acquire()
            watch = self.watches.get(event.wd)
            self.lock.release()
            watch.callback(event)
            if mask&ISDIR and mask&CREATE and watch.auto:
                self.add(event.path, watch.mask,
                    watch.callback, auto=True, _parent=watch)
            if mask&IGNORED:
                self.rem(watch)
    def add(self, path, mask=ALL, callback=default, auto=True, _parent=None):
        self.lock.acquire()
        wd=self.inotify.add_watch(path, mask)
        watch = Watch(wd, self, mask, path, callback, auto, _parent)
        self.watches[wd] = watch
        self.lock.release()
        return watch
    def rem(self, watch):
        self.lock.acquire()
        for w in list(self.watches.values()):
            if w._parent==watch: self.rem(w)
        wd=watch.wd
        self.watches.pop(wd)
        self.lock.release()
    def close(self):
        self.inotify.close()

if __name__ == '__main__':

    def tail(event):
        fil, mask = event.path, mask_str(event.mask)
        print '%s %s\n\t%s\n' % (
            fil, mask, '\t'.join(open(fil).readlines()[-5:])
        )

    watcher = Watcher()
    watcher.add('/etc')
    watcher.add('/var/log', MODIFY, tail)
    try:
        while True: sleep(11)
    except KeyboardInterrupt:
        print
    finally:
        watcher.close()
