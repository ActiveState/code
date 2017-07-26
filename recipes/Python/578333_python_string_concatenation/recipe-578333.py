#! /usr/bin/env python
""" (Q): which way to use for concatenating strings? 
    (A): run the script and find out yourself.
"""
import time

bloated_string = 'bloat me' * 10

# method 1, simple concatenation
def slow():    
    test_string = '' 
    start = time.clock()
    for i in range(1000):
        test_string += bloated_string
    end = time.clock()
    delta = float(end-start)
#    print 'slow len: ', len(test_string)
    return delta

# method 2, use list.append() and ''.join()
def fast():
    test_string = list()
    start = time.clock()
    for i in range(1000):
            test_string.append('%s' % bloated_string)
    test_string = ''.join(test_string)
    end = time.clock()
    delta = float(end-start)
#    print 'fast len: ', len(test_string)
    return delta

# method 3, use list comprehension and ''.join()
def fastest():
    test_string = bloated_string
    start = time.clock()
    test_string = ''.join([test_string for i in range(1000)])
    end = time.clock()
    delta = float(end-start)
#    print 'fastest len', len(test_string)
    return delta

if __name__ == '__main__':
    print '--- CPU TIMES ---'
    delta_slow = slow()
    print 'delta slow: {delta_slow}'.format(delta_slow=delta_slow)
    delta_fast = fast()
    print 'delta fast: {delta_fast}'.format(delta_fast=delta_fast)
    delta_fastest = fastest()
    print 'delta fastest: {delta_fastest}'.format(delta_fastest=delta_fastest)
    print '---'
    
    print 'listcomps is %f times faster than (list.append + ''.join())' % \
            (delta_fast/delta_fastest)
    print 'the latter is %f times faster (slower) than simple concat' %\
            (delta_slow/delta_fast)
