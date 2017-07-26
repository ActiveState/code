## Python Unittest - Obtain the results of all the tests run as a listOriginally published: 2014-04-24 08:20:37 
Last updated: 2014-04-24 08:52:32 
Author: Cosmin Niculae 
 
So far, there is no way of returning the results of the tests run with unittest in any form, except for having the results printed. The purpose of this code is to have the name of the test cases, their indexes, as well as the results (Pass, Fail, Error) as a list. This is extremely used when you want to create a table with the results, as it has all the information needed. \n\nThe affected file is the result.py in the unittest library folder.