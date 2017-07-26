from threading import Thread, Event

class future:
    """
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
    """
    def __init__(self, f):
        self.__f = f
        self.__init_values__()
    
    def __init_values__(self):
        self.__thread = []
        self.__vals = []
        self.__exception = None
        self.__curr_index = 0
        self.__event = Event()
        
    def __call__(self, *args, **kwargs):
        t = Thread(target=self.runfunc, args=args, kwargs=kwargs)
        t.start()
        self.__thread.append(t)
        return self
    
    def runfunc(self, *args, **kw):
        try:
            self.__vals.append(self.__f(*args, **kw))
            self.__event.set()
        except Exception, e:
            self.__exception = e

    def get(self):
        """
        Returns the first possible value without order of calling the function.
        """
        if self.__curr_index == len(self.__thread):
            raise IndexError('The element doesn\'t exists')
        if not self.__event.is_set():
            self.__event.wait()
        self.__event.clear()
        res = self.__vals[self.__curr_index]
        self.__curr_index += 1
        return res

    
    def get_all(self):
        """
        Returns all the possible values and initialize them.
        """
        for t in self.__thread:
            t.join()
        
        if self.__exception is not None:
            raise self.__exception

        res = self.__vals
        
        # Get rid of everything
        self.__init_values__()
        
        return res

    

if __name__ == '__main__':
    import time
    import unittest
    

    
    @future
    def sleeping(s, t):
        time.sleep(s)
        return 'slept for '+str(s) + ' sec dreaming: ' + str(t)
    
    sleeping(2, t='world')
    sleeping(5, 'sheeps')
    sleeping(1, t='soccer')
    print(sleeping(2, t='women').get())
    print(sleeping(1, 'beach').get_all())
    
    class FutureTestCase(unittest.TestCase):
        def tearDown(self):
            sleeping(0, '').get_all()
            
        def test_positive(self):
            sleeping(5, t='sheeps')
            sleeping(1, 'beach')
            o = sleeping(3, 'nothing')
            res = o.get_all()
            self.assertEqual(3, len(res))

        def test_bad_index(self):
            sleeping(5, t='sheeps')
            o = sleeping(4, 'world')
            o.get()
            o.get()
            self.assertRaises(IndexError, o.get)
            
    unittest.main(verbosity=2)
    
    
