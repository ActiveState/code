'''
File: callback_demo2.py
To demonstrate implementation and use of callbacks in Python, 
using classes with methods as the callbacks.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

from __future__ import print_function
import sys
from time import sleep

class FileReporter(object):

    def __init__(self, filename):
        self._filename = filename
        try:
            self._fil = open(self._filename, "w")
        except IOError as ioe:
            sys.stderr.write("While opening {}, caught IOError: {}\n".format(
                self._filename, repr(ioe)))
            sys.exit(1)

    def report(self, message):
        self._fil.write(message)

class ScreenReporter(object):

    def __init__(self, dest):
        self._dest = dest

    def report(self, message):
        self._dest.write(message)

def square(i):
    return i * i

def cube(i):
    return i * i * i

def processor(process, times, report_interval, reporter):
    result = 0
    for i in range(1, times + 1):
        result += process(i)
        sleep(0.1)
        if i % report_interval == 0:
            # This is the call to the callback method 
            # that was passed to this function.
            reporter.report("Items processed: {}. Running result: {}.\n".format(i, result))

file_reporter = FileReporter("processor_report.txt")
processor(square, 20, 5, file_reporter)

stdout_reporter = ScreenReporter(sys.stdout)
processor(square, 20, 5, stdout_reporter)

stderr_reporter = ScreenReporter(sys.stderr)
processor(square, 20, 5, stderr_reporter)
