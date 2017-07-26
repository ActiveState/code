## Future decorator in a pretty pythonic way  
Originally published: 2011-10-20 16:51:47  
Last updated: 2011-10-20 16:51:48  
Author: Filippo Squillace  
  
Without thinking in thread creation the idea is to call several times 
a function assigning a thread for each call with related parameters 
and returning the list of results in a pretty pythonic way.
For example, if we have already defined the function 'func':
    res = func(par)
we want to call that several times and get the values in the future. So: 
    func(par1)
    func(par2)
    func(par3).get()
    func(par4).get_all()
    
assigning a thread for each call. The 'get' method returns the first possible results,
and 'get_all' returns all the values in a list. The decorator works fine with kwargs too.
    
This recipe is based on:
http://code.activestate.com/recipes/355651-implementing-futures-with-decorators/
that use only one call for the function. The problem in that recipe is that each call blocks the execution.

Vote if you like it!