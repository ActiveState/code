conversions = {}  # the data structure -- a dict-of-dicts

def converter(source, dest):
    '''A decorator that fills the conversions table with entries'''
    def decorate(function):
        '''Update the conversions table and return the original'''
        try:
            previous = conversions[source][dest]
        except KeyError:
            conversions.setdefault(source, {})[dest] = function
            return function
        raise ValueError, 'Two conversions from %r to %r: %r and %r' % (
              source, dest, getattr(previous, '__name__', previous),
              getattr(function, '__name__', function))
    return decorate

@converter('inch', 'feet')
def tofeet(measure):
    return 12 * measure

@converter('feet', 'inch')
def toinch(measure):
    return measure / 12.

# ...
# converter can be used as a non-decorator to load other values.
converter('feet', 'hectare')(None)

print conversions['feet']['inch'](123)
print conversions['inch']['feet'](123)
print conversions['feet']['hectare']
