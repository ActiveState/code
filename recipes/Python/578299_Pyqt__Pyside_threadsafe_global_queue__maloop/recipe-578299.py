#idle_queue.py

import Queue

#Global queue, import this from anywhere, you will get the same object.
idle_loop = Queue.Queue()

def idle_add(func, *args, **kwargs):
    #use this function to add your callbacks/methods
    def idle():
        func(*args, **kwargs)
        return False
    idle_loop.put(idle)


#idle_queue_dispatcher.py

from PySide.QtGui import *
from PySide.QtCore import *

from idle_queue import idle_loop


class ThreadDispatcher(QThread):
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        while True:
            callback = idle_loop.get()
            if callback is None:
                break
            QApplication.postEvent(self.parent, _Event(callback))

    def stop(self):
        idle_loop.put(None)
        self.wait()


class _Event(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, callback):
        #thread-safe
        QEvent.__init__(self, _Event.EVENT_TYPE)
        self.callback = callback


#main.py

from PySide.QtGui import *
from PySide.QtCore import *

from idle_queue_dispatcher import ThreadDispatcher


class Gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        #....
        
        self.dispatcher = ThreadDispatcher(self)
        self.dispatcher.start()
        
        self.show()

    def customEvent(self, event):
        #process idle_queue_dispatcher events
        event.callback()


if __name__ == "__main__":
    app = QApplication(['']) #QApplication(sys.argv)
    gui = Gui()
    app.exec_()
    gui.dispatcher.stop()
