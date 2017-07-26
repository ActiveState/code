from operator import itemgetter
from itertools import groupby,imap

_undefined = object()

def iterblocks(iterable, start, end=_undefined, skip_delim=True):
    '''Create an iterator over consecutive items (I{blocks}) of the given iterable.

    @param start: The delimiter denoting the start of a block. It can be:
        1. a predicate C{p(item)} that returns true if the item is a
        delimiter and false otherwise, or
        2. a non-callable object C{obj}: equivalent to C{lambda item: item==start}
    @param end: If not None, the delimiter denoting the end of a block. Items
        after an end delimiter but before the next start delimiter are skipped.
        Takes the same values as C{start}.

    @param skip_delim: True if the delimiter(s) are to be skipped, false otherwise.
    @type skip_delim: C{bool}
    '''
    def get_predicate(arg):
        return arg if callable(arg) else (
               arg.__eq__ if hasattr(arg,'__eq__') else
               lambda item: item == arg)
    def stamped_items(items):
        count = 0
        startsblock = get_predicate(start)
        if end is _undefined:
            for item in items:
                if startsblock(item):
                    count += 1
                    if skip_delim: continue
                yield count,item
        else:
            endsblock = get_predicate(end)
            inblock = False
            for item in items:
                if inblock:
                    if endsblock(item):
                        inblock = False
                        if skip_delim: continue
                elif startsblock(item):
                    count += 1
                    inblock = True
                    if skip_delim: continue
                else: continue
                yield count,item
    get2nd = itemgetter(1)
    for count, block in groupby(stamped_items(iterable), itemgetter(0)):
        yield imap(get2nd, block)

if __name__ == '__main__':
    import re
    # a slow version of str.split
    for chars in iterblocks('Hello World', re.compile(r'\s').match):
        print ''.join(chars)
    source = """\
> name1....

line_11
line_12
line_13
...
> name2 ...

line_21
line_22
...""".splitlines()
    for lines in iterblocks(source, start=re.compile('>').match, end='...'):
        print list(lines)
