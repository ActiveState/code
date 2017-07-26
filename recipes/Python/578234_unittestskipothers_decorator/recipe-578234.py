def skip_other_tests():
    """
    Decorator which skips all tests except the one decorated with it.
    Based on original python-ideas proposal:
    http://mail.python.org/pipermail/python-ideas/2010-August/007992.html
    Working with Python from 2.5 to 3.3.

    Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
    License: MIT
    """
    import unittest
    from unittest import TextTestRunner as _TextTestRunner

    class CustomTestRunner(_TextTestRunner):
        def run(self, test):
            if test._tests:
                for t1 in test._tests:
                    for t2 in t1._tests:
                        if t2._testMethodName == self._special_name:
                            return _TextTestRunner.run(self, t2)
                raise RuntimeError("couldn't isolate test")

    def outer(fun, *args, **kwargs):
        # monkey patch unittest module
        unittest.TextTestRunner = CustomTestRunner
        if hasattr(unittest, 'runner'):  # unittest2
            unittest.runner.TextTestRunner = CustomTestRunner
        CustomTestRunner._special_name = fun.__name__

        def inner(self):
            return fun(self, *args, **kwargs)
        return inner

    return outer


# ===================================================================
# --- test
# ===================================================================

if __name__ == '__main__':
    import unittest

    flag = []

    class TestCase1(unittest.TestCase):

        @skip_other_tests()
        def test_a(self):
            flag.append(None)

        def test_b(self):
            assert 0

        def test_c(self):
            assert 0

        def test_d(self):
            assert 0

    class TestCase2(unittest.TestCase):

        def test_a(self):
            assert 0

        def test_b(self):
            assert 0

        def test_c(self):
            assert 0

    unittest.main()
    assert flag == [None]
