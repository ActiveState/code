def recursive(func):
    func.func_globals[func.__name__] = func
    return func

class Test:
    def method(self, x = False):
        if x:
            print(x)
        else:
            self.method("I'm method")

    @staticmethod
    def smethod(x = False):
        if x:
            print(x)
        else:
            method("I'm static method")

    @staticmethod
    @recursive
    def rmethod(x = False):
        if x:
            print(x)
        else:
            rmethod("I'm recursive method")
        
test = Test()

test.method()  # I'm method
test.rmethod() # I'm recursive method
test.smethod() # raises NameError: global name 'method' is not defined
