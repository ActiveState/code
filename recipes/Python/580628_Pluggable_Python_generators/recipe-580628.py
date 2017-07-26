# Program to show that generators are pluggable, i.e.,
# can be passed as function arguments, and then used 
# inside those functions to which they are passed.
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram

def gen_squares(fro, to):
    '''A generator function that returns a generator 
    that returns squares of values in a range.'''
    for val in range(fro, to + 1):
        yield val * val

def gen_cubes(fro, to):
    '''A generator function that returns a generator 
    that returns cubes of values in a range.'''
    for val in range(fro, to + 1):
        yield val * val * val

def use(gen):
    print "In use() function:"
    print "Using:", gen
    print "Items:",
    for item in gen:
        print item,
    print

print "Pluggable Python generators.\n"
print "In main module:"
print "type(use): ", type(use)
print "use:", use
print
print "type(gen_squares): ", type(gen_squares)
print "gen_squares: ", gen_squares
print "type(gen_squares(1, 5)): ", type(gen_squares(1, 5))
print "gen_squares(1, 5): ", gen_squares(1, 5)
print
print "type(gen_cubes): ", type(gen_cubes)
print "gen_cubes: ", gen_cubes
print "type(gen_cubes(1, 5)): ", type(gen_cubes(1, 5))
print "gen_cubes(1, 5): ", gen_cubes(1, 5)
print
for gen_obj in (gen_squares(1, 5), gen_cubes(1, 5)):
    use(gen_obj)
    print
