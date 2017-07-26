class C:
    def handlerFunctionClosure(self,name):
        def handlerFunction(*args,**kwargs):
            print name,args,kwargs    # do what you want to here
        return handlerFunction
    def __getattr__(self,name):
        return self.handlerFunctionClosure(name)

# Use as follows
# >>> c = C()
# >>> c.foo(1,color="blue")
#foo (1,) {'color': 'blue'}
