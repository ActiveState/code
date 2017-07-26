import sys
import time

def timeit(f):
    """ Annotate a function with its elapsed execution time. """
    def timed_f(*args, **kwargs):
         t1 = time.time()

         try:
             f(*args, **kwargs)
         finally:
             t2 = time.time()

         timed_f.func_time = ((t2 - t1) / 60.0, t2 - t1, (t2 - t1) * 1000.0)

         if __debug__:
             sys.stdout.write("%s took %0.3fm %0.3fs %0.3fms\n" % (
                 f.func_name,
                 timed_f.func_time[0],
                 timed_f.func_time[1],
                 timed_f.func_time[2],
             ))

    return timed_f


def timeme():
    time.sleep(2)

timeme = timeit(timeme)
