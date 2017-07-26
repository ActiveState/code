#!/usr/bin/env python

import sys, os, cPickle, time, mmap

TICKS = ('|', '/', '\\')
ESC = chr(27)

class Busy(object):

    def __init__(self, pid):
        self.tick = -1
        sys.stdout.write('Running Child(pid:%d)...%s[s' % (pid, ESC))
        self.next()

    def next(self):
        self.tick += 1
        sys.stdout.write('%s[K %s%s[u' % (ESC, TICKS[self.tick%3], ESC))
        sys.stdout.flush()

    def stop(self, status):
        sys.stdout.write('Done(status: %d)\n' % status)

class ForkedProcessException(Exception):
    pass


def run_in_separate_process(waitclass, func, *args, **kwds):
    try:
        mmsize = kwds['mmsize']
        del kwds['mmsize']
        mmsize = max(mmsize, 1024)
    except KeyError:
        mmsize = 1024
    mm = mmap.mmap(-1, mmsize) 
    pid = os.fork()
    if pid != 0:
        # the parent process
        busy = waitclass(pid)
        try:
            while 1:
                busy.next()
                wpid, wstatus = os.waitpid(pid, os.WNOHANG)
                if wpid == pid:
                    break
        except KeyboardInterrupt:
            raise ForkedProcessException('User cancelled!')
        if os.WIFEXITED(wstatus):
            status = os.WEXITSTATUS(wstatus)
            busy.stop(status)
        elif os.WIFSIGNALED(wstatus):
            raise ForkedProcessException('Child killed by signal: %d' % os.WTERMSIG(wstatus))
        else:
            raise RuntimeError('Unknown child exit status!')
        mm.seek(0)
        result = cPickle.load(mm)
        if status  == 0:
            return result
        else:
            raise result
    else: # the child process 
        try:
            mm.seek(0)
            result = func(*args, **kwds)
            status = 0 # success
            cPickle.dump(result, mm, cPickle.HIGHEST_PROTOCOL)
        except cPickle.PicklingError, exc:
            status = 2 # failure
            cPickle.dump(exc, mm, cPickle.HIGHEST_PROTOCOL)
        except (KeyboardInterrupt), exc:
            status = 4 # failure
            cPickle.dump(ForkedProcessException('User cancelled!'), mm, cPickle.HIGHEST_PROTOCOL)
        except ValueError:
            status = 3 # failure
            pstr = cPickle.dumps(result, cPickle.HIGHEST_PROTOCOL)
            mm.seek(0)
            cPickle.dump(ForkedProcessException('mmsize: %d, need: %d' % (mmsize, len(pstr))), mm, cPickle.HIGHEST_PROTOCOL)
        except (Exception), exc:
            status = 1 # failure
            cPickle.dump(exc, mm, cPickle.HIGHEST_PROTOCOL)
        os._exit(status)

# Functions to run in a separate process
def treble(x, fail=False):
    if fail: 1/0
    return 3 * x
def suicide():
    os.kill(os.getpid(), 15)
def toobig():
    return '1234567890' * 110
def nocanpickle():
    return globals()
def waitaround(seconds=3, fail=False):
    while seconds:
        if fail: 1/0
        time.sleep(1)
        seconds -= 1
    return ['here', 'is', 'the', 'dead', 'tree', 'devoid', 'of', 'leaves']
def sysexit():
    sys.exit(9)

# General test function call
def run(direct, func, *args, **kwargs):
    try:
        print '\nRunning %s(%s, %s) ' % (func.func_name, args, kwargs),
        if direct:
            print 'directly...' 
            result = func(*args, **kwargs)
            print 'Needs minimum mmsize of %d' % (len(cPickle.dumps(result, cPickle.HIGHEST_PROTOCOL)))
        else:
            print 'in separate process...'
            result = run_in_separate_process(Busy, func, *args, **kwargs)
        print '%s returned: %s' % (func.func_name, result)
    except Exception, e:
        print '%s raised %s: %s' % (func.func_name, e.__class__.__name__, str(e))

def main():
    direct = True
    run(not direct, waitaround, seconds=30)
    run(not direct, waitaround)
    run(not direct, waitaround, fail=True)
    run(not direct, toobig)
    run(not direct, nocanpickle)
    run(not direct, suicide)
    run(direct, waitaround, seconds=5)
    run(not direct, sysexit)
    run(not direct, treble, 4)
    run(direct, treble, 4)

if __name__ == '__main__':
    main()
