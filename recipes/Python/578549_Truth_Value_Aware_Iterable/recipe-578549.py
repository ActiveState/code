from itertools import chain

class TruthValueAwareIterable(object):
    def __init__(self, iterable):
        self._iterator = iter(iterable)
        try:
            self._head = [self._iterator.next()]
            self._has_value = True
        except StopIteration:
            self._head = []
            self._has_value = False

    def __nonzero__(self):
        return self._has_value

    def __iter__(self):
        return chain(self._head, self._iterator)

if __name__ == "__main__":
    def integer_generator():
        yield 1
        yield 2
        yield 3

    assert not TruthValueAwareIterable(iter([]))
    assert TruthValueAwareIterable(integer_generator())

    assert list(TruthValueAwareIterable([])) == []
    assert list(TruthValueAwareIterable(integer_generator())) == [1, 2, 3]
