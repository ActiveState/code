import os, sys

def locate_regression_tests():
    for path in sys.path:
        if os.path.isdir(path):
            path = os.path.join(path, 'test')
            if os.path.isdir(path):
                return path
    raise RuntimeError('unable to locate standard regression tests')
