#!/usr/bin/python
""" A python bubble-babble generator, inspired by
<http://woozle.org/t/bubblebabble.c>.
Here are the original Perl bubble-babble examples, for doctests:

    >>> babble('432cc46b5c67c9adaabdcc6c69e23d6d'.decode('hex'))
    'xibod-sycik-rilak-lydap-tipur-tifyk-sipuv-dazok-tixox'
    >>> babble('5a1edbe07020525fd28cba1ea3b76694'.decode('hex'))
    'xikic-vikyv-besed-begyh-zagim-sevic-vomer-lunon-gexex'
    >>> babble('1c453603cdc914c1f2eeb1abddae2e03'.decode('hex'))
    'xelag-hatyb-fafes-nehys-cysyv-vasop-rylop-vorab-fuxux'
    >>> babble('df8ec33d78ae78280e10873f5e58d5ad'.decode('hex'))
    'xulom-vebyf-tevyp-vevid-mufic-bucef-zylyh-mehyp-tuxax'
    >>> babble('02b682a73739a9fb062370eaa8bcaec9'.decode('hex'))
    'xebir-kybyp-latif-napoz-ricid-fusiv-popir-soras-nixyx'
"""
import itertools

consonants = "bcdfghklmnprstvz"
vowels     = "aeiouy"

def maybe_ord(x):
    """If x is a string of length 1, return the ascii value.  If it's a
    longer string, return an iterator of values.  Otherwise, coerce it
    to an int()
    >>> maybe_ord('A')
    65
    >>> tuple(maybe_ord('lol'))
    (108, 111, 108)
    >>> maybe_ord(242)
    242
    >>> maybe_ord(242.2222)
    242
    """
    try:
        if len(x) is 1 and len(x[0]) is 1:
            return ord(x)
        else:
            return itertools.imap(maybe_ord, x)
    except:
        return int(x)


def babble(digest, seed=1):
    """ Compute bubble babble for input buffer.
    >>> babble('')
    'xexax'
    >>> babble('1234567890')
    'xesef-disof-gytuf-katof-movif-baxux'
    >>> babble('Pineapple')
    'xigak-nyryk-humil-bosek-sonax'
    >>> babble('lol')
    'xirak-zorex'
    >>> import hashlib
    >>> babble(hashlib.sha1('lol').digest())
    'xibaf-nanob-fyzib-bikyh-davot-zotos-ryzah-decir-lucus-donoz-poxex'
    >>> babble([70, 85, 129, 199])
    'xicih-habes-laxex'
    >>> babble(0)
    'xebax'
    """
    ret = 'x'
    x = y = None
    iters = [maybe_ord(digest)] * 2
    for x,y in itertools.izip_longest(fillvalue=None, *iters):
        ret += vowels[(((x >> 6) & 3) + seed) % 6]
        ret += consonants[(x >> 2) & 15]
        ret += vowels[((x & 3) + (seed / 6)) % 6]
        if y is not None:
            seed = ((seed * 5) + (x * 7) + y) % 36
            ret += consonants[(y >> 4) & 15]
            ret += '-'
            ret += consonants[y & 15]
    if y is not None or x is None:
        ret += vowels[seed % 6] + 'x' + vowels[seed / 6]
    return ret + 'x'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
