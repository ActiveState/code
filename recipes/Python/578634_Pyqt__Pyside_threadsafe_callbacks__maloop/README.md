###Pyqt / Pyside: thread-safe callbacks + main loop integration

Originally published: 2013-08-09 22:29:43
Last updated: 2013-10-12 08:43:09
Author: Justin Israel

A mechanism for communication from any thread to the main thread.\n\nIt uses the same custom Event, but adds a classmethod convenience for taking a callback and params, wrapping it into an event and posting it to the receiver. Also adds in support for weak method references to the callback, in case the source object gets deleted before its callback is actually called.\n\nMerges forks of both:\nhttp://code.activestate.com/recipes/81253/#c5\nhttp://code.activestate.com/recipes/578299-pyqt-pyside-thread-safe-global-queue-main-loop-int/