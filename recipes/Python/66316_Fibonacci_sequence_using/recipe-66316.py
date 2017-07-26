from __future__ import generators

# needs Python 2.2 or above!
def fib():
    "unbounded generator, creates Fibonacci sequence"
    x = 0
    y = 1
    while 1:
        x, y = y, x + y
        yield x


if __name__ == "__main__":
    g = fib()
    for i in range(9):
        print g.next(),
