# token_bucket.py
#! /usr/bin/python3

from time import time
from threading import Lock


class TokenBucket:
    """
    An implementation of the token bucket algorithm.
    """
    def __init__(self):
        self.tokens = 0
        self.rate = 0
        self.last = time()
        self.lock = Lock()

    def set_rate(self, rate):
        with self.lock:
            self.rate = rate
            self.tokens = self.rate

    def consume(self, tokens):
        with self.lock:
            if not self.rate:
                return 0

            now = time()
            lapse = now - self.last
            self.last = now
            self.tokens += lapse * self.rate

            if self.tokens > self.rate:
                self.tokens = self.rate

            self.tokens -= tokens

            if self.tokens >= 0:
                return 0
            else:
                return -self.tokens / self.rate


if __name__ == '__main__':
    import sys
    from time import sleep
    one_kb = 1024 * 1024
    bucket = TokenBucket()
    bucket.set_rate(one_kb)
    for _ in range(10):
        nap = bucket.consume(one_kb)
        sleep(nap)
        print(".")
    sys.exit(0)



#######################################################


#! /usr/bin/python3
 
import logging
import time
 
import unittest
 
from .token_bucket import TokenBucket
 
logging.disable(logging.CRITICAL)
 
 
class UtilsHTTPRateLimitTest(unittest.TestCase):
    def setUp(self):
        self.bucket = TokenBucket()
    def tearDown(self):
        pass
 
    def test_set_rate(self):
        self.bucket.set_rate(1024*1024)
        self.assertEqual(self.bucket.rate, 1024*1024)
        self.assertEqual(self.bucket.tokens, self.bucket.rate)
 
    def test_consume(self):
        self.assertEqual(self.bucket.consume(0), 0)
        self.assertEqual(self.bucket.consume(999), 0)
        self.bucket.set_rate(1024*1024)
        self.assertEqual(self.bucket.consume(1024*1024), 0)
        self.assertLessEqual(self.bucket.consume(1024*1024*2), 2)
        self.assertLessEqual(self.bucket.consume(1024*1024*4), 6)
        self.assertLessEqual(self.bucket.consume(1024*1024*6), 12)
        self.bucket.set_rate(1024*1024)
        time.sleep(1)
        self.assertEqual(self.bucket.consume(1024*1024), 0)
        self.assertGreater(self.bucket.consume(1024*1024), 0)
