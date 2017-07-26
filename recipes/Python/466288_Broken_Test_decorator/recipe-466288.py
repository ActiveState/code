import unittest
import types

class BrokenTest(unittest.TestCase.failureException):
    def __repr__(self):
        name, reason = self.args
        return '%s: %s: %s works now' % (
            (self.__class__.__name__, name, reason))

def broken_test_XXX(reason, *exceptions):
    '''Indicates a failing (or erroneous) test case fails that should succeed.
    If the test fails with an exception, list the exception type in args'''
    def wrapper(test_method):
        def replacement(*args, **kwargs):
            try:
                test_method(*args, **kwargs)
            except exceptions or unittest.TestCase.failureException:
                pass
            else:
                raise BrokenTest(test_method.__name__, reason)
        replacement.__doc__ = test_method.__doc__
        replacement.__name__ = 'XXX_' + test_method.__name__
        replacement.todo = reason
        return replacement
    return wrapper

def find_broken_tests(module):
    '''Generate class, methodname for test cases marked "broken".'''
    for class_name in dir(module):
        class_ = getattr(module, class_name)
        if (isinstance(class_, (type, types.ClassType)) and
                      issubclass(class_, unittest.TestCase)):
            for test_name in dir(class_):
                if test_name.startswith('test'):
                    test = getattr(class_, test_name)
                    if (hasattr(test, '__name__') and
                                test.__name__.startswith('XXX_')):
                        yield class_, test_name

#######################################
##### Typical use in a test suite:
import unittest

class SillyTestCase(unittest.TestCase):
    def test_one(self):
        self.assertEqual(2 + 2, 4)

    def test_two(self):
        self.assertEqual(2 * 2, 4)

    @broken_test_XXX('arithmetic might change')
    def test_three(self):
        self.assertEqual(2 - 2, 4)

    @broken_test_XXX('exception failure demo', TypeError)
    def test_four(self):
        real, imaginary = 2 - 2j
        self.assertEqual(real, imaginary)

    @broken_test_XXX('exception failure demo', TypeError,
                             unittest.TestCase.failureException)
    def test_five(self):
        value = 2 - 2j
        real, imaginary = value.real, value.imag
        self.assertEqual(real, imaginary)


if __name__ == '__main__':
    # Typical report generation for a large suite
    import sys
    import sometests  # which may import other tests
    import moretests  # and so on.

    for module_name, module in sys.modules.iteritems():
        for class_, message in find_broken_tests(module):
            if module_name:
                print '\nIn module', module_name
                module_name = last_class = None
            if class_ != last_class:
                print '\nclass %s:' % class_.__name__
                last_class = class_
            print '  ', message, '\t', getattr(class_, message).todo
