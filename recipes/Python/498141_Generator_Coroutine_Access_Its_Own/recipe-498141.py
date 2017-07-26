# sample generator coroutine getting access to its own handle

import functools

def coroutine(function):
    """
    decorator to create a generator coroutine 
    Note that except for the calll to 'send()', this comes from PEP 342
    """
    @functools.wraps(function)
    def wrapper(*args, **kw):
        generator = function(*args, **kw) 
        result = generator.next() # one to get ready
        result = generator.send(generator) # two to store our own handle   
        return generator        
    return wrapper

process_queue = list() # queue for some imaginary process

def factory():
    @coroutine
    def test_function():
        """a simple function to test the coroutine decorator"""
        this_generator = (yield "foop")
        process_queue.append(this_generator)
    
        # now pretend to do some real work
        while True:
            result = (yield 42)
    return test_function()

print "creating generator instance"    
factory()

print "obtaining instance from queue"
generator = process_queue.pop()

print "executing one step"
x = generator.send(None)

print "result =", x         
