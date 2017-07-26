#!/usr/bin/env python

"""
    pyunit2.py - extends the facilities in the unittest module (PyUnit ),
    which is supplied with the Python Standard Library (since version 2.1,
    see the unittest.py module or go to the original project home page at
    http://pyunit.sourceforge.net/pyunit.html for more info).

    Example:

    #!/usr/bin/env python

    from pyunit2 import * #includes class Fixture

    class ExampleTestFixture(Fixture):
        @test
        def anExampleTest(self):
            self.assertEqual(1, 2) #fails

        @test
        @expected_exception(NameError)
        def usingExpectedExceptions(self):
            class Foo: pass
            f = Foo()
            print f.non_existent_attribute

    if __name__ == "__main__":
        #the following line(s) equate to
        #import unittest
        #unittest.main()
        #... etc
        import pyunit2
        pyunit2.main()
"""
__author__ = "Tim Watson"
__version__ = "$Revision: 0.2 $"
__license__ = "Python"

##############################################################################
# Exported classes and functions
##############################################################################
__all__ = [
    'expected_exception',
    'test',
    'Fixture'
]

import unittest

##############################################################################
# utility classes
##############################################################################

class TestDeclaration( object ):
    declarations = {}
    def __init__( self, func, doc_string=None ):
        if func.func_name.startswith( "test" ): return
        func.__doc__ = doc_string or func.__doc__
        fname = "test_%s" % func.func_name
        if not fname in TestDeclaration.declarations:
            TestDeclaration.declarations[ fname ] = func

    def __call__( self, func ):
        if func.func_name.startswith( "test" ):
            def execute( *args, **kwargs ):
                return func( *args, **kwargs )
            return execute
        raise Exception( 'should not have arrived here!?' )

class ExpectedException( object ):
    def __init__( self, exception_class ):
        self.exception_class = exception_class

    def __call__( self, func ):
        def execute( *args, **kwargs ):
            self_pointer = args [ 0 ]
            assert not self_pointer is None
            self_pointer.assertRaises( self.exception_class,
                func, *args, **kwargs )
        return execute

##############################################################################
# replacement base class 'Fixture' and supporting meta-class(es)
##############################################################################

class TestFixtureManager( type ):
    """
    A meta-class for mapping the decorator based test syntax
    from this module, to standard PyUnit style test method names, etc.
    """
    def __new__( cls, name, bases, attrs ):
        new_class = type.__new__( cls, name, bases, attrs )
        if not bases: return new_class
        [ setattr( new_class, func_name, func )
            for func_name, func in TestDeclaration.declarations.iteritems() ]
        TestDeclaration.declarations.clear()
        return new_class

    def __init__( cls, name, bases, dict ):
        #todo: deal with fixture setup/teardown here!
        pass

class Fixture( unittest.TestCase ): __metaclass__ = TestFixtureManager

##############################################################################
# decorators to make declaring tests/expected exceptions easier!
##############################################################################

def test( func, doc_string=None ):
    """
        Marks a method as a test method. Removes the need
        to call all your test methods testXXX and so on.
    """
    return TestDeclaration( func, doc_string )

def expected_exception( ex_cls ):
    """
        Marks a method as expecting an exception of class -> ex_cls
    """
    return ExpectedException( ex_cls )

##############################################################################
# support for fixture wide setup/teardown (NOT IMPLEMENTED YET)
##############################################################################

def testFixtureSetUp():
    """
        Adds support for a setup method that runs
        only once per testcase/fixture. The method must be defined
        as a staticmethod.
    """
    pass

def testFixtureTearDown():
    """
        Adds support for a teardown method that runs
        only once per testcase/fixture. The method should be defined
        as a staticmethod.
    """
    pass

def main():
    unittest.main()

if __name__ == "__main__":
    main()
