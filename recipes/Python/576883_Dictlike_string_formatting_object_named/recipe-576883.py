import re

exp_rx = re.compile('%\((\w+)\)')

def format_obj(obj, text):
    """
    >>> o = Duck(one='one', two='two', three=5)
    >>> format_obj(o, '%(one)s %(two)s %(three)d')
    'one two 5'
    """
    return text % dict((a, getattr(obj, a))
                               for a in re.findall(exp_rx, text))

# ---- Support for the doctest from here down:

class Duck(object):
    """Quack!"""

    def __init__(self, **kw):
        self.__dict__.update(kw)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
