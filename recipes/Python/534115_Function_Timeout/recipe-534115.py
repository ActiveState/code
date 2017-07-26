import signal

def timeout(signum, frame):
    raise TimeExceededError, "Timed Out"

#this is an infinite loop, never ending under normal circumstances
def main():
    print 'it keeps going and going ',
    while 1:
        print 'and going ',

#SIGALRM is only usable on a unix platform
signal.signal(signal.SIGALRM, timeout)

#change 5 to however many seconds you need
signal.alarm(5)

try:
    main()
except TimeExceededError:
    print "whoops"
