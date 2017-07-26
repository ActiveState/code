from string import Formatter

class EmptyNoneType(object):

    def __nonzero__(self):
        return False

    def __str__(self):
        return ''

    def __getattr__(self, name):
        return EmptyNone

    def __getitem__(self, idx):
        return EmptyNone
    

EmptyNone = EmptyNoneType()

class EmptyNoneFormatter(Formatter):

    def get_value(self, field_name, args, kwds):
        v = Formatter.get_value(self, field_name, args, kwds)
        if v is None:
            return EmptyNone
        return v

def test_getattr_on_None():
    fmt = EmptyNoneFormatter()
    assert fmt.format('{0}', None) == ''
    assert fmt.format('{0.foo}', None) == ''
    assert fmt.format('{0[0]}', None) == ''

    assert fmt.format('{bar}', bar=None) == ''
    assert fmt.format('{bar.foo}', bar=None) == ''
    assert fmt.format('{bar[0]}', bar=None) == ''
