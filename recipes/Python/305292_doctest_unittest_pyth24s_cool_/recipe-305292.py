A simple doctest involves pasting the results of actually using a
function into a string at the beginning of the function.  Doctest then
checks to make sure that the usage examples work, including
errors. Note -- doctest ignores traceback information, just include
the first line of the traceback and the actual error. In this case,
create a file called example1.py and put into it the following add
function. Simply, running example1.py is all that is necessary to go
thru the tests. If you run example1.py -y, you'll get verbose output.

def add(a,b):
     """
     >>> import example1
     >>> example1.add(1,2)
     3
     >>> example1.add([1],[2])
     [1, 2]
     >>> example1.add([1],2)
     Traceback (most recent call last):
     TypeError: can only concatenate list (not "int") to list
     """
     return a+b

if __name__ == "__main__":
    print '**running standard doctest'
    import doctest,example1
    doctest.testmod(example1)


#To put additional doctests somewhere else and make them a unittest
#testcase, put your tests in a different file like test1.txt. Note ---
#no quoting needed

 >>> import example1
 >>> example1.add('a','b')
'ab'

#then add a few likes of code to the end of example1.py to run the unittest
if __name__ == "__main__":
    print '**running standard doctest'
    import doctest,example1
    doctest.testmod(example1)
    print '**running unittest doctest'
    suite = doctest.DocFileSuite('test1.txt')
    unittest.TextTestRunner().run(suite)
