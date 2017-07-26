#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

class Increment(object):
    """Class to calculate increment based on units per second"""
    def __init__(self, units_per_second):
        self.UPS = units_per_second
        self.last_time = time.time()
    def __call__(self):
        now = time.time()
        delta_seconds = (now - self.last_time)
        self.last_time = now
        return delta_seconds * self.UPS

def TimedRange(begin, end, seconds):
    units_per_second = (end - begin) / seconds
    return Increment(units_per_second)

if __name__ == '__main__':
    # usage example
    test1 = 0
    test1_increment = Increment(20) # 20 units per second
    test2 = 800
    test2_increment = TimedRange(800, 5, 5) # 0 to 800 in 5 seconds

    begin = time.time()

    while test1 < 100:
        # do other stuff here,
        # I simulate processing time by sleeping random time up to 0.1 second
        time.sleep(random.random() * 0.1)

        # increment variables based on time passed:
        test1 += test1_increment()
        test2 += test2_increment()
        print test1, test2

    print "It took about %.2f seconds to get test1 from 0 to 100." % (time.time() - begin)
