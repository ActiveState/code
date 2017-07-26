from __future__ import with_statement

import threading
import sys

# Implementation of Ticker class
class Ticker(threading.Thread):
    def __init__(self, msg):
	threading.Thread.__init__(self)
	self.msg = msg
	self.event = threading.Event()
    def __enter__(self):
	self.start()
    def __exit__(self, ex_type, ex_value, ex_traceback):
	self.event.set()
	self.join()
    def run(self):
	sys.stdout.write(self.msg)
	while not self.event.isSet():
	    sys.stdout.write(".")
	    sys.stdout.flush()
	    self.event.wait(1)

# Here's how we use it...
if __name__ == '__main__':
    import time
    with Ticker("A test"):
	time.sleep(10)
    with Ticker("Second test"):
	time.sleep(5)
	raise Exception("Bang!")
