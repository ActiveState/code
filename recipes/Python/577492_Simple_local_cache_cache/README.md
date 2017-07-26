## Simple local cache and cache decorator  
Originally published: 2010-12-08 09:03:01  
Last updated: 2010-12-08 09:06:34  
Author: Andrey Nikishaev  
  
Simple local cache.
It saves local data in singleton dictionary with convenient interface

#Examples of use:
    # Initialize
    SimpleCache({'data':{'example':'example data'}})
    # Getting instance
    c = SimpleCache.getInstance()
    
    c.set('re.reg_exp_compiled',re.compile(r'\W*'))
    reg_exp = c.get('re.reg_exp_compiled',default=re.compile(r'\W*'))

    # --------------------------------------------------------------

    c = SimpleCache.getInstance()
    reg_exp = c.getset('re.reg_exp_compiled',re.compile(r'\W*'))

    # --------------------------------------------------------------    

    @scache
    def func1():
        return 'OK'