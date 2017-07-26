from qt import *

class BaseQObject(QObject):

    MAIN_THREAD_ID = 0

    def __init__(self):
        QObject.__init__(self)
        self.installEventFilter(self)
        self.event = None

    def eventFilter(self,obj,event):
        # FIXME:  This is a workaround for an unexplained bug
        # The events were getting posted through postEVentWithCallback()
        # But the event() method wasn't getting called.  But the eventFilter()
        # method is getting called.  
        if event.type()==QEvent.User:
            cb = event.__dict__.get('callback')
            if cb: self._doEvent(event)
            return False
        return QObject.eventFilter(self,obj,event)

    def _doEvent(self,event):
        cb = event.__dict__.get('callback')
        if not cb: return
        data = event.__dict__.get('data')
        if data or type(data)==type(False): cb(data)
        else: cb()
        del event

    def event(self, event):
        if event.type()==QEvent.User:
            self._doEvent(event)
            return True
        return QObject.event(self, event)

    def postEventWithCallback(self, callback, data=None):
        # if we're in main thread, just fire off callback
        if get_ident()==BaseQObject.MAIN_THREAD_ID:
            if data or type(data)==type(False): callback(data)
            else: callback()
        # send callback to main thread 
        else:
            event = QEvent(QEvent.User)
            event.callback = callback
            if data or type(data)==type(False): event.data = data
            qApp.postEvent(self, event)


class ThreadLock:

    def __init__(self):
        if sys.platform == 'win32':
            from qt import QMutex
            self.mutex = QMutex(True)
        elif sys.platform == 'darwin':
            from Foundation import NSRecursiveLock
            self.mutex = NSRecursiveLock.alloc().init()

    def lock(self): self.mutex.lock()
    def unlock(self): self.mutex.unlock()
        

import thread

class Foo(BaseQObject):

    def doMainFoo(self):
        print 'doMainFoo(): thread id = '%thread.get_ident()
    
    def doFoo(self):
        print 'doFoo(): thread id = '%thread.get_ident()
        self.postEventWithCallback(self.doMainFoo)

if __name__=="__main__":
    foofoo = Foo()
    
    import threading
    threading.Timer(1.0, foofoo.doFoo)

    from qt import QApplication
    app = QApplication([])
    app.exec_loop()
