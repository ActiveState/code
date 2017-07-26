#>>>>>>>>>> Icon example of recursive generator >>>>>>>>>
##procedure star(chars)
##   suspend "" | (star(chars) || !chars)
##end
##

class bang(object):
    """ a generator with saved state that can be reset """
    def __init__(self, arg):
        self.arg = arg
        self.reset()
    def __iter__(self):
        for item in self.iterable:
            yield item
    def next(self):
        return self.iterable.next()
    def reset(self):
        if  hasattr(self.arg, '__iter__') and \
                hasattr(self.arg, 'next') :
            self.iterable = self.arg
        elif hasattr(self.arg, '__getitem__'):
            if self.arg:
                self.iterable = iter(self.arg)
            else: self.iterable = iter([""])
        else:
            self.iterable = iter([self.arg])
    def __repr__(self):
        return repr(self.arg)

def alternation( *items ):
    """Lazy evaluation that flattens input items """
    for alt_item in items:
        if hasattr(alt_item, '__iter__'):
            #flatten generator item
            for item in alt_item:
                yield item
        else:
            yield alt_item
    
def concatenate(g1, g2):
    """Lazy evaluation concatenation """
    #list, tuple, and string iterators are not used implicitly
    #Not generalized for sequences other than strings
    if hasattr(g1, '__iter__') and hasattr(g2, '__iter__'):
        #concatenations of left items to right items
        #map(operator.plus, leftseq, rightseq)
        for x in g1:
            g2.reset()
            for y in g2:
                yield x + y
    elif hasattr(g1, '__iter__') :
        #concatenations of left items to right sequence
        #map(operator.plus, [leftseq]*len(rightseq), rightseq)
        for x in g1:
            yield x + g2
    elif hasattr(g2, '__iter__') :
        #concatenations of left sequence to right items
        #map(operator.plus, leftseq, [rightseq]*len(leftseq))
        for x in g2:
            yield g1 + x
    else:
        #string concatenation like Python
        yield g1 + g2

def star(chars):
    """ Recursive, infinite generator for all permutations
        of a string taken 1 to N characters at time """
    for item in alternation("", concatenate(star(chars),  bang(chars))):
        yield item

#star test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
chars = 'abc'
limit = 3 # Limit infinite recursion
for n, x in enumerate(star(chars)):
    if len(x) > limit: break
    print n+1, repr(x)
