class compare(object):
    def __init__(self, function):
        self.function = function

    def __eq__(self, other):
        def c(l, r): return l == r
        return comparator(self.function, c, other)

    def __ne__(self, other):
        def c(l, r): return l != r
        return comparator(self.function, c, other)

    def __lt__(self, other):
        def c(l, r): return l < r
        return comparator(self.function, c, other)

    def __le__(self, other):
        def c(l, r): return l <= r
        return comparator(self.function, c, other)
      
    def __gt__(self, other):
        def c(l, r): return l > r
        return comparator(self.function, c, other)

    def __ge__(self, other):
        def c(l, r): return l >= r
        return comparator(self.function, c, other)

class comparator(object):
    def __init__(self, function, comparison, value):
        self.function = function
        self.comparison = comparison
        self.value = value
      
    def __call__(self, *arguments, **keywords):
        return self.comparison(self.function(*arguments, **keywords), self.value)
