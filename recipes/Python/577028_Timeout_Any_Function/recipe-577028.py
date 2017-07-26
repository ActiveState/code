import multiprocessing as MP
from sys import exc_info
from time import clock

DEFAULT_TIMEOUT = 60

################################################################################

def timeout(limit=None):
    if limit is None:
        limit = DEFAULT_TIMEOUT
    if limit <= 0:
        raise ValueError()
    def wrapper(function):
        return _Timeout(function, limit)
    return wrapper

class TimeoutError(Exception): pass

################################################################################

def _target(queue, function, *args, **kwargs):
    try:
        queue.put((True, function(*args, **kwargs)))
    except:
        queue.put((False, exc_info()[1]))

class _Timeout:

    def __init__(self, function, limit):
        self.__limit = limit
        self.__function = function
        self.__timeout = clock()
        self.__process = MP.Process()
        self.__queue = MP.Queue()

    def __call__(self, *args, **kwargs):
        self.cancel()
        self.__queue = MP.Queue(1)
        args = (self.__queue, self.__function) + args
        self.__process = MP.Process(target=_target, args=args, kwargs=kwargs)
        self.__process.daemon = True
        self.__process.start()
        self.__timeout = self.__limit + clock()

    def cancel(self):
        if self.__process.is_alive():
            self.__process.terminate()

    @property
    def ready(self):
        if self.__queue.full():
            return True
        elif not self.__queue.empty():
            return True
        elif self.__timeout < clock():
            self.cancel()
        else:
            return False

    @property
    def value(self):
        if self.ready is True:
            flag, load = self.__queue.get()
            if flag:
                return load
            raise load
        raise TimeoutError()

    def __get_limit(self):
        return self.__limit

    def __set_limit(self, value):
        if value <= 0:
            raise ValueError()
        self.__limit = value

    limit = property(__get_limit, __set_limit)
