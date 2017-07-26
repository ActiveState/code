#####################
# source/exe_queue.py
#####################

import queue

################################################################################

class Pipe:

    def __init__(self, obj):
        self.__obj = obj
        self.__queue = queue.Queue()

    def __getattr__(self, name):
        method = _Method(self.__queue, name)
        setattr(self, name, method)
        return method

    def update(self):
        while not self.__queue.empty():
            name, args, kwargs = self.__queue.get()
            getattr(self.__obj, name)(*args, **kwargs)

################################################################################

class _Method:

    def __init__(self, queue, name):
        self.__queue = queue
        self.__name = name

    def __call__(self, *args, **kwargs):
        self.__queue.put((self.__name, args, kwargs))
