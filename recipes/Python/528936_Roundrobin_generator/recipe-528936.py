from itertools import cycle, islice

def roundrobin(*iterables):
    pending = len(iterables)
    nexts = cycle(iter(iterable).next for iterable in iterables)
    while pending:
        try:
            for next in nexts: yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))
