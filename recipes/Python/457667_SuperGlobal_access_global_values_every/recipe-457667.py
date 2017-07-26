import __main__

class SuperGlobal:

    def __getattr__(self, name):
        return __main__.__dict__.get(name, None)
        
    def __setattr__(self, name, value):
        __main__.__dict__[name] = value
        
    def __delattr__(self, name):
        if __main__.__dict__.has_key(name):
            del  __main__.__dict__[name]

superglobal1 = SuperGlobal()
superglobal1.test = 1
print superglobal1.test
superglobal2 = SuperGlobal()
print superglobal2.test
del superglobal2.test
print superglobal1.test
print superglobal2.test
