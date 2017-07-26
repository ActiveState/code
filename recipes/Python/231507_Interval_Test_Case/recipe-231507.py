import unittest

class IntervalTestCase( unittest.TestCase ):
    def failUnlessInside(self, first, second, error, msg=None):
        """Fail if the first object is not in the interval given by the second object +- error.
        """
        if (first > second + error) or (first < second - error):
            raise self.failureException, \
                  (msg or '%s != %s (+-%s)' % (`first`, `second`, `error`))

    def failIfInside(self, first, second, error, msg=None):
        """Fail if the first object is in the interval given by the second object +- error.
        """
        if (first <= second + error) and (first >= second - error):
            raise self.failureException, \
                  (msg or '%s == %s (+-%s)' % (`first`, `second`, `error`))

    assertInside = failUnlessInside

    assertNotInside = failIfInside

class IntegerArithmenticTestCase( IntervalTestCase ):
    def testAdd(self):  ## test method names begin 'test*'
        self.assertInside((1 + 2), 3.3, 0.5)
        self.assertInside(0 + 1, 1.1, 0.01)
        
    def testMultiply(self):
        self.assertNotInside((0 * 10), .1, .05)
        self.assertNotInside((5 * 8), 40.1, .2)

if __name__ == '__main__':
    unittest.main()
