#!/usr/bin/env python
# Added by <ctang@redhat.com>
# Added on Sept 14 2012 

'''
A pipeline made of several coroutines
that can be turned off gracefully.

This script is inspired by David Beazley with his PyCon 09 talks.
Based on his ideas, I have extended a bit to make the pipeline
able to be monitored and turned off gracefully.
'''

import time


file_name = './food.txt'


def coroutine(func):
    '''A decorator that advances
    the execution to the first 'yield'
    in a generator so that this generator
    is "primed".
    '''
    def generator(*args, **kwargs):
        primed_func = func(*args, **kwargs)
        primed_func.next()
        return primed_func
    return generator

def contains_word(line):
    if line.find('a') > 0:
        return True
    return False

def turn_off_when_too_long(line):
    print 'length:', len(line)
    if len(line) > 200:
        return True
    return False

def tail(target_file, target):
    '''Mimic Unix tail -f
    This is the source of the pipeline
    a pipeline must have a source.
    '''
    # Moves to the end of file
    target_file.seek(0, 2)
    try:
        while True:
            line = target_file.readline()
            if line:
                target.send(line)
            else:
                time.sleep(0.1)
                continue
    except StopIteration:
        print "Pipeline Ended"

@coroutine
def printer():
    '''Display the line
    This is the end-point(sink) of the pipeline.
    '''
    try:
        while True:
            line = (yield)
            print line,
    except GeneratorExit:
        print 'Printer Pipeline Ended'

@coroutine
def grep(pattern_check, target):
    try:
        while True:
            line = (yield)
            if pattern_check(line):
                target.send(line)
            else:
                continue
    except GeneratorExit:
        print "Grep Pipeline Ended"
        target.close()

@coroutine
def monitor(pattern_check, target):
    while True:
        line = (yield)
        if pattern_check(line):
            break
        else:
            target.send(line)
    target.close()

def main():
    f = open(file_name)
    tail(f, monitor(turn_off_when_too_long, grep(contains_word, printer())))

if __name__ == '__main__':
    main()
    
