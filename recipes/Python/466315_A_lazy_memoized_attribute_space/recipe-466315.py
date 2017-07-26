class LazySpace(object):
    def __init__(self, function):
        self.__dict__["function"] = function
        self.__dict__["arguments"] = {}
        
    def __call__(self, *args, **kw):
        arg_pack = args, kw
        return arg_pack
    
    def __setattr__(self, key, arg_pack):
        self.arguments[key] = arg_pack
        
    def __getattr__(self, key):
        args, kw = self.arguments[key]
        r = self.__dict__[key] = self.function(*args, **kw)
        return r


if __name__ == "__main__":

    def something_we_might_need(a,b,x=0):
        print 'Executing something_we_might_need'
        return "AB=%s, X=%s" % ((a*b),x)
        
        
    #create a lazy space for storing results from this function
    lz = LazySpace(something_we_might_need)
    
    #call our lazy function, and assign its results into an attribute in the 
    #lazy namespace
    lz.ab = lz(1,2,x=1)
    
    #print the attribute (notice this is when the function is first run)
    print lz.ab
    
    #next time the attibute is accessed, there is no need for the function to 
    #run again.
    print lz.ab
    
    #deleting the attribute will remove it from the lazy space, and force the 
    #function to run again, next time the attribute is accessed.
    del lz.ab
    
    print lz.ab
    
    
