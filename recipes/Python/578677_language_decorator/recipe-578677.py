import sys

import lua as _lua  # lua (lunatic-pathon)
import os           # bash
import scipy.weave  # Cpp

# more languages can and should be added


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# Definition of Decorators
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def lua(function):
    def wrapper(*args):
        # 1. Do some preprocessing.
        #print function.__doc__

        # 2. Call 'function' with given arguments.
        _lua.execute(function.__doc__)
        function(*args)

        # 3. Do some postprocessing.
        # ...
    return wrapper

def bash(function):
    def wrapper(*args):
        # 1. Do some preprocessing.
        #print function.__doc__

        # 2. Call 'function' with given arguments.
        os.system(function.__doc__)
        function(*args)

        # 3. Do some postprocessing.
        # ...
    return wrapper

def Cpp(function):
    def wrapper(*args):
        # 1. Do some preprocessing.
        #print function.__doc__
 
        # 2. Call 'function' with given arguments.
        #scipy.weave.inline(function.__doc__,
        #                   ['u', 'dx2', 'dy2', 'dnr_inv', 'nx', 'ny'],
        #                   type_converters=converters.blitz,
        #                   compiler = 'gcc')
        scipy.weave.inline(function.__doc__)
        function(*args)

        # 3. Do some postprocessing.
        # ...
    return wrapper


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# Example
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

@lua
def lua_test():
    """print('lua run')
       print('Hello lua World')
       print('lua ok')
    """
    pass

@bash
def bash_test():
    """echo bash run
       echo Hello bash world!
       ls -la
       echo bash ok
    """
    pass

@Cpp
def Cpp_test():
    """printf("C++ run\\n");
       printf("Hello C++ world!\\n");
       printf("C++ ok\\n");
    """
    pass


print "run\n"

lua_test()
print "\n"
bash_test()
print "\n"
Cpp_test()
print "\n"

print "ok"
