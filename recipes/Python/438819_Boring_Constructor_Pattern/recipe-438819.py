def vars_private(func):
    def wrapper(*args):
        for i, arg in enumerate(args[1:]):
            setattr(args[0], '_' + func.func_code.co_varnames[i + 1], arg)
        return func(*args)
    return wrapper


# -- Test --
class Student:
    @vars_private
    def __init__(self, name, age):
        # make young
        self._age = self._age - 2
    
    def info(self):
        return self._name, self._age

s = Student('Ravi Teja', 28)
print s.info()
