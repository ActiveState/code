class winnow:
    """A heap structure allows you to easily keep track of one extreme of a
    set of values, at the expense of most other forms of order.  The
    theory is explained in many places, including the heapq documentation
    (http://www.python.org/doc/2.3.4/lib/node162.html).

    The winnow heap is implemented as a fixed length list with the worst
    item at position 0.  Candidates worse than item 0 are ignored; when
    one is better, item 0 is dropped and the worst remaining item is brought
    to the front.  This happens in winnow.test.

    Because the length of its heap is unchanging and known in advance, the
    winnow can use shortcuts unavailable to the queue.  You'll see that four
    arguments are needed for instance construction:

      def __init__(self, length, op, abject, target, seq=[])

    Length is an integer indicating how many items you want to collect.
    Op is a comparison function, taking two arguments and returning true if
    the first argument is better than the second.  To select the lowest, you
    would use probably use operator.lt.  Abject is a value beneath
    consideration, something worse than all the values you want to consider.
    Target is abject's mirror, an unachievably good value.  This sets up a
    precondition - you have to know just a little about your data.

    The heap is initialised thus:

      self.heap = [abject] * length + [target]

    which already meets the heap invariant, saving the trouble of
    heapification.  As data is thrown against the heap, it  will fill up with
    real values.

    Winnow.answer returns the heap with abject and target values stripped
    away.  As syntax sugar,  __call__ calls test and answer in turn.
    """

    def __init__(self, length, op, abject, target, seq=[]):
        """Arguments:
        length - the number of items wanted.
        op - a comparison operator. op(a, b) should return true if a is 
        better than b, and false if b is best. If a and b are equally good,
        then either true or false will work, with differing effects.
        abject - a value such that op(x, abject) will return false for any
        values of x that you want to catch.
        target - a value such that op(target, x) will return false for 
        any value of x.
        seq - optional iterable to initialise the heap.
        """
        self.abject = abject
        self.target = target
        self.op = op
        self.length = length
        self.heap = [abject] * length + [target]
        if seq:
            self.test(*seq)

    def test(self, *args):
        """This method examines each argument in turn.  If one is more
        suitable than the worst in the heap, it displaces it and triggers
        some shuffling in the heap to bring the new worst item to the fore.
        """
        for x in args:
            if self.op(x, self.heap[0]):
                pos = 0
                while True:
                    child = 2 * pos + 1
                    if child >= self.length:
                        break
                    child += self.op(self.heap[child], self.heap[child + 1])
                    if not self.op(x, self.heap[child]):
                        break
                    self.heap[pos] = self.heap[child]
                    pos = child
                self.heap[pos] = x

    def answer(self):
        """Returns a list containing the best results so far. If less
        than <self.length> values have been tested, the list will be
        of corresponding length."""
        return [ x for x in self.heap[:-1] if x != self.abject ]


    def __call__(self, *args):
        """Both the above methods combined in a convenient syrup.

        >>> from  operator import ge
        >>> top5 = winnow(5, ge, -1e+1000, 1e+1000)
        >>> top5(*[x*x for x in range(10)])
        [25, 36, 64, 49, 81]
        >>> top5(45, 22, 777)
        [45, 49, 64, 777, 81]
        """
        self.test(*args)
        return self.answer()


import operator
inf = 1e9999  

def lowest(length, seq=[], abject=inf, target=-inf):
    return winnow(length, operator.lt, abject, target, seq)

def highest(length, seq=[], abject=-inf, target=inf):
    return winnow(length, operator.gt, abject, target, seq)



if __name__ == '__main__':
    #simpleminded  tests
    r = range(50)
    r2 = r + r
    import random
    random.shuffle(r)
    random.shuffle(r2)

    low5 = lowest(5)
    print low5(*r)
    #should contain 0,1,2,3,4 in arbitrary order

    high12 = highest(12, r2)
    print high12()
    # should contain range(44,50) twice over, in arbitrary order.

    def cmp_3s(a, b):
        return str(a).count('3') > str(b).count('3')

    def most_3s(length, seq):
        return winnow(length, cmp_3s, '', '3'*50, seq)

    print most_3s(5, r2)()
    #should contain two 33s and three numbers with one 3
