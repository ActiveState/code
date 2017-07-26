# libc_time.py
# Example of calling C library functions from Python
# using the Python ctypes module.
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram - https://vasudevram.github.io

from __future__ import print_function
from ctypes import cdll
import time

libc = cdll.msvcrt

def test_libc_time(n_secs):
    t1 = libc.time(None)
    time.sleep(n_secs)
    t2 = libc.time(None)
    print("n_secs = {}, int(t2 - t1) = {}".format(n_secs, int(t2 - t1)))
    
print("Calling the C standard library's time() function via ctypes:")
for i in range(1, 6):
    test_libc_time(i)
