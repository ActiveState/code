__author__ = "Andrey Nikishaev"
__copyright__ = "Copyright 2010, http://creotiv.in.ua"
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "Andrey Nikishaev"
__email__ = "creotiv@gmail.com"
__status__ = "Production"

"""
Simple local cache.
It saves local data in singleton dictionary with convenient interface

Examples of use:
    # Initialize
    SimpleCache({'data':{'example':'example data'}})
    # Getting instance
    c = SimpleCache.getInstance()
    
    c.set('re.reg_exp_compiled',re.compile(r'\W*'))
    reg_exp = c.get('re.reg_exp_compiled',default=re.compile(r'\W*'))

or

    c = SimpleCache.getInstance()
    reg_exp = c.getset('re.reg_exp_compiled',re.compile(r'\W*'))

or
    @scache
    def func1():
        return 'OK'

"""

class SimpleCache(dict):
    
    def __new__(cls,*args):
        if not hasattr(cls,'_instance'):
            cls._instance = dict.__new__(cls)
        else:
            raise Exception('SimpleCache already initialized')
        return cls._instance
    
    @classmethod
    def getInstance(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = dict.__new__(cls)
        return cls._instance

    def get(self,name,default=None):
        """Multilevel get function.
        Code:        
        Config().get('opt.opt_level2.key','default_value')
        """
        if not name: 
            return default
        levels = name.split('.')
        data = self            
        for level in levels:
            try:            
                data = data[level]
            except:
                return default

        return data
    
    def set(self,name,value):
        """Multilevel set function
        Code:        
        Config().set('opt.opt_level2.key','default_value')
        """
        levels = name.split('.')
        arr = self        
        for name in levels[:-1]:
            if not arr.has_key(name):         
                arr[name] = {}   
            arr = arr[name]
        arr[levels[-1]] = value
        
    def getset(self,name,value):
        """Get cache, if not exists set it and return set value
        Code:        
        Config().getset('opt.opt_level2.key','default_value')
        """
        g = self.get(name)
        if not g:
            g = value
            self.set(name,g)
        return g

def scache(func):
    def wrapper(*args, **kwargs):
        cache = SimpleCache.getInstance()
        fn = "scache." + func.__module__ + func.__class__.__name__ + \
             func.__name__ + str(args) + str(kwargs)		
        val = cache.get(fn)
        if not val:
            res = func(*args, **kwargs)
            cache.set(fn,res)
            return res
        return val
    return wrapper
