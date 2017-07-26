from inspect import getcallargs, getargspec, ismethod
from functools import wraps

class KeywordRepeatedTypeError(TypeError): pass

def insert_keyword_first(fun, a, k): # based on recipe: 577922
    a = list(a)
    for idx, arg in enumerate(getargspec(fun).args, -ismethod(fun)): # or [0] in 2.5
        if arg in k:
            if idx < len(a):
                a.insert(idx, k.pop(arg))
            else:
                break
    return (a, k)

def currying(f):
    def collector(*a, **k):
        @wraps(f)
        def caller(*args, **kwargs):
            try:
                for key in kwargs:
                    if key in k:
                        raise KeywordRepeatedTypeError(
                            "TypeError: %s() got multiple values "
                            "for keyword argument '%s'" % (f.func_name, key))
                kwargs.update(k)
                args, kwargs = insert_keyword_first(f, a + args, kwargs)
                getcallargs(f, *args, **kwargs)
            except KeywordRepeatedTypeError, e:
                raise TypeError(e)
            except TypeError:
                spec = getargspec(f)
                if not spec.keywords:
                    for key in kwargs:
                        if key not in spec.args:
                            raise
                if len(spec.args) > len(args) + len(set(spec.args) & set(kwargs)):
                    return collector(*args, **kwargs)
                raise
            else:
                return f(*args, **kwargs)
        return caller
    return collector()

if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_args(self):
            
            @currying
            def function(a, b, c, d, e, f, *ar, **kw): return (a, b, c, d, e, f, ar, kw)
            print function(2, e=5)(4)(x=100, y=1000)(c=3, a=1)(6, 7, 8, z=10000)
            #returns (1, 2, 3, 4, 5, 6, (7, 8), {'y': 1000, 'x': 100, 'z': 10000})

            @currying
            def args(a, b, c): return (a, b, c)
            self.assertEquals(args()()(a=1)()(2, 3), (1, 2, 3))
            with self.assertRaises(TypeError): args(d=4)
       
            f = args(1)
            for x in range(1, 6):
                ff = f(x)
                for y in range(10, 101, 30):
                    print ff(y)

            @currying
            def default_args(a=10, b=20, c=30): return (a, b, c) #cannot curry but works
            self.assertEquals(default_args(1, c=3), (1, 20, 3))
    
            @currying
            def varargs_keywords(*a, **k): 
                '''function like that canonot be curried
                because it always eats up all arguments on the first call, but will work anyway...'''
                return a, k
       
            @currying
            def args_varargs(a, b, c, *ar): return a, b, c, ar
            self.assertEquals(args_varargs(1, c=3)(2, 4), (1, 2, 3, (4,)))
            with self.assertRaises(TypeError): args_varargs(d=4)
    
            @currying
            def args_keywords(a, b, c, **k): return a, b, c, k
            self.assertEquals(args_keywords(d=4)(1, 3)(b=2), (1, 2, 3, {'d':4}))
            with self.assertRaises(TypeError): args_keywords(c=3)(4, b=2, a=1)

            @currying
            def args_varargs_keywords(a, b, c, *ar, **k): return a, b, c, ar, k
            self.assertEquals(args_varargs_keywords(1, 2)(3, d=4), (1, 2, 3, (), {'d':4}))
            self.assertEquals(args_varargs_keywords(d=6)(2,a=1)(4,5, c=3), (1,2,3,(4,5),{'d':6}))
            with self.assertRaises(TypeError): args_varargs_keywords(a=1)(a=2)(3, 4)
       
            class ObjectMethod(object):
                @currying
                def metdhod(self, a, b): return a, b
            self.assertEquals(ObjectMethod().metdhod(2)(a=1), (1,2))
            self.assertEquals(ObjectMethod().metdhod(a=1)(2), (1,2))   
    unittest.main()

   
   
