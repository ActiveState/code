class AttributeHelper(object):
    def __new__(typ, *attr_args, **attr_kwargs):
        self = object.__new__(typ)

        def f2(orig_func):
            def f3(*func_args, **func_kwargs):
                # Take argument list for original function
                return self(*func_args, **func_kwargs)

            f3.func_name = orig_func.func_name
            self.orig_func = orig_func
            self.new_func = f3
            self.__init__(*attr_args, **attr_kwargs)                
            return f3
        
        return f2
        
    def __init__(self, *attr_args, **attr_kwargs):
        return self.on_init(*attr_args, **attr_kwargs)
            
    def __call__(self, *args, **kwargs):
        return self.on_call(*args, **kwargs)
        
    def on_call(self, *args, **kwargs):
        return self.orig_func(*args, **kwargs)
   
##### Example
class DebugAttribute(AttributeHelper):
    def on_init(self, msg):
        self.msg = msg
        self.log = []
        self.new_func.print_log = self.print_log
        
    def on_call(self, *args, **kwargs):
        result = super(DebugAttribute, self).on_call(*args, **kwargs)
        self.log.append((args, kwargs,result))
        return result
        
    def print_log(self):
        name = self.orig_func.func_name
        for args, kwargs, result in self.log:
            join_str = ', '
            if args==():
                args_str = ''
                join_str=''
            else:
                args_str = ', '.join(str(i) for i in args)
                
            if kwargs=={}:
                kwargs_str = ''
                join_str=''
            else:
                kwargs_str = ', '.join('%s=%s'%(str(k),str(v)) for k,v in kwargs.items())
                
            result_str = str(result)
                
            print '%s(%s%s%s) -> %s'%(name, args_str, join_str, kwargs_str, result_str)
                
        
if __name__=='__main__':
    @DebugAttribute('hi')
    def hi(a,b):
        return a+b
        
    hi(1,2)
    hi(4,5)
    hi(a=6,b=9)
    hi.print_log()
