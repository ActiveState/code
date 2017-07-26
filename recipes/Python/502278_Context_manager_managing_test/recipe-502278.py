from contextlib import contextmanager
import os

@contextmanager
def test_file(path):
    try:
        open_file = open(path, 'w')
        yield open_file
    finally:
        open_file.close()
        if os.path.exists(path):
            os.unlink(path)
