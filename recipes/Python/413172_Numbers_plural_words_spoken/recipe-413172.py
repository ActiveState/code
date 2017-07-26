_known = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
    }
def _positive_spoken_number(n):
    """Assume n is a positive integer.
    >>> _positive_spoken_number(900)
    'nine hundred'
    >>> _positive_spoken_number(100)
    'one hundred'
    >>> _positive_spoken_number(100000000000)
    'one hundred billion'
    >>> _positive_spoken_number(1000000000000)
    'one trillion'
    >>> _positive_spoken_number(33000000000000)
    'thirty-three trillion'
    >>> _positive_spoken_number(34954523539)
    'thirty-four billion, nine hundred fifty-four million, five hundred twenty-three thousand, five hundred thirty-nine'
    """
    #import sys; print >>sys.stderr, n
    if n in _known:
        return _known[n]
    bestguess = str(n)
    remainder = 0
    if n<=20:
        print >>sys.stderr, n, "How did this happen?"
        assert 0
    elif n < 100:
        bestguess= _positive_spoken_number((n//10)*10) + '-' + \
                   _positive_spoken_number(n%10)
        return bestguess
    elif n < 1000:
        bestguess= _positive_spoken_number(n//100) + ' ' + 'hundred'
        remainder = n%100
    elif n < 1000000:
        bestguess= _positive_spoken_number(n//1000) + ' ' + 'thousand'
        remainder = n%1000
    elif n < 1000000000:
        bestguess= _positive_spoken_number(n//1000000) + ' ' + 'million'
        remainder = n%1000000
    elif n < 1000000000000:
        bestguess= _positive_spoken_number(n//1000000000) + ' ' + 'billion'
        remainder = n%1000000000
    else:
        bestguess= _positive_spoken_number(n//1000000000000)+' '+'trillion'
        remainder = n%1000000000000
    if remainder:
        if remainder >= 100: comma = ','
        else:                comma = ''
        return bestguess + comma + ' ' + _positive_spoken_number(remainder)
    else:
        return bestguess
    
def spoken_number(n):
    """Return the number as it would be spoken, or just str(n) if unknown.
    >>> spoken_number(0)
    'zero'
    >>> spoken_number(1)
    'one'
    >>> spoken_number(2)
    'two'
    >>> spoken_number(-2)
    'minus two'
    >>> spoken_number(42)
    'forty-two'
    >>> spoken_number(-1011)
    'minus one thousand eleven'
    >>> spoken_number(1111)
    'one thousand, one hundred eleven'
    """
    if not isinstance(n, int) and not isinstance(n, long): return n
    if n<0:
        if n in _known: return _known[n]
        else:           return 'minus ' + _positive_spoken_number(-n)
    return _positive_spoken_number(n)

_aberrant_plurals = {	'knife' 	: 'knives',
                        'self'		: 'selves',
                        'elf'		: 'elves',
                        'life'		: 'lives',
                        'hoof'		: 'hooves',
                        'leaf'		: 'leaves',
                        'echo'		: 'echoes',
                        'embargo'	: 'embargoes',
                        'hero'		: 'heroes',
                        'potato'	: 'potatoes',
                        'tomato'	: 'tomatoes',
                        'torpedo'	: 'torpedoes',
                        'veto'		: 'vetoes',
                        'child'		: 'children',
                        'woman'		: 'women',
                        'man'		: 'men',
                        'person'	: 'people',
                        'goose'		: 'geese',
                        'mouse'		: 'mice',
                        'barracks'	: 'barracks',
                        'deer'		: 'deer',
                        'nucleus'	: 'nuclei',
                        'syllabus'	: 'syllabi',
                        'focus'		: 'foci',
                        'fungus'	: 'fungi',
                        'cactus'	: 'cacti',
                        'phenomenon'	: 'phenomena',
                        'index'		: 'indices',
                        'appendix'	: 'appendices',
                        'criterion'	: 'criteria'
                        }

def how_many(n, singular, plural=None):
    """Return a string describing a number of thing or things
    If plural is not supplied, it is guessed from singular.
    Assume that all letters (except maybe the first) are lower case, for now.
    @todo: Handle upper-case
    >>> how_many(0, 'error')
    'zero errors'
    >>> how_many(1, 'error')
    'one error'
    >>> how_many(0, 'zero')
    'zero zeroes'
    >>> how_many(-99, 'penny')
    'minus ninety-nine pennies'
    >>> how_many(42, 'radius')
    'forty-two radii'
    >>> how_many(100, 'fuss')
    'one hundred fusses'
    >>> how_many(111, 'goose')
    'one hundred eleven geese'
    >>> how_many(-1, 'Chris', "Chris's")
    "minus one Chris's"
    """
    try: said = spoken_number(n)
    except: said = str(n)
    if n == 1:
        return said + ' ' + singular
    if plural: pass
    elif singular in _aberrant_plurals: plural = _aberrant_plurals[singular]
    else:
        root = singular
        post = ''
        try:
            vowels = 'aeiou'
            if singular[-1] == 'y' and singular[-2] not in vowels:
                root = singular[:-1]; post = 'ies'
            elif singular[-1] == 's':
                if singular[-2] in vowels:
                    if singular[-3:] == 'ius': root = singular[:-2]; post = 'i'
                    else: root = singular[:-1]; post = 'ses'
                else: post = 'es'
            elif singular[-1] in 'o' or singular[-2:] in ('ch', 'sh'):
                post = 'es'
            else:
                post = 's'
        except:
            post = 's'
        plural = root + post
    return said + ' ' + plural


def _test():
    import doctest
    return doctest.testmod()
    
if __name__ == '__main__':
    _test()
