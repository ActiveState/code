# Driving Python function execution from a text file.
# Author: Vasudev Ram: 
# https://vasudevram.github.io, 
# http://jugad2.blogspot.com
# Copyright 2016 Vasudev Ram

def square(n): return n * n
def cube(n): return n * square(n)
def fourth(n):  return square(square(n))

# 1) Define the fns dict literally ...
#fns = {'square': square, 'cube': cube, 'fourth': fourth}
# 2a) ... or programmatically with a dict comprehension ...
fns = { fn.func_name : fn for fn in (square, cube, fourth) }
# OR:
# 2b) 
# fns = { fn.__name__ : fn for fn in (square, cube, fourth) }
# The latter approach (2a or 2b) scales better with more functions, 
# and reduces the chance of typos in the function names.

with open('functions.txt') as fil:
    for line in fil:
        print
        line = line[:-1] 
        if line.lower() not in fns:
            print "Skipping invalid function name:", line
            continue
        for item in range(1, 5):
            print 'item: ' + str(item) + ' : ' + line + \
            '(' + str(item) + ') : ' + str(fns[line](item)).rjust(3)
