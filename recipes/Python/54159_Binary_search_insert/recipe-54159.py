#!/usr/bin/env python
# This demonstrates a binary search through sorted data using bisect.
# A large array of random numbers is generated and then sorted.
# The the application shows where a given number would be inserted
# in the random data list.

from bisect import bisect
from random import randrange
import sys

# Get the given number from the command line argument.
# If the command line argument does not work then use a random number.
try:
    number = int(sys.argv[1])
except:
    print 'A number was not given, so a random number will be used.'
    number = randrange(10000000)

# Generate a sorted list of 100 thousand random numbers.
print 'Generating sorted random list...'
list = []
for i in range (0,100000):
    list.append(randrange(10000000))

# This does all the work.
list.sort()
insert_point = bisect (list, number)

# Show where number would be inserted.
print
print 'list[%d]=%d' % (insert_point - 1, list[insert_point - 1])
print ' > %s goes here <' % (number)
print 'list[%d]=%d' % (insert_point, list[insert_point])

# End.
