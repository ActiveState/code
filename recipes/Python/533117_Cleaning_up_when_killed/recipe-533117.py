#!/usr/bin/env python

from signal import signal, SIGTERM
from sys import exit
import atexit

def cleanup():
    print "Cleanup"

if __name__ == "__main__":
    from time import sleep
    atexit.register(cleanup)

    # Normal exit when killed
    signal(SIGTERM, lambda signum, stack_frame: exit(1))

    sleep(10)
