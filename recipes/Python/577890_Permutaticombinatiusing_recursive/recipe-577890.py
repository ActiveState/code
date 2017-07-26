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

def permute(alist):
    if len(alist) <= 1:
        yield alist
        alist = []

    for s in alist:
        rest = list(alist[:])
        rest.remove(s)
        for p in permute(rest):
            yield [s] + p

def choosenk(alist, n):
    if len(alist) <= n:
        yield alist
        alist = []

    if alist:
        head = alist[0]
        rest = list(alist[1:])
        for c in choosenk(rest, n-1):
            yield [head] + c
        for c in choosenk(rest, n):
            yield c


def test_permute(lst):
    print('\n%s permute(%s):' % ('-' * 20, lst))
    for p in permute(lst):
        print(p)


def test_chosenk(lst, n):
    print('\n%s choosenk(%s, %d):' % ('-' * 20, lst, n))
    for c in choosenk(lst, n):
        print(c)


test_permute([1,2,3,4])
test_permute('abc')
test_permute('')
test_permute([1])

test_chosenk([1,2,3,4], 2)
test_chosenk('abc', 2)
test_chosenk('abc', 1)
test_chosenk('abc', 0)
test_chosenk('a', 2)
test_chosenk('', 2)
