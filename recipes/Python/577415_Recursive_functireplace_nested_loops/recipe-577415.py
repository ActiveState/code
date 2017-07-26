def recursiveLooper(iterators, pos=0):
    """ Implements the same functionality as nested for loops, but is 
        more dynamic. iterators can either be a list of methods which
        return iterables, a list of iterables, or a combination of both.
    """
    nextLoop, v = None, []
    try:
        gen = iter(iterators[pos]())
    except TypeError:
        gen = iter(iterators[pos])
        
    while True:
        try:
            yield v + nextLoop.next()
        except (StopIteration, AttributeError):
            v = [gen.next(),]
                
            if pos < len(iterators) - 1:
                nextLoop = recursiveLooper(iterators, pos + 1)
            else:
                yield v

# Some examples of how to use it:
def gen():
    for x in [1, 2]:
        yield x

for x in gen():
    for y in gen():
        for z in gen():
            print x, y, z

print "-" * 10

for x, y, z in recursiveLooper([gen,] * 3):
    print x, y, z

print "-" * 10

for x, y, z in recursiveLooper([[1, 2],] * 3):
    print x, y, z
