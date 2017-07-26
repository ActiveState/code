"""
    @author  Thomas Lehmann
    @file    enum.py

    @note The singleton example is taken from:
          http://www.python.org/dev/peps/pep-0318/#examples
    @note I don't use TAB's and indentation is 4.
    @note epydoc wrongly interprets the class as a function.
          Probably because of the decorator (without it works).
"""
__docformat__ = "javadoc en"

import inspect
import unittest

def singleton(theClass):
    """ decorator for a class to make a singleton out of it """
    classInstances = {}

    def getInstance():
        """ creating or just return the one and only class instance """
        if theClass not in classInstances:
            classInstances[theClass] = theClass()
        return classInstances[theClass]

    return getInstance

@singleton
class Enum(object):
    """ class for providing enum functionality. An enum in C++ usually looks
        like this: enum { A, B, C }; and the results are 0, 1 and 2 for A, B and C.
        We provide similar functionality means auto incrementing of values for constants
        added to an enum...

        >>> TOP    = enum("direction") # or enum(Direction) when Direction is a class
        >>> LEFT   = enum("direction") # or enum(Direction) when Direction is a class
        >>> RIGHT  = enum("direction") # or enum(Direction) when Direction is a class
        >>> BOTTOM = enum("direction") # or enum(Direction) when Direction is a class
        >>> assert TOP < LEFT < RIGHT < BOTTOM

        <ul>
            <li>You still can assign an individual value.
            <li>You can place constants inside the class (if you like) -> Direction.TOP
            <li>Same to C++: you have to pay attention where new constants are added. When
                you insert it inbetween then you will 'move' the other values.
        </ul>
    """

    def __init__(self):
        """ registered enums """
        self.contexts = {}

    def getNextId(self, context):
        """ providing next id >= 0 on each call per context
            @param context is a string
            @return is an integer value being unique for given context
        """
        if not context in self.contexts:
            self.contexts[context] = -1
        self.contexts[context] += 1
        return self.contexts[context]

def enum(context):
    """ wrapper for calling the singleton. Documentation is placed
        at the class Enum.
        @param context can be a string or a class
        @return is an integer value being unique for given context
    """
    if inspect.isclass(context):
        return Enum().getNextId(context.__name__)
    return Enum().getNextId(context)

class EnumTestCase(unittest.TestCase):
    """ testing of class Enum """

    def testSingleton(self):
        """ testing the singleton mechanism """
        instanceA = Enum()
        instanceB = Enum()
        self.assertEqual(instanceA, instanceB)

    def testGetNextId(self):
        """ example of creating two constants """
        instance   = Enum()
        HORIZONTAL = instance.getNextId("orientation")
        VERTICAL   = instance.getNextId("orientation")
        self.assertTrue(HORIZONTAL < VERTICAL)

    def testEnumFunctionWithStringContext(self):
        """ example of creating four constants with string as context """
        class Direction:
            TOP    = enum("direction")
            LEFT   = enum("direction")
            RIGHT  = enum("direction")
            BOTTOM = enum("direction")

        self.assertTrue(Direction.TOP < Direction.LEFT < Direction.RIGHT < Direction.BOTTOM)

    def testEnumFunctionWithClassContext(self):
        """ example of creating four constants with a class as context
            @note I have tried to move the enum code to the class but this
                  seems not to work """
        class Vector:
            def __init__(self):
                self.vector = [0, 0]

        X = enum(Vector)
        Y = enum(Vector)

        self.assertTrue(X < Y)
        self.assertEqual(X, 0)
        self.assertEqual(Y, 1)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(EnumTestCase)
    unittest.TextTestRunner(verbosity=3).run(suite)
