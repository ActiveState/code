from math import e, pi
from os.path import basename
from sys import argv
from threading import currentThread, Thread
from time import ctime, sleep

NAP_TIME = 1
BUSY_TIME = 40000

def main():
    try:
        if len(argv) != 3:
            raise Exception
        engine(int(argv[1]), int(argv[2]))
    except:
        print basename(argv[0]), '<threads> <seconds>'

def engine(threads, seconds):
        print 'Suite starting at', ctime()
        for thread in range(threads):
            temp = Thread(target = threadWork)
            temp.setDaemon(True)
            temp.start()
        sleep(seconds)

def threadWork():
    while True:
        try:
            for i in range(BUSY_TIME):
                y = pi ** e
            sleep(NAP_TIME)
            print currentThread().getName(), 'just woke up.'
        except:
            pass

if __name__ == '__main__':
    main()
