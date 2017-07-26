import signal, time

class TimedOutExc(Exception):
    def __init__(self, value = "Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)

def TimedOutFn(f, timeout, *args, **kwargs):
    def handler(signum, frame):
        raise TimedOutExc()
    
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        result = f(*args, **kwargs)
    finally:
        signal.signal(signal.SIGALRM, old)
    signal.alarm(0)
    return result


def timed_out(timeout):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()
        
        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
            return result
        
        new_f.func_name = f.func_name
        return new_f

    return decorate


def fn_1(secs):
    time.sleep(secs)
    return "Finished"

@timed_out(4)
def fn_2(secs):
    time.sleep(secs)
    return "Finished"

@timed_out(2)
def fn_3(secs):
    time.sleep(secs)
    return "Finished"

@timed_out(2)
def fn_4(secs):
    try:
        time.sleep(secs)
        return "Finished"
    except TimedOutExc:
        print "(Caught TimedOutExc, so cleaining up, and re-raising it) - ",
        raise TimedOutExc
        
if __name__ == '__main__':

    try:
        print "fn_1 (sleep 2, timeout 4): ",
        print TimedOutFn(fn_1, 4, 2)
    except TimedOutExc:
        print "took too long"
        
    try:
        print "fn_2 (sleep 2, timeout 4): ",
        print fn_2(2)
    except TimedOutExc:
        print "took too long"

    try:
        print "fn_1 (sleep 4, timeout 2): ",
        print TimedOutFn(fn_1, 2, 4)
    except TimedOutExc:
        print "took too long"
        
    try:
        print "fn_3 (sleep 4, timeout 2): ",
        print fn_3(4)
    except TimedOutExc:
        print "took too long"

    try:
        print "fn_4 (sleep 4, timeout 2): ",
        print fn_4(4)
    except TimedOutExc:
        print "took too long"
