def genkvs(d, keys, joiner):
    for key in keys:
        yield '%s%s%s' % (key, joiner, d[key])

def dictjoin(_dict, joiner, sep):
    keys = sorted(_dict.iterkeys())
    return sep.join(genkvs(_dict, keys, joiner))

def test_dictjoin():
    """This test function can be used for testing dictjoin with py.test of
    nosetests."""
    def dictjointest(_dict, expected):
        assert dictjoin(_dict, '=', '; ') == expected

    yield dictjointest, {}, ''
    yield dictjointest, dict(a=1), 'a=1'
    yield dictjointest, dict(a=1, b=2), 'a=1; b=2'

if __name__ == '__main__':
    # Simple demonstration
    print dictjoin(dict(a=1, b=2, c=3, d=4), ' = ', '; ')
