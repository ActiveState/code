## More strict unittests using a validator  
Originally published: 2013-12-20 10:35:15  
Last updated: 2014-03-01 12:37:47  
Author: Thomas Lehmann  
  
The main point is that **there was no binding between a unit tests and the concrete class**. It did happend often that you are indirectly testing a class using it also the concrete test class has missed some concrete test methods. I found this fact sometimes very irritating seeing 100% coverage.

Therefor I now provide this class decorator where you can specify the class that will be tested. If you do not specify test methods for each method of the testable class **an exception will be thrown providing a list of missed tests**.

Here some examples how it works: You implemented a
 * method "__eq__", then write a "testEqual" method
 * method "__init__", then write a testInit" method
 * method "scalar_product", then write a testScalarProduct" method
 * and so on ...

The way to use this class decorator you can see in the doctest area (see below in the code)
The only point to be aware of is that when you use the decorator you have to implement all test to get rid of the thrown execption. Of course you can implement more tests for same class.

New in revision 4 (1st march 2014):

 * Bugfix: the algorithm were not correctly detecting which methods were really overwritten forcing to implement tests for methods which were base class only.
 * Bugfix: decorated classes which contain the attribute "decorated_object" can be handled properly. 
 * A new second parameter now allows you to implement several classes in same test class forcing you to include the class name in the test method:

   
  * @ValidateTestResponsibilityFor(Square, True)
  * @ValidateTestResponsibilityFor(Sin, True)
  * => testSquareInit, testSquareGet, testSinInit, testSinGet, ...
  * This for smaller classes to avoid too many files (at least ... you decided)
