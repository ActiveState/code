import itertools

def imapzip(generator, *iterables):
    """
    Make an iterator that aggregates the iteration of generator using
    arguments aggregated from each of the iterables.

    >>> it = imapzip(xrange, (0, 3), (2, 5))
    >>> it.next()
    (0, 3)
    >>> it.next()
    (1, 4)
    """
    return itertools.izip(*tuple(itertools.starmap(generator, zip(*iterables))))

def imapmethod(methodname, *iterables):
    """
    If methodname is a string, make an iterator that calls the method
    on each of the iterables named methodname with no
    arguments. Otherwise, make an iterator that calls the method on
    each of the iterables named by the corresponding element in
    methodname.
    
    >>> a = ["aBrA", "cAdAbRa"]
    >>> b = ["aLa", "kAzAm"]
    >>> it1 = imapmethod("title", a)
    >>> it1.next()
    'Abra'
    >>> it1.next()
    'Cadabra'
    >>> it2 = imapmethod(("upper", "lower"), a, b)
    >>> it2.next()
    ('ABRA', 'ala')
    >>> it2.next()
    ('CADABRA', 'kazam')
    """
    def methodcall(item):
        return getattr(item, methodname)()

    if isinstance(methodname, str):
        if len(iterables) == 1:
            return itertools.imap(methodcall, *iterables)
        else:
            return imapzip(itertools.imap, [methodcall] * len(iterables), iterables)
    else:
        return imapzip(imapmethod, methodname, iterables)

def curryimapmethod(methodname):
    """
    Make a function that will call imapmethod with a preset
    methodname.
    """
    def imapmethod_call(*iterables):
        return imapmethod(methodname, *iterables)
    return imapmethod_call

istrip = curryimapmethod("strip")
irstrip = curryimapmethod("rstrip")
ilstrip = curryimapmethod("lstrip")
