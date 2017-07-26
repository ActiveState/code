# by Tarek Ziadé

# let's use pystone instead of seconds here
# (from Stephan Richter idea)
from test import pystone
import time

# TOLERANCE in Pystones
kPS = 1000
TOLERANCE = 0.5*kPS 

class DurationError(AssertionError): pass

def local_pystone():
    return pystone.pystones(loops=pystone.LOOPS)

def timedtest(max_num_pystones, current_pystone=local_pystone()):
    """ decorator timedtest """
    if not isinstance(max_num_pystones, float):
        max_num_pystones = float(max_num_pystones)

    def _timedtest(function):
        def wrapper(*args, **kw):
            start_time = time.time()
            try:
                return function(*args, **kw)
            finally:
                total_time = time.time() - start_time
                if total_time == 0:
                    pystone_total_time = 0
                else:
                    pystone_rate = current_pystone[0] / current_pystone[1]
                    pystone_total_time = total_time / pystone_rate
                if pystone_total_time > (max_num_pystones + TOLERANCE):
                    raise DurationError((('Test too long (%.2f Ps, '
                                        'need at most %.2f Ps)')
                                        % (pystone_total_time,
                                            max_num_pystones)))
        return wrapper

    return _timedtest

This decorator is not to use in production code, and would rather
 fit in functional or unit tests. This make performance tests portable to any box and fits performance regression tests you would want to run in unit tests.

For example, in this test we want to be sure test_critical() does not last more than 2kPS:

  >>> import unittest
  >>> class MesTests(unittest.TestCase):
  ...     @timedtest(2*kPS)
  ...     def test_critical(self):
  ...         a =''
  ...         for i in range(50000):
  ...             a = a + 'x' * 200
  >>> suite = unittest.makeSuite(MesTests)
  >>> unittest.TextTestRunner().run(suite)
  <unittest._TextTestResult run=1 errors=0 failures=0>
