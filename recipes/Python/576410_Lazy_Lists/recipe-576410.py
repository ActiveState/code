"""Module for the creation and use of iterator-based lazy lists.
this module defines a class LazyList which can be used to represent sequences
of values generated lazily. One can also create recursively defined lazy lists
that generate their values based on ones previously generated."""

__author__ = 'Dan Spitz'
__all__ = ('LazyList', 'RecursiveLazyList', 'lazylist')

import itertools
import abc

class LazyList(metaclass = abc.ABCMeta):
    """A Sequence whose values are computed lazily by an iterator.
    """
    def __init__(self, iterable):
        self._exhausted = False
        self._iterator = iter(iterable)
        self._data = []

    def __len__(self):
        """Get the length of a LazyList's computed data."""
        return len(self._data)

    def __getitem__(self, i):
        """Get an item from a LazyList.
        i should be a positive integer or a slice object."""
        if isinstance(i, int):
            #index has not yet been yielded by iterator (or iterator exhausted
            #before reaching that index)
            if i >= len(self):
                self.exhaust(i)
            elif i < 0:
                raise ValueError('cannot index LazyList with negative number')
            return self._data[i]

        #LazyList slices are iterators over a portion of the list.
        elif isinstance(i, slice):
            start, stop, step = i.start, i.stop, i.step
            if any(x is not None and x < 0 for x in (start, stop, step)):
                raise ValueError('cannot index or step through a LazyList with'
                                 'a negative number')
            #set start and step to their integer defaults if they are None.
            if start is None:
                start = 0
            if step is None:
                 step = 1

            def LazyListIterator():
                count = start
                predicate = ((lambda: True) if stop is None
                             else (lambda: count < stop))
                while predicate():
                    try:
                        yield self[count]
                    #slices can go out of actual index range without raising an
                    #error
                    except IndexError:
                        break
                    count += step
            return LazyListIterator()

        raise TypeError('i must be an integer or slice')

    def __iter__(self):
        """return an iterator over each value in the sequence,
        whether it has been computed yet or not."""
        return self[:]

    def computed(self):
        """Return an iterator over the values in a LazyList that have
        already been computed."""
        return self[:len(self)]

    def exhaust(self, index = None):
        """Exhaust the iterator generating this LazyList's values.
        if index is None, this will exhaust the iterator completely.
        Otherwise, it will iterate over the iterator until either the list
        has a value for index or the iterator is exhausted.
        """
        if self._exhausted:
            return
        if index is None:
            ind_range = itertools.count(len(self))
        else:
            ind_range = range(len(self), index + 1)

        for ind in ind_range:
            try:
                self._data.append(next(self._iterator))
            except StopIteration: #iterator is fully exhausted
                self._exhausted = True
                break

class RecursiveLazyList(LazyList):
    @abc.abstractmethod
    def _producer(self):
        """generator method that yields the LazyList's contents"""
        while False:
            yield

    def __init__(self, *args, **kwds):
        super().__init__(self._producer(*args, **kwds))

def lazylist(producer):
    """Decorator for creating a RecursiveLazyList subclass.
    This should decorate a generator function taking the LazyList object as its
    first argument which yields the contents of the list in order.
    """
    #ABCMeta is the metaclass of LazyList and its subclasses
    return abc.ABCMeta(producer.__name__,
                       (RecursiveLazyList,),
                       dict(_producer = producer))

#two examples
if __name__ = '__main__':
    #fibonnacci sequence in a lazy list.
    @lazylist
    def fibgen(lst):
        yield 0
        yield 1
        for a, b in zip(lst, lst[1:]):
            yield a + b
    fibs = fibgen() #now fibs can be indexed or iterated over as if it were
                    #an infinitely long list containing the fibonnaci sequence

    #prime numbers in a lazy list.
    @lazylist
    def primegen(lst):
        yield 2
        for candidate in itertools.count(3): #start at next number after 2
            #if candidate is not divisible by any smaller prime numbers,
            #it is a prime.
            if all(candidate % p for p in lst.computed()):
                yield candidate
    primes = primegen() #same for primes- treat it like an infinitely long list
                        #containing all prime numbers.
    print(fibs[0], fibs[1], fibs[2], primes[0], primes[1], primes[2])
    print(list(fibs[:10]), list(primes[:10]))
