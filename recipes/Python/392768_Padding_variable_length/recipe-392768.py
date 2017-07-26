def demo():
    for firstname,lastname,age,skills in map(
                padfactory(minLength=1, defaults=["",0], extraItems=False),
                [("Tony", "Caley", 23),
                 ("Mike", "Balboa"),
                 ["Aristotle"],
                 ("Nick", "Fulton", 31, "python", "C++", "oracle"),]):
        print "%s %s (%d): %s" % (firstname, lastname, age,
                                  ' '.join(skills) or None)

def padfactory(minLength=0, defaults=(), extraItems=False):
    '''Return a function that can pad variable-length iterables.

    The returned function f:iterable -> iterable attempts to return an
    iterable of the same type as the original; if this fails it returns a list.

    @param minLength: The minimum required length of the iterable.
    @param defaults: A sequence of default values to pad shorter iterables.
    @param extraItems: Controls what to do with iterables longer than
        minlength + len(defaults).
            - If extraItems is None, the extra items are ignored.
            - else if bool(extraItems) is True, the extra items are packed in
              a tuple which is appended to the returned iterable. An empty
              tuple is appended if there are no extra items.
            - else a ValueError is thrown (longer iterables are not acceptable).
    '''
    # maximum sequence length (without considering extraItems)
    maxLength = minLength + len(defaults)
    from itertools import islice
    def closure(iterable):
        iterator = iter(iterable)   # make sure you can handle any iterable
        padded = list(islice(iterator,maxLength))
        if len(padded) < maxLength:
            # extend by the slice of the missing defaults
            for default in islice(defaults, len(padded) - minLength,
                                  maxLength - minLength):
                padded.append(default)
        if len(padded) < maxLength:
            raise ValueError("unpack iterable of smaller size")
        if extraItems:               # put the rest elements in a tuple
            padded.append(tuple(iterator))
        elif extraItems is None:     # silently ignore the rest of the iterable
            pass
        else:                        # should not have more elements
            try: iterator.next()
            except StopIteration: pass
            else: raise ValueError("unpack iterable of larger size")
        # try to return the same type as the original iterable;
        itype = type(iterable)
        if itype != list:
            try: padded = itype(padded)
            except TypeError: pass
        return padded
    return closure
