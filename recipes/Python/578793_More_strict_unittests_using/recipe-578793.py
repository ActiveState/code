"""
.. module:: decorators
    :platform: Unix, Windows
    :synopis: some decorator tools

.. moduleauthor:: Thomas Lehmann <thomas.lehmann.private@googlemail.com>

   =======
   License
   =======
   Copyright (c) 2014 Thomas Lehmann

   Permission is hereby granted, free of charge, to any person obtaining a copy of this
   software and associated documentation files (the "Software"), to deal in the Software
   without restriction, including without limitation the rights to use, copy, modify, merge,
   publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
   to whom the Software is furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all copies
   or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import inspect

if sys.version.startswith("2."):
    from types import NoneType
else:
    NoneType = type(None)

class ValidateTestResponsibilityFor(object):
    """ a class decorator that throws an exception when the test class does not
        implement all tests for all methods of the testable class (unit).
        The next code gives you an example on how it is used and what does happen:

        >>> class Value:
        ...     def __init__(self, value):
        ...         self.value = value
        ...
        >>> try:
        ...     import unittest
        ...     @ValidateTestResponsibilityFor(Value)
        ...     class TestValue(unittest.TestCase):
        ...         pass
        ... except Exception as e:
        ...     print("|%s|" % str(e).strip())
        |...failed to provide test method 'TestValue.testInit' for method 'Value.__init__'|

    """
    def __init__(self, testableClass, includeClassName=False):
        """ stores the class for test and checks all methods of that class """
        if hasattr(testableClass, "decorated_object"):
            testableClass = testableClass.decorated_object

        self.testableClass = testableClass
        self.includeClassName = includeClassName
        self.methodsInTestableClass\
            = self.getEntries(self.testableClass, inspect.isfunction)\
            + self.getEntries(self.testableClass, inspect.ismethod)


    @staticmethod
    def getEntries(the_class, mode):
        """ get all entries by given mode (function or method) but the
            members of the concrete class only; not from its base """

        classes = {}
        for concrete_class in reversed(inspect.getmro(the_class)):
            classes[concrete_class] = {}
            for name, definition in dict(inspect.getmembers(concrete_class, mode)).items():
                object_name = name
                is_base_method_only = False

                for known_class in classes:
                    if not object_name in classes[known_class]:
                        continue

                    if classes[known_class][object_name] == definition:
                        is_base_method_only = True
                        break

                if not is_base_method_only:
                    classes[concrete_class][object_name] = definition

        return list(classes[the_class].keys())

    def __call__(self, testClass):
        """ called when instantiated; then we have to verify for the required test methods """
        self.verify(testClass)
        return testClass

    @staticmethod
    def getTestMethod(name, prefix=""):
        """ adjusting final test method name """
        # no underscores wanted (change "__init__" => "init")
        finalName = name.strip("_")
        # if we find "_" as separator between words ...
        if finalName.find("_") > 0:
            finalName = "".join(subName.title() for subName in finalName.split("_"))

        # ensure more readable name (like "equal" instead of "eq")
        if name == "__eq__":
            finalName = "equal"
        elif name == "__lt__":
            finalName = "less"
        elif name == "__gt__":
            finalName = "greater"

        return "test" + prefix + finalName[0].upper() + finalName[1:]

    def verify(self, test_class):
        """ verification that for each testable method a test method does exist """
        methodsInTestClass\
            = self.getEntries(test_class, inspect.isfunction)\
            + self.getEntries(test_class, inspect.ismethod)

        missing = []
        for testableMethod in self.methodsInTestableClass:
            prefix = ""
            if self.includeClassName:
                prefix = self.testableClass.__name__

            testMethod = self.getTestMethod(testableMethod, prefix)
            if testMethod in methodsInTestClass:
                continue

            missing.append((test_class.__name__ + "." + testMethod,
                            self.testableClass.__name__ + "." + testableMethod))

        if len(missing) > 0:
            # creates message with all missing methods throwing an exception for it
            message = ""
            for testMethod, testableMethod in missing:
                message += "\n...failed to provide test method '%s' for method '%s'" \
                           % (testMethod, testableMethod)
            raise Exception(message)
