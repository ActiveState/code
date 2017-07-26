"""
   Copyright 2011 Shao-Chuan Wang <shaochuan.wang AT gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import operator
from itertools import imap, repeat
import functools

iterable = lambda obj: isinstance(obj, basestring) or hasattr(obj, '__iter__')
def vector_op(op, x, y):
    if iterable(x) and iterable(y):
        return type(x)(imap(op, x, y))
    if not iterable(x):
        return type(y)(imap(op, repeat(x), y))
    if not iterable(y):
        return type(x)(imap(op, x, repeat(y)))

vector_add = functools.partial(vector_op, operator.add)
vector_sub = functools.partial(vector_op, operator.sub)
vector_mul = functools.partial(vector_op, operator.mul)
vector_div = functools.partial(vector_op, operator.div)
vector_and = functools.partial(vector_op, operator.and_)
vector_or  = functools.partial(vector_op, operator.or_)

def vector_sum(has_len):
    if not has_len:
        return has_len
    return reduce(vector_add, has_len)

def vector_mean(has_len):
    vsum = vector_sum(has_len)
    return type(vsum)(float(e)/float(len(has_len)) for e in vsum)

if __name__ == '__main__':
    positions = [(1,2,1), (3,4,3), (5,6,3)]
    print vector_sum(positions)
    print vector_mean(positions)
