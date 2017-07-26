# this is not entirely serious

import re

_patterns = dict((k, re.compile('_*' + v)) for (k, v)
                    in dict(allcamel=r'(?:[A-Z]+[a-z0-9]*)+$',
                            trailingcamel=r'[a-z]+(?:[A-Z0-9]*[a-z0-9]*)+$',
                            underscores=r'(?:[a-z]+_*)+[a-z0-9]+$').iteritems())

_caseTransition = re.compile('([A-Z][a-z]+)')

def translate(name, _from, to):
    leading_underscores = str()
    while name[0] == '_':
        leading_underscores += '_'
        name = name[1:]

    if _from in ('allcamel', 'trailingcamel'):
        words = _caseTransition.split(name)
    else:
        words = name.split('_')

    words = list(w for w in words if w is not None and 0 < len(w))

    camelize = lambda words: ''.join(w[0].upper() + w[1:] for w in words)

    v = dict(smushed=lambda: ''.join(words).lower(),
             allcamel=lambda: camelize(words),
             trailingcamel=lambda: words[0].lower() + camelize(words[1:]),
             underscores=lambda: '_'.join(words).lower())[to]()

    return leading_underscores + v

def rename_members(obj, _from, to, explode_for_non_matches=True,
                   acceptance_function=callable, debug=False):

    assert _from in _patterns
    if to != 'smushed':
        assert to in _patterns

    for name in dir(obj):
        if name.startswith('__') and name.endswith('__'):
            continue
        thing = getattr(obj, name)
        if not acceptance_function(thing):
            continue
        if _patterns[_from].match(name):
            newname = translate(name, _from, to)
            if hasattr(obj, newname):
                raise ValueError('%r already has a %r attribute' % (obj, newname))
            setattr(obj, newname, thing)
            if debug:
                print obj, ':', name, '->', newname
        else:
            if explode_for_non_matches:
                raise ValueError('attribute %r of %r is not well formed %r' % (name, obj, _from))
    return obj

# examples

class Foo:
    def thisIsAMethod(self):
        pass

rename_members(Foo, 'trailingcamel', 'underscores')
assert hasattr(Foo, 'this_is_a_method')

# you could of course pass a module or an instance or anything else

class Foo:
    def this_is_a_method(self):
        pass

rename_members(Foo, 'underscores', 'allcamel')
assert hasattr(Foo, 'ThisIsAMethod')
