"""
Implemetation of eiffel like methods (methods with preconditions and postconditions).

eiffelmethod is a new descriptor that implements eiffel like methods. It accepts a method and 
optional pre and post conditions. fI the pre or post conditions are not given it searchs methodName_pre
and methodName_post.
"""

import types 

class eiffelmethod(object):
    def __init__(self, method, pre=None, post = None):
        self._method = method
        self._pre = pre
        self._post = post
    def __get__(self, inst, type=None):
    	result = EiffelMethodWraper(inst,self._method,self._pre, self._post) 
    	setattr(inst, self._method.__name__,result)
        return result

class EiffelMethodWraper:
    def __init__(self, inst, method, pre, post):
        self._inst = inst
        self._method = method
        if not pre:
        	pre = getattr(inst,method.__name__+"_pre",None)
        	if pre: pre = pre.im_func
        self._pre = pre
        if not post:
        	post = getattr(inst,method.__name__+"_post",None)
        	if post: post = post.im_func
        self._post = post
   
    def __call__(self, *args, **kargs):
        if self._pre:
        	apply(self._pre,(self._inst,)+args, kargs)
        result = apply(self._method,(self._inst,)+args, kargs)
        if self._post:
			apply(self._post,(self._inst,result)+args, kargs)
        return result

def _test():
    class C:
        def f(self, arg):
            return arg+1
        def f_pre(self, arg):
            assert arg>0
        def f_post(self, result, arg):
            assert result>arg
        f = eiffelmethod(f,f_pre,f_post)
    c = C()
    c.f(1)
    try:
    	c.f(-1)
    except AssertionError:
    	pass
    else:
    	raise "c.f(-1) bad implemented"
    print "OK"


if __name__=='__main__':
    _test()
