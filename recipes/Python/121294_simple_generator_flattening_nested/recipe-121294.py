def flatten(*args):
    for arg in args:
            try: 
                for i in arg:
                    for l in flatten(i):
                        yield l

            except TypeError,e: yield arg


#---
# if you dislike the try and exception type of programming (which is
# usually a bit dangerous as it may hide a valid exception), you
# could instead do:

for arg in args: 
    if type(arg) in (type(()),type([])):
        for elem in arg:
            for f in flatten(elem):
                yield f
    else: yield arg

# which is obviously restricted to lists and tuples and does
# not work with user defined containers.
# note that you pass more than one container to flatten and
# all elements of every containers will yielded.
 
