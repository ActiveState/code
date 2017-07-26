import re

class MultiRegex(object):
    flags = re.DOTALL
    regexes = ()

    def __init__(self):
        '''
        compile a disjunction of regexes, in order
        '''
        self._regex = re.compile("|".join(self.regexes), self.flags)

    def sub(self, s):
        return self._regex.sub(self._sub, s)

    def _sub(self, mo):
        '''
        determine which partial regex matched, and
        dispatch on self accordingly.
        '''
        for k,v in mo.groupdict().iteritems():
            if v:
                sub = getattr(self, k)
                if callable(sub):
                    return sub(mo)
                return sub
        raise AttributeError, \
             'nothing captured, matching sub-regex could not be identified'


class TrivialExample(MultiRegex):
    regexes = (
        r'(?P<lower>[a-z]{2,})',
        r'(?P<upper>[A-Z]{2,})',
        r'(?P<mixed>[A-Za-z]+)'
    )

    def lower(self, mo):
        return 'lower:' + mo.group()

    upper = lambda self, mo: 'upper:' + mo.group()
    mixed = 'stuff'


class TrivialExample2(TrivialExample):
    '''
    this illustrates that the order of regexes is important
    '''
    regexes = (
        r'(?P<mixed>[a-zA-Z]+)',
        r'(?P<lower>[a-z]{2,})',
        r'(?P<upper>[A-Z]{2,})'
    )

a = 'That cake was AWESOME, dude!'
print TrivialExample().sub(a)
print TrivialExample2().sub(a)

'''
produces:                                                                      
stuff lower:cake lower:was upper:AWESOME, lower:dude!
stuff stuff stuff stuff, stuff!
'''
